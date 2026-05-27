---
id: security-crack-cewl
namespace: security:crack:cewl
name: cewl
description: Custom wordlist generator that spiders websites to gather unique words
  for crafting targeted password lists.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.wordlist.generate
  - security.crack.password
  - web.spider.content
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
  - crunch
  - cupp
  - rsmangler
artifacts:
  - type: security.wordlist.txt
    description: Generated wordlist file
    mime: text/plain
    trust_level: verified
  - type: security.emails.txt
    description: Discovered email addresses
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - wordlist
    - email-list
    - metadata
  consumes:
    - target-url
contract:
  inputs:
    - type: network.target.url
      description: Target URL to spider for word generation
    - type: web.spider.depth
      description: Maximum link depth to spider
  outputs:
    - type: security.wordlist
      description: Generated wordlist file
      mime: text/plain
    - type: security.email.list
      description: Discovered email addresses
      mime: text/plain
    - type: web.metadata
      description: Extracted metadata from documents
      mime: text/plain
  side_effects:
    - network_traffic
    - network_traffic
  resource_cost:
    cpu: low
    memory_mb: 256
    network: medium
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 256
  network: medium
  disk_io: low
allowed-tools:
  - cewl
  - crunch
  - Bash
  - execFile
parameters:
  - name: url
    type: string
    required: true
    description: "Target URL to spider (positional argument)"
    aliases: []
  - name: flag-w
    type: string
    required: false
    description: "Write wordlist to output file"
    aliases:
      - -w
      - --write
  - name: flag-d
    type: integer
    required: false
    description: "Spider depth (default 2)"
    aliases:
      - -d
      - --depth
  - name: flag-m
    type: integer
    required: false
    description: "Minimum word length (default 3)"
    aliases:
      - -m
      - --min-word-length
  - name: flag-x
    type: integer
    required: false
    description: "Maximum word length"
    aliases:
      - -x
      - --max-word-length
  - name: flag-n
    type: boolean
    required: false
    description: "Do not include word count in output"
    aliases:
      - -n
      - --no-count
  - name: flag-o
    type: boolean
    required: false
    description: "Allow offsite spidering"
    aliases:
      - -o
      - --offsite
  - name: with-numbers
    type: boolean
    required: false
    description: "Include words containing numbers"
    aliases:
      - --with-numbers
  - name: lowercase
    type: boolean
    required: false
    description: "Convert all words to lowercase"
    aliases:
      - --lowercase
  - name: convert-umlauts
    type: boolean
    required: false
    description: "Convert umlauts to ASCII equivalents"
    aliases:
      - --convert-umlauts
  - name: flag-a
    type: boolean
    required: false
    description: "Extract metadata from documents"
    aliases:
      - -a
      - --meta
  - name: flag-e
    type: boolean
    required: false
    description: "Extract email addresses"
    aliases:
      - -e
      - --email
  - name: email_file
    type: string
    required: false
    description: "Write discovered emails to file"
    aliases:
      - --email_file
  - name: flag-c
    type: boolean
    required: false
    description: "Include word count in output"
    aliases:
      - -c
      - --count
  - name: flag-u
    type: string
    required: false
    description: "Custom user agent string"
    aliases:
      - -u
      - --user-agent
  - name: flag-v
    type: boolean
    required: false
    description: "Verbose output"
    aliases:
      - -v
      - --verbose
  - name: debug
    type: boolean
    required: false
    description: "Debug mode with extra output"
    aliases:
      - --debug
execution:
  template: "cewl {url} -w {output}"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
global_vars:
  url: ""
  output: "wordlist.txt"
examples:
  - description: "Generate wordlist from website"
    command: cewl https://example.com -w wordlist.txt
  - description: "Spider deeper with custom depth"
    command: cewl https://example.com -d 3 -w wordlist.txt
  - description: "Minimum 6 character words"
    command: cewl https://example.com -m 6 -w wordlist.txt
  - description: "Extract emails from website"
    command: cewl https://example.com -e --email_file emails.txt
  - description: "Extract document metadata"
    command: cewl https://example.com -a -w wordlist.txt
  - description: "Lowercase with numbers allowed"
    command: cewl https://example.com --lowercase --with-numbers -w wordlist.txt
  - description: "Verbose output with custom user agent"
    command: cewl https://example.com -v -u "Mozilla/5.0" -w wordlist.txt
  - description: "Include word count and offsite links"
    command: cewl https://example.com -c -o -w wordlist.txt
references:
  - label: "CeWL GitHub"
    url: "https://github.com/digininja/CeWL"
  - label: "CeWL Documentation"
    url: "https://www.kali.org/tools/cewl/"
phase: exploitation
techniques:
  - credential-access
  - credential-access
items:
  - NoCreds
  - Hash
services: []
attack_types:
  - CredentialAccess
---

# CeWL — Custom Wordlist Generator

CeWL (Custom Word List) is a Ruby application that spiders a given website to a specified depth, returning a list of unique words found on the site. These words are ideal for crafting targeted password lists in penetration tests.

## Key Features

- **Web spidering**: Crawls sites up to configurable depth
- **Metadata extraction**: Pulls metadata from Office documents
- **Email harvesting**: Extracts email addresses found on pages
- **Custom filtering**: Min/max word length, numbers, case control

## Usage Patterns

| Operation | Command | Description |
|-----------|---------|-------------|
| Basic | `cewl https://target.com -w words.txt` | Simple wordlist generation |
| Deep | `cewl https://target.com -d 5 -m 5 -w words.txt` | Deep crawl, min 5 chars |
| Metadata | `cewl https://target.com -a -w words.txt` | Extract document metadata |
| Emails | `cewl https://target.com -e --email_file emails.txt` | Harvest email addresses |

## Wordlist Enhancement

Combine CeWL output with other tools:
- `crunch` — generate permutations based on CeWL words
- `rsmangler` — apply common mangling rules
- `cupp` — generate smart entries from personal info
