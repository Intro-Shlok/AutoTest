---
id: security-ad-kerbrute
namespace: security:ad:kerbrute
name: kerbrute
description: Tool for performing Kerberos pre-authentication brute-forcing, user enumeration,
  and password spraying against Active Directory.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.ad.kerberos.bruteforce
  - security.ad.kerberos.userenum
  - security.ad.kerberos.passwordspray
  - security.ad.kerberos.preauth
platforms:
  - linux
  - cross-platform
risk_level: high
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies: []
related_tools:
  - impacket
  - netexec
  - rpcclient
phase: exploitation
techniques:
  - credential-access
  - discovery
  - lateral-movement
items:
  - NoCreds
  - Hash
services:
  - Kerberos
attack_types:
  - Enumeration
  - CredentialAccess
  - LateralMovement
contract:
  inputs:
    - type: network.target.ip
      description: Domain controller IP
    - type: domain.name
      description: Target domain name
    - type: credential.username
      description: Single username for enumeration
    - type: credential.userlist
      description: File path to list of usernames
  outputs:
    - type: security.credential.hash
      description: Captured Kerberos pre-authentication hashes
  side_effects:
    - network_traffic
    - filesystem_write
  resource_cost:
    cpu: low
    memory_mb: 32
    network: medium
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 32
  network: medium
  disk_io: low
allowed-tools:
  - kerbrute
parameters:
  - name: domain
    type: string
    required: true
    description: "Domain FQDN (e.g. evilcorp.local)"
    aliases:
      - -d
      - --domain
  - name: user
    type: string
    required: false
    description: "Single username for testing"
    aliases:
      - -u
      - --user
  - name: userlist
    type: file
    required: false
    description: "File containing list of usernames"
    aliases:
      - -U
      - --userlist
  - name: password
    type: string
    required: false
    description: "Single password for spraying"
    aliases:
      - -p
      - --password
  - name: passwordlist
    type: file
    required: false
    description: "File containing list of passwords"
    aliases:
      - -P
      - --passwordlist
  - name: threads
    type: integer
    required: false
    default_value: 10
    description: "Number of concurrent threads"
    aliases:
      - -t
      - --threads
  - name: dc-ip
    type: string
    required: false
    description: "Domain controller IP address"
    aliases:
      - --dc
      - --dc-ip
  - name: output
    type: string
    required: false
    description: "Output file for results"
    aliases:
      - -o
      - --output
  - name: verbose
    type: boolean
    required: false
    default_value: false
    description: "Enable verbose output"
    aliases:
      - -v
      - --verbose
  - name: delay
    type: integer
    required: false
    default_value: 0
    description: "Delay in milliseconds between requests"
    aliases:
      - --delay
  - name: timeout
    type: integer
    required: false
    default_value: 5
    description: "Timeout in seconds for each request"
    aliases:
      - --timeout
  - name: safe
    type: boolean
    required: false
    default_value: false
    description: "Safe mode — stop on account lockout risk"
    aliases:
      - -s
      - --safe
execution:
  template: "kerbrute userenum -d {domain} -U {userlist} --dc {dc-ip}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
global_vars:
  target: ip
  domain: domain
  dc-ip: ip
examples:
  - description: "Enumerate valid usernames via Kerberos pre-auth"
    command: kerbrute userenum -d evilcorp.local -U usernames.txt --dc 10.10.10.1
  - description: "Password spray one password across all users"
    command: kerbrute passwordspray -d evilcorp.local -U usernames.txt -p Password123 --dc 10.10.10.1
  - description: "Brute-force password for a single user"
    command: kerbrute bruteforce -d evilcorp.local -u administrator -P passwords.txt --dc 10.10.10.1
  - description: "Enumerate users with verbose output and safe mode"
    command: kerbrute userenum -d evilcorp.local -U usernames.txt --dc 10.10.10.1 -v -s
  - description: "Password spray with custom thread count and delay"
    command: kerbrute passwordspray -d evilcorp.local -U usernames.txt -p Passw0rd --dc 10.10.10.1 -t 5 --delay 1000
references:
  - label: "kerbrute GitHub"
    url: "https://github.com/ropnop/kerbrute"
install:
    - method: go
      repo_url: "github.com/ropnop/kerbrute"
      commands:
        - "go install github.com/ropnop/kerbrute@latest"
---

# kerbrute — Kerberos Pre-Authentication Attacks

kerbrute is a Go-based tool for performing Kerberos pre-authentication attacks against Active Directory, including **user enumeration**, **password spraying**, and **brute-forcing**.

## Subcommands

| Subcommand | Description |
|------------|-------------|
| `userenum` | Enumerate valid domain users via Kerberos AS-REP |
| `passwordspray` | Spray a single password across multiple users |
| `bruteforce` | Brute-force passwords for known users |
| `winrmbrute` | Kerberos-based WinRM brute-force (deprecated) |

## How It Works

kerbrute sends AS-REQ packets to the domain controller. If the user exists, Kerberos responds with `KDC_ERR_PREAUTH_REQUIRED`; if the user does not exist, it responds with `KDC_ERR_C_PRINCIPAL_UNKNOWN`. This allows user enumeration without ever sending a password.
