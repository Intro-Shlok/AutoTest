---
id: security-web-dirsearch
namespace: security:web:dirsearch
name: dirsearch
description: Advanced web path and content discovery tool for brute-forcing directories
  and files on web servers.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.discovery.path
  - web.discovery.file
  - web.fingerprint.directory
  - web.content.brute
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
dependencies:
  - python3
related_tools:
  - gobuster
  - feroxbuster
  - ffuf
  - wfuzz
artifacts:
  - type: web.discovery.results
    description: Discovered directories and files
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
      description: Wordlist for directory brute-forcing
    - type: web.file.extension
      description: File extensions to discover
  outputs:
    - type: web.discovery.results
      description: Discovered paths and status codes
      mime: application/json
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
  - dirsearch
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
  - name: wordlist
    type: file
    required: false
    description: "Path to wordlist file"
    aliases:
      - -w
      - --wordlist
  - name: extensions
    type: string
    required: false
    description: "File extensions to search (comma-separated)"
    aliases:
      - -e
      - --extensions
  - name: threads
    type: integer
    required: false
    description: "Number of threads (default 30)"
    default_value: "30"
    aliases:
      - -t
      - --threads
  - name: recursive
    type: boolean
    required: false
    description: "Enable recursive brute-force"
    aliases:
      - -r
      - --recursive
  - name: depth
    type: integer
    required: false
    description: "Maximum recursion depth"
    aliases:
      - -R
      - --recursive-depth
  - name: exclude-status
    type: string
    required: false
    description: "Exclude status codes (comma-separated)"
    aliases:
      - -x
      - --exclude-status
  - name: timeout
    type: integer
    required: false
    description: "Request timeout in seconds"
    aliases:
      - --timeout
  - name: follow-redirects
    type: boolean
    required: false
    description: "Follow HTTP redirects"
    aliases:
      - --follow-redirects
  - name: format
    type: string
    required: false
    description: "Output format: json, xml, csv, plain"
    default_value: "plain"
    aliases:
      - --format
  - name: output
    type: file
    required: false
    description: "Output file path"
    aliases:
      - -o
      - --output
  - name: random-agent
    type: boolean
    required: false
    description: "Use random User-Agent headers"
    aliases:
      - --random-agent
  - name: proxy
    type: string
    required: false
    description: "Proxy URL (e.g. http://127.0.0.1:8080)"
    aliases:
      - --proxy
execution:
  template: "dirsearch -u {target} -w {wordlist} -t {threads}"
  sandbox: execFile
  timeout_seconds: 1800
  shell: false
global_vars:
  target: url
  wordlist: "/usr/share/wordlists/dirb/common.txt"
  threads: "30"
examples:
  - description: "Basic directory scan with common wordlist"
    command: dirsearch -u https://example.com -w /usr/share/wordlists/dirb/common.txt
  - description: "Scan with file extensions for web technologies"
    command: dirsearch -u https://example.com -e php,asp,html,js -t 50
  - description: "Recursive scan with depth limit"
    command: dirsearch -u https://example.com -r -R 3 -t 20
  - description: "Exclude 404 and 403 status codes"
    command: dirsearch -u https://example.com -x 404,403
  - description: "Output results to JSON with random user-agent"
    command: dirsearch -u https://example.com --format json -o results.json --random-agent
  - description: "Scan through a proxy (e.g. Burp Suite)"
    command: dirsearch -u https://example.com --proxy http://127.0.0.1:8080
references:
  - label: "Dirsearch GitHub"
    url: "https://github.com/maurosoria/dirsearch"
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

# Dirsearch — Web Path Discovery

Dirsearch is an advanced command-line tool designed to brute-force directories and files in web servers. It is commonly used for content discovery and hidden resource enumeration.

## Key Features

- **Multi-threaded**: Fast scanning with configurable thread count
- **Recursive Scanning**: Automatically discover nested directories
- **Extension Support**: Search for specific file types (php, asp, html, etc.)
- **Multiple Output Formats**: JSON, XML, CSV, plain text
- **Proxy Support**: Route through Burp Suite or other intercepting proxies

## Basic Usage

```bash
# Basic scan
dirsearch -u https://example.com -w /usr/share/wordlists/dirb/common.txt

# With file extensions and recursion
dirsearch -u https://example.com -e php,html -r -R 2

# Output to JSON with proxy
dirsearch -u https://example.com --format json -o results.json --proxy http://127.0.0.1:8080
```

## Operational Security

- High thread counts can cause excessive server load
- Use `--random-agent` to avoid simple User-Agent filtering
- Scanning without authorization is illegal in many jurisdictions
