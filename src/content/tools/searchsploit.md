---
id: security-exploit-searchsploit
namespace: security:exploit:searchsploit
name: searchsploit
description: Command-line search tool for the Exploit-DB archive, enabling offline searching of exploits and shellcode.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - exploit.search
  - vulnerability.lookup
  - exploitdb.query
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
  - metasploit
  - exploit-db
workflow_edges:
  produces:
    - exploit-paths
    - exploit-details
  consumes:
    - search-term
    - cve-id
contract:
  inputs:
    - type: query.string
      description: Search term or CVE ID to look up
  outputs:
    - type: exploit.paths
      description: Local file paths to matching exploits
      mime: text/plain
  side_effects: []
  resource_cost:
    cpu: low
    memory_mb: 32
    network: low
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 32
  network: low
  disk_io: low
allowed-tools:
  - searchsploit
  - Bash
  - execFile
parameters:
  - name: search-term
    type: string
    required: true
    description: "Search term, CVE ID, or exploit title"
    aliases: []
  - name: flag-c
    type: boolean
    required: false
    description: "Case-sensitive search"
    aliases:
      - -c
      - --case
  - name: flag-e
    type: boolean
    required: false
    description: "Exact match search"
    aliases:
      - -e
      - --exact
  - name: flag-w
    type: boolean
    required: false
    description: "Show URLs to Exploit-DB"
    aliases:
      - -w
      - --www
  - name: flag-t
    type: string
    required: false
    description: "Filter by type (dos, local, remote, webapps, shellcode, poc)"
    aliases:
      - -t
      - --type
  - name: flag-p
    type: boolean
    required: false
    description: "Show full path to exploit file"
    aliases:
      - -p
      - --path
  - name: flag-j
    type: boolean
    required: false
    description: "Output results in JSON"
    aliases:
      - -j
      - --json
  - name: flag-id
    type: string
    required: false
    description: "Show details for specific EDB-ID"
    aliases:
      - --id
  - name: flag-title
    type: boolean
    required: false
    description: "Display titles only"
    aliases:
      - --title
  - name: flag-url
    type: boolean
    required: false
    description: "Show Exploit-DB URLs (same as -w)"
    aliases:
      - --url
  - name: flag-nmap
    type: string
    required: false
    description: "Search using Nmap service version output"
    aliases:
      - --nmap
  - name: flag-update
    type: boolean
    required: false
    description: "Update exploit database"
    aliases:
      - --update
execution:
  template: "searchsploit {search-term}"
  sandbox: execFile
  timeout_seconds: 60
  shell: false
global_vars:
  search-term: "eternalblue"
examples:
  - description: "Search for EternalBlue exploits"
    command: searchsploit eternalblue
  - description: "Search by CVE ID"
    command: searchsploit CVE-2021-41773
  - description: "Exact match search"
    command: searchsploit -e Apache 2.4.49
  - description: "Show full local paths"
    command: searchsploit -p 48191
  - description: "Filter by type (webapps)"
    command: searchsploit -t webapps Wordpress
  - description: "Show Exploit-DB URLs and JSON output"
    command: searchsploit -w -j eternalblue
  - description: "Search by Nmap service version"
    command: searchsploit --nmap file.xml
  - description: "Update local exploit database"
    command: searchsploit --update
references:
  - label: "Exploit-DB"
    url: "https://www.exploit-db.com/"
  - label: "Searchsploit manual"
    url: "https://www.exploit-db.com/searchsploit"
phase: enumeration
techniques:
  - discovery
  - enumeration
  - recon
items:
  - NoCreds
services: []
attack_types:
  - Discovery
---
# SearchSploit — Exploit-DB Command-Line Search Tool

SearchSploit is an offline command-line search tool for the Exploit-DB archive. It allows penetration testers to search through the complete collection of exploits, shellcode, and papers without requiring internet access.

## Usage

```bash
searchsploit [options] <search-term>
```

## Common Searches

- **Software name**: `searchsploit apache 2.4.49`
- **CVE ID**: `searchsploit CVE-2024-12345`
- **Platform type**: `searchsploit -t webapps wordpress`
- **Vulnerability type**: `searchsploit -t dos smb`

## Output Fields

| Field | Description |
|-------|-------------|
| EDB-ID | Unique Exploit-DB identifier |
| Title | Exploit title and description |
| Type | Category (webapps, remote, local, dos) |
| Platform | Target platform (windows, linux, etc.) |
| Path | Full local file path to the exploit |
| URL | Exploit-DB web URL |
