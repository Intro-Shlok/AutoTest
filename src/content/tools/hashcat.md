---
id: security-crack-hashcat
namespace: security:crack:hashcat
name: hashcat
description: World's fastest password recovery tool supporting GPU acceleration,
  hundreds of hash types, and advanced attack modes.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.crack.password
  - security.crack.hash
  - security.audit.credential
  - hardware.gpu.accelerate
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
  - john
  - hash-utils
artifacts:
  - type: security.crack.potfile
    description: Hashcat potfile with cracked passwords
    mime: text/plain
    trust_level: verified
  - type: security.crack.result
    description: Cracked password output file
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - cracked-passwords
    - hash-analysis
  consumes:
    - hash-file
    - wordlist
    - rule-file
contract:
  inputs:
    - type: security.hash.file
      description: File containing password hashes
    - type: security.wordlist
      description: Dictionary file for wordlist attack
    - type: security.rule.file
      description: Rule file for wordlist mutations
  outputs:
    - type: security.cracked.passwords
      description: Successfully cracked passwords
      mime: text/plain
    - type: security.crack.status
      description: Cracking status and statistics
      mime: text/plain
  side_effects:
    - filesystem_write
    - filesystem_write
    - filesystem_write
  resource_cost:
    cpu: medium
    memory_mb: 1024
    network: none
    disk_io: low
resource_profile:
  cpu: medium
  memory_mb: 1024
  network: none
  disk_io: low
allowed-tools:
  - hashcat
  - john
  - Bash
  - execFile
parameters:
  - name: flag-m
    type: string
    required: false
    description: "Hash type number (e.g. 0=MD5, 1000=NTLM, 3200=bcrypt)"
    aliases:
      - -m
      - --hash-type
  - name: flag-a
    type: integer
    required: false
    description: "Attack mode (0=Straight, 1=Combination, 3=Brute-force, 6=Hybrid, 7=PRINCE)"
    aliases:
      - -a
      - --attack-mode
  - name: flag-o
    type: string
    required: false
    description: "Output file for cracked passwords"
    aliases:
      - -o
      - --output
  - name: outfile-format
    type: string
    required: false
    description: "Output format (1=hash[:salt]:plain, 2=plain, 3=hex)"
    aliases:
      - --outfile-format
  - name: potfile-path
    type: string
    required: false
    description: "Custom potfile path"
    aliases:
      - --potfile-path
  - name: force
    type: boolean
    required: false
    description: "Ignore warnings and force startup"
    aliases:
      - --force
  - name: show
    type: boolean
    required: false
    description: "Show cracked passwords from potfile"
    aliases:
      - --show
  - name: benchmark
    type: boolean
    required: false
    description: "Run benchmark for all hash modes"
    aliases:
      - --benchmark
  - name: status
    type: boolean
    required: false
    description: "Enable automatic status screen updates"
    aliases:
      - --status
  - name: status-timer
    type: integer
    required: false
    description: "Status screen update interval in seconds"
    aliases:
      - --status-timer
  - name: session
    type: string
    required: false
    description: "Session name for save/restore"
    aliases:
      - --session
  - name: flag-r
    type: string
    required: false
    description: "Rule file for wordlist attack"
    aliases:
      - -r
      - --rule
  - name: flag-i
    type: boolean
    required: false
    description: "Enable incremental mask mode"
    aliases:
      - -i
      - --increment
  - name: increment-min
    type: integer
    required: false
    description: "Minimum password length in increment mode"
    aliases:
      - --increment-min
  - name: increment-max
    type: integer
    required: false
    description: "Maximum password length in increment mode"
    aliases:
      - --increment-max
  - name: flag-w
    type: integer
    required: false
    description: "Workload profile (1=Low, 2=Default, 3=High, 4=Nightmare)"
    aliases:
      - -w
      - --workload-profile
  - name: flag-O
    type: boolean
    required: false
    description: "Enable optimized kernel (limits password length)"
    aliases:
      - -O
      - --optimized-kernel
  - name: backend-devices
    type: string
    required: false
    description: "Backend device IDs to use (comma-separated)"
    aliases:
      - --backend-devices
  - name: flag-d
    type: string
    required: false
    description: "OpenCL device to use"
    aliases:
      - -d
      - --device
  - name: keyspace
    type: boolean
    required: false
    description: "Calculate keyspace for current attack"
    aliases:
      - --keyspace
  - name: example-hashes
    type: boolean
    required: false
    description: "Print example hashes for all hash modes"
    aliases:
      - --example-hashes
execution:
  template: "hashcat -m {hash-type} -a {attack-mode} {hash-file} {wordlist}"
  sandbox: execFile
  timeout_seconds: 86400
  shell: false
global_vars:
  hash-type: "0"
  attack-mode: "0"
  hash-file: ""
  wordlist: ""
examples:
  - description: "Dictionary attack on MD5 hashes"
    command: hashcat -m 0 -a 0 hashes.txt rockyou.txt
  - description: "Brute-force attack on NTLM hashes"
    command: hashcat -m 1000 -a 3 hashes.txt ?a?a?a?a?a?a?a?a
  - description: "Rule-based attack with custom rules"
    command: hashcat -m 0 -a 0 hashes.txt rockyou.txt -r best64.rule
  - description: "Incremental mask attack on bcrypt"
    command: hashcat -m 3200 -a 3 hashes.txt ?l?l?l?l?l --increment --increment-min=4
  - description: "Run benchmark for all hash modes"
    command: hashcat --benchmark
  - description: "Show cracked passwords from potfile"
    command: hashcat --show hashes.txt
  - description: "Hybrid attack (wordlist + mask)"
    command: hashcat -m 0 -a 6 hashes.txt rockyou.txt ?d?d?d
  - description: "Use GPU device 1 with optimized kernel"
    command: hashcat -m 0 -a 0 hashes.txt rockyou.txt -d 1 -O
references:
  - label: "Hashcat GitHub"
    url: "https://github.com/hashcat/hashcat"
  - label: "Hashcat Wiki"
    url: "https://hashcat.net/wiki/"
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

# Hashcat — GPU-Accelerated Password Recovery

Hashcat is the world's fastest password cracking tool, leveraging GPU acceleration to achieve billions of hashes per second. It supports over 300 hash types and six attack modes: straight (wordlist), combination, brute-force, hybrid wordlist+mask, hybrid mask+wordlist, and PRINCE.

## Attack Modes

| Mode | Flag  | Description |
|------|-------|-------------|
| Straight | `-a 0` | Wordlist-based dictionary attack |
| Combination | `-a 1` | Combines words from two wordlists |
| Brute-force | `-a 3` | Mask-based exhaustive search |
| Hybrid wl+mask | `-a 6` | Wordlist with mask appended |
| Hybrid mask+wl | `-a 7` | Mask with wordlist appended |
| PRINCE | `-a 8` | PRINCE algorithm attack |

## Key Optimization Flags

- `-O` — optimized kernel (faster but caps password length)
- `-w 3` — high workload profile (use with caution)
- `-d 1` — select specific GPU device
- `--backend-devices` — specify compute devices

## Session and Status

- `--session=name` — save/restore cracking sessions
- `--status` — real-time status updates
- `--status-timer=N` — update interval in seconds
- `--potfile-path` — custom potfile location
