---
id: security-crack-medusa
namespace: security:crack:medusa
name: medusa
description: Parallel network login auditor for brute-forcing authentication across
  multiple protocols and services.
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
  - ncrack
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
  - medusa
  - hydra
  - ncrack
  - Bash
  - execFile
parameters:
  - name: flag-h
    type: string
    required: false
    description: "Target hostname or IP address"
    aliases:
      - -h
      - --host
  - name: flag-H
    type: string
    required: false
    description: "File with list of target hosts"
    aliases:
      - -H
      - --host-list
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
  - name: flag-M
    type: string
    required: false
    description: "Service module to use (e.g. ssh, ftp, smbnt)"
    aliases:
      - -M
      - --module
  - name: flag-m
    type: string
    required: false
    description: "Module-specific parameter"
    aliases:
      - -m
      - --module-parameter
  - name: flag-t
    type: integer
    required: false
    description: "Number of parallel threads (default 5)"
    aliases:
      - -t
      - --threads
  - name: flag-f
    type: boolean
    required: false
    description: "Stop after first valid credential found"
    aliases:
      - -f
      - --stop-after-first
  - name: flag-F
    type: boolean
    required: false
    description: "Stop all hosts after first credential"
    aliases:
      - -F
      - --stop-all-first
  - name: flag-O
    type: string
    required: false
    description: "Output file for results"
    aliases:
      - -O
      - --output
  - name: flag-e
    type: string
    required: false
    description: "Extra checks (n=null, s=same-as-login)"
    aliases:
      - -e
      - --extra
  - name: flag-s
    type: integer
    required: false
    description: "Target port number"
    aliases:
      - -s
      - --port
  - name: flag-r
    type: integer
    required: false
    description: "Number of retries on failure"
    aliases:
      - -r
      - --retry
  - name: flag-R
    type: integer
    required: false
    description: "Retry period in seconds"
    aliases:
      - -R
      - --retry-period
  - name: flag-c
    type: integer
    required: false
    description: "Timeout in seconds"
    aliases:
      - -c
      - --timeout
  - name: flag-q
    type: boolean
    required: false
    description: "Quiet mode (suppress banner)"
    aliases:
      - -q
      - --quiet
  - name: flag-v
    type: integer
    required: false
    description: "Verbose level (1-6)"
    aliases:
      - -v
      - --verbose
  - name: flag-d
    type: boolean
    required: false
    description: "Debug mode"
    aliases:
      - -d
      - --debug
execution:
  template: "medusa -h {target} -u {username} -P {password-list} -M {module}"
  sandbox: execFile
  timeout_seconds: 3600
  shell: false
global_vars:
  target: ""
  username: "admin"
  password-list: ""
  module: "ssh"
examples:
  - description: "Brute-force SSH with password list"
    command: medusa -h 192.168.1.100 -u root -P passwords.txt -M ssh
  - description: "Brute-force FTP with username list"
    command: medusa -h 192.168.1.100 -U users.txt -P passwords.txt -M ftp
  - description: "Multiple hosts from file with verbose output"
    command: medusa -H targets.txt -U users.txt -P passwords.txt -M smbnt -v 4
  - description: "HTTP form-based authentication"
    command: medusa -h 192.168.1.100 -U users.txt -P passwords.txt -M web-form -m FORM:"/login.php" -m DENY-SIGNAL:"Login failed"
  - description: "Stop on first credential found"
    command: medusa -h 192.168.1.100 -u admin -P passwords.txt -M ssh -f
  - description: "Extra checks for null and same-as-login"
    command: medusa -h 192.168.1.100 -u admin -P passwords.txt -M ssh -e ns
  - description: "Save results to file"
    command: medusa -h 192.168.1.100 -u admin -P passwords.txt -M ssh -O results.txt
  - description: "Custom port and timeout"
    command: medusa -h 192.168.1.100 -u admin -P passwords.txt -M mysql -s 3307 -c 10
references:
  - label: "Medusa GitHub"
    url: "https://github.com/jmk-foofus/medusa"
  - label: "Medusa Documentation"
    url: "https://www.kali.org/tools/medusa/"
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
      package_name: "medusa"
      commands:
        - "apt-get install -y medusa"
---

# Medusa — Parallel Network Login Auditor

Medusa is a massively parallel network login auditor designed to brute-force authentication credentials across numerous services. Its modular architecture supports pluggable protocol modules for extensibility.

## Supported Modules

| Module | Service | Default Port |
|--------|---------|-------------|
| `ssh` | SSH | 22 |
| `ftp` | FTP | 21 |
| `smbnt` | SMB/NTLM | 445 |
| `web-form` | HTTP Form | 80/443 |
| `mysql` | MySQL | 3306 |
| `pop3` | POP3 | 110 |
| `imap` | IMAP | 143 |
| `vnc` | VNC | 5900 |

## Threading Model

- `-t` controls threads per host (default 5)
- Medusa parallelizes across hosts when using `-H`
- More threads increase speed but may trigger rate limiting

## Module Parameters

Use `-m` to pass module-specific options:
- `medusa -h target -U users -P pass -M web-form -m FORM:"/login.php" -m DENY-SIGNAL:"Invalid"`
- Use `-m` multiple times for multiple parameters
