---
id: security-web-smuggler
namespace: security:web:smuggler
name: smuggler
description: HTTP request smuggling scanner that detects and tests for CL.TE, TE.CL, and TE.TE smuggling vulnerabilities in web servers and proxies.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.smuggle.detect
  - web.smuggle.cl-te
  - web.smuggle.te-cl
  - web.smuggle.te-te
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
  - burpsuite
  - nmap
  - h2csmuggler
artifacts:
  - type: web.smuggling.report
    description: Request smuggling scan results
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
      description: Scan results with detected smuggling vectors
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
  - smuggler
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
  - name: flag-no-color
    type: boolean
    required: false
    description: "Disable colored output"
    aliases:
      - --no-color
  - name: flag-timeout
    type: integer
    required: false
    description: "Request timeout in seconds"
    aliases:
      - --timeout
  - name: flag-methods
    type: boolean
    required: false
    description: "Check HTTP method-based smuggling"
    aliases:
      - --methods
execution:
  template: "smuggler {flag-no-color} {flag-methods} {flag-timeout} -u {url}"
  sandbox: execFile
  timeout_seconds: 120
  shell: false
examples:
  - description: "Basic smuggling scan"
    command: smuggler -u https://example.com
  - description: "Scan with extended timeout"
    command: smuggler -u https://example.com --timeout 10
  - description: "Check method-based smuggling"
    command: smuggler -u https://example.com --methods
references:
  - label: "Smuggler GitHub"
    url: "https://github.com/defparam/smuggler"
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
---

# Smuggler — HTTP Request Smuggling Scanner

Smuggler is a Python-based tool for detecting HTTP request smuggling vulnerabilities. It tests for CL.TE (Content-Length / Transfer-Encoding), TE.CL (Transfer-Encoding / Content-Length), and TE.TE (Transfer-Encoding with obfuscation) variants.

## Usage

```bash
# Basic scan
smuggler -u https://example.com

# Disable colors
smuggler -u https://example.com --no-color

# Check method-based smuggling
smuggler -u https://example.com --methods

# Custom timeout
smuggler -u https://example.com --timeout 10
```
