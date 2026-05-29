---
id: security-web-dalfox
namespace: security:web:dalfox
name: dalfox
description: Fast parameter analysis and XSS scanner written in Go with WAF detection, mining, and multi-format output.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.injection.xss
  - web.analysis.parameter
  - security.evasion.waf
  - web.scan.mass
platforms:
  - linux
  - macos
  - cross-platform
risk_level: high
trust_level: community
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies: []
related_tools:
  - xsstrike
  - commix
artifacts:
  - type: web.xss.report
    description: XSS scan results
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - xss-results
    - vulnerable-params
  consumes:
    - target-url
contract:
  inputs:
    - type: web.target.url
      description: Target URL to scan for XSS
  outputs:
    - type: web.injection.xss.results
      description: XSS vulnerability findings
      mime: text/plain
  side_effects:
    - network_traffic
  resource_cost:
    cpu: medium
    memory_mb: 64
    network: medium
    disk_io: low
resource_profile:
  cpu: medium
  memory_mb: 64
  network: medium
  disk_io: low
allowed-tools:
  - dalfox
  - Bash
  - execFile
parameters:
  - name: url
    type: string
    required: true
    description: "Target URL (positional argument)"
    aliases: []
  - name: cookie
    type: string
    required: false
    description: "Cookie string (--cookie)"
    aliases:
      - --cookie
  - name: header
    type: string
    required: false
    description: "Custom HTTP headers (--header)"
    aliases:
      - --header
  - name: data
    type: string
    required: false
    description: "POST data (--data)"
    aliases:
      - --data
  - name: user-agent
    type: string
    required: false
    description: "Custom User-Agent (--user-agent)"
    aliases:
      - --user-agent
  - name: proxy
    type: string
    required: false
    description: "Proxy URL (--proxy)"
    aliases:
      - --proxy
  - name: output
    type: string
    required: false
    description: "Output file (--output)"
    aliases:
      - --output
  - name: format
    type: string
    required: false
    description: "Output format (json, xml, plain) (--format)"
    default_value: "plain"
    aliases:
      - --format
  - name: silent
    type: boolean
    required: false
    description: "Silent mode (--silent)"
    aliases:
      - --silent
  - name: worker
    type: integer
    required: false
    description: "Number of worker threads (-w)"
    default_value: "10"
    aliases:
      - -w
  - name: mass
    type: boolean
    required: false
    description: "Mass scan mode (--mass)"
    aliases:
      - --mass
  - name: timeout
    type: integer
    required: false
    description: "Request timeout in seconds (--timeout)"
    default_value: "10"
    aliases:
      - --timeout
  - name: delay
    type: integer
    required: false
    description: "Delay between requests in ms (--delay)"
    default_value: "0"
    aliases:
      - --delay
  - name: blind
    type: boolean
    required: false
    description: "Blind XSS detection (--blind)"
    aliases:
      - --blind
  - name: mining
    type: boolean
    required: false
    description: "Enable mining mode (--mining)"
    aliases:
      - --mining
execution:
  template: "dalfox url {target}"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
global_vars:
  target: url
examples:
  - description: "Basic XSS scan"
    command: dalfox url http://target.com/page.php?q=test
  - description: "Scan with POST data"
    command: dalfox url http://target.com/login --data "user=admin&pass=test"
  - description: "Mass scan from file"
    command: dalfox pipe < urls.txt
  - description: "Scan with WAF evasion"
    command: dalfox url http://target.com/page.php?q=test --waf-evasion
  - description: "Output in JSON format"
    command: dalfox url http://target.com/page.php?q=test --format json --output results.json
references:
  - label: "Dalfox GitHub"
    url: "https://github.com/hahwul/dalfox"
phase: exploitation
techniques:
  - discovery
  - discovery
  - defense-evasion
items:
  - NoCreds
services: []
attack_types:
  - Exploitation
install:
    - method: go
      repo_url: "github.com/hahwul/dalfox/v2"
      commands:
        - "go install github.com/hahwul/dalfox/v2@latest"
---

# Dalfox — Fast XSS Scanner

Dalfox is a fast, parameter-analysis-based XSS scanner written in Go with WAF detection, mining capabilities, and multiple output format support.

## Basic Usage

```bash
# Single URL scan
dalfox url http://target.com/page.php?id=1

# With POST data
dalfox url http://target.com/login --data "user=test&pass=test"

# With custom headers
dalfox url http://target.com/page.php?id=1 --header "Authorization: Bearer token"
```

## Mass Scanning

```bash
# Pipe URLs from file
cat urls.txt | dalfox pipe

# Mass scan mode
dalfox url http://target.com/page.php?id=1 --mass
```

## Advanced Options

```bash
# Mining mode (find parameters)
dalfox url http://target.com/page.php?id=1 --mining

# WAF evasion
dalfox url http://target.com/page.php?id=1 --waf-evasion

# Blind XSS
dalfox url http://target.com/page.php?id=1 --blind

# JSON output
dalfox url http://target.com/page.php?id=1 --format json -o results.json
```
