/**
 * STIX 2.1 bundle generator for AutoTest tool definitions.
 * Replaces the Python SDK (src/sdk/cli.py export --stix) with pure JS.
 */

export function toStixBundle(commands) {
  const objects = commands
    .filter((cmd) => cmd.id && /^[a-z0-9]+(-[a-z0-9]+)+$/.test(cmd.id))
    .map((cmd) => {
      const killChainPhases = [];
      if (cmd.phase) {
        killChainPhases.push({
          kill_chain_name: "mitre-attack",
          phase_name: cmd.phase,
        });
      }

      const externalReferences = [];
      if (cmd.references) {
        for (const ref of cmd.references) {
          externalReferences.push({
            source_name: ref.label,
            url: ref.url,
          });
        }
      }
      if (cmd.mitre_ids) {
        for (const mid of cmd.mitre_ids) {
          externalReferences.push({
            source_name: "mitre-attack",
            external_id: mid,
            url: `https://attack.mitre.org/techniques/${mid.replace(".", "/")}/`,
          });
        }
      }

      return {
        type: "attack-pattern",
        spec_version: "2.1",
        id: `attack-pattern--${cmd.id}`,
        name: cmd.name,
        description: cmd.description,
        aliases: [cmd.namespace],
        kill_chain_phases: killChainPhases,
        external_references: externalReferences,
        x_mitre_platforms: cmd.platforms || [],
        x_autotest_namespace: cmd.namespace,
        x_autotest_version: cmd.version,
        x_autotest_capabilities: cmd.capabilities || [],
        x_autotest_techniques: cmd.techniques || [],
        x_autotest_attack_types: cmd.attack_types || [],
        x_autotest_phase: cmd.phase || null,
        x_autotest_services: cmd.services || [],
      };
    });

  const timestamp = new Date()
    .toISOString()
    .replace(/[:-]/g, "")
    .replace(/\..+/, "");

  return {
    type: "bundle",
    id: `bundle--${timestamp}`,
    spec_version: "2.1",
    objects,
  };
}
