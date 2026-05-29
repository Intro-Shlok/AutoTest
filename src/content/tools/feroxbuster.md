---
id: security-web-feroxbuster
namespace: security:web:feroxbuster
name: feroxbuster
description: Fast, recursive content discovery tool written in Rust for directory and
  file brute-forcing with automatic filtering and Burp integration.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.discovery.path
  - web.discovery.file
  - web.discovery.recursive
  - web.content.brute
  - web.filter.response
platforms:
  - linux
  - macos
  - cross-platform
risk_level: medium
trust_level: community
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies: []
related_tools:
  - gobuster
  - dirsearch
  - ffuf
  - wfuzz
artifacts:
  - type: web.discovery.results
    description: Discovered URLs and directories
    mime: application/json
    trust_level: community
workflow_edges:
  produces:
    - discovered-paths
    - content-map
  consumes:
    - target-url
    - wordlist
contract:
  inputs:
    - type: web.target.url
      description: Target URL
    - type: file.wordlist
      description: Wordlist for brute-forcing
    - type: web.file.extension
      description: File extensions to discover
  outputs:
    - type: web.discovery.results
      description: Found paths with status codes
      mime: application/json
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
  - feroxbuster
  - Bash
  - execFile
parameters:
  - name: url
    type: string
    required: true
    description: "Target URL"
    aliases:
      - -u
  - name: wordlist
    type: file
    required: true
    description: "Path to wordlist file"
    aliases:
      - -w
  - name: extensions
    type: string
    required: false
    description: "File extensions to scan (comma-separated)"
    aliases:
      - -x
  - name: threads
    type: integer
    required: false
    description: "Number of concurrent threads"
    default_value: "50"
    aliases:
      - -t
  - name: depth
    type: integer
    required: false
    description: "Maximum recursion depth"
    aliases:
      - -d
  - name: follow-redirect
    type: boolean
    required: false
    description: "Follow HTTP redirects"
    aliases:
      - -r
  - name: status-codes
    type: string
    required: false
    description: "Status codes to include"
    aliases:
      - -s
  - name: output
    type: file
    required: false
    description: "Output file path"
    aliases:
      - -o
  - name: json
    type: boolean
    required: false
    description: "Enable JSON output"
    aliases:
      - --json
  - name: silent
    type: boolean
    required: false
    description: "Silent mode (only output results)"
    aliases:
      - --silent
  - name: headers
    type: string
    required: false
    description: "Custom HTTP headers"
    aliases:
      - -H
  - name: user-agent
    type: string
    required: false
    description: "Custom User-Agent string"
    aliases:
      - -a
  - name: proxy
    type: string
    required: false
    description: "Proxy URL"
    aliases:
      - -P
  - name: timeout
    type: integer
    required: false
    description: "Request timeout in seconds"
    aliases:
      - -T
  - name: verbose
    type: boolean
    required: false
    description: "Verbose output"
    aliases:
      - -v
  - name: filter-status
    type: string
    required: false
    description: "Filter by status codes"
    aliases:
      - --filter-status
  - name: filter-size
    type: string
    required: false
    description: "Filter by response size"
    aliases:
      - --filter-size
  - name: filter-regex
    type: string
    required: false
    description: "Filter by regex pattern"
    aliases:
      - --filter-regex
  - name: filter-words
    type: string
    required: false
    description: "Filter by word count"
    aliases:
      - --filter-words
  - name: filter-lines
    type: string
    required: false
    description: "Filter by line count"
    aliases:
      - --filter-lines
  - name: auto-tune
    type: boolean
    required: false
    description: "Automatically tune scan parameters"
    aliases:
      - --auto-tune
execution:
  template: "feroxbuster -u {target} -w {wordlist} -x {extensions}"
  sandbox: execFile
  timeout_seconds: 1800
  shell: false
global_vars:
  target: url
  wordlist: "/usr/share/wordlists/seclists/Discovery/Web-Content/common.txt"
  extensions: "php,html,js,txt"
examples:
  - description: "Basic directory scan with extensions"
    command: feroxbuster -u https://example.com -w /usr/share/wordlists/dirb/common.txt -x php,html,js -t 50
  - description: "Recursive scan with depth control"
    command: feroxbuster -u https://example.com -w wordlist.txt -d 3 -r -t 30
  - description: "Scan with proxy (Burp Suite integration)"
    command: feroxbuster -u https://example.com -w wordlist.txt -P http://127.0.0.1:8080
  - description: "JSON output with status code filtering"
    command: feroxbuster -u https://example.com -w wordlist.txt --json -o results.json -s 200,204,301
  - description: "Silent mode with custom headers"
    command: 'feroxbuster -u https://example.com -w wordlist.txt --silent -H "Authorization: Bearer token"'
  - description: "Advanced filtering by response attributes"
    command: feroxbuster -u https://example.com -w wordlist.txt --filter-size 0 --filter-status 404,403
  - description: "Auto-tuning for optimal performance"
    command: feroxbuster -u https://example.com -w wordlist.txt --auto-tune
references:
  - label: "Feroxbuster GitHub"
    url: "https://github.com/epi052/feroxbuster"
phase: enumeration
techniques:
  - discovery
  - enumeration
items:
  - NoCreds
services: []
attack_types:
  - Enumeration
install:
    - method: apt
      package_name: "feroxbuster"
      commands:
        - "apt-get install -y feroxbuster"
    - method: cargo
      package_name: "feroxbuster"
      commands:
        - "cargo install feroxbuster"
---

# Feroxbuster — Fast Content Discovery

Feroxbuster is a fast, recursive content discovery tool written in Rust. It combines speed with advanced features like automatic filtering, Burp Suite integration, and recursive scanning.

## Key Features

- **Recursive Scanning**: Automatically crawls discovered directories
- **Auto-Tuning**: Dynamically adjusts scan parameters for speed
- **Advanced Filtering**: Filter by status, size, regex, words, or lines
- **Burp Replay**: Forward results directly to Burp Suite
- **JSON Output**: Structured output for programmatic processing

## Basic Usage

```bash
# Basic directory scan
feroxbuster -u https://example.com -w wordlist.txt -x php,html

# Recursive scan with auto-tuning
feroxbuster -u https://example.com -w wordlist.txt -d 3 -r --auto-tune

# Proxy integration with JSON output
feroxbuster -u https://example.com -w wordlist.txt -P http://127.0.0.1:8080 --json -o output.json
```

## Operational Security

- Use `--silent` to minimize console output
- Auto-tuning adjusts speed to avoid overwhelming targets
- Scanning without authorization is illegal
