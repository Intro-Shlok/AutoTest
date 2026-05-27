---
id: network-transfer-scp
namespace: network:transfer:scp
name: scp
description: Secure copy over SSH protocol
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.transfer.scp
  - network.transfer.download
  - network.transfer.upload
platforms:
  - linux
risk_level: medium
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
features:
  - remote
  - network-intensive
  - encryption
techniques:
  - exfiltration
  - collection
parameters:
  - name: flag-3
    type: string
    required: false
    description: "Copies between two remote hosts are transferred through the lo-"
    aliases:
      - "-3"
  - name: flag-4
    type: string
    required: false
    description: "Forces scp to use IPv4 addresses only"
    aliases:
      - "-4"
  - name: flag-6
    type: string
    required: false
    description: "Forces scp to use IPv6 addresses only"
    aliases:
      - "-6"
  - name: flag-c
    type: string
    required: false
    description: "Selects the cipher to use for encrypting the data transfer. This
      option is directly passed to ssh(1)"
    aliases:
      - -c
  - name: flag-D
    template_key: flag-d
    type: string
    required: false
    description: "Connect directly to a local SFTP server program rather than a remote
      one via ssh(1). This option may be useful in debugging the client and server"
    aliases:
      - -D
  - name: flag-F
    template_key: flag-f
    type: string
    required: false
    description: "Specifies an alternative per-user configuration file for ssh. This
      option is directly passed to ssh(1)"
    aliases:
      - -F
  - name: flag-i
    type: string
    required: false
    description: "Selects the file from which the identity (private key) for pub-
      lic key authentication is read. This option is directly passed to ssh(1)"
    aliases:
      - -i
  - name: flag-J
    template_key: flag-j
    type: string
    required: false
    description: "Connect to the target host by first making an scp connection to
      the jump host described by destination and then establishing a TCP forwarding
      to the ultimate destination from there. Multiple jump h..."
    aliases:
      - -J
  - name: flag-l
    type: string
    required: false
    description: "Limits the used bandwidth, specified in Kbit/s"
    aliases:
      - -l
  - name: flag-o
    type: string
    required: false
    description: "Can be used to pass options to ssh in the format used in ssh_config(5).
      This is useful for specifying options for which there is no separate scp command-line
      flag. For full details of the options l..."
    aliases:
      - -o
  - name: flag-P
    template_key: flag-p
    type: string
    required: false
    description: "Specifies the port to connect to on the remote host. Note that this
      option is written with a capital `P', because -p is already reserved for preserving
      the times and mode bits of the file"
    aliases:
      - -P
  - name: flag-p
    type: string
    required: false
    description: "Preserves modification times, access times, and file mode bits"
    aliases:
      - -p
  - name: flag-q
    type: string
    required: false
    description: "Quiet mode: disables the progress meter as well as warning and"
    aliases:
      - -q
  - name: flag-r
    type: string
    required: false
    description: "Recursively copy entire directories. Note that scp follows sym-"
    aliases:
      - -r
  - name: flag-S
    template_key: flag-s
    type: string
    required: false
    description: "Name of program to use for the encrypted connection. The pro- gram
      must understand ssh(1) options"
    aliases:
      - -S
  - name: flag-v
    type: string
    required: false
    description: "Verbose mode. Causes scp and ssh(1) to print debugging messages"
    aliases:
      - -v
  - name: flag-X
    template_key: flag-x
    type: string
    required: false
    description: "Specify an option that controls aspects of SFTP protocol behav-
      iour. The valid options are:"
    aliases:
      - -X
execution:
  template: "scp -3 {flag-3} -4 {flag-4} -6 {flag-6} -c {flag-c} -D {flag-d}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
global_vars:
  target: ip
  user: user
  port: port
examples:
  - description: "Basic usage with flag-3"
    command: "scp ${flag-3}"
  - description: "Display help message"
    command: "scp --help"
  - description: Securely copies files from remote ADDR's PATH to the current-working-directory.
      By default here, port 22 is used, or whichever port is otherwise configured.
    command: scp ADDR:PATH ./
  - description: Using aliases (not Bash aliases) work with scp(1) as well. In this
      example, - the PATH1 of the first remote source defined as ALIAS1 is sent to
      PATH2 of the remote destination defined as ALIAS2.
    command: scp ALIAS1:PATH1 ALIAS2:PATH2
  - description: You can use the `-P` flag -- uppercase, unlike ssh(1) -- to determine
      the PORT, in-case it's non-standard (not 22) or not defined within an alias.
    command: scp -P PORT ADDR:PATH ./
related_tools:
  - network-remote-ssh
  - network-transfer-sftp
  - system-sync-rsync
---

# scp — Secure copy over SSH protocol

## Overview

`scp` is a command-line utility for secure copy over ssh protocol.

## Usage

```
scp -3 {flag-3} -4 {flag-4} -6 {flag-6} -c {flag-c} -D {flag-d}
```
