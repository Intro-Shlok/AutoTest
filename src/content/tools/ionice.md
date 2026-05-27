---
id: system-process-ionice
namespace: system:process:ionice
name: ionice
description: Set/get I/O scheduling class and priority
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.process.ionice
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
techniques:
  - execution
  - impact
parameters:
  - name: class
    type: integer
    required: false
    description: "name or number of scheduling class"
    aliases:
      - -c
      - --class <class>
  - name: classdata
    type: integer
    required: false
    description: "only for the realtime and best-effort classes"
    aliases:
      - -n
      - --classdata <num>
  - name: pid
    type: string
    required: false
    description: "act on these already running processes"
    aliases:
      - -p
      - --pid <pid>
  - name: pgid
    type: string
    required: false
    description: "act on already running processes in these groups"
    aliases:
      - -P
      - --pgid <pgrp>
  - name: ignore
    type: string
    required: false
    description: "ignore failures"
    aliases:
      - -t
      - --ignore
  - name: uid
    type: string
    required: false
    description: "act on already running processes owned by these users"
    aliases:
      - -u
      - --uid <uid>
  - name: help
    type: string
    required: false
    description: "display this help"
    aliases:
      - -h
      - --help
  - name: version
    type: string
    required: false
    description: "display version"
    aliases:
      - -V
      - --version
execution:
  template: "ionice -c {class} -n {classdata} -p {pid} -P {pgid} -t {ignore}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Display help message"
    command: "ionice --help"
related_tools:
  - system-process-nice
---

# ionice — Set/get I/O scheduling class and priority

## Overview

`ionice` is a command-line utility for set/get i/o scheduling class and priority.

## Usage

```
ionice -c {class} -n {classdata} -p {pid} -P {pgid} -t {ignore}
```
