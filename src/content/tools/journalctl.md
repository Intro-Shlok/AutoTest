---
id: system-service-journalctl
namespace: system:service:journalctl
name: journalctl
description: Query the systemd journal
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.service.journalctl
platforms:
  - linux
risk_level: medium
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
features:
  - local
  - requires-root
techniques:
  - execution
  - persistence
parameters:
  - name: system
    type: string
    required: false
    description: "Show the system journal"
    aliases:
      - --system
  - name: user
    type: string
    required: false
    description: "Show the user journal for the current user"
    aliases:
      - --user
  - name: machine
    type: string
    required: false
    description: "Operate on local container"
    aliases:
      - -M
      - --machine
  - name: merge
    type: string
    required: false
    description: "Show entries from all available journals"
    aliases:
      - -m
      - --merge
  - name: directory
    type: file
    required: false
    description: "Show journal files from directory"
    aliases:
      - -D
      - --directory
  - name: file
    type: file
    required: false
    description: "Show journal file"
    aliases:
      - -i
      - --file
  - name: root
    type: file
    required: false
    description: "Operate on an alternate filesystem root"
    aliases:
      - --root
  - name: image
    type: file
    required: false
    description: "Operate on disk image as filesystem root"
    aliases:
      - --image
  - name: image-policy
    type: string
    required: false
    description: "Specify disk image dissection policy"
    aliases:
      - --image-policy
  - name: namespace
    type: string
    required: false
    description: "Show journal data from specified journal namespace"
    aliases:
      - --namespace
  - name: since
    type: string
    required: false
    description: "Show entries not older than the specified date"
    aliases:
      - -S
      - --since
  - name: until
    type: string
    required: false
    description: "Show entries not newer than the specified date"
    aliases:
      - -U
      - --until
  - name: cursor
    type: string
    required: false
    description: "Show entries starting at the specified cursor"
    aliases:
      - -c
      - --cursor
  - name: after-cursor
    type: string
    required: false
    description: "Show entries after the specified cursor"
    aliases:
      - --after-cursor
  - name: cursor-file
    type: file
    required: false
    description: "Show entries after cursor in FILE and update FILE"
    aliases:
      - --cursor-file
  - name: boot
    type: string
    required: false
    description: "Show current boot or the specified boot"
    aliases:
      - -b
      - --boot
  - name: unit
    type: string
    required: false
    description: "Show logs from the specified unit"
    aliases:
      - -u
      - --unit
  - name: user-unit
    type: string
    required: false
    description: "Show logs from the specified user unit"
    aliases:
      - --user-unit
  - name: invocation
    type: string
    required: false
    description: "Show logs from the matching invocation ID"
    aliases:
      - --invocation
  - name: identifier
    type: string
    required: false
    description: "Show entries with the specified syslog identifier"
    aliases:
      - -t
      - --identifier
  - name: exclude-identifier
    type: string
    required: false
    description: "Hide entries with the specified syslog identifier"
    aliases:
      - -T
      - --exclude-identifier
  - name: priority
    type: integer
    required: false
    description: "Show entries within the specified priority range"
    aliases:
      - -p
      - --priority
  - name: facility
    type: string
    required: false
    description: "Set the facility parameter"
    aliases:
      - --facility
  - name: grep
    type: string
    required: false
    description: "Show entries with MESSAGE matching PATTERN"
    aliases:
      - -g
      - --grep
  - name: case-sensitive
    type: string
    required: false
    description: "Set the case-sensitive parameter"
    aliases:
      - --case-sensitive
  - name: dmesg
    type: string
    required: false
    description: "Show kernel message log from the current boot"
    aliases:
      - -k
      - --dmesg
  - name: output
    type: string
    required: false
    description: "Change journal output mode (short, short-precise"
    aliases:
      - -o
      - --output
  - name: output-fields
    type: array
    required: false
    description: "Select fields to print in verbose/export/json modes"
    aliases:
      - --output-fields
  - name: lines
    type: integer
    required: false
    description: "Number of journal entries to show"
    aliases:
      - -n
      - --lines
  - name: reverse
    type: string
    required: false
    description: "Show the newest entries first"
    aliases:
      - -r
      - --reverse
execution:
  template: "journalctl --system {system} --user {user} -M {machine} -m {merge} -D
    {directory}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with system"
    command: "journalctl ${system}"
  - description: "Display help message"
    command: "journalctl --help"
related_tools:
  - system-service-systemctl
install:
    - method: apt
      package_name: "systemd"
      commands:
        - "apt-get install -y systemd"
---

# journalctl — Query the systemd journal

## Overview

`journalctl` is a command-line utility for query the systemd journal.

## Usage

```
journalctl --system {system} --user {user} -M {machine} -m {merge} -D {directory}
```
