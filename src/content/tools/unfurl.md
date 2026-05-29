---
id: security-recon-unfurl
namespace: security:recon:unfurl
name: unfurl
description: URL extraction and analysis tool by tomnomnom that parses URLs and extracts components (domains, paths, params, values) for recon and data processing.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.recon.url-parse
  - web.recon.url-extract
  - web.recon.data-filter
platforms:
  - linux
  - macos
  - cross-platform
risk_level: low
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies: []
related_tools:
  - waybackurls
  - gau
  - waymore
  - katana
artifacts:
  - type: web.url.components
    description: Extracted URL components
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - url-components
    - extracted-domains
    - extracted-paths
  consumes:
    - url-list
contract:
  inputs:
    - type: web.url.list
      description: List of URLs to analyze
  outputs:
    - type: web.url.components
      description: Extracted URL components by category
      mime: text/plain
  side_effects: []
  resource_cost:
    cpu: low
    memory_mb: 32
    network: none
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 32
  network: none
  disk_io: low
allowed-tools:
  - unfurl
  - Bash
  - execFile
parameters:
  - name: flag-unique
    type: boolean
    required: false
    description: "Unique values only"
    aliases:
      - -u
      - --unique
  - name: mode
    type: string
    required: false
    description: "Extraction mode (domains, paths, keys, values, combos)"
  - name: flag-input
    type: string
    required: false
    description: "Input file (default: stdin)"
    aliases:
      - -i
      - --input
execution:
  template: "unfurl {flag-unique} {mode}"
  sandbox: execFile
  timeout_seconds: 60
  shell: false
examples:
  - description: "Extract unique domains from URLs"
    command: "cat urls.txt | unfurl unique domains"
  - description: "Extract paths from URLs"
    command: "cat urls.txt | unfurl paths"
  - description: "Extract URL parameter keys"
    command: "cat urls.txt | unfurl keys"
  - description: "Extract parameter values"
    command: "cat urls.txt | unfurl values"
  - description: "Extract key=value pairs"
    command: "cat urls.txt | unfurl combos"
references:
  - label: "Unfurl GitHub"
    url: "https://github.com/tomnomnom/unfurl"
phase: recon
techniques:
  - recon
  - discovery
items:
  - NoCreds
services: []
attack_types:
  - Discovery
  - Enumeration
install:
    - method: go
      repo_url: "github.com/tomnomnom/unfurl"
      commands:
        - "go install github.com/tomnomnom/unfurl@latest"
---

# Unfurl — URL Extraction and Analysis

Unfurl is a Go tool by tomnomnom for extracting and analyzing URLs. It parses URLs from stdin and outputs specific components like domains, paths, query parameters, and values — useful for processing large URL lists from recon tools.

## Usage

```bash
# Extract unique domains
cat urls.txt | unfurl unique domains

# Extract paths
cat urls.txt | unfurl paths

# Extract parameter keys
cat urls.txt | unfurl keys

# Extract parameter values
cat urls.txt | unfurl values

# Extract key=value combos
cat urls.txt | unfurl combos
```
