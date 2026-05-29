---
id: security-web-kadimus
namespace: security:web:kadimus
name: kadimus
description: LFI (Local File Inclusion) scanning and exploitation tool that detects file inclusion vulnerabilities and leverages them for RCE and file reading.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.lfi.scan
  - web.lfi.exploit
  - web.lfi.rce
  - web.lfi.read-file
platforms:
  - linux
  - macos
  - cross-platform
risk_level: high
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies:
  - libcurl
  - libpcre
related_tools:
  - commix
  - tplmap
  - nmap
artifacts:
  - type: web.lfi.output
    description: LFI exploitation output
    mime: text/plain
    trust_level: verified
  - type: web.lfi.shell
    description: Remote shell access
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - lfi-scan-results
    - remote-access
  consumes:
    - target-url
contract:
  inputs:
    - type: web.target.url
      description: Target URL with file parameter
  outputs:
    - type: web.lfi.output
      description: Read file content or command output
      mime: text/plain
  side_effects:
    - network_traffic
  resource_cost:
    cpu: low
    memory_mb: 32
    network: low
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 32
  network: low
  disk_io: low
allowed-tools:
  - kadimus
  - Bash
  - execFile
parameters:
  - name: url
    type: string
    required: true
    description: "Target URL with injection parameter"
    aliases:
      - -u
      - --url
  - name: flag-parameter
    type: string
    required: false
    description: "Parameter name to test"
    aliases:
      - -p
      - --parameter
  - name: flag-command
    type: string
    required: false
    description: "Command to execute via LFI"
    aliases:
      - -C
      - --command
  - name: flag-scan
    type: boolean
    required: false
    description: "Scan mode - discover possible LFI parameters"
    aliases:
      - -s
      - --scan
  - name: flag-data
    type: string
    required: false
    description: "POST data string"
    aliases:
      - -d
      - --data
  - name: flag-cookie
    type: string
    required: false
    description: "HTTP Cookie header"
    aliases:
      - --cookie
  - name: flag-user-agent
    type: string
    required: false
    description: "Custom User-Agent"
    aliases:
      - -A
      - --user-agent
  - name: flag-proxy
    type: string
    required: false
    description: "HTTP proxy"
    aliases:
      - --proxy
execution:
  template: "kadimus {flag-scan} {flag-parameter} {flag-command} {flag-data} {flag-cookie} {flag-user-agent} {flag-proxy} -u {url}"
  sandbox: execFile
  timeout_seconds: 120
  shell: false
examples:
  - description: "Basic LFI scan"
    command: kadimus -u "http://example.com/page.php?file=test"
  - description: "Execute command via LFI"
    command: kadimus -u "http://example.com/page.php?file=test" -C "id"
  - description: "Scan for LFI parameters"
    command: kadimus -u "http://example.com/page.php?file=test" -s
references:
  - label: "Kadimus GitHub"
    url: "https://github.com/P0cL4bs/Kadimus"
phase: exploitation
techniques:
  - execution
  - discovery
items:
  - Shell
  - NoCreds
services:
  - HTTP
attack_types:
  - Exploitation
  - Execution
install:
    - method: git
      repo_url: "https://github.com/P0cL4bs/kadimus.git"
      commands:
        - "git clone https://github.com/P0cL4bs/kadimus.git"
---

# Kadimus — LFI Scanning and Exploitation

Kadimus is a C-based tool for detecting and exploiting Local File Inclusion (LFI) vulnerabilities. It supports file reading, remote command execution via log poisoning and /proc/self/environ techniques, and automated scanning.

## Usage

```bash
# Basic scan
kadimus -u "http://target.com/page.php?file=test"

# Execute command via LFI
kadimus -u "http://target.com/page.php?file=test" -C "whoami"

# POST request
kadimus -u "http://target.com/page.php" -d "file=test" -C "id"
```
