---
id: security-crack-cupp
namespace: security:crack:cupp
name: cupp
description: Common User Passwords Profiler — generates intelligent wordlists based on personal profile information gathered from the target.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - wordlist.generate
  - wordlist.profile
  - wordlist.social
  - wordlist.mangle
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
  - python3
related_tools:
  - crunch
  - cewl
  - rsmangler
artifacts:
  - type: wordlist
    description: Generated profile-based wordlist
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - wordlist
  consumes:
    - profile-data
contract:
  inputs:
    - type: wordlist.profile.name
      description: Target name
    - type: wordlist.profile.birth
      description: Target birth date
    - type: wordlist.profile.pet
      description: Target pet name
    - type: wordlist.profile.company
      description: Target company name
  outputs:
    - type: wordlist.file
      description: Generated profile-based wordlist
      mime: text/plain
  side_effects: []
  resource_cost:
    cpu: low
    memory_mb: 64
    network: none
    disk_io: medium
resource_profile:
  cpu: low
  memory_mb: 64
  network: none
  disk_io: medium
allowed-tools:
  - cupp
  - python3
  - Bash
parameters:
  - name: flag-i
    type: boolean
    required: false
    description: Interactive mode — prompts for personal details
    aliases:
      - -i
  - name: flag-l
    type: file
    required: false
    description: Parse a username list from file
    aliases:
      - -l
  - name: flag-w
    type: string
    required: false
    description: Wordlist output filename
    aliases:
      - -w
  - name: flag-a
    type: boolean
    required: false
    description: Parse all usernames from a web page
    aliases:
      - -a
  - name: flag-q
    type: boolean
    required: false
    description: Quiet mode (no banner)
    aliases:
      - -q
  - name: flag-v
    type: boolean
    required: false
    description: Verbose mode
    aliases:
      - -v
  - name: name
    type: string
    required: false
    description: Target first name
    aliases:
      - --name
  - name: surname
    type: string
    required: false
    description: Target surname
    aliases:
      - --surname
  - name: nick
    type: string
    required: false
    description: Target nickname
    aliases:
      - --nick
  - name: birth
    type: string
    required: false
    description: Target birth date (DDMMYYYY)
    aliases:
      - --birth
  - name: pet
    type: string
    required: false
    description: Target pet name
    aliases:
      - --pet
  - name: company
    type: string
    required: false
    description: Target company name
    aliases:
      - --company
execution:
  template: "cupp -i"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
global_vars:
  output: "cupp-wordlist.txt"
examples:
  - description: "Interactive profile-based wordlist generation"
    command: cupp -i
  - description: "Generate wordlist from a list of usernames"
    command: cupp -l usernames.txt
  - description: "Parse all usernames from a website and build wordlist"
    command: cupp -a https://example.com
  - description: "Quiet mode with custom output file"
    command: cupp -i -w passwords.txt -q
  - description: "Generate using CLI flags instead of interactive prompts"
    command: cupp --name John --surname Doe --birth 01011990 --pet Rex --company Acme
references:
  - label: "CUPP GitHub"
    url: "https://github.com/Mebus/cupp"
  - label: "Kali Tools — CUPP"
    url: "https://www.kali.org/tools/cupp/"
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
      package_name: "cupp"
      commands:
        - "apt-get install -y cupp"
---

# CUPP — Common User Passwords Profiler

CUPP is an interactive wordlist generator that builds targeted password lists from personal profile information such as name, birth date, pet name, partner, company, and interests. It uses common password patterns and mutations to create highly relevant candidate passwords for social engineering and credential attacks.
