---
id: security-crack-crunch
namespace: security:crack:crunch
name: crunch
description: Wordlist generator that produces all possible combinations and permutations of specified character sets.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - wordlist.generate
  - wordlist.combination
  - wordlist.permutation
  - wordlist.bruteforce
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
  - cewl
  - cupp
  - rsmangler
artifacts:
  - type: wordlist
    description: Generated wordlist file
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - wordlist
  consumes:
    - charset
contract:
  inputs:
    - type: wordlist.minlen
      description: Minimum length of generated words
    - type: wordlist.maxlen
      description: Maximum length of generated words
    - type: wordlist.charset
      description: Character set to use for generation
  outputs:
    - type: wordlist.file
      description: Generated wordlist file
      mime: text/plain
  side_effects: []
  resource_cost:
    cpu: high
    memory_mb: 256
    network: none
    disk_io: high
resource_profile:
  cpu: high
  memory_mb: 256
  network: none
  disk_io: high
allowed-tools:
  - crunch
  - Bash
parameters:
  - name: min-len
    type: integer
    required: true
    description: Minimum length of generated words
    aliases:
      - min
  - name: max-len
    type: integer
    required: true
    description: Maximum length of generated words
    aliases:
      - max
  - name: charset
    type: string
    required: false
    description: Character set to use for generation
    default_value: "abcdefghijklmnopqrstuvwxyz"
    aliases: []
  - name: flag-o
    type: string
    required: false
    description: Output file for wordlist
    aliases:
      - -o
  - name: flag-b
    type: string
    required: false
    description: Size limit (e.g. 50MB)
    aliases:
      - -b
  - name: flag-c
    type: integer
    required: false
    description: Number of words per output file (file splitting)
    aliases:
      - -c
  - name: flag-d
    type: string
    required: false
    description: Limit duplicate characters (e.g. 2@)
    aliases:
      - -d
  - name: flag-e
    type: string
    required: false
    description: Stop generating at this word
    aliases:
      - -e
  - name: flag-f
    type: file
    required: false
    description: Charset file path and charset name
    aliases:
      - -f
  - name: flag-i
    type: boolean
    required: false
    description: Invert output order
    aliases:
      - -i
  - name: flag-p
    type: string
    required: false
    description: Generate permutations of specified words
    aliases:
      - -p
  - name: flag-s
    type: string
    required: false
    description: Start word for generation
    aliases:
      - -s
  - name: flag-t
    type: string
    required: false
    description: Pattern with @,%^ placeholders
    aliases:
      - -t
  - name: flag-z
    type: string
    required: false
    description: Compress output (gzip, bzip2, lzma)
    aliases:
      - -z
execution:
  template: "crunch {min} {max} {charset} -o {output}"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
global_vars:
  min: "8"
  max: "12"
  charset: "abcdefghijklmnopqrstuvwxyz"
  output: "wordlist.txt"
examples:
  - description: "Generate all 6-8 character lowercase words"
    command: crunch 6 8 abcdefghijklmnopqrstuvwxyz -o wordlist.txt
  - description: "Generate words with specific pattern"
    command: crunch 4 4 -t @@%%
  - description: "Generate permutations of words"
    command: crunch 0 0 -p word1 word2 word3
  - description: "Use a charset file"
    command: crunch 6 8 -f /usr/share/crunch/charset.lst mixalpha-numeric
  - description: "Generate with start word"
    command: crunch 8 8 abcdefghijklmnopqrstuvwxyz -s aaaabbbb -o output.txt
  - description: "Limit output to 50MB and compress"
    command: crunch 6 8 abcdefghijklmnopqrstuvwxyz -b 50MB -o START -z gzip
references:
  - label: "Crunch GitHub"
    url: "https://github.com/crunchsec/crunch"
  - label: "Kali Tools — Crunch"
    url: "https://www.kali.org/tools/crunch/"
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
install:
    - method: apt
      package_name: "crunch"
      commands:
        - "apt-get install -y crunch"
---

# Crunch — Wordlist Generator

Crunch is a wordlist generator that creates all possible combinations and permutations from specified character sets. It supports patterns with placeholders (@ for lowercase, , for uppercase, % for numbers, ^ for symbols), output compression (gzip, bzip2, lzma), file splitting, resume capability, and charset file integration.
