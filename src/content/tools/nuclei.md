---
id: security-web-nuclei
namespace: security:web:nuclei
name: nuclei
description: Fast, template-based vulnerability scanner from ProjectDiscovery that uses YAML templates to scan for CVEs, misconfigurations, and security issues.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.scan.vulnerability
  - security.scan.cve
  - web.scan.misconfiguration
  - security.scan.automated
  - network.discovery.vulnerability
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
  - httpx
  - katana
  - subfinder
  - nikto
artifacts:
  - type: report.json
    description: Nuclei scan results as JSON
    mime: application/json
    trust_level: verified
  - type: report.txt
    description: Nuclei scan results as text
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - scan-results
    - vulnerability-report
  consumes:
    - target-url
    - host-list
contract:
  inputs:
    - type: network.target.url
      description: Single target URL
    - type: network.target.domain.list
      description: File with list of targets
    - type: network.target.ip
      description: Target IP address
  outputs:
    - type: report.json
      description: Scan findings in JSON format
      mime: application/json
    - type: report.txt
      description: Scan findings in text format
      mime: text/plain
  side_effects:
    - network_traffic
    - network_traffic
  resource_cost:
    cpu: medium
    memory_mb: 256
    network: high
    disk_io: low
resource_profile:
  cpu: medium
  memory_mb: 256
  network: high
  disk_io: low
allowed-tools:
  - nuclei
  - Bash
  - execFile
parameters:
  - name: target
    type: string
    required: false
    description: "Single target URL"
    aliases:
      - -u
      - --target
  - name: list
    type: string
    required: false
    description: "File with list of targets"
    aliases:
      - -l
      - --list
  - name: templates
    type: string
    required: false
    description: "Template or directory of templates to run"
    aliases:
      - -t
      - --templates
  - name: severity
    type: string
    required: false
    description: "Filter by severity (info, low, medium, high, critical)"
    aliases:
      - -s
      - --severity
  - name: tags
    type: string
    required: false
    description: "Filter by template tags"
    aliases:
      - -tags
  - name: flag-json
    type: boolean
    required: false
    description: "Output as JSON lines"
    aliases:
      - -j
      - --json
  - name: flag-o
    type: string
    required: false
    description: "Output file path"
    aliases:
      - -o
      - --output
  - name: flag-rate-limit
    type: integer
    required: false
    description: "Maximum requests per second"
    aliases:
      - -rl
      - --rate-limit
  - name: flag-bulk-size
    type: integer
    required: false
    description: "Max targets to process in parallel"
    aliases:
      - -bs
      - --bulk-size
  - name: flag-stats
    type: boolean
    required: false
    description: "Display scan statistics"
    aliases:
      - -stats
  - name: flag-verbose
    type: boolean
    required: false
    description: "Verbose output"
    aliases:
      - -v
      - --verbose
execution:
  template: "nuclei {flags} {target}"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
examples:
  - description: "Scan a single target with all templates"
    command: nuclei -u https://example.com
  - description: "Run only CVE templates on a target"
    command: nuclei -u https://example.com -t cves/
  - description: "Scan multiple targets from a file"
    command: nuclei -l urls.txt -json -o results.json
  - description: "Filter by severity"
    command: nuclei -u https://example.com -severity critical,high
  - description: "Scan using specific tags"
    command: nuclei -u https://example.com -tags rce,oauth
  - description: "Pipeline from httpx"
    command: subfinder -d example.com | httpx -silent | nuclei -t cves/ -json
references:
  - label: "nuclei GitHub"
    url: "https://github.com/projectdiscovery/nuclei"
  - label: "nuclei Documentation"
    url: "https://docs.projectdiscovery.io/tools/nuclei"
  - label: "nuclei Templates"
    url: "https://github.com/projectdiscovery/nuclei-templates"
phase: exploitation
techniques:
  - discovery
  - execution
items:
  - NoCreds
services:
  - HTTP
  - HTTPS
  - DNS
attack_types:
  - Exploitation
  - Discovery
---

# nuclei — Template-Based Vulnerability Scanner

nuclei is a fast vulnerability scanner from ProjectDiscovery that sends requests across targets using customizable YAML templates, enabling rapid and extensible scanning for CVEs, misconfigurations, exposed panels, and security issues.

## Template Categories

| Directory | Purpose |
|-----------|---------|
| `cves/` | CVE-identified vulnerabilities |
| `exposed-panels/` | Admin/login panels |
| `misconfiguration/` | Security misconfigurations |
| `technologies/` | Technology fingerprinting |
| `default-logins/` | Default credentials |

## Pipeline Scanning

```bash
# Full recon pipeline
subfinder -d target.com | httpx -silent | nuclei -t cves/ -json

# Scan from live hosts only
cat live-hosts.txt | nuclei -t ~/nuclei-templates/ -severity critical,high
```

## Common Scans

```bash
# Scan a single URL
nuclei -u https://example.com

# Run specific template categories
nuclei -u https://example.com -t cves/ -t misconfiguration/

# Output results
nuclei -l targets.txt -json -o scan-results.json
```
