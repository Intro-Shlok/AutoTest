---
id: network-transfer-sftp
namespace: network:transfer:sftp
name: sftp
description: Secure file transfer over SSH
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.transfer.sftp
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
  - execution
parameters:
  - name: flag-4
    type: string
    required: false
    description: "Forces sftp to use IPv4 addresses only"
    aliases:
      - "-4"
  - name: flag-6
    type: string
    required: false
    description: "Forces sftp to use IPv6 addresses only"
    aliases:
      - "-6"
  - name: flag-a
    type: string
    required: false
    description: "Attempt to continue interrupted transfers rather than overwrit-"
    aliases:
      - -a
  - name: flag-B
    template_key: flag-b
    type: string
    required: false
    description: "Specify the size of the buffer that sftp uses when transferring
      files. Larger buffers require fewer round trips at the cost of higher memory
      consumption. The default is 32768 bytes"
    aliases:
      - -B
  - name: flag-b
    type: string
    required: false
    description: "Batch mode reads a series of commands from an input batchfile instead
      of stdin. Since it lacks user interaction, it should be used in conjunction
      with non-interactive authentication to obvi- ate th..."
    aliases:
      - -b
  - name: flag-c
    type: string
    required: false
    description: "Selects the cipher to use for encrypting the data transfers. This
      option is directly passed to ssh(1)"
    aliases:
      - -c
  - name: flag-D
    template_key: flag-d
    type: string
    required: false
    description: "Connect directly to a local sftp server (rather than via ssh(1)).
      A command and arguments may be specified, for example \"/path/sftp-server -el
      debug3\". This option may be useful in debugging the ..."
    aliases:
      - -D
  - name: flag-F
    template_key: flag-f
    type: string
    required: false
    description: "Specifies an alternative per-user configuration file for ssh(1).
      This option is directly passed to ssh(1)"
    aliases:
      - -F
  - name: flag-f
    type: string
    required: false
    description: "Requests that files be flushed to disk immediately after trans-"
    aliases:
      - -f
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
    description: "Connect to the target host by first making an sftp connection to
      the jump host described by destination and then establishing a TCP forwarding
      to the ultimate destination from there. Multiple jump ..."
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
      This is useful for specifying options for which there is no separate sftp command-line
      flag. For example, to specify an alter..."
    aliases:
      - -o
  - name: flag-P
    template_key: flag-p
    type: string
    required: false
    description: "Specifies the port to connect to on the remote host"
    aliases:
      - -P
  - name: flag-p
    type: string
    required: false
    description: "Preserves modification times, access times, and modes from the"
    aliases:
      - -p
  - name: flag-q
    type: string
    required: false
    description: "Quiet mode: disables the progress meter as well as warning and"
    aliases:
      - -q
  - name: flag-R
    template_key: flag-r
    type: string
    required: false
    description: "Specify how many requests may be outstanding at any one time. Increasing
      this may slightly improve file transfer speed but will increase memory usage.
      The default is 64 outstanding re- quests"
    aliases:
      - -R
  - name: flag-r
    type: string
    required: false
    description: "Recursively copy entire directories when uploading and download-"
    aliases:
      - -r
  - name: flag-S
    template_key: flag-s
    type: string
    required: false
    description: "Name of the program to use for the encrypted connection. The program
      must understand ssh(1) options"
    aliases:
      - -S
  - name: flag-s
    type: string
    required: false
    description: "Specifies the SSH2 subsystem or the path for an sftp server on the
      remote host. A path is useful when the remote sshd(8) does not have an sftp
      subsystem configured"
    aliases:
      - -s
  - name: flag-v
    type: string
    required: false
    description: "Raise logging level. This option is also passed to ssh"
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
  - name: flag-1
    type: string
    required: false
    description: "Produce single columnar output"
    aliases:
      - "-1"
  - name: flag-a-2
    type: string
    required: false
    description: "List files beginning with a dot (`.')"
    aliases:
      - -a
  - name: flag-f-2
    type: string
    required: false
    description: "Do not sort the listing. The default sort order is lex-"
    aliases:
      - -f
  - name: flag-h
    type: string
    required: false
    description: "When used with a long format option, use unit suffixes:"
    aliases:
      - -h
  - name: flag-l-2
    type: string
    required: false
    description: "Display additional details including permissions and"
    aliases:
      - -l
  - name: flag-n
    type: string
    required: false
    description: "Produce a long listing with user and group information"
    aliases:
      - -n
  - name: flag-r-2
    type: string
    required: false
    description: "Reverse the sort order of the listing"
    aliases:
      - -r
  - name: flag-t
    type: string
    required: false
    description: "Sort the listing by last modification time"
    aliases:
      - -t
execution:
  template: "sftp -4 {flag-4} -6 {flag-6} -a {flag-a} -B {flag-b} -b {flag-b}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
global_vars:
  target: ip
  user: user
  port: port
examples:
  - description: "Basic usage with flag-4"
    command: "sftp ${flag-4}"
  - description: "Display help message"
    command: "sftp --help"
  - description: Can be used to execute any command or file on a system, but without
      stdin/stdout/stderr.
    command: "sftp -D\"touch /tmp/korewashere\"\n"
  - description: Proxy execution of specified command, can be used as a defensive
      evasion.
    command: sftp -o ProxyCommand="{CMD}" .
mitre_ids:
  - T1202
contributor: Swachchhanda Shrawan Poudel
detections:
  - type: ioc
    description: sftp.exe executions with ProxyCommand on the command line
  - type: ioc
    description: sftp.exe spawning ssh.exe with ProxyCommand on the command line
  - type: sigma
    url: https://github.com/SigmaHQ/sigma/pull/5414/files
related_tools:
  - network-remote-ssh
  - network-transfer-scp
  - system-sync-rsync
---

# sftp — Secure file transfer over SSH

## Overview

`sftp` is a command-line utility for secure file transfer over ssh.

## Usage

```
sftp -4 {flag-4} -6 {flag-6} -a {flag-a} -B {flag-b} -b {flag-b}
```
