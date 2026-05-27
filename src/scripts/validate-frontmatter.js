/**
 * Validate YAML frontmatter in all Markdown files against the JSON Schema.
 * Run locally before committing: node src/scripts/validate-frontmatter.js
 */

import fs from "node:fs";
import path from "node:path";
import { glob } from "node:fs/promises";
import matter from "gray-matter";

const DOCS_DIR = path.resolve("docs");
const SCHEMA_PATH = path.resolve("schemas/command-schema.json");
const REQUIRED_FIELDS = ["id", "namespace", "name", "description", "version", "execution"];

async function validate() {
  console.log("Validating frontmatter in docs/...\n");

  const schema = JSON.parse(fs.readFileSync(SCHEMA_PATH, "utf-8"));
  const schemaProps = schema.properties || {};
  let errors = 0;
  let filesChecked = 0;

  for await (const filePath of glob("**/*.md", { cwd: DOCS_DIR, root: DOCS_DIR })) {
    const fullPath = path.join(DOCS_DIR, filePath);
    const raw = fs.readFileSync(fullPath, "utf-8");
    filesChecked++;

    let parsed;
    try {
      parsed = matter(raw);
    } catch {
      console.log(`  SKIP ${filePath}: cannot parse frontmatter`);
      continue;
    }

    if (!parsed.data || Object.keys(parsed.data).length === 0) {
      console.log(`  SKIP ${filePath}: no frontmatter`);
      continue;
    }

    const data = parsed.data;
    let fileErrors = 0;

    for (const field of REQUIRED_FIELDS) {
      if (!(field in data)) {
        console.log(`  FAIL ${filePath}: missing required field '${field}'`);
        fileErrors++;
      }
    }

    if (data.id && !/^[a-z0-9]+(-[a-z0-9]+)+$/.test(data.id)) {
      console.log(`  FAIL ${filePath}: 'id' must match ^[a-z0-9]+(-[a-z0-9]+)+$ (got '${data.id}')`);
      fileErrors++;
    }

    if (data.namespace && !/^[a-z]+(\.[a-z0-9]+)*:[a-z]+:[a-z0-9-]+(:[a-z0-9-]+)?$/.test(data.namespace)) {
      console.log(`  FAIL ${filePath}: 'namespace' must match domain:category:tool[:action] (got '${data.namespace}')`);
      fileErrors++;
    }

    if (data.parameters && Array.isArray(data.parameters)) {
      for (const param of data.parameters) {
        if (!param.name || !param.type || !param.description) {
          console.log(`  FAIL ${filePath}: parameter missing required fields (name, type, description)`);
          fileErrors++;
        }
      }
    }

    if (data.execution && !data.execution.template) {
      console.log(`  FAIL ${filePath}: execution.template is required`);
      fileErrors++;
    }

    // Cross-validate template placeholders against parameters
    if (data.execution && data.execution.template && data.parameters && Array.isArray(data.parameters)) {
      const paramKeys = new Set();
      for (const p of data.parameters) {
        paramKeys.add(p.name);
        if (p.template_key) paramKeys.add(p.template_key);
      }
      const placeholderRe = /\{([^}]+)\}|(\{\{[^}]+\}\})/g;
      let match;
      while ((match = placeholderRe.exec(data.execution.template)) !== null) {
        const raw = (match[1] || match[2] || "").replace(/[{}]/g, "");
        if (raw && !paramKeys.has(raw)) {
          console.log(`  FAIL ${filePath}: template placeholder '{${raw}}' has no matching parameter name or template_key`);
          fileErrors++;
        }
      }
    }

    // Validate template_key values
    if (data.parameters && Array.isArray(data.parameters)) {
      const seenKeys = new Set();
      for (const p of data.parameters) {
        if (p.template_key) {
          if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(p.template_key)) {
            console.log(`  FAIL ${filePath}: parameter '${p.name}' template_key '${p.template_key}' must be kebab-case`);
            fileErrors++;
          }
          if (seenKeys.has(p.template_key)) {
            console.log(`  FAIL ${filePath}: duplicate template_key '${p.template_key}' on parameter '${p.name}'`);
            fileErrors++;
          }
          seenKeys.add(p.template_key);
        }
      }
    }

    // Validate global_vars if present
    if (data.global_vars) {
      if (typeof data.global_vars !== "object" || Array.isArray(data.global_vars)) {
        console.log(`  FAIL ${filePath}: global_vars must be an object (string-to-string mapping)`);
        fileErrors++;
      } else {
        for (const [key, val] of Object.entries(data.global_vars)) {
          if (typeof val !== "string") {
            console.log(`  FAIL ${filePath}: global_vars.${key} must map to a string (cosmos key), got ${typeof val}`);
            fileErrors++;
          }
        }
      }
    }

    // Validate mitre_ids format if present
    if (data.mitre_ids && Array.isArray(data.mitre_ids)) {
      for (const mid of data.mitre_ids) {
        if (!/^T\d{4}(\.\d{3})?$/.test(mid)) {
          console.log(`  FAIL ${filePath}: mitre_id '${mid}' must match T#### or T####.###`);
          fileErrors++;
        }
      }
    }

    // Validate phase enum if present
    const validPhases = ["recon","enumeration","exploitation","post-exploitation","forensics","defense-evasion","discovery","collection","lateral-movement","exfiltration"];
    if (data.phase && !validPhases.includes(data.phase)) {
      console.log(`  FAIL ${filePath}: phase '${data.phase}' not in [${validPhases.join(", ")}]`);
      fileErrors++;
    }

    // Validate plugins if present
    const validPlugins = ["copyCode","mermaid","tabs","zoomable"];
    if (data.plugins && Array.isArray(data.plugins)) {
      for (const p of data.plugins) {
        if (!validPlugins.includes(p)) {
          console.log(`  FAIL ${filePath}: plugin '${p}' not in [${validPlugins.join(", ")}]`);
          fileErrors++;
        }
      }
    }

    // Validate items if present
    const validItems = ["Username","Password","Hash","TGS","TGT","PFX","Shell","NoCreds"];
    if (data.items && Array.isArray(data.items)) {
      for (const item of data.items) {
        if (!validItems.includes(item)) {
          console.log(`  FAIL ${filePath}: item '${item}' not in [${validItems.join(", ")}]`);
          fileErrors++;
        }
      }
    }

    // Validate services if present
    const validServices = ["SMB","WMI","DCOM","Kerberos","RPC","LDAP","NTLM","DNS","HTTP","HTTPS","FTP","SMTP","MSSQL","MySQL","PostgreSQL","WinRM","LLMNR","NBT-NS","MDNS","ADCS","SSH"];
    if (data.services && Array.isArray(data.services)) {
      for (const svc of data.services) {
        if (!validServices.includes(svc)) {
          console.log(`  FAIL ${filePath}: service '${svc}' not in [${validServices.join(", ")}]`);
          fileErrors++;
        }
      }
    }

    // Validate attack_types if present
    const validAttackTypes = ["Enumeration","Exploitation","Persistence","PrivilegeEscalation","DefenseEvasion","CredentialAccess","Discovery","LateralMovement","Collection","Exfiltration","Execution"];
    if (data.attack_types && Array.isArray(data.attack_types)) {
      for (const at of data.attack_types) {
        if (!validAttackTypes.includes(at)) {
          console.log(`  FAIL ${filePath}: attack_type '${at}' not in [${validAttackTypes.join(", ")}]`);
          fileErrors++;
        }
      }
    }

    // Validate detections if present
    const validDetectionTypes = ["sigma","elastic","splunk","yara","clamav","sysmon","wdac","ioc","blockrule","other"];
    if (data.detections && Array.isArray(data.detections)) {
      for (const d of data.detections) {
        if (!d.type || !validDetectionTypes.includes(d.type)) {
          console.log(`  FAIL ${filePath}: detection type '${d.type}' not in [${validDetectionTypes.join(", ")}]`);
          fileErrors++;
        }
      }
    }

    if (fileErrors > 0) {
      errors += fileErrors;
    } else {
      const ns = data.namespace || "unknown";
      console.log(`  OK   ${filePath} (${ns})`);
    }
  }

  console.log(`\nChecked ${filesChecked} files. ${errors} error(s) found.`);
  if (errors > 0) {
    process.exit(1);
  }
}

validate().catch((err) => {
  console.error("Validation failed:", err);
  process.exit(1);
});
