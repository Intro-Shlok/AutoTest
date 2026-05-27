---
id: system-process-top
namespace: system:process:top
name: top
description: Display Linux processes
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.process.top
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
  - credential-access
  - defense-evasion
  - lateral-movement
  - persistence
  - process-manip
parameters:
  - name: batch-mode
    type: string
    required: false
    description: "run in non-interactive batch mode"
    aliases:
      - -b
      - --batch-mode
  - name: cmdline-toggle
    type: string
    required: false
    description: "reverse last remembered 'c' state"
    aliases:
      - -c
      - --cmdline-toggle
  - name: delay
    type: string
    required: false
    description: "iterative delay as SECS [.TENTHS]"
    aliases:
      - -d
      - --delay
  - name: scale-summary-mem
    type: string
    required: false
    description: "Set the scale-summary-mem parameter"
    aliases:
      - -E
      - --scale-summary-mem
  - name: scale-task-mem
    type: string
    required: false
    description: "set mem with: k,m,g,t,p for SCALE"
    aliases:
      - -e
      - --scale-task-mem
  - name: threads-show
    type: string
    required: false
    description: "show tasks plus all their threads"
    aliases:
      - -H
      - --threads-show
  - name: idle-toggle
    type: string
    required: false
    description: "reverse last remembered 'i' state"
    aliases:
      - -i
      - --idle-toggle
  - name: iterations
    type: string
    required: false
    description: "exit on maximum iterations NUMBER"
    aliases:
      - -n
      - --iterations
  - name: list-fields
    type: string
    required: false
    description: "output all field names, then exit"
    aliases:
      - -O
      - --list-fields
  - name: sort-override
    type: string
    required: false
    description: "force sorting on this named FIELD"
    aliases:
      - -o
      - --sort-override
  - name: pid
    type: string
    required: false
    description: "monitor only the tasks in PIDLIST"
    aliases:
      - -p
      - --pid
  - name: accum-time-toggle
    type: string
    required: false
    description: "reverse last remembered 'S' state"
    aliases:
      - -S
      - --accum-time-toggle
  - name: secure-mode
    type: string
    required: false
    description: "run with secure mode restrictions"
    aliases:
      - -s
      - --secure-mode
  - name: filter-any-user
    type: string
    required: false
    description: "show only processes owned by USER"
    aliases:
      - -U
      - --filter-any-user
  - name: filter-only-euser
    type: string
    required: false
    description: "show only processes owned by USER"
    aliases:
      - -u
      - --filter-only-euser
  - name: width
    type: integer
    required: false
    description: "change print width [,use COLUMNS]"
    aliases:
      - -w
      - --width [
  - name: single-cpu-toggle
    type: string
    required: false
    description: "reverse last remembered '1' state"
    aliases:
      - "-1"
      - --single-cpu-toggle
  - name: help
    type: string
    required: false
    description: "display this help text, then exit"
    aliases:
      - -h
      - --help
  - name: version
    type: string
    required: false
    description: "output version information & exit"
    aliases:
      - -V
      - --version
execution:
  template: "top -b {batch-mode} -c {cmdline-toggle} -d {delay} -E {scale-summary-mem}
    -e {scale-task-mem}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with batch-mode"
    command: "top ${batch-mode}"
  - description: "Display help message"
    command: "top --help"
phase: enumeration
---

# top — Display Linux processes

## Overview

`top` is a command-line utility for display linux processes.

## Usage

```
top -b {batch-mode} -c {cmdline-toggle} -d {delay} -E {scale-summary-mem} -e {scale-task-mem}
```
