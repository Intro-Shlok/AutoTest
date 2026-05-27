---
id: security-web-arjun
namespace: security:web:arjun
name: arjun
description: HTTP parameter discovery tool that finds hidden GET/POST parameters
  by analyzing server responses.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.discovery.parameter
  - web.enumeration.endpoint
  - web.fingerprint.application
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
  - ffuf
  - wfuzz
  - dirsearch
artifacts:
  - type: report.json
    description: Discovered parameters as JSON
    mime: application/json
    trust_level: verified
  - type: report.txt
    description: Discovered parameters as text
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - parameter-list
    - hidden-endpoints
  consumes:
    - target-url
contract:
  inputs:
    - type: web.target.url
      description: Target URL for parameter discovery
    - type: web.target.headers
      description: Custom HTTP headers for requests
    - type: web.target.method
      description: HTTP method (GET/POST) for parameter scanning
  outputs:
    - type: report.json
      description: Discovered parameters as JSON
      mime: application/json
    - type: report.txt
      description: Discovered parameters as text
      mime: text/plain
  side_effects:
    - network_traffic
  resource_cost:
    cpu: low
    memory_mb: 128
    network: medium
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 128
  network: medium
  disk_io: low
allowed-tools:
  - arjun
  - Bash
  - execFile
parameters:
  - name: url
    type: string
    required: true
    description: "Target URL for parameter discovery"
    aliases:
      - -u
      - --url
  - name: output
    type: string
    required: false
    description: "Save output as JSON file"
    aliases:
      - -o
      - --output
  - name: output-text
    type: string
    required: false
    description: "Save output as text file"
    aliases:
      - -oT
      - --output-text
  - name: output-burp
    type: string
    required: false
    description: "Export results in Burp Suite format"
    aliases:
      - -oB
      - --output-burp
  - name: delay
    type: integer
    required: false
    description: "Delay between requests in seconds"
    default_value: "0"
    aliases:
      - -d
      - --delay
  - name: threads
    type: integer
    required: false
    description: "Number of concurrent threads"
    default_value: "2"
    aliases:
      - -t
      - --threads
  - name: wordlist
    type: file
    required: false
    description: "Custom parameter wordlist file"
    aliases:
      - -w
      - --wordlist
  - name: method
    type: string
    required: false
    description: "HTTP method to use (GET or POST)"
    default_value: "GET"
    aliases:
      - -m
      - --method
  - name: import
    type: string
    required: false
    description: "Import parameters from a file"
    aliases:
      - -i
      - --import
  - name: timeout
    type: integer
    required: false
    description: "Request timeout in seconds"
    default_value: "15"
    aliases:
      - -T
      - --timeout
  - name: chunks
    type: integer
    required: false
    description: "Number of parameter chunks to process"
    default_value: "10"
    aliases:
      - -c
      - --chunks
  - name: rate-limit
    type: integer
    required: false
    description: "Maximum requests per second"
    aliases:
      - --rate-limit
  - name: headers
    type: string
    required: false
    description: "Custom HTTP headers (JSON format)"
    aliases:
      - --headers
  - name: passive
    type: boolean
    required: false
    description: "Use passive sources (no active requests)"
    aliases:
      - --passive
  - name: include
    type: string
    required: false
    description: "Include specific parameters to test"
    aliases:
      - --include
  - name: disable-redirects
    type: boolean
    required: false
    description: "Do not follow HTTP redirects"
    aliases:
      - --disable-redirects
  - name: stable
    type: boolean
    required: false
    description: "Use stable mode (no concurrency)"
    aliases:
      - --stable
  - name: quiet
    type: boolean
    required: false
    description: "Suppress banner and progress output"
    aliases:
      - -q
      - --quiet
execution:
  template: "arjun -u {target}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
global_vars:
  target: url
examples:
  - description: "Basic parameter discovery"
    command: arjun -u http://target.com/api/endpoint
  - description: "Multi-threaded discovery with 10 threads"
    command: arjun -u http://target.com/api/endpoint -t 10
  - description: "POST method parameter discovery"
    command: arjun -u http://target.com/login -m POST
  - description: "Save results as JSON"
    command: arjun -u http://target.com/api -o params.json
  - description: "Passive parameter discovery (no active requests)"
    command: arjun -u http://target.com/api --passive
  - description: "Scan with custom wordlist and headers"
    command: "arjun -u http://target.com/api -w custom_params.txt --headers '{\"X-Custom\": \"value\"}'"
references:
  - label: "Arjun GitHub"
    url: "https://github.com/s0md3v/Arjun"
  - label: "Arjun on PyPI"
    url: "https://pypi.org/project/arjun/"
phase: enumeration
techniques:
  - discovery
  - enumeration
items:
  - NoCreds
services: []
attack_types:
  - Enumeration
---

# Arjun — HTTP Parameter Discovery Tool

Arjun is a fast HTTP parameter discovery tool that finds hidden GET and POST parameters by analyzing server response variations. It uses both active brute-forcing and passive sources to uncover undocumented API parameters.

## Basic Usage

```bash
# Basic parameter discovery
arjun -u http://target.com/api/endpoint

# POST method with threads
arjun -u http://target.com/login -m POST -t 10

# Save output as JSON
arjun -u http://target.com/api -o params.json

# Passive mode
arjun -u http://target.com/api --passive
```

## Output Formats

| Format | Flag | Description |
|--------|------|-------------|
| JSON | `-o` | Structured JSON output |
| Text | `-oT` | Plain text parameter list |
| Burp | `-oB` | Burp Suite compatible format |
