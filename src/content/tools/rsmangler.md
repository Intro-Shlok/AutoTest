---
id: security-crack-rsmangler
namespace: security:crack:rsmangler
name: rsmangler
description: Wordlist mangling/generation tool that takes a base wordlist and applies transformation rules to create variants.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - wordlist.mangle
  - wordlist.transform
  - wordlist.generate
  - wordlist.mutate
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
  - cewl
artifacts:
  - type: wordlist
    description: Generated mangled wordlist
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - wordlist
  consumes:
    - wordlist
contract:
  inputs:
    - type: wordlist.file
      description: Base wordlist file to mangle
    - type: wordlist.rules
      description: Mangling rules to apply
  outputs:
    - type: wordlist.file
      description: Mangling-generated wordlist
      mime: text/plain
  side_effects: []
  resource_cost:
    cpu: medium
    memory_mb: 128
    network: none
    disk_io: high
resource_profile:
  cpu: medium
  memory_mb: 128
  network: none
  disk_io: high
allowed-tools:
  - rsmangler
  - Bash
parameters:
  - name: flag-i
    type: file
    required: false
    description: Input wordlist file to mangle
    aliases:
      - -i
  - name: flag-o
    type: string
    required: false
    description: Output file for mangled wordlist
    aliases:
      - -o
  - name: flag-l
    type: integer
    required: false
    description: Minimum word length to output
    aliases:
      - -l
  - name: flag-L
    type: integer
    required: false
    description: Maximum word length to output
    aliases:
      - -L
  - name: flag-m
    type: string
    required: false
    description: Mangle rules to apply (comma-separated)
    aliases:
      - -m
  - name: flag-f
    type: string
    required: false
    description: Output format (txt, csv)
    aliases:
      - -f
  - name: flag-p
    type: string
    required: false
    description: Prefix to add to each word
    aliases:
      - -p
  - name: flag-s
    type: string
    required: false
    description: Suffix to add to each word
    aliases:
      - -s
  - name: flag-c
    type: boolean
    required: false
    description: Capitalise first letter of each word
    aliases:
      - -c
  - name: flag-u
    type: boolean
    required: false
    description: Convert all words to uppercase
    aliases:
      - -u
  - name: flag-n
    type: boolean
    required: false
    description: Append numeric sequences to words
    aliases:
      - -n
  - name: flag-v
    type: boolean
    required: false
    description: Verbose output during processing
    aliases:
      - -v
  - name: flag-t
    type: integer
    required: false
    description: Number of threads to use
    aliases:
      - -t
execution:
  template: "rsmangler -i {wordlist} -o {output}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
global_vars:
  wordlist: "base.txt"
  output: "mangled.txt"
examples:
  - description: "Mangle a wordlist with default rules"
    command: rsmangler -i base.txt -o mangled.txt
  - description: "Capitalise first letter and add numeric suffixes"
    command: rsmangler -i base.txt -o mangled.txt -c -n
  - description: "Add prefix and suffix to every word"
    command: rsmangler -i base.txt -o mangled.txt -p "2024" -s "!"
  - description: "Filter output by length and apply custom rules"
    command: rsmangler -i base.txt -l 6 -L 16 -m cap,leet,reverse -o output.txt
  - description: "Uppercase all words with verbose logging"
    command: rsmangler -i base.txt -o output.txt -u -v
references:
  - label: "rsmangler on Kali"
    url: "https://www.kali.org/tools/rsmangler/"
  - label: "rsmangler GitHub"
    url: "https://github.com/digininja/rsmangler"
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
  - CredentialAccess
---

# rsmangler — Wordlist Mangling Tool

rsmangler takes a base wordlist and applies configurable transformation rules — capitalisation, uppercase, leet substitution, prefix/suffix, numeric append, reverse, and more — to produce a much larger set of password candidates for cracking workflows.
