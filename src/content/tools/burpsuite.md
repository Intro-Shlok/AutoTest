---
id: security-web-burpsuite
namespace: security:web:burpsuite
name: burpsuite
description: Integrated platform for web application security testing with proxy, scanner,
  intruder, repeater, and decoder tools.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.proxy.intercept
  - web.scan.active
  - web.scan.passive
  - web.fuzzing
  - web.session.handling
  - web.decoder
  - web.repeater
  - web.intruder
platforms:
  - linux
  - macos
  - cross-platform
risk_level: medium
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies: []
related_tools:
  - owasp-zap
  - nikto
  - whatweb
artifacts:
  - type: web.scan.project
    description: Burp Suite project file
    mime: application/octet-stream
    trust_level: verified
  - type: web.scan.report
    description: Burp Suite scan report
    mime: text/html
    trust_level: verified
workflow_edges:
  produces:
    - scan-results
    - discoveryed-requests
    - session-tokens
  consumes:
    - target-url
    - proxy-traffic
contract:
  inputs:
    - type: web.target.url
      description: Target application URL
    - type: web.target.host
      description: Target hostname or IP
  outputs:
    - type: web.scan.report
      description: HTML scan report
      mime: text/html
    - type: web.scan.project
      description: Burp project file
      mime: application/octet-stream
  side_effects:
    - network_traffic
    - network_traffic
  resource_cost:
    cpu: high
    memory_mb: 1024
    network: medium
    disk_io: low
resource_profile:
  cpu: high
  memory_mb: 1024
  network: medium
  disk_io: low
allowed-tools:
  - burpsuite
  - Bash
  - execFile
parameters:
  - name: collab-config
    type: file
    required: false
    description: "Collaborator server configuration file"
    aliases:
      - --collaborator-config
  - name: project-file
    type: file
    required: false
    description: "Project file to load"
    aliases:
      - --project-file
  - name: use-defaults
    type: boolean
    required: false
    description: "Start with default configuration"
    aliases:
      - --use-defaults
  - name: diagnostics
    type: boolean
    required: false
    description: "Show diagnostics information"
    aliases:
      - --diagnostics
  - name: help
    type: boolean
    required: false
    description: "Display help information"
    aliases:
      - --help
      - -h
execution:
  template: "burpsuite"
  sandbox: execFile
  timeout_seconds: 3600
  shell: false
global_vars:
  target: url
examples:
  - description: "Launch Burp Suite with default configuration"
    command: burpsuite --use-defaults
  - description: "Launch Burp Suite with a specific project file"
    command: burpsuite --project-file /path/to/project.burp
  - description: "Launch with custom Collaborator configuration"
    command: burpsuite --collaborator-config collab.config
  - description: "Show diagnostics and troubleshooting info"
    command: burpsuite --diagnostics
references:
  - label: "Burp Suite Documentation"
    url: "https://portswigger.net/burp/documentation"
  - label: "Burp Suite Community Edition"
    url: "https://portswigger.net/burp/communitydownload"
phase: exploitation
techniques:
  - discovery
  - discovery
  - discovery
  - discovery
items:
  - NoCreds
services: []
attack_types:
  - Exploitation
install:
    - method: custom
      commands:
        - "wget -O burpsuite.sh https://portswigger.net/burp/releases/download?product=community&type=linux"
        - "chmod +x burpsuite.sh && ./burpsuite.sh"
---

# Burp Suite — Web Application Security Testing Platform

Burp Suite is an integrated platform for performing security testing of web applications. It includes a proxy, scanner, intruder, repeater, sequencer, decoder, and extender tools.

## Key Components

- **Proxy**: Intercept and modify HTTP/HTTPS traffic between browser and target
- **Scanner**: Automated vulnerability scanning (active/passive)
- **Intruder**: Automated parameter fuzzing and brute-forcing
- **Repeater**: Manual request modification and replay
- **Decoder**: Decode/encode data in various formats
- **Extender**: Extend functionality via BApp store plugins

## Basic Usage

```bash
# Launch Burp Suite Community Edition
burpsuite

# Launch with project file
burpsuite --project-file project.burp

# Use defaults (skip config prompts)
burpsuite --use-defaults
```

## Operational Security

- Burp Suite CA certificate must be installed in the browser for HTTPS interception
- Burp Intruder can generate substantial traffic; use rate limiting responsibly
- Scanning without authorization is illegal in many jurisdictions
