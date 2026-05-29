---
id: security-web-whatweb
namespace: security:web:whatweb
name: whatweb
description: Next-generation web server fingerprinting tool that identifies CMS platforms, frameworks, and technologies.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.fingerprint
  - web.discovery.technology
  - web.recon.cms
  - security.fingerprint.http
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
  - wappalyzer
  - builtwith
  - nikto
artifacts:
  - type: web.fingerprint.report
    description: Technology fingerprint results
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - fingerprint-results
    - technology-stack
  consumes:
    - target-url
contract:
  inputs:
    - type: web.target.url
      description: Target URL to fingerprint
  outputs:
    - type: web.fingerprint.results
      description: List of detected technologies
      mime: text/plain
  side_effects:
    - network_traffic
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
  - whatweb
  - Bash
  - execFile
parameters:
  - name: url
    type: string
    required: true
    description: "Target URL to fingerprint"
    aliases:
      - -u
  - name: verbose
    type: boolean
    required: false
    description: "Verbose output including all plugins (-v)"
    aliases:
      - -v
  - name: aggression
    type: integer
    required: false
    description: "Aggression level 1-5 (-a)"
    default_value: "1"
    aliases:
      - -a
  - name: log-verbose
    type: string
    required: false
    description: "Log verbose output to file (-l)"
    aliases:
      - -l
  - name: output
    type: string
    required: false
    description: "Output file (-o)"
    aliases:
      - -o
  - name: user-agent
    type: string
    required: false
    description: "Custom User-Agent header (-U)"
    aliases:
      - -U
  - name: input-file
    type: string
    required: false
    description: "Read targets from file (-i)"
    aliases:
      - -i
  - name: threads
    type: integer
    required: false
    description: "Number of threads (-t)"
    default_value: "1"
    aliases:
      - -t
  - name: proxy
    type: string
    required: false
    description: "Proxy URL (--proxy)"
    aliases:
      - --proxy
  - name: cookie
    type: string
    required: false
    description: "Cookie string (--cookie)"
    aliases:
      - --cookie
  - name: header
    type: string
    required: false
    description: "Custom HTTP header (--header)"
    aliases:
      - --header
  - name: plugins
    type: string
    required: false
    description: "List of plugins to run (--plugins)"
    aliases:
      - --plugins
  - name: quiet
    type: boolean
    required: false
    description: "Do not display brief banner (--quiet)"
    aliases:
      - --quiet
  - name: no-errors
    type: boolean
    required: false
    description: "Suppress error messages (--no-errors)"
    aliases:
      - --no-errors
  - name: color
    type: boolean
    required: false
    description: "Enable color output (--color)"
    aliases:
      - --color
execution:
  template: "whatweb {target} -v"
  sandbox: execFile
  timeout_seconds: 120
  shell: false
global_vars:
  target: url
examples:
  - description: "Basic fingerprint scan"
    command: whatweb example.com
  - description: "Verbose output with all plugins"
    command: whatweb example.com -v
  - description: "Aggressive scan with level 3"
    command: whatweb example.com -a 3
  - description: "Scan multiple targets from file"
    command: whatweb -i targets.txt
  - description: "Output results to file"
    command: whatweb example.com -o report.txt
references:
  - label: "WhatWeb GitHub"
    url: "https://github.com/urbanadventurer/WhatWeb"
  - label: "WhatWeb documentation"
    url: "https://github.com/urbanadventurer/WhatWeb/wiki"
phase: enumeration
techniques:
  - recon
  - recon
items:
  - NoCreds
services: []
attack_types:
  - Enumeration
install:
    - method: apt
      package_name: "whatweb"
      commands:
        - "apt-get install -y whatweb"
---

# WhatWeb — Web Fingerprinting Tool

WhatWeb identifies websites by recognizing various content management systems, JavaScript libraries, web servers, and other technologies through HTTP response analysis.

## Basic Usage

```bash
# Simple fingerprint scan
whatweb example.com

# Verbose output with full plugin details
whatweb example.com -v

# Aggressive scan (level 3)
whatweb example.com -a 3

# Scan from file
whatweb -i targets.txt
```

## Aggression Levels

| Level | Description |
|-------|-------------|
| 1 | Passive: fast, minimal requests |
| 2 | Polite: moderate requests |
| 3 | Aggressive: active probing |
| 4 | Heavy: intensive scanning |
| 5 | Complete: all plugins at max depth |

## Output Formats

```bash
# Verbose log to file
whatweb example.com -l verbose.log

# Colored output
whatweb example.com --color

# Quiet mode (no banner)
whatweb example.com --quiet
```
