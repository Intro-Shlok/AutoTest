---
id: security-crack-john
namespace: security:crack:john
name: john
description: Leading password cracking tool supporting hundreds of hash types with
  multiple cracking modes (single, wordlist, incremental, external).
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.crack.password
  - security.crack.hash
  - security.audit.credential
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
  - hashcat
  - hash-identifier
artifacts:
  - type: security.crack.potfile
    description: Cracked password database
    mime: text/plain
    trust_level: verified
  - type: security.crack.session
    description: Cracking session state for restore
    mime: application/octet-stream
    trust_level: verified
workflow_edges:
  produces:
    - cracked-passwords
    - password-candidates
  consumes:
    - hash-file
    - wordlist
contract:
  inputs:
    - type: security.hash.file
      description: File containing password hashes to crack
    - type: security.wordlist
      description: Wordlist for dictionary attack
    - type: security.rules
      description: Mangling rules for wordlist mutations
  outputs:
    - type: security.cracked.passwords
      description: Successfully cracked passwords
      mime: text/plain
    - type: security.crack.session
      description: Cracking session state
      mime: application/octet-stream
  side_effects:
    - filesystem_write
    - filesystem_write
    - filesystem_write
  resource_cost:
    cpu: high
    memory_mb: 512
    network: none
    disk_io: medium
resource_profile:
  cpu: high
  memory_mb: 512
  network: none
  disk_io: medium
allowed-tools:
  - john
  - hashcat
  - Bash
  - execFile
parameters:
  - name: wordlist
    type: string
    required: false
    description: "Wordlist file for dictionary attack"
    aliases:
      - --wordlist
  - name: rules
    type: string
    required: false
    description: "Wordlist mangling rules"
    aliases:
      - --rules
  - name: format
    type: string
    required: false
    description: "Hash format (e.g. raw-md5, bcrypt, sha512crypt)"
    aliases:
      - --format
  - name: incremental
    type: string
    required: false
    description: "Incremental (brute-force) mode with charset"
    aliases:
      - --incremental
  - name: mask
    type: string
    required: false
    description: "Mask for brute-force (e.g. ?l?l?l?d?d)"
    aliases:
      - --mask
  - name: session
    type: string
    required: false
    description: "Session name for save/restore"
    aliases:
      - --session
  - name: restore
    type: string
    required: false
    description: "Restore a previous cracking session"
    aliases:
      - --restore
  - name: show
    type: boolean
    required: false
    description: "Show cracked passwords from pot file"
    aliases:
      - --show
  - name: pot
    type: string
    required: false
    description: "Pot file path for cracked passwords"
    aliases:
      - --pot
  - name: node
    type: string
    required: false
    description: "Node/distribution for cluster cracking"
    aliases:
      - --node
  - name: fork
    type: integer
    required: false
    description: "Number of forked processes"
    aliases:
      - --fork
  - name: mem-file-size
    type: integer
    required: false
    description: "Max memory per file buffer in MB"
    aliases:
      - --mem-file-size
  - name: max-candidates
    type: integer
    required: false
    description: "Max candidates per second per thread"
    aliases:
      - --max-candidates
  - name: reject-printable
    type: boolean
    required: false
    description: "Reject plaintexts with non-printable chars"
    aliases:
      - --reject-printable
  - name: limit
    type: integer
    required: false
    description: "Max number of cracked passwords"
    aliases:
      - --limit
  - name: single
    type: boolean
    required: false
    description: "Single crack mode using login/GECOS info"
    aliases:
      - --single
  - name: external
    type: string
    required: false
    description: "External mode using user-defined functions"
    aliases:
      - --external
  - name: stdin
    type: boolean
    required: false
    description: "Read candidates from stdin"
    aliases:
      - --stdin
execution:
  template: "john --wordlist={wordlist} {hash-file}"
  sandbox: execFile
  timeout_seconds: 86400
  shell: false
global_vars:
  wordlist: ""
  hash-file: ""
examples:
  - description: "Single crack mode using login information"
    command: john --single hashes.txt
  - description: "Wordlist mode with rules"
    command: john --wordlist=rockyou.txt --rules hashes.txt
  - description: "Incremental (brute-force) mode"
    command: john --incremental hashes.txt
  - description: "Show cracked passwords from pot file"
    command: john --show hashes.txt
  - description: "Crack specific format with mask attack"
    command: john --format=raw-md5 --mask=?l?l?l?l?d?d hashes.txt
  - description: "Restore a saved session"
    command: john --restore my-session
  - description: "Fork across 4 CPU cores"
    command: john --fork=4 hashes.txt
  - description: "Cluster cracking with node distribution"
    command: john --node=1/4 hashes.txt
references:
  - label: "John the Ripper GitHub"
    url: "https://github.com/openwall/john"
  - label: "John the Ripper Documentation"
    url: "https://www.openwall.com/john/doc/"
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

# John the Ripper — Password Cracking

John the Ripper is a fast password cracker supporting hundreds of hash and cipher types across Unix, Windows, and web platforms. It offers multiple cracking modes: single (weak passwords from login info), wordlist (dictionary with rules), incremental (brute-force), and external (custom C-style functions).

## Cracking Modes

| Mode | Command | Description |
|------|---------|-------------|
| Single | `john --single hashes.txt` | Uses login/GECOS info as password guesses |
| Wordlist | `john --wordlist=rockyou.txt hashes.txt` | Dictionary attack with optional mangling rules |
| Incremental | `john --incremental hashes.txt` | Brute-force using character set permutations |
| Mask | `john --mask=?l?l?l?d?d hashes.txt` | Targeted brute-force with positional masks |
| External | `john --external=myfilter hashes.txt` | Custom C-style password generation functions |

## Session Management

- `--session=name` — assign a name to save/restore sessions
- `--restore=name` — resume an interrupted cracking session
- `--pot=mypot.pot` — specify custom pot file location
- `--show` — display cracked passwords from pot file

## Distributed Cracking

- `--fork=N` — run N parallel processes on multi-core CPUs
- `--node=M/N` — run as node M of N in a cluster
