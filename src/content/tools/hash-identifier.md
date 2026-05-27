---
id: security-crack-hash-identifier
namespace: security:crack:hash-identifier
name: hash-identifier
description: Simple hash identification tool that determines the probable hash type from a given hash string.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - hash.identify
  - hash.analyze
  - hash.classify
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
  - john
  - hashcat
  - hashid
artifacts: []
workflow_edges:
  produces:
    - hash-type
  consumes:
    - hash-string
contract:
  inputs:
    - type: hash.string
      description: Hash string to identify
  outputs:
    - type: hash.type
      description: Identified hash type(s) with confidence
  side_effects: []
  resource_cost:
    cpu: low
    memory_mb: 16
    network: none
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 16
  network: none
  disk_io: low
allowed-tools:
  - hash-identifier
  - python3
  - Bash
parameters:
  - name: hash
    type: string
    required: false
    description: Hash string to identify (passed as positional argument)
    aliases: []
  - name: stdin
    type: boolean
    required: false
    description: Read hash from stdin
    aliases: []
execution:
  template: "hash-identifier"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
global_vars: {}
examples:
  - description: "Start interactive mode to identify hashes"
    command: hash-identifier
  - description: "Identify an MD5 hash"
    command: echo "5d41402abc4b2a76b9719d911017c592" | hash-identifier
  - description: "Identify a SHA-256 hash"
    command: echo "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824" | hash-identifier
references:
  - label: "Hash-Identifier on Kali"
    url: "https://www.kali.org/tools/hash-identifier/"
  - label: "Hash-Identifier GitHub"
    url: "https://github.com/psypanda/hashID"
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

# Hash-Identifier — Hash Type Detection

hash-identifier is a lightweight Python tool that accepts a hash string and returns likely hash types with sample formats. It supports over 200 hash types and works interactively or via stdin, helping analysts choose the correct hashcat or John mode for cracking.
