---
id: security-brute-patator
namespace: security:brute:patator
name: patator
description: Multi-protocol brute-forcing tool that supports FTP, SSH, HTTP, SMTP, SNMP, and many other services for login credential testing.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - brute.ftp.login
  - brute.ssh.login
  - brute.http.login
  - brute.smtp.login
  - brute.snmp.community
  - brute.service.login
platforms:
  - linux
  - macos
  - cross-platform
risk_level: high
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies:
  - python3
related_tools:
  - hydra
  - medusa
  - ncrack
  - crowbar
artifacts:
  - type: brute.results
    description: Brute-force results with valid credentials
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - valid-credentials
    - brute-force-results
  consumes:
    - target-host
    - username-list
    - password-list
contract:
  inputs:
    - type: network.target.host
      description: Target hostname or IP
    - type: credential.username.list
      description: Username wordlist
    - type: credential.password.list
      description: Password wordlist
  outputs:
    - type: brute.results
      description: Found valid credentials
      mime: text/plain
  side_effects:
    - network_traffic
  resource_cost:
    cpu: low
    memory_mb: 64
    network: medium
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 64
  network: medium
  disk_io: low
allowed-tools:
  - patator
  - python3
  - Bash
  - execFile
parameters:
  - name: module
    type: string
    required: true
    description: "Module name (ftp_login, ssh_login, http_fuzz, etc.)"
  - name: flag-hosts
    type: string
    required: false
    description: "Target hosts (file or comma-separated)"
    aliases:
      - host
  - name: flag-users
    type: string
    required: false
    description: "Usernames (file or string)"
    aliases:
      - user
  - name: flag-passwords
    type: string
    required: false
    description: "Passwords (file or string)"
    aliases:
      - password
  - name: flag-port
    type: integer
    required: false
    description: "Service port"
    aliases:
      - port
  - name: flag-threads
    type: integer
    required: false
    description: "Number of threads"
    aliases:
      - -x
      - --threads
  - name: flag-timeout
    type: integer
    required: false
    description: "Connection timeout"
    aliases:
      - -t
      - --timeout
  - name: flag-max-retries
    type: integer
    required: false
    description: "Maximum retries per attempt"
    aliases:
      - -R
      - --max-retries
  - name: flag-output
    type: string
    required: false
    description: "Output file for results"
    aliases:
      - -o
      - --output
execution:
  template: "patator {module} {flag-hosts} {flag-users} {flag-passwords} {flag-port} {flag-threads} {flag-timeout} {flag-max-retries} {flag-output}"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
examples:
  - description: "FTP brute-force"
    command: patator ftp_login host=10.0.0.1 user=FILE0 password=FILE1 0=users.txt 1=passwords.txt
  - description: "SSH brute-force"
    command: patator ssh_login host=10.0.0.1 user=FILE0 password=FILE1 0=users.txt 1=passwords.txt
  - description: "HTTP form brute-force"
    command: patator http_fuzz url=http://example.com/login method=POST body='user=FILE0&pass=FILE1' 0=users.txt 1=passwords.txt
references:
  - label: "Patator GitHub"
    url: "https://github.com/lanjelot/patator"
phase: exploitation
techniques:
  - credential-access
  - execution
items:
  - Password
  - Username
services:
  - SSH
  - FTP
  - HTTP
attack_types:
  - CredentialAccess
  - Exploitation
install:
    - method: apt
      package_name: "patator"
      commands:
        - "apt-get install -y patator"
---

# Patator — Multi-Protocol Brute-Forcer

Patator is a Python-based multi-protocol brute-force tool designed for modular and flexible authentication testing across many services including FTP, SSH, HTTP, SMTP, SNMP, SMB, Telnet, and more.

## Usage

```bash
# FTP brute-force
patator ftp_login host=10.0.0.1 user=FILE0 password=FILE1 0=users.txt 1=passwords.txt

# SSH brute-force
patator ssh_login host=10.0.0.1 user=FILE0 password=FILE1 0=users.txt 1=passwords.txt -x ignore:mesg='Authentication failed.'

# HTTP form brute-force
patator http_fuzz url=http://target.com/login method=POST body='user=COMBO00&pass=COMBO01' 0=combo.txt

# SNMP community scan
patator snmp_login host=10.0.0.0/24 community=FILE0 0=communities.txt -x ignore:mesg='No response'
```
