---
id: security-web-xsstrike
namespace: security:web:xsstrike
name: xsstrike
description: Advanced XSS detection suite with context-aware payload generation, WAF detection/evasion, and DOM XSS scanning.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.injection.xss
  - web.discovery.xss
  - security.evasion.waf
  - web.scan.dom
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
dependencies:
  - python3
related_tools:
  - dalfox
  - commix
  - beef
artifacts:
  - type: web.xss.report
    description: XSS vulnerability report
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
      description: Target URL to test for XSS
  outputs:
    - type: web.injection.xss.results
      description: XSS vulnerability findings
      mime: text/plain
  side_effects:
    - network_traffic
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
  - xsstrike
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
  - name: json
    type: boolean
    required: false
    description: "Treat POST data as JSON (--json)"
    aliases:
      - --json
  - name: path
    type: boolean
    required: false
    description: "Inject payloads into path (--path)"
    aliases:
      - --path
  - name: crawl
    type: boolean
    required: false
    description: "Crawl the target URL (--crawl)"
    aliases:
      - --crawl
  - name: depth
    type: integer
    required: false
    description: "Crawl depth level (-l)"
    default_value: "2"
    aliases:
      - -l
  - name: threads
    type: integer
    required: false
    description: "Number of threads (-t)"
    default_value: "1"
    aliases:
      - -t
  - name: timeout
    type: integer
    required: false
    description: "Request timeout in seconds (--timeout)"
    default_value: "30"
    aliases:
      - --timeout
  - name: delay
    type: integer
    required: false
    description: "Delay between requests in seconds (-d)"
    default_value: "0"
    aliases:
      - -d
  - name: headers
    type: string
    required: false
    description: "Custom HTTP headers (--headers)"
    aliases:
      - --headers
  - name: proxy
    type: string
    required: false
    description: "Proxy URL (--proxy)"
    aliases:
      - --proxy
  - name: skip-dom
    type: boolean
    required: false
    description: "Skip DOM XSS scanner (--skip-dom)"
    aliases:
      - --skip-dom
  - name: fuzzer
    type: boolean
    required: false
    description: "Enable payload fuzzer (--fuzzer)"
    aliases:
      - --fuzzer
  - name: blind
    type: boolean
    required: false
    description: "Enable blind XSS detection (--blind)"
    aliases:
      - --blind
  - name: silent
    type: boolean
    required: false
    description: "Suppress output banner (-s)"
    aliases:
      - -s
execution:
  template: "python3 xsstrike.py -u {target}"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
global_vars:
  target: url
examples:
  - description: "Basic XSS scan"
    command: python3 xsstrike.py -u "http://target.com/page.php?q=test"
  - description: "Scan with POST data"
    command: python3 xsstrike.py -u "http://target.com/search" --data "q=test"
  - description: "Crawl and scan for XSS"
    command: python3 xsstrike.py -u "http://target.com" --crawl -l 3
  - description: "Use proxy and custom headers"
    command: 'python3 xsstrike.py -u "http://target.com/page.php?q=test" --proxy "http://127.0.0.1:8080" --headers "X-Custom: test"'
  - description: "Blind XSS with fuzzer"
    command: python3 xsstrike.py -u "http://target.com/page.php?q=test" --blind --fuzzer
references:
  - label: "XSStrike GitHub"
    url: "https://github.com/s0md3v/XSStrike"
phase: exploitation
techniques:
  - discovery
  - defense-evasion
  - discovery
items:
  - NoCreds
services: []
attack_types:
  - Exploitation
---

# XSStrike — Advanced XSS Detection

XSStrike is an advanced XSS detection tool with context-aware payload generation, WAF detection and evasion, and DOM XSS scanning capabilities.

## Basic Usage

```bash
# Simple GET parameter test
python3 xsstrike.py -u "http://target.com/page.php?q=test"

# POST request test
python3 xsstrike.py -u "http://target.com/search" --data "q=test"

# JSON data test
python3 xsstrike.py -u "http://target.com/api" --data '{"q":"test"}' --json
```

## Advanced Scanning

```bash
# Crawl and scan
python3 xsstrike.py -u "http://target.com" --crawl -l 3

# Blind XSS detection
python3 xsstrike.py -u "http://target.com/feedback" --blind

# Fuzzer mode
python3 xsstrike.py -u "http://target.com/page.php?q=test" --fuzzer

# WAF evasion
python3 xsstrike.py -u "http://target.com/page.php?q=test" --skip-dom
```
