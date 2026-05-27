---
id: system-process-watch
namespace: system:process:watch
name: watch
description: Execute a program periodically
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.process.watch
  - system.process.list
  - system.process.signal
  - system.process.monitor
platforms:
  - linux
risk_level: low
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
features:
  - local
  - process-manip
  - streaming
techniques:
  - execution
  - impact
  - command-and-control
  - defense-evasion
  - discovery
  - enumeration
  - persistence
  - privilege-escalation
  - process-manip
parameters:
  - name: beep
    type: string
    required: false
    description: "beep if command has a non-zero exit"
    aliases:
      - -b
      - --beep
  - name: color
    type: string
    required: false
    description: "interpret ANSI color and style sequences"
    aliases:
      - -c
      - --color
  - name: no-color
    type: string
    required: false
    description: "do not interpret ANSI color and style sequences"
    aliases:
      - -C
      - --no-color
  - name: differences
    type: string
    required: false
    description: "highlight changes between updates"
    aliases:
      - -d
      - --differences
  - name: errexit
    type: string
    required: false
    description: "exit if command has a non-zero exit"
    aliases:
      - -e
      - --errexit
  - name: chgexit
    type: string
    required: false
    description: "exit when output from command changes"
    aliases:
      - -g
      - --chgexit
  - name: equexit
    type: string
    required: false
    description: "exit when output from command does not change"
    aliases:
      - -q
      - --equexit <cycles>
  - name: interval
    type: string
    required: false
    description: "Set the interval parameter"
    aliases:
      - -n
      - --interval <secs>
  - name: precise
    type: number
    required: false
    description: "attempt run command in precise intervals"
    aliases:
      - -p
      - --precise
  - name: no-rerun
    type: string
    required: false
    description: "do not rerun program on window resize"
    aliases:
      - -r
      - --no-rerun
  - name: no-title
    type: string
    required: false
    description: "turn off header"
    aliases:
      - -t
      - --no-title
  - name: no-wrap
    type: string
    required: false
    description: "turn off line wrapping"
    aliases:
      - -w
      - --no-wrap
  - name: exec
    type: string
    required: false
    description: "pass command to exec instead of \"sh -c\""
    aliases:
      - -x
      - --exec
  - name: help
    type: string
    required: false
    description: "display this help and exit"
    aliases:
      - -h
      - --help
  - name: version
    type: string
    required: false
    description: "Set the version parameter"
    aliases:
      - -v
      - --version
execution:
  template: "watch -b {beep} -c {color} -C {no-color} -d {differences} -e {errexit}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with beep"
    command: "watch ${beep}"
  - description: "Display help message"
    command: "watch --help"
---

# watch — Execute a program periodically

## Overview

`watch` is a command-line utility for execute a program periodically.

## Usage

```
watch -b {beep} -c {color} -C {no-color} -d {differences} -e {errexit}
```
