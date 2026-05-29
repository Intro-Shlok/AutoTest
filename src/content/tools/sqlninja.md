---
id: security-sqli-sqlninja
namespace: security:sqli:sqlninja
name: sqlninja
description: SQL Server injection and takeover tool that exploits blind SQL injection vulnerabilities for privilege escalation, command execution, and data extraction.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - sqli.blind-exploit
  - sqli.mssql-inject
  - sqli.cmd-exec
  - sqli.privilege-escalation
  - sqli.data-exfil
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
  - perl
  - nmap
related_tools:
  - sqlmap
  - ghauri
  - nmap
artifacts:
  - type: sqli.output
    description: SQL injection exploitation results
    mime: text/plain
    trust_level: verified
  - type: sqli.shell
    description: Command shell via SQL injection
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - sqli-scan-results
    - remote-shell
    - extracted-data
  consumes:
    - target-host
    - target-port
    - inject-point
contract:
  inputs:
    - type: network.target.host
      description: Target SQL Server host
    - type: network.port
      description: Target SQL Server port
    - type: web.target.url
      description: URL with injection point
  outputs:
    - type: sqli.output
      description: Command execution output
      mime: text/plain
    - type: sqli.shell
      description: Interactive shell session
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
  - sqlninja
  - perl
  - Bash
  - execFile
parameters:
  - name: conf
    type: string
    required: true
    description: "Configuration file for the target"
    aliases:
      - -f
      - --conf
  - name: flag-mode
    type: string
    required: false
    description: "Mode (test, attack, sql-shell, os-shell, etc.)"
    aliases:
      - -m
      - --mode
  - name: flag-payload
    type: integer
    required: false
    description: "Payload type number"
    aliases:
      - -p
      - --payload
  - name: flag-timeout
    type: integer
    required: false
    description: "Query timeout in seconds"
    aliases:
      - -t
      - --timeout
execution:
  template: "sqlninja {flag-mode} {flag-payload} {flag-timeout} -f {conf}"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
examples:
  - description: "Test injection point"
    command: sqlninja -f target.conf -m test
  - description: "Get SQL shell"
    command: sqlninja -f target.conf -m sql-shell
  - description: "Get OS shell"
    command: sqlninja -f target.conf -m os-shell
  - description: "Extract data"
    command: sqlninja -f target.conf -m data
references:
  - label: "Sqlninja GitHub"
    url: "https://github.com/sqlmapproject/sqlninja"
phase: exploitation
techniques:
  - execution
  - credential-access
items:
  - Shell
  - Password
  - Hash
services:
  - HTTP
  - MSSQL
attack_types:
  - Exploitation
  - CredentialAccess
install:
    - method: apt
      package_name: "sqlninja"
      commands:
        - "apt-get install -y sqlninja"
---

# Sqlninja — SQL Server Injection Toolkit

Sqlninja is a Perl-based tool for exploiting blind SQL injection vulnerabilities in Microsoft SQL Server. It provides features for privilege escalation, command execution, data extraction, and reverse shell access via out-of-band channels.

## Usage

```bash
# Test injection point (after editing target.conf)
sqlninja -f target.conf -m test

# Interactive SQL shell
sqlninja -f target.conf -m sql-shell

# Interactive OS shell (via xp_cmdshell)
sqlninja -f target.conf -m os-shell

# Data extraction
sqlninja -f target.conf -m data
```
