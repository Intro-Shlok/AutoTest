---
id: security-ad-smbmap
namespace: security:ad:smbmap
name: smbmap
description: SMB enumeration tool that provides recursive listing, file download/upload,
  and command execution across SMB shares on Windows networks.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.ad.share.list
  - security.ad.share.download
  - security.ad.share.upload
  - security.ad.share.delete
  - security.ad.share.exec
  - security.ad.share.content
platforms:
  - linux
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
  - smbclient
  - enum4linux-ng
  - impacket
phase: exploitation
techniques:
  - credential-access
  - discovery
  - lateral-movement
items:
  - NoCreds
  - Hash
services:
  - SMB
attack_types:
  - Enumeration
  - CredentialAccess
  - LateralMovement
contract:
  inputs:
    - type: network.target.ip
      description: Target IP or hostname
    - type: credential.username
      description: Username for SMB authentication
    - type: credential.password
      description: Password or NTLM hash
  outputs:
    - type: security.ad.share.list
      description: Recursive share listing with permissions
    - type: file.content
      description: Downloaded file contents
  side_effects:
    - network_traffic
    - filesystem_write
  resource_cost:
    cpu: low
    memory_mb: 32
    network: low
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 32
  network: low
  disk_io: low
allowed-tools:
  - smbmap
parameters:
  - name: host
    type: string
    required: true
    description: "Target IP address or hostname"
    aliases:
      - -H
      - --host
  - name: username
    type: string
    required: false
    description: "Username for SMB authentication"
    aliases:
      - -u
      - --username
  - name: password
    type: string
    required: false
    description: "Password or NTLM hash for authentication"
    aliases:
      - -p
      - --password
  - name: domain
    type: string
    required: false
    description: "Domain name for authentication"
    aliases:
      - -d
      - --domain
  - name: port
    type: integer
    required: false
    default_value: 445
    description: "SMB port number"
    aliases:
      - -P
      - --port
  - name: share
    type: string
    required: false
    description: "Specify a share to enumerate"
    aliases:
      - -s
      - --share
  - name: recursive
    type: boolean
    required: false
    default_value: false
    description: "Recursive directory listing"
    aliases:
      - -r
      - --recursive
  - name: depth
    type: integer
    required: false
    default_value: 10
    description: "Recursion depth for directory listing"
    aliases:
      - -R
      - --depth
  - name: command
    type: string
    required: false
    description: "Command to execute via SMB"
    aliases:
      - -x
      - --command
  - name: content
    type: boolean
    required: false
    default_value: false
    description: "Show file contents"
    aliases:
      - -C
      - --content
  - name: download
    type: string
    required: false
    description: "Download file by path"
    aliases:
      - --download
  - name: upload
    type: string
    required: false
    description: "Upload file (local:remote)"
    aliases:
      - --upload
  - name: timeout
    type: integer
    required: false
    default_value: 10
    description: "Network timeout in seconds"
    aliases:
      - --timeout
execution:
  template: "smbmap -H {target} -u {username} -p {password}"
  sandbox: execFile
  timeout_seconds: 120
  shell: false
global_vars:
  target: ip
  username: user
examples:
  - description: "Enumerate all shares with null session"
    command: smbmap -H 10.10.10.1 -u null -p null
  - description: "Authenticated recursive share listing"
    command: smbmap -H 10.10.10.1 -u jdoe -p Pass123 -r
  - description: "Download a specific file from a share"
    command: smbmap -H 10.10.10.1 -u jdoe -p Pass123 --download C$/Users/Administrator/Desktop/notes.txt
  - description: "Upload a file to a share"
    command: smbmap -H 10.10.10.1 -u jdoe -p Pass123 --upload /tmp/shell.exe C$/temp/shell.exe
  - description: "Execute a command via SMB"
    command: smbmap -H 10.10.10.1 -u jdoe -p Pass123 -x "ipconfig"
  - description: "Show contents of text files in a share"
    command: smbmap -H 10.10.10.1 -u jdoe -p Pass123 -s Shared -C
references:
  - label: "smbmap GitHub"
    url: "https://github.com/ShawnDEvans/smbmap"
---

# smbmap — SMB Share Enumeration

smbmap is a Python-based SMB enumeration tool that recursively lists share contents, checks permissions, downloads/uploads files, and executes commands—all without needing a full interactive SMB session.

## Key Features

- **Recursive listing**: Map out entire directory trees across shares
- **Permission-aware**: Shows READ/WRITE/DENIED per share and path
- **File operations**: Download, upload, and delete files
- **Command execution**: Run shell commands via SMB (admin required)
- **NTLM hash auth**: Authenticate with LM:NT hash instead of password

## Usage Modes

| Mode | Command | Description |
|------|---------|-------------|
| Basic enum | `smbmap -H target -u user -p pass` | List all accessible shares |
| Recursive | `smbmap -H target -u user -p pass -r` | Deep directory listing |
| Download | `smbmap -H target -u user -p pass --download PATH` | Grab a specific file |
| Upload | `smbmap -H target -u user -p pass --upload L R` | Push a file to target |
| Exec | `smbmap -H target -u user -p pass -x cmd` | Remote command execution |
