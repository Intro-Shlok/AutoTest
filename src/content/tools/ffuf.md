---
id: security-web-ffuf
namespace: security:web:ffuf
name: ffuf
description: Fast web fuzzer written in Go for directory discovery, parameter fuzzing,
  virtual host enumeration, and value brute-forcing.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.fuzzing.directory
  - web.fuzzing.parameter
  - web.discovery.vhost
  - web.fuzzing.value
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
  - feroxbuster
  - dirsearch
  - wfuzz
artifacts:
  - type: web.fuzzing.results
    description: Fuzzing results in JSON format
    mime: application/json
    trust_level: community
  - type: web.fuzzing.html
    description: HTML fuzzing report
    mime: text/html
    trust_level: community
workflow_edges:
  produces:
    - discovery-results
    - discovered-paths
    - discovered-vhosts
  consumes:
    - target-url
    - wordlist
    - fuzz-parameters
contract:
  inputs:
    - type: web.target.url
      description: Target URL with FUZZ keyword
    - type: file.wordlist
      description: Wordlist for fuzzing
    - type: web.http.method
      description: HTTP method (GET, POST, etc.)
  outputs:
    - type: web.fuzzing.results
      description: Fuzzing results in JSON
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
  - ffuf
  - Bash
  - execFile
parameters:
  - name: url
    type: string
    required: true
    description: "Target URL with FUZZ keyword"
    aliases:
      - -u
  - name: wordlist
    type: file
    required: true
    description: "Path to wordlist file"
    aliases:
      - -w
  - name: method
    type: string
    required: false
    description: "HTTP method (GET, POST, PUT, etc.)"
    default_value: "GET"
    aliases:
      - -X
  - name: headers
    type: string
    required: false
    description: "Custom HTTP headers"
    aliases:
      - -H
  - name: data
    type: string
    required: false
    description: "POST request body"
    aliases:
      - -d
  - name: proxy
    type: string
    required: false
    description: "Proxy URL"
    aliases:
      - -p
  - name: threads
    type: integer
    required: false
    description: "Number of concurrent threads"
    default_value: "40"
    aliases:
      - -t
  - name: output
    type: file
    required: false
    description: "Output file path"
    aliases:
      - -o
  - name: output-format
    type: string
    required: false
    description: "Output format: json, csv, html, md"
    default_value: "json"
    aliases:
      - -of
  - name: filter-code
    type: string
    required: false
    description: "Filter by HTTP status codes"
    aliases:
      - -fc
  - name: filter-size
    type: string
    required: false
    description: "Filter by response size"
    aliases:
      - -fs
  - name: filter-words
    type: string
    required: false
    description: "Filter by word count"
    aliases:
      - -fw
  - name: filter-lines
    type: string
    required: false
    description: "Filter by line count"
    aliases:
      - -fl
  - name: follow-redirect
    type: boolean
    required: false
    description: "Follow HTTP redirects"
    aliases:
      - -r
  - name: recursion
    type: boolean
    required: false
    description: "Enable recursion"
    aliases:
      - -recursion
  - name: recursion-depth
    type: integer
    required: false
    description: "Maximum recursion depth"
    aliases:
      - -recursion-depth
  - name: auto-calibration
    type: boolean
    required: false
    description: "Auto-calibrate filtering"
    aliases:
      - -ac
  - name: extension
    type: string
    required: false
    description: "File extension to append"
    aliases:
      - -e
  - name: silent
    type: boolean
    required: false
    description: "Silent mode"
    aliases:
      - -s
  - name: verbose
    type: boolean
    required: false
    description: "Verbose output"
    aliases:
      - -v
  - name: timeout
    type: integer
    required: false
    description: "HTTP request timeout in seconds"
    aliases:
      - -timeout
execution:
  template: "ffuf -u {target} -w {wordlist} -t {threads}"
  sandbox: execFile
  timeout_seconds: 1800
  shell: false
global_vars:
  target: url
  wordlist: "/usr/share/wordlists/seclists/Discovery/Web-Content/common.txt"
  threads: "40"
examples:
  - description: "Directory discovery with common wordlist"
    command: ffuf -u https://example.com/FUZZ -w /usr/share/wordlists/dirb/common.txt
  - description: "Parameter fuzzing with POST data"
    command: ffuf -u https://example.com/login -X POST -d "user=admin&password=FUZZ" -w passwords.txt -fc 401
  - description: "Virtual host enumeration"
    command: 'ffuf -u https://example.com -H "Host: FUZZ.example.com" -w vhosts.txt -fc 200'
  - description: "Extension-based directory discovery"
    command: ffuf -u https://example.com/FUZZ -w wordlist.txt -e .php,.html,.asp -t 50
  - description: "Recursive scan with auto-calibration"
    command: ffuf -u https://example.com/FUZZ -w wordlist.txt -recursion -recursion-depth 3 -ac
  - description: "Output to JSON with status code filtering"
    command: ffuf -u https://example.com/FUZZ -w wordlist.txt -o results.json -of json -fc 404,403
  - description: "Through Burp proxy"
    command: ffuf -u https://example.com/FUZZ -w wordlist.txt -p http://127.0.0.1:8080
references:
  - label: "FFUF GitHub"
    url: "https://github.com/ffuf/ffuf"
  - label: "FFUF Documentation"
    url: "https://github.com/ffuf/ffuf/wiki"
phase: enumeration
techniques:
  - discovery
  - enumeration
  - discovery
items:
  - NoCreds
services: []
attack_types:
  - Enumeration
---

# FFUF — Fast Web Fuzzer

FFUF (Fuzz Faster U Fool) is a fast web fuzzer written in Go. It is designed for directory discovery, parameter fuzzing, virtual host enumeration, and value brute-forcing with advanced filtering capabilities.

## Key Features

- **Multi-Mode Fuzzing**: Directory, parameter, vhost, and value fuzzing
- **Advanced Filtering**: Filter by status code, size, words, or lines
- **Recursion**: Automatically fuzz discovered directories
- **Auto-Calibration**: Intelligent baseline detection
- **Multiple Output Formats**: JSON, CSV, HTML, Markdown

## Fuzzing Modes

| Mode | Example |
|------|---------|
| Directory | `ffuf -u https://target/FUZZ -w wordlist.txt` |
| Parameter | `ffuf -u https://target/page?FUZZ=1 -w params.txt` |
| VHost | `ffuf -u https://target -H "Host: FUZZ.target" -w hosts.txt` |
| POST data | `ffuf -u https://target/login -X POST -d "user=FUZZ" -w users.txt` |

## Basic Usage

```bash
# Directory discovery
ffuf -u https://example.com/FUZZ -w /usr/share/wordlists/dirb/common.txt -t 50

# VHost enumeration
ffuf -u https://example.com -H "Host: FUZZ.example.com" -w vhosts.txt -fc 200

# Parameter fuzzing with filtering
ffuf -u https://example.com/page?FUZZ=1 -w params.txt -fc 404 -fs 0
```

## Operational Security

- High thread counts can overwhelm targets
- Use auto-calibration (`-ac`) for smarter filtering
- FFUF does not follow redirects by default (use `-r`)
- Scanning without authorization is illegal
