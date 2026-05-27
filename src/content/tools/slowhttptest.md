---
id: security-dos-slowhttptest
namespace: security:dos:slowhttptest
name: slowhttptest
description: DoS testing tool that simulates Slow HTTP attacks including Slowloris, Slow HTTP POST, and Slow Read to test server resilience against application-layer DoS.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - dos.slowloris
  - dos.slow-post
  - dos.slow-read
  - dos.test-resilience
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
dependencies: []
related_tools:
  - nmap
  - metasploit
artifacts:
  - type: dos.test.report
    description: Slow HTTP test results
    mime: text/html
    trust_level: verified
  - type: dos.test.csv
    description: Test results as CSV
    mime: text/csv
    trust_level: verified
workflow_edges:
  produces:
    - dos-test-results
    - server-stats
  consumes:
    - target-host
    - target-port
contract:
  inputs:
    - type: network.target.host
      description: Target hostname or IP
    - type: network.port
      description: Target port (default 80 or 443)
  outputs:
    - type: dos.test.report
      description: HTML report of DoS test
      mime: text/html
    - type: dos.test.csv
      description: Statistics in CSV format
      mime: text/csv
  side_effects:
    - network_traffic
  resource_cost:
    cpu: low
    memory_mb: 64
    network: high
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 64
  network: high
  disk_io: low
allowed-tools:
  - slowhttptest
  - Bash
  - execFile
parameters:
  - name: target
    type: string
    required: true
    description: "Target hostname or IP"
  - name: flag-port
    type: integer
    required: false
    description: "Target port"
    aliases:
      - -p
      - --port
  - name: flag-type
    type: string
    required: false
    description: "Attack type (slowloris, slowbody, slowread)"
    aliases:
      - -t
      - --type
  - name: flag-num-connections
    type: integer
    required: false
    description: "Number of connections"
    aliases:
      - -c
      - --connections
  - name: flag-interval
    type: integer
    required: false
    description: "Interval between follow-up data in seconds"
    aliases:
      - -i
      - --interval
  - name: flag-duration
    type: integer
    required: false
    description: "Test duration in seconds"
    aliases:
      - -d
      - --duration
  - name: flag-ssl
    type: boolean
    required: false
    description: "Use SSL/TLS"
    aliases:
      - -s
      - --ssl
  - name: flag-verbose
    type: boolean
    required: false
    description: "Verbose output"
    aliases:
      - -v
      - --verbose
  - name: flag-output
    type: string
    required: false
    description: "Output file prefix for report files"
    aliases:
      - -o
      - --output
  - name: flag-random-agent
    type: boolean
    required: false
    description: "Random User-Agent header"
    aliases:
      - -r
      - --random-agent
  - name: flag-method
    type: string
    required: false
    description: "HTTP method for slowbody (POST, PUT)"
    aliases:
      - -m
      - --method
  - name: flag-content-length
    type: integer
    required: false
    description: "Content-Length header value for slowbody"
    aliases:
      - -l
      - --content-length
execution:
  template: "slowhttptest {flag-type} {flag-ssl} {flag-verbose} {flag-random-agent} {flag-num-connections} {flag-interval} {flag-duration} {flag-content-length} {flag-method} {flag-output} -p {flag-port} {target}"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
examples:
  - description: "Slowloris attack"
    command: slowhttptest -c 1000 -i 10 -d 120 -t slowloris -p 80 example.com
  - description: "Slow HTTP POST attack"
    command: slowhttptest -c 500 -i 5 -d 120 -t slowbody -p 443 -s example.com
  - description: "Slow Read attack"
    command: slowhttptest -c 200 -i 10 -d 60 -t slowread -p 443 -s example.com
  - description: "SSL test with verbose output"
    command: slowhttptest -c 1000 -i 10 -d 180 -t slowloris -p 443 -s -v example.com
references:
  - label: "slowhttptest GitHub"
    url: "https://github.com/shekyan/slowhttptest"
phase: exploitation
techniques:
  - impact
  - execution
items:
  - NoCreds
services:
  - HTTP
  - HTTPS
attack_types:
  - Exploitation
---

# slowhttptest — Slow HTTP DoS Testing

slowhttptest is a C-based tool for testing web server resilience against Slow HTTP DoS attacks. It implements Slowloris (slow headers), Slow HTTP POST (slow body), and Slow Read attacks to exhaust server connection pools.

## Usage

```bash
# Slowloris attack
slowhttptest -c 1000 -i 10 -d 120 -t slowloris example.com

# Slow HTTP POST
slowhttptest -c 500 -i 5 -d 180 -t slowbody example.com

# Slow Read over SSL
slowhttptest -c 200 -i 10 -d 60 -t slowread -s example.com:443

# Generate HTML report
slowhttptest -c 1000 -i 10 -d 120 -t slowloris -o report example.com
```
