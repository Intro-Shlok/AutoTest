import { defineCollection, z } from "astro:content";

const capPattern = z.string().regex(/^[a-z]+(\.[a-z0-9-]+)*$/);
const artifactTypePattern = z.string().regex(/^[a-z]+(\.[a-z0-9]+)*$/);
const semverPattern = z.string().regex(/^\d+\.\d+\.\d+$/);

const contractArtifact = z.object({
  type: artifactTypePattern,
  description: z.string().optional(),
  mime: z.string().optional(),
  schema_version: semverPattern.optional(),
});

const toolsCollection = defineCollection({
  type: "content",
  schema: ({ image }) =>
    z.object({
      id: z.string().regex(/^[a-z0-9]+(-[a-z0-9]+)+$/),
      namespace: z.string().regex(/^[a-z]+(\.[a-z0-9]+)*:[a-z]+:[a-z0-9-]+(:[a-z0-9-]+)?$/),
      name: z.string(),
      description: z.string().max(512),
      author: z.union([z.string(), z.array(z.string())]).optional(),
      version: z.string().regex(/^\d+\.\d+\.\d+$/),
      capabilities: z.array(capPattern).optional(),
      platforms: z
        .array(z.enum(["linux", "windows", "macos", "bsd", "cross-platform"]))
        .optional(),
      architectures: z
        .array(z.enum(["amd64", "arm64", "arm", "riscv64", "i386", "cross-platform"]))
        .optional(),
      risk_level: z.enum(["low", "medium", "high", "critical"]).optional(),
      execution_policy: z.enum(["enabled", "read-only", "disabled"]).default("enabled").optional(),
      trust_level: z.enum(["verified", "experimental", "community", "ai-generated"]).default("community").optional(),
      features: z
        .array(z.enum(["stealth", "requires-root", "network-intensive", "output-json", "output-xml", "streaming", "interactive", "batch", "encryption", "compression", "remote", "local", "pipes-stdin", "pipes-stdout", "file-system", "process-manip"]))
        .optional(),
      techniques: z
        .array(z.enum(["recon", "enumeration", "exfiltration", "privilege-escalation", "persistence", "lateral-movement", "discovery", "collection", "command-and-control", "credential-access", "defense-evasion", "execution", "impact", "data-manipulation", "monitoring", "backup", "forensics", "analysis", "network-manipulation", "process-discovery", "process-termination", "network-sniffing", "remote-services", "encryption", "process-manip"]))
        .optional(),
      "allowed-tools": z.array(z.string()).optional(),
      artifacts: z
        .array(
          z.object({
            type: artifactTypePattern,
            description: z.string(),
            mime: z.string().optional(),
            schema_version: semverPattern.optional(),
            trust_level: z.enum(["verified", "experimental", "community", "ai-generated"]).default("community").optional(),
          })
        )
        .optional(),
      dependencies: z.array(z.string()).optional(),
      related_tools: z.array(z.string()).optional(),
      resource_profile: z
        .object({
          cpu: z.enum(["low", "medium", "high"]).default("medium"),
          memory_mb: z.number().int().min(1).optional(),
          network: z.enum(["none", "low", "medium", "high"]).default("low"),
          disk_io: z.enum(["none", "low", "medium", "high"]).default("low"),
        })
        .optional(),
      workflow_edges: z
        .object({
          produces: z.array(z.string()).optional(),
          consumes: z.array(z.string()).optional(),
        })
        .optional(),
      contract: z
        .object({
          inputs: z.array(contractArtifact).optional(),
          outputs: z.array(contractArtifact).optional(),
          side_effects: z
            .array(z.enum(["network_traffic", "raw_socket_access", "filesystem_write", "process_spawn", "privilege_escalation", "none"]))
            .optional(),
          resource_cost: z
            .object({
              cpu: z.enum(["low", "medium", "high"]).optional(),
              memory_mb: z.number().int().min(1).optional(),
              network: z.enum(["none", "low", "medium", "high"]).optional(),
              disk_io: z.enum(["none", "low", "medium", "high"]).optional(),
            })
            .optional(),
        })
        .optional(),
      parameters: z
        .array(
          z.object({
            name: z.string(),
            template_key: z.string().regex(/^[a-z0-9]+(-[a-z0-9]+)*$/).optional(),
            type: z.enum([
              "string",
              "integer",
              "number",
              "boolean",
              "array",
              "file",
              "url",
            ]),
            required: z.boolean().default(false),
            default_value: z.union([z.string(), z.number(), z.boolean()]).nullable().optional(),
            description: z.string(),
            aliases: z.array(z.string()).optional(),
            enum: z.array(z.string()).optional(),
            pattern: z.string().optional(),
            minimum: z.number().optional(),
            maximum: z.number().optional(),
          })
        )
        .optional(),
      execution: z.object({
        template: z.string(),
        sandbox: z.enum(["docker", "execFile", "none"]).default("execFile"),
        timeout_seconds: z.number().int().min(1).default(30).optional(),
        shell: z.boolean().default(false).optional(),
        workdir: z.string().optional(),
        env: z.record(z.string()).optional(),
        container: z
          .object({
            image: z.string(),
          })
          .optional(),
      }),
      examples: z
        .array(
          z.object({
            description: z.string(),
            command: z.string(),
          })
        )
        .optional(),
      references: z
        .array(
          z.object({
            label: z.string(),
            url: z.string().url(),
          })
        )
        .optional(),
      mitre_ids: z.array(z.string().regex(/^T\d{4}(\.\d{3})?$/)).optional(),
      phase: z.enum(["recon", "enumeration", "exploitation", "post-exploitation", "forensics", "defense-evasion", "discovery", "collection", "lateral-movement", "exfiltration"]).optional(),
      contributor: z.string().optional(),
      plugins: z.array(z.enum(["copyCode", "mermaid", "tabs", "zoomable"])).optional(),
      items: z.array(z.enum(["Username", "Password", "Hash", "TGS", "TGT", "PFX", "Shell", "NoCreds"])).optional(),
      services: z.array(z.enum(["SMB", "WMI", "DCOM", "Kerberos", "RPC", "LDAP", "NTLM", "DNS", "HTTP", "HTTPS", "FTP", "SMTP", "MSSQL", "MySQL", "PostgreSQL", "WinRM", "LLMNR", "NBT-NS", "MDNS", "ADCS", "SSH"])).optional(),
      attack_types: z.array(z.enum(["Enumeration", "Exploitation", "Persistence", "PrivilegeEscalation", "DefenseEvasion", "CredentialAccess", "Discovery", "LateralMovement", "Collection", "Exfiltration", "Execution"])).optional(),
      global_vars: z.record(z.string()).optional(),
      detections: z.array(z.object({
        type: z.enum(["sigma", "elastic", "splunk", "yara", "clamav", "sysmon", "wdac", "ioc", "blockrule", "other"]),
        url: z.string().url().optional(),
        description: z.string().optional(),
        rule_id: z.string().optional(),
      })).optional(),
    }),
});

export const collections = {
  tools: toolsCollection,
};
