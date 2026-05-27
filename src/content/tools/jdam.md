---
id: security-web-jdam
namespace: security:web:jdam
name: jdam
description: JSON fuzzer that tests REST APIs and JSON endpoints for input validation vulnerabilities, schema bypass, and injection flaws.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - api.fuzz.json
  - api.test.validation
  - api.discovery.endpoint
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
  - ffuf
  - wfuzz
  - nmap
artifacts:
  - type: api.fuzz.report
    description: JSON fuzzing results
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - fuzz-results
    - vulnerable-endpoints
  consumes:
    - target-url
    - json-schema
contract:
  inputs:
    - type: web.target.url
      description: Target API endpoint URL
    - type: api.schema.json
      description: JSON schema for structure-aware fuzzing
  outputs:
    - type: api.fuzz.report
      description: Fuzzing results with findings
      mime: text/plain
  side_effects:
    - network_traffic
  resource_cost:
    cpu: low
    memory_mb: 64
    network: medium
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 64
  network: medium
  disk_io: low
allowed-tools:
  - jdam
  - python3
  - Bash
  - execFile
parameters:
  - name: url
    type: string
    required: true
    description: "Target API endpoint URL"
    aliases:
      - -u
      - --url
  - name: flag-method
    type: string
    required: false
    description: "HTTP method (GET, POST, PUT, PATCH)"
    aliases:
      - -X
      - --method
  - name: flag-data
    type: string
    required: false
    description: "Base JSON data for fuzzing"
    aliases:
      - -d
      - --data
  - name: flag-header
    type: string
    required: false
    description: "Custom HTTP header"
    aliases:
      - -H
      - --header
  - name: flag-cookie
    type: string
    required: false
    description: "HTTP Cookie header"
    aliases:
      - --cookie
  - name: flag-threads
    type: integer
    required: false
    description: "Number of threads"
    aliases:
      - -t
      - --threads
  - name: flag-proxy
    type: string
    required: false
    description: "HTTP proxy"
    aliases:
      - -p
      - --proxy
  - name: flag-timeout
    type: integer
    required: false
    description: "Request timeout in seconds"
    aliases:
      - --timeout
execution:
  template: "jdam {flag-method} {flag-header} {flag-cookie} {flag-threads} {flag-proxy} {flag-timeout} {flag-data} -u {url}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
examples:
  - description: "Basic JSON fuzzing"
    command: jdam -u https://api.example.com/endpoint -d '{"key":"value"}'
  - description: "POST request with multiple headers"
    command: 'jdam -X POST -u https://api.example.com/submit -d ''{"name":"test"}'' -H "Authorization: Bearer token"'
  - description: "Fuzz through a proxy"
    command: jdam -u https://api.example.com/endpoint -p http://127.0.0.1:8080
references:
  - label: "Jdam GitHub"
    url: "https://github.com/FSecureLABS/Jdam"
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

# Jdam — JSON Fuzzer

Jdam is a JSON fuzzer for testing REST APIs and JSON endpoints. It sends malformed, mutated, and edge-case JSON payloads to detect input validation issues, schema bypasses, and injection vulnerabilities in API implementations.

## Usage

```bash
# Basic fuzzing
jdam -u https://api.target.com/users -d '{"id":1,"name":"test"}'

# POST method
jdam -X POST -u https://api.target.com/create -d '{"title":"test"}'

# Through proxy
jdam -u https://api.target.com/endpoint -p http://127.0.0.1:8080

# Custom auth header
jdam -u https://api.target.com/admin -d '{"role":"user"}' -H "Authorization: Bearer token"
```
