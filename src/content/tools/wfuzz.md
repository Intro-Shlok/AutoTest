---
id: security-web-wfuzz
namespace: security:web:wfuzz
name: wfuzz
description: Web application bruteforcer for discovering hidden resources, parameter fuzzing, and content discovery.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.fuzz
  - web.discovery.hidden
  - web.bruteforce.parameters
  - web.content.discovery
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
dependencies: []
related_tools:
  - ffuf
  - gobuster
  - dirsearch
artifacts:
  - type: web.fuzz.output
    description: Fuzzing output results
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - fuzz-results
    - discovered-paths
  consumes:
    - target-url
    - wordlist
contract:
  inputs:
    - type: web.target.url
      description: Target URL with FUZZ placeholder
    - type: web.fuzz.wordlist
      description: Wordlist file for fuzzing
  outputs:
    - type: web.fuzz.results
      description: Fuzzing results with response codes/sizes
      mime: text/plain
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
  - wfuzz
  - Bash
  - execFile
parameters:
  - name: wordlist
    type: string
    required: true
    description: "Path to wordlist file (-w)"
    aliases:
      - -w
  - name: url
    type: string
    required: true
    description: "Target URL with FUZZ keyword (-u)"
    aliases:
      - -u
  - name: method
    type: string
    required: false
    description: "HTTP method (GET, POST, etc.) (-X)"
    default_value: "GET"
    aliases:
      - -X
  - name: headers
    type: string
    required: false
    description: "Additional HTTP headers (-H)"
    aliases:
      - -H
  - name: post-data
    type: string
    required: false
    description: "POST data payload (-d)"
    aliases:
      - -d
  - name: cookies
    type: string
    required: false
    description: "Cookie string (-c)"
    aliases:
      - -c
  - name: threads
    type: integer
    required: false
    description: "Number of concurrent threads (-t)"
    default_value: "10"
    aliases:
      - -t
  - name: proxy
    type: string
    required: false
    description: "Proxy URL (-p)"
    aliases:
      - -p
  - name: filter
    type: string
    required: false
    description: "Filter results by code/word/line (-f)"
    aliases:
      - -f
  - name: hide-codes
    type: string
    required: false
    description: "Hide responses with these HTTP codes (--hc)"
    aliases:
      - --hc
  - name: show-codes
    type: string
    required: false
    description: "Show only responses with these HTTP codes (--sc)"
    aliases:
      - --sc
  - name: verbose
    type: boolean
    required: false
    description: "Verbose output (-v)"
    aliases:
      - -v
  - name: recursive
    type: boolean
    required: false
    description: "Recursive scan (-R)"
    aliases:
      - -R
  - name: follow-redirects
    type: boolean
    required: false
    description: "Follow HTTP redirects (--follow)"
    aliases:
      - --follow
  - name: output
    type: string
    required: false
    description: "Output file (-o)"
    aliases:
      - -o
execution:
  template: "wfuzz -w {wordlist} -u {target}"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
global_vars:
  target: url
  wordlist: "/usr/share/wordlists/dirb/common.txt"
examples:
  - description: "Basic directory fuzzing"
    command: wfuzz -w /usr/share/wordlists/dirb/common.txt -u http://target.com/FUZZ
  - description: "Fuzz with POST method"
    command: wfuzz -w users.txt -X POST -d "username=FUZZ&password=test" -u http://target.com/login
  - description: "Filter out 404 responses"
    command: wfuzz -w wordlist.txt -u http://target.com/FUZZ --hc 404
  - description: "Show only 200 responses"
    command: wfuzz -w wordlist.txt -u http://target.com/FUZZ --sc 200
references:
  - label: "WFuzz GitHub"
    url: "https://github.com/xmendez/wfuzz"
  - label: "WFuzz documentation"
    url: "https://wfuzz.readthedocs.io/"
phase: enumeration
techniques:
  - discovery
  - enumeration
  - credential-access
items:
  - NoCreds
services: []
attack_types:
  - Enumeration
install:
    - method: apt
      package_name: "wfuzz"
      commands:
        - "apt-get install -y wfuzz"
    - method: pip
      package_name: "wfuzz"
      commands:
        - "pip install wfuzz"
---

# WFuzz — Web Application Bruteforcer

WFuzz is a web application bruteforcing tool for discovering hidden resources, fuzzing parameters, and performing content discovery through HTTP response analysis.

## Basic Usage

```bash
# Directory fuzzing
wfuzz -w /usr/share/wordlists/dirb/common.txt -u http://target.com/FUZZ

# Parameter fuzzing
wfuzz -w params.txt -u http://target.com/page.php?FUZZ=1

# POST data fuzzing
wfuzz -w users.txt -X POST -d "username=FUZZ&password=test" -u http://target.com/login
```

## Filtering Results

| Filter | Description |
|--------|-------------|
| `--hc CODE` | Hide responses with specific HTTP code |
| `--hl NUM` | Hide responses with specific line count |
| `--hw NUM` | Hide responses with specific word count |
| `--hh NUM` | Hide responses with specific char count |
| `--sc CODE` | Show only responses with specific code |
| `--sl NUM` | Show only responses with specific line count |
| `--sw NUM` | Show only responses with specific word count |
| `--sh NUM` | Show only responses with specific char count |

## Iterators

WFuzz supports multiple payload types via `-z`:
- `-z list,item1-item2` — inline list
- `-z range,0-10` — numeric range
- `-z file,/path/wordlist.txt` — file-based
