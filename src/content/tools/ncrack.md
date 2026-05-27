---
id: security-crack-ncrack
namespace: security:crack:ncrack
name: ncrack
description: High-speed network authentication cracking tool for testing credential
  strength across multiple network services.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.crack.password
  - security.auth.bruteforce
  - network.auth.test
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
  - hydra
  - medusa
artifacts:
  - type: security.crack.results
    description: Brute-force results log
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - valid-credentials
  consumes:
    - target
    - username-list
    - password-list
contract:
  inputs:
    - type: network.target.ip
      description: Target IP address or hostname
    - type: security.username.list
      description: File containing usernames
    - type: security.password.list
      description: File containing passwords
  outputs:
    - type: security.valid.credentials
      description: Successfully discovered credentials
      mime: text/plain
  side_effects:
    - network_traffic
    - filesystem_write
  resource_cost:
    cpu: medium
    memory_mb: 128
    network: high
    disk_io: low
resource_profile:
  cpu: medium
  memory_mb: 128
  network: high
  disk_io: low
allowed-tools:
  - ncrack
  - hydra
  - medusa
  - Bash
  - execFile
parameters:
  - name: flag-i
    type: string
    required: false
    description: "Input file with target specifications"
    aliases:
      - -i
      - --input-file
  - name: flag-u
    type: string
    required: false
    description: "Single username to test"
    aliases:
      - -u
      - --username
  - name: flag-U
    type: string
    required: false
    description: "File with list of usernames"
    aliases:
      - -U
      - --username-list
  - name: flag-p
    type: string
    required: false
    description: "Single password to test"
    aliases:
      - -p
      - --password
  - name: flag-P
    type: string
    required: false
    description: "File with list of passwords"
    aliases:
      - -P
      - --password-list
  - name: flag-s
    type: string
    required: false
    description: "Service to test (e.g. ssh, ftp, rdp)"
    aliases:
      - -s
      - --service
  - name: flag-m
    type: string
    required: false
    description: "Module-specific options"
    aliases:
      - -m
      - --module-options
  - name: flag-f
    type: boolean
    required: false
    description: "Stop after first valid credential"
    aliases:
      - -f
      - --stop-after-first
  - name: flag-F
    type: boolean
    required: false
    description: "Stop after first credential per service"
    aliases:
      - -F
      - --stop-all-first
  - name: flag-T
    type: integer
    required: false
    description: "Number of parallel threads"
    aliases:
      - -T
      - --threads
  - name: flag-t
    type: string
    required: false
    description: "Timing template (0-5, higher is faster)"
    aliases:
      - -t
      - --timing
  - name: flag-v
    type: boolean
    required: false
    description: "Verbose output"
    aliases:
      - -v
      - --verbose
  - name: flag-o
    type: string
    required: false
    description: "Output file for results"
    aliases:
      - -o
      - --output
  - name: flag-r
    type: integer
    required: false
    description: "Number of retries on connection failure"
    aliases:
      - -r
      - --retries
  - name: flag-d
    type: integer
    required: false
    description: "Delay in milliseconds between attempts"
    aliases:
      - -d
      - --delay
  - name: flag-x
    type: string
    required: false
    description: "Password generation pattern"
    aliases:
      - -x
      - --generate-password
  - name: connection-limit
    type: integer
    required: false
    description: "Maximum simultaneous connections"
    aliases:
      - --connection-limit
  - name: rate
    type: integer
    required: false
    description: "Maximum attempts per second"
    aliases:
      - --rate
  - name: flag-6
    type: boolean
    required: false
    description: "Use IPv6"
    aliases:
      - "-6"
      - --ipv6
  - name: ssl
    type: boolean
    required: false
    description: "Use SSL/TLS for connection"
    aliases:
      - --ssl
  - name: log
    type: string
    required: false
    description: "Log file path"
    aliases:
      - --log
execution:
  template: "ncrack -u {username} -P {password-list} {target}:{service}"
  sandbox: execFile
  timeout_seconds: 3600
  shell: false
global_vars:
  username: "admin"
  password-list: ""
  target: ""
  service: "ssh"
examples:
  - description: "Brute-force SSH with password list"
    command: ncrack -u root -P passwords.txt 192.168.1.100:ssh
  - description: "Brute-force RDP with username list"
    command: ncrack -U users.txt -P passwords.txt 192.168.1.100:rdp
  - description: "Multiple targets from input file"
    command: ncrack -i targets.txt -U users.txt -P passwords.txt
  - description: "Stop after first credential found"
    command: ncrack -u admin -P passwords.txt -f 192.168.1.100:ssh
  - description: "Verbose mode with timing template"
    command: ncrack -u admin -P passwords.txt -v -t 3 192.168.1.100:ssh
  - description: "Custom rate limit and connection limit"
    command: ncrack -u admin -P passwords.txt --rate=50 --connection-limit=10 192.168.1.100:rdp
  - description: "SSL-enabled service on custom port"
    command: ncrack -u admin -P passwords.txt --ssl 192.168.1.100:https
  - description: "Save results to output file"
    command: ncrack -u admin -P passwords.txt -o results.txt 192.168.1.100:ftp
references:
  - label: "Ncrack GitHub"
    url: "https://github.com/nmap/ncrack"
  - label: "Ncrack Documentation"
    url: "https://nmap.org/ncrack/"
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

# Ncrack — High-Speed Network Cracker

Ncrack is a high-speed network authentication cracking tool built on the Nmap ecosystem. It is designed for rapid credential testing across network services with an emphasis on performance and flexibility.

## Supported Services

| Service | Argument | Default Port |
|---------|----------|-------------|
| SSH | `ssh` | 22 |
| RDP | `rdp` | 3389 |
| FTP | `ftp` | 21 |
| HTTP(S) | `http` / `https` | 80/443 |
| Telnet | `telnet` | 23 |
| IMAP | `imap` | 143 |
| POP3 | `pop3` | 110 |

## Performance Tuning

- `-T` — set number of parallel threads
- `--rate=N` — max attempts per second
- `--connection-limit=N` — max simultaneous connections
- `-t 0-5` — timing template (aggressive=5, polite=0)

## Timing Templates

| Template | Name | Description |
|----------|------|-------------|
| 0 | Polite | Slows down to avoid detection |
| 1 | Normal | Default timing |
| 2 | Aggressive | Faster, more noise |
| 3 | Crazy | Very aggressive |
| 4 | Insane | Maximum speed |
