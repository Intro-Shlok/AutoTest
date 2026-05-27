---
id: security-crack-hydra
namespace: security:crack:hydra
name: hydra
description: Very fast parallel network logon cracker supporting numerous protocols
  for brute-force authentication testing.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.crack.password
  - security.auth.bruteforce
  - security.audit.credential
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
  - medusa
  - ncrack
  - patator
artifacts:
  - type: security.crack.results
    description: Brute-force results log
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - valid-credentials
    - auth-test-results
  consumes:
    - target
    - username-list
    - password-list
contract:
  inputs:
    - type: network.target.ip
      description: Target IP address or hostname
    - type: network.target.port
      description: Target port (optional, auto-detected for most services)
    - type: security.username.list
      description: File containing usernames
    - type: security.password.list
      description: File containing passwords
  outputs:
    - type: security.valid.credentials
      description: Successfully discovered credentials
      mime: text/plain
    - type: security.auth.results
      description: Authentication attempt results
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
  - hydra
  - medusa
  - ncrack
  - Bash
  - execFile
parameters:
  - name: flag-l
    type: string
    required: false
    description: "Single username to try"
    aliases:
      - -l
      - --login
  - name: flag-L
    type: string
    required: false
    description: "File with list of usernames"
    aliases:
      - -L
      - --login-list
  - name: flag-p
    type: string
    required: false
    description: "Single password to try"
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
    type: integer
    required: false
    description: "Target port number"
    aliases:
      - -s
      - --port
  - name: flag-t
    type: integer
    required: false
    description: "Number of parallel tasks (default 16)"
    aliases:
      - -t
      - --tasks
  - name: flag-v
    type: boolean
    required: false
    description: "Verbose output"
    aliases:
      - -v
      - --verbose
  - name: flag-V
    type: boolean
    required: false
    description: "Show each login attempt"
    aliases:
      - -V
      - --verbose-login
  - name: flag-o
    type: string
    required: false
    description: "Output file for results"
    aliases:
      - -o
      - --output
  - name: flag-f
    type: boolean
    required: false
    description: "Exit after first found login/password pair"
    aliases:
      - -f
      - --found
  - name: flag-F
    type: boolean
    required: false
    description: "Exit per service after first found pair"
    aliases:
      - -F
      - --quit-per-service
  - name: flag-M
    type: string
    required: false
    description: "File with list of target servers"
    aliases:
      - -M
      - --server-list
  - name: flag-w
    type: integer
    required: false
    description: "Wait time in seconds between attempts"
    aliases:
      - -w
      - --wait
  - name: flag-e
    type: string
    required: false
    description: "Extra checks (n=null, s=same-as-login, r=reverse-login)"
    aliases:
      - -e
      - --extra
  - name: flag-x
    type: string
    required: false
    description: "Password generation pattern (e.g. -x 6:8:a1)"
    aliases:
      - -x
      - --password-generation
  - name: flag-S
    type: boolean
    required: false
    description: "Connect via SSL"
    aliases:
      - -S
      - --ssl
  - name: flag-u
    type: boolean
    required: false
    description: "Loop around users (not passwords) on each attempt"
    aliases:
      - -u
      - --loop-round-users
  - name: flag-I
    type: boolean
    required: false
    description: "Ignore restore file (do not resume)"
    aliases:
      - -I
      - --ignore-restore
  - name: flag-R
    type: boolean
    required: false
    description: "Restore previous aborted session"
    aliases:
      - -R
      - --restore
  - name: flag-q
    type: boolean
    required: false
    description: "Quiet mode (no banner)"
    aliases:
      - -q
      - --quiet
execution:
  template: "hydra -l {username} -P {password-list} {target} {service}"
  sandbox: execFile
  timeout_seconds: 3600
  shell: false
global_vars:
  username: "admin"
  password-list: ""
  target: ""
  service: "ssh"
examples:
  - description: "Brute-force SSH with username and password list"
    command: hydra -l admin -P passwords.txt 192.168.1.100 ssh
  - description: "Brute-force HTTP form with user list"
    command: hydra -L users.txt -P passwords.txt 192.168.1.100 http-post-form "/login:user=^USER^&pass=^PASS^:F=invalid"
  - description: "Brute-force FTP with verbose output"
    command: hydra -l root -P passwords.txt -v 192.168.1.100 ftp
  - description: "Multiple targets from file"
    command: hydra -l admin -P passwords.txt -M targets.txt ssh
  - description: "Null and same-as-login checks"
    command: hydra -l admin -P passwords.txt -e ns 192.168.1.100 rdp
  - description: "SSL-enabled service on custom port"
    command: hydra -l admin -P passwords.txt -s 2222 -S 192.168.1.100 ssh
  - description: "Restore aborted session"
    command: hydra -R
  - description: "Password generation mode"
    command: hydra -l admin -x 6:8:a1 192.168.1.100 ftp
references:
  - label: "Hydra GitHub"
    url: "https://github.com/vanhauser-thc/thc-hydra"
  - label: "Hydra Manual"
    url: "https://www.kali.org/tools/hydra/"
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

# THC-Hydra — Network Logon Cracker

Hydra is a highly parallel network authentication cracking tool that supports over 50 protocols including SSH, FTP, HTTP(S), RDP, SMB, MySQL, PostgreSQL, SMTP, and many more. It is designed to quickly test credential strength across network services.

## Supported Protocols

| Protocol | Service Argument | Default Port |
|----------|-----------------|-------------|
| SSH | `ssh` | 22 |
| FTP | `ftp` | 21 |
| HTTP(S) | `http-get` / `http-post-form` | 80/443 |
| RDP | `rdp` | 3389 |
| SMB | `smb` | 445 |
| MySQL | `mysql` | 3306 |
| PostgreSQL | `postgres` | 5432 |

## Performance Tuning

- `-t 64` — increase parallel tasks (default 16)
- `-w 1` — add wait time between attempts
- `-f` — stop after first valid credential found
- `-F` — stop per service after first credential

## Smart Checks

- `-e n` — try null password
- `-e s` — try password same as login
- `-e r` — try reverse login as password
- Combine as `-e nsr` for all extra checks
