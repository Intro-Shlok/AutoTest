---
id: security-web-aquatone
namespace: security:web:aquatone
name: aquatone
description: Tool for automatic visual inspection and screenshot capture of websites
  across large attack surfaces.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.discovery.asset
  - web.screenshot.service
  - web.fingerprint.http
  - web.enumeration.subdomain
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
  - eyewitness
  - gowitness
artifacts:
  - type: screenshot.png
    description: Website screenshot
    mime: image/png
    trust_level: verified
  - type: report.json
    description: Scan report as JSON
    mime: application/json
    trust_level: verified
  - type: report.html
    description: Visual HTML report with screenshots
    mime: text/html
    trust_level: verified
workflow_edges:
  produces:
    - screenshot-list
    - http-fingerprint
    - live-hosts
  consumes:
    - target-domain
    - subdomain-list
contract:
  inputs:
    - type: network.target.domain
      description: Target domain or list of domains
    - type: network.target.file
      description: File containing list of domains/hosts
    - type: network.target.ports
      description: Ports to check for HTTP/HTTPS services
  outputs:
    - type: screenshot.png
      description: Website screenshot image
      mime: image/png
    - type: report.html
      description: Visual HTML report
      mime: text/html
    - type: report.json
      description: Scan results as JSON
      mime: application/json
  side_effects:
    - network_traffic
    - process_spawn
  resource_cost:
    cpu: medium
    memory_mb: 512
    network: medium
    disk_io: medium
resource_profile:
  cpu: medium
  memory_mb: 512
  network: medium
  disk_io: medium
allowed-tools:
  - aquatone
  - Bash
  - execFile
parameters:
  - name: domains
    type: string
    required: false
    description: "List of domains to scan (space/comma-separated)"
    aliases:
      - --domains
  - name: screenshot-timeout
    type: integer
    required: false
    description: "Timeout for taking screenshots in seconds"
    default_value: "30"
    aliases:
      - --screenshot-timeout
  - name: scan-timeout
    type: integer
    required: false
    description: "Timeout for HTTP requests in seconds"
    default_value: "10"
    aliases:
      - --scan-timeout
  - name: resolve-timeout
    type: integer
    required: false
    description: "Timeout for DNS resolution in seconds"
    default_value: "5"
    aliases:
      - --resolve-timeout
  - name: threads
    type: integer
    required: false
    description: "Number of concurrent threads"
    default_value: "5"
    aliases:
      - --threads
  - name: chrome-path
    type: string
    required: false
    description: "Path to Chrome/Chromium executable"
    aliases:
      - --chrome-path
  - name: proxy
    type: string
    required: false
    description: "HTTP proxy address"
    aliases:
      - --proxy
  - name: ports
    type: string
    required: false
    description: "Ports to scan (comma-separated)"
    default_value: "80,443"
    aliases:
      - --ports
  - name: http-port
    type: string
    required: false
    description: "HTTP ports to check"
    default_value: "80"
    aliases:
      - --http-port
  - name: https-port
    type: string
    required: false
    description: "HTTPS ports to check"
    default_value: "443"
    aliases:
      - --https-port
  - name: fallback-http
    type: boolean
    required: false
    description: "Fall back to HTTP when HTTPS fails"
    aliases:
      - --fallback-http
  - name: output-dir
    type: string
    required: false
    description: "Directory to write output files"
    default_value: "aquatone"
    aliases:
      - --output-dir
      - -out
  - name: quiet
    type: boolean
    required: false
    description: "Suppress verbose output"
    aliases:
      - --quiet
  - name: sites
    type: string
    required: false
    description: "File containing list of sites (one per line)"
    aliases:
      - --sites
  - name: version
    type: boolean
    required: false
    description: "Show version information"
    aliases:
      - --version
      - -v
execution:
  template: "aquatone -out {output-dir} < {input-file}"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
global_vars:
  output-dir: "aquatone"
  input-file: "domains.txt"
examples:
  - description: "Take screenshots of domains from file"
    command: cat domains.txt | aquatone -out screenshots
  - description: "Scan specific ports with custom thread count"
    command: cat domains.txt | aquatone -ports 80,443,8080,8443 -threads 10
  - description: "Use custom Chrome binary"
    command: cat domains.txt | aquatone -chrome-path /usr/bin/chromium-browser
  - description: "Scan through HTTP proxy"
    command: cat domains.txt | aquatone -proxy http://127.0.0.1:8080
  - description: "Screenshot with longer timeout"
    command: cat domains.txt | aquatone -screenshot-timeout 60
references:
  - label: "Aquatone GitHub"
    url: "https://github.com/michenriksen/aquatone"
  - label: "Aquatone on Kali"
    url: "https://www.kali.org/tools/aquatone/"
phase: enumeration
techniques:
  - discovery
  - recon
items:
  - NoCreds
services: []
attack_types:
  - Enumeration
---

# Aquatone — Visual Website Inspection Tool

Aquatone is a tool for automatic visual inspection and screenshot capture of websites across a large number of hosts. It helps identify interesting targets and assess attack surface visually. It also performs HTTP header analysis and provides a beautiful HTML report.

## Basic Usage

```bash
# Screenshot domains from a file
cat domains.txt | aquatone -out screenshots

# Scan with custom ports
cat domains.txt | aquatone -ports 80,443,8080 -threads 10

# Use custom Chrome path
cat domains.txt | aquatone -chrome-path /usr/bin/chromium-browser

# Scan through proxy
cat domains.txt | aquatone -proxy http://127.0.0.1:8080
```

## Output Structure

| File/Directory | Description |
|----------------|-------------|
| `screenshots/` | PNG screenshot files |
| `aquatone_report.html` | Visual HTML report |
| `aquatone_session.json` | Session data |
| `hosts.json` | Host resolution data |
| `urls.txt` | List of discovered URLs |
