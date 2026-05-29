---
id: security-web-h2csmuggler
namespace: security:web:h2csmuggler
name: h2csmuggler
description: HTTP/2 cleartext smuggling tool that exploits connection upgrade to smuggle requests through reverse proxies and load balancers.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.smuggle.h2c
  - web.smuggle.detect
  - web.protocol.h2c-upgrade
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
dependencies:
  - python3
related_tools:
  - smuggler
  - burpsuite
  - nmap
artifacts:
  - type: web.smuggling.report
    description: h2c smuggling scan results
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - smuggling-scan-results
  consumes:
    - target-url
contract:
  inputs:
    - type: web.target.url
      description: Target web server URL
  outputs:
    - type: web.smuggling.report
      description: Scan results for h2c smuggling
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
  - h2csmuggler
  - python3
  - Bash
  - execFile
parameters:
  - name: target
    type: string
    required: true
    description: "Target URL or host:port"
  - name: flag-x
    type: boolean
    required: false
    description: "Check all smuggling variants"
    aliases:
      - -x
      - --check-all
  - name: flag-wait
    type: integer
    required: false
    description: "Wait time in seconds between requests"
    aliases:
      - -w
      - --wait
  - name: flag-proxy
    type: string
    required: false
    description: "HTTP proxy to use"
    aliases:
      - -p
      - --proxy
execution:
  template: "h2csmuggler {flag-x} {flag-wait} {flag-proxy} {target}"
  sandbox: execFile
  timeout_seconds: 120
  shell: false
examples:
  - description: "Basic h2c smuggling test"
    command: h2csmuggler https://example.com
  - description: "Check all smuggling variants"
    command: h2csmuggler -x https://example.com
  - description: "Use proxy for testing"
    command: h2csmuggler -p http://127.0.0.1:8080 https://example.com
references:
  - label: "h2csmuggler GitHub"
    url: "https://github.com/BishopFox/h2csmuggler"
phase: exploitation
techniques:
  - execution
  - discovery
items:
  - NoCreds
services:
  - HTTP
attack_types:
  - Exploitation
install:
    - method: git
      repo_url: "https://github.com/BishopFox/h2csmuggler.git"
      commands:
        - "git clone https://github.com/BishopFox/h2csmuggler.git"
---

# h2csmuggler — HTTP/2 Cleartext Smuggling

h2csmuggler is a tool from Bishop Fox for detecting HTTP/2 cleartext (h2c) smuggling vulnerabilities. It exploits the HTTP/1.1 to HTTP/2 upgrade mechanism to smuggle requests through reverse proxies and load balancers.

## Usage

```bash
# Basic test
h2csmuggler https://example.com

# Check all variants
h2csmuggler -x https://example.com

# Through proxy
h2csmuggler -p http://127.0.0.1:8080 https://example.com
```
