---
id: security-ad-smbclient
namespace: security:ad:smbclient
name: smbclient
description: SMB/CIFS client for accessing and managing file shares on Windows systems,
  part of the Samba suite of interoperability tools.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.ad.share.list
  - security.ad.share.access
  - security.ad.share.download
  - security.ad.file.transfer
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
  - smbmap
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
      description: Password for SMB authentication
  outputs:
    - type: security.ad.share.list
      description: List of available SMB shares
    - type: file.content
      description: Downloaded file contents
  side_effects:
    - network_traffic
    - filesystem_write
  resource_cost:
    cpu: low
    memory_mb: 16
    network: low
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 16
  network: low
  disk_io: low
allowed-tools:
  - smbclient
parameters:
  - name: list
    type: boolean
    required: false
    default_value: false
    description: "List available shares on target"
    aliases:
      - -L
      - --list
  - name: no-pass
    type: boolean
    required: false
    default_value: false
    description: "Do not prompt for password (null session)"
    aliases:
      - -N
      - --no-pass
  - name: username
    type: string
    required: false
    description: "Username for SMB authentication"
    aliases:
      - -U
      - --user
      - --username
  - name: password
    type: string
    required: false
    description: "Password for SMB authentication"
    aliases:
      - -P
      - --password
  - name: workgroup
    type: string
    required: false
    default_value: WORKGROUP
    description: "Workgroup or domain name"
    aliases:
      - -W
      - --workgroup
  - name: ip
    type: string
    required: false
    description: "Target IP address"
    aliases:
      - -I
      - --ip
  - name: port
    type: integer
    required: false
    default_value: 445
    description: "SMB port number"
    aliases:
      - -p
      - --port
  - name: directory
    type: string
    required: false
    description: "Change to initial directory"
    aliases:
      - -D
      - --directory
  - name: command
    type: string
    required: false
    description: "Execute SMB command non-interactively"
    aliases:
      - -c
      - --command
  - name: max-protocol
    type: string
    required: false
    description: "Maximum SMB protocol version"
    aliases:
      - -m
      - --max-protocol
  - name: encrypt
    type: boolean
    required: false
    default_value: false
    description: "Require SMB encryption"
    aliases:
      - -e
      - --encrypt
  - name: debug
    type: integer
    required: false
    default_value: 0
    description: "Debug level (0-10)"
    aliases:
      - -d
      - --debug
execution:
  template: "smbclient -L {target} -U {username}"
  sandbox: execFile
  timeout_seconds: 60
  shell: false
global_vars:
  target: ip
  username: user
examples:
  - description: "List shares with null session"
    command: smbclient -L 10.10.10.1 -N
  - description: "List shares with authenticated session"
    command: smbclient -L 10.10.10.1 -U jdoe
  - description: "Connect to a share and list contents"
    command: smbclient //10.10.10.1/C$ -U jdoe -c ls
  - description: "Download a file from a share"
    command: smbclient //10.10.10.1/Shared -U jdoe -c "get confidential.docx"
  - description: "Upload a file to a share"
    command: smbclient //10.10.10.1/Shared -U jdoe -c "put backdoor.exe"
  - description: "Non-interactive recursive directory listing"
    command: smbclient //10.10.10.1/C$/Users -U jdoe -c "recurse;ls"
references:
  - label: "Samba smbclient man page"
    url: "https://www.samba.org/samba/docs/current/man-html/smbclient.1.html"
install:
    - method: apt
      package_name: "smbclient"
      commands:
        - "apt-get install -y smbclient"
---

# smbclient — SMB/CIFS Client

smbclient is a command-line SMB/CIFS client included in the Samba suite, used to access file shares, printers, and named pipes on Windows systems.

## Common Operations

| Operation | Command |
|-----------|---------|
| List shares | `smbclient -L target -U user` |
| Connect to share | `smbclient //target/share -U user` |
| Download file | `smbclient //target/share -U user -c "get file"` |
| Upload file | `smbclient //target/share -U user -c "put file"` |
| Recurse dirs | `smbclient //target/share -U user -c "recurse;ls"` |
| Null session | `smbclient -L target -N` |

## Interactive Commands

Once connected, smbclient provides an FTP-like interface: `ls`, `cd`, `get`, `put`, `rm`, `mkdir`, `rmdir`, `recurse`, `prompt`, `mask`, `tar`, `blocksize`, `tarmode`, `setmode`, `help`.
