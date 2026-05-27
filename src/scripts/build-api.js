/**
 * Build the static JSON API from Markdown + YAML frontmatter files.
 * Crawls docs/, parses frontmatter, and outputs structured JSON.
 * Generates:
 *   - commands.json       Full tool database
 *   - registry.json       Registry index
 *   - by-domain.json      Tools grouped by domain
 *   - by-capability.json  Inverted capability index
 *   - by-workflow.json    Workflow edge graph (produces/consumes)
 *   - embeddings.jsonl    Vector DB ingestion format
 *   - snapshots/          Versioned timestamped snapshots
 */

import fs from "node:fs";
import path from "node:path";
import { glob } from "node:fs/promises";
import { createHash } from "node:crypto";
import matter from "gray-matter";
import { toStixBundle } from "./build-api.stix.js";

const DOCS_DIR = path.resolve("docs");
const API_DIR = path.resolve("api/v1");
const PUBLIC_API_DIR = path.resolve("public/api/v1");
const SNAPSHOT_BASE = path.resolve("snapshots");
const CONFIG_PATH = path.resolve("settings/convert.json");

const SNAPSHOT_RETENTION_DAYS = 30;

async function loadConfig() {
  if (fs.existsSync(CONFIG_PATH)) {
    return JSON.parse(fs.readFileSync(CONFIG_PATH, "utf-8"));
  }
  return {
    src: "docs",
    filePattern: "**/*.md",
    metadata: true,
    deterministicOrder: true,
    exclude: [],
  };
}

function isoFilename() {
  const now = new Date();
  return now.toISOString().replace(/[:.]/g, "-").slice(0, 19) + "Z";
}

function pruneSnapshots() {
  if (!fs.existsSync(SNAPSHOT_BASE)) return;
  const cutoff = Date.now() - SNAPSHOT_RETENTION_DAYS * 86400000;
  let pruned = 0;
  for (const entry of fs.readdirSync(SNAPSHOT_BASE)) {
    const dirPath = path.join(SNAPSHOT_BASE, entry);
    const stat = fs.statSync(dirPath);
    if (stat.isDirectory() && stat.mtimeMs < cutoff) {
      fs.rmSync(dirPath, { recursive: true, force: true });
      pruned++;
    }
  }
  if (pruned > 0) console.log(`  Pruned ${pruned} old snapshot(s)`);
}

function writeOutputs(dir, commands, byDomain, byCapability, byWorkflow, embeddingsLines) {
  fs.mkdirSync(dir, { recursive: true });

  fs.writeFileSync(path.join(dir, "commands.json"), JSON.stringify(commands, null, 2));

  const registry = {
    version: "1.0.0",
    last_updated: new Date().toISOString(),
    total_tools: commands.length,
    tools: commands,
  };
  fs.writeFileSync(path.join(dir, "registry.json"), JSON.stringify(registry, null, 2));

  fs.writeFileSync(path.join(dir, "by-domain.json"), JSON.stringify(byDomain, null, 2));
  fs.writeFileSync(path.join(dir, "by-capability.json"), JSON.stringify(byCapability, null, 2));
  fs.writeFileSync(path.join(dir, "by-workflow.json"), JSON.stringify(byWorkflow, null, 2));
  fs.writeFileSync(path.join(dir, "embeddings.jsonl"), embeddingsLines.join("\n"));

  console.log(`  Wrote ${commands.length} commands to ${dir}`);
}

async function buildApi() {
  console.log("Building static API from Markdown...");
  const config = await loadConfig();
  const commands = [];

  const pattern = config.filePattern || "**/*.md";
  const srcDir = path.resolve(config.src || "docs");
  const excludePatterns = config.exclude || [];

  for await (const filePath of glob(pattern, { cwd: srcDir, root: srcDir })) {
    const fullPath = path.join(srcDir, filePath);
    const shouldExclude = excludePatterns.some((p) => {
      if (p.startsWith("**")) {
        return filePath.includes(p.slice(2));
      }
      return filePath === p;
    });
    if (shouldExclude) continue;

    const raw = fs.readFileSync(fullPath, "utf-8");
    try {
      const parsed = matter(raw);
      if (!parsed.data || Object.keys(parsed.data).length === 0) continue;

      const entry = {
        ...parsed.data,
        _source: filePath,
        _body: parsed.content,
      };

      // Merge parameters from data/parsed_params/<name>.json if available
      const toolName = (entry.name || "unknown").toLowerCase();
      const paramsPath = path.resolve("data/parsed_params", toolName + ".json");
      if (fs.existsSync(paramsPath)) {
        try {
          entry.parameters = JSON.parse(fs.readFileSync(paramsPath, "utf-8"));
        } catch (e) {
          // ignore parse errors for individual files
        }
      }

      if (config.deterministicOrder) {
        const ordered = {};
        for (const k of Object.keys(entry).sort()) ordered[k] = entry[k];
        commands.push(ordered);
      } else {
        commands.push(entry);
      }
    } catch (err) {
      console.warn(`  SKIP ${filePath}: ${err.message}`);
    }
  }

  if (config.deterministicOrder) {
    commands.sort((a, b) => (a.namespace || "").localeCompare(b.namespace || ""));
  }

  // --- by-domain index ---
  const byDomain = {};
  for (const cmd of commands) {
    const ns = cmd.namespace || "unknown";
    const domain = ns.split(":")[0];
    if (!byDomain[domain]) byDomain[domain] = [];
    byDomain[domain].push({
      id: cmd.id,
      name: cmd.name,
      namespace: ns,
      description: cmd.description,
    });
  }

  // --- by-capability inverted index ---
  const byCapability = {};
  for (const cmd of commands) {
    const caps = cmd.capabilities || [];
    for (const cap of caps) {
      if (!byCapability[cap]) byCapability[cap] = [];
      if (!byCapability[cap].includes(cmd.id)) {
        byCapability[cap].push(cmd.id);
      }
    }
  }
  const sortedCaps = {};
  for (const k of Object.keys(byCapability).sort()) {
    sortedCaps[k] = byCapability[k];
  }

  // --- workflow graph ---
  const byWorkflow = { nodes: [], edges: [] };
  const toolMap = {};
  for (const cmd of commands) {
    const nodeId = cmd.id || cmd.name || "unknown";
    toolMap[nodeId] = cmd;
    byWorkflow.nodes.push({
      id: nodeId,
      name: cmd.name,
      namespace: cmd.namespace,
      capabilities: cmd.capabilities || [],
    });
    const edges = cmd.workflow_edges || {};
    for (const produced of (edges.produces || [])) {
      byWorkflow.edges.push({ from: nodeId, type: "produces", artifact: produced });
    }
    for (const consumed of (edges.consumes || [])) {
      byWorkflow.edges.push({ to: nodeId, type: "consumes", artifact: consumed });
    }
  }

  // --- embeddings export ---
  const embeddingsLines = [];
  for (const cmd of commands) {
    const name = cmd.name || "unknown";
    const desc = cmd.description || "";
    const caps = (cmd.capabilities || []).join(", ");
    const template = cmd.execution ? cmd.execution.template || "" : "";
    const content = `${name} - ${desc}. Capabilities: ${caps}. Template: ${template}`.replace(/\s+/g, " ");
    embeddingsLines.push(JSON.stringify({
      id: cmd.id || "unknown",
      namespace: cmd.namespace || "unknown",
      name: name,
      content: content,
    }));
  }

  // --- write to live directories ---
  for (const dir of [PUBLIC_API_DIR, API_DIR]) {
    writeOutputs(dir, commands, byDomain, sortedCaps, byWorkflow, embeddingsLines);
  }

  // --- generate STIX 2.1 bundle ---
  try {
    const stixBundle = toStixBundle(commands);
    const stixJson = JSON.stringify(stixBundle, null, 2);
    for (const dir of [PUBLIC_API_DIR, API_DIR]) {
      fs.writeFileSync(path.join(dir, "stix-bundle.json"), stixJson);
    }
    console.log(`  Generated STIX 2.1 bundle (${stixBundle.objects.length} objects)`);
  } catch (e) {
    console.warn("  STIX generation skipped:", e.message);
  }

  // --- generate integrity manifest ---
  const integrityManifest = {};
  for await (const filePath of glob("**/*.md", { cwd: DOCS_DIR, root: DOCS_DIR })) {
    const fullPath = path.join(DOCS_DIR, filePath);
    const content = fs.readFileSync(fullPath);
    const hash = createHash("sha256").update(content).digest("hex");
    integrityManifest[filePath] = hash;
  }
  for (const dir of [PUBLIC_API_DIR, API_DIR]) {
    fs.writeFileSync(path.join(dir, "integrity-manifest.json"), JSON.stringify(integrityManifest, null, 2));
  }
  console.log(`  Generated integrity manifest (${Object.keys(integrityManifest).length} entries)`);

  // --- write versioned snapshot ---
  const timestamp = isoFilename();
  const snapshotDir = path.join(SNAPSHOT_BASE, timestamp);
  writeOutputs(snapshotDir, commands, byDomain, sortedCaps, byWorkflow, embeddingsLines);
  pruneSnapshots();

  console.log(`API build complete: ${commands.length} commands, ${Object.keys(byDomain).length} domains, ${Object.keys(sortedCaps).length} capabilities, ${byWorkflow.edges.length} workflow edges`);
  return commands;
}

buildApi().catch((err) => {
  console.error("API build failed:", err);
  process.exit(1);
});
