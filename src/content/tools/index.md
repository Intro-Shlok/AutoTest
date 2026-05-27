---
id: repo-root
namespace: internal:meta:repository
name: AutoTest Knowledge Repository
description: Dual-purpose repository for human study and machine-readable automation
version: "1.0.0"
execution:
  template: "echo root documentation page"
  sandbox: none
---

# AutoTest Knowledge Repository

This repository serves as a **dual-purpose knowledge base**:

1. **Human study**: Well-structured, narrative-driven documentation for deep learning
2. **Machine automation**: Highly structured YAML frontmatter and JSON static API for AI agents and MCP servers

## Architecture

- `docs/` — Markdown + YAML frontmatter source files organized by domain
- `schemas/` — JSON Schema definitions for frontmatter validation
- `api/v1/` — Compiled static API endpoints (commands.json, registry.json, by-domain.json)
- `src/` — Astro static site source code

## Quick Start

### For Humans

Browse the [tools index](/tools) or explore by domain.

### For Machines

The repository exposes a static API at:

```
/api/v1/commands.json    — All tools with full metadata
/api/v1/registry.json    — Registry index
/api/v1/by-domain.json   — Tools grouped by domain
```

### For AI Agents

- `/llms.txt` — Curated index for LLM discovery
- `/llms-full.txt` — Concatenated content for one-shot retrieval

## Domains

- [network](/tools?domain=network) — Networking tools (curl, dig, nmap, etc.)
- [system](/tools?domain=system) — OS-level tooling (tar, ps, grep, etc.)
- [security](/tools?domain=security) — Security tools (nmap, metasploit, volatility, etc.)
- [container](/tools?domain=container) — Container ecosystems (docker, podman, kubernetes)
