---
id: security-web-dotdotpwn
namespace: security:web:dotdotpwn
name: dotdotpwn
description: Directory traversal fuzzing tool that tests for path traversal vulnerabilities in web applications and services via HTTP, FTP, and TFTP protocols.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.traversal.fuzz
  - web.traversal.detect
  - web.traversal.http
  - web.traversal.ftp
  - web.traversal.payload
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
dependencies:
  - perl
  - libwww-perl
related_tools:
  - kadimus
  - lfi-suite
  - commix
  - nmap
artifacts:
  - type: web.traversal.report
    description: Directory traversal scan results
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - traversal-scan-results
    - vulnerable-paths
  consumes:
    - target-url
    - target-host
contract:
  inputs:
    - type: web.target.url
      description: Target URL or host
    - type: network.port
      description: Target port
  outputs:
    - type: web.traversal.report
      description: Detected traversal vulnerabilities
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
  - dotdotpwn
  - perl
  - Bash
  - execFile
parameters:
  - name: target
    type: string
    required: true
    description: "Target host or URL"
    aliases:
      - -m
      - --host
  - name: flag-port
    type: integer
    required: false
    description: "Target port"
    aliases:
      - -p
      - --port
  - name: flag-protocol
    type: string
    required: false
    description: "Protocol (http, ftp, tftp)"
    aliases:
      - -P
      - --protocol
  - name: flag-url
    type: string
    required: false
    description: "Full target URL with traversal placeholder"
    aliases:
      - -u
      - --url
  - name: flag-dictionary
    type: string
    required: false
    description: "Custom wordlist file"
    aliases:
      - -d
      - --dictionary
  - name: flag-depth
    type: integer
    required: false
    description: "Traversal depth"
    aliases:
      - --depth
  - name: flag-os
    type: string
    required: false
    description: "Target OS (unix, windows)"
    aliases:
      - -O
      - --os
  - name: flag-file
    type: string
    required: false
    description: "File to search for"
    aliases:
      - -f
      - --file
  - name: flag-output
    type: string
    required: false
    description: "Output file for results"
    aliases:
      - -o
      - --output
  - name: flag-threads
    type: integer
    required: false
    description: "Number of threads"
    aliases:
      - -T
      - --threads
  - name: flag-cookie
    type: string
    required: false
    description: "HTTP Cookie header"
    aliases:
      - -C
      - --cookie
execution:
  template: "dotdotpwn {flag-protocol} {flag-port} {flag-depth} {flag-os} {flag-file} {flag-threads} {flag-dictionary} {flag-cookie} {flag-output} {flag-url} -m {target}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
examples:
  - description: "HTTP directory traversal scan"
    command: dotdotpwn -m http://example.com -u /page.php?file=TRAVERSAL -d /etc/passwd
  - description: "FTP traversal scan"
    command: dotdotpwn -m ftp://example.com -p 21
  - description: "Custom depth and OS"
    command: dotdotpwn -m http://example.com -u /page.php?file=TRAVERSAL -d /etc/passwd --depth 10 -O unix
references:
  - label: "DotDotPwn GitHub"
    url: "https://github.com/wireghoul/dotdotpwn"
phase: exploitation
techniques:
  - execution
  - discovery
items:
  - NoCreds
services:
  - HTTP
  - FTP
attack_types:
  - Exploitation
  - Discovery
install:
    - method: git
      repo_url: "https://github.com/wireghoul/dotdotpwn.git"
      commands:
        - "git clone https://github.com/wireghoul/dotdotpwn.git"
---

# DotDotPwn — Directory Traversal Fuzzer

DotDotPwn is a Perl-based directory/path traversal fuzzer that tests web applications, FTP servers, and TFTP servers for path traversal vulnerabilities. It supports multiple encoding techniques and traversal depths.

## Usage

```bash
# HTTP traversal
dotdotpwn -m http://target.com -u /page.php?file=TRAVERSAL -d /etc/passwd

# FTP traversal
dotdotpwn -m ftp://target.com -p 21

# With cookie authentication
dotdotpwn -m http://target.com -u /page.php?file=TRAVERSAL -C "PHPSESSID=abc123" -d /etc/passwd

# Custom wordlist
dotdotpwn -m http://target.com -u /page.php?file=TRAVERSAL -d mylist.txt --depth 8
```
