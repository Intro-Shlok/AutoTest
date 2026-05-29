---
id: system-process-timeout
namespace: system:process:timeout
name: timeout
description: Run a command with a time limit
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.process.timeout
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
    - name: foreground
      type: number
      required: false
      description: "when not running timeout directly from a shell prompt, allow COMMAND to read from the TTY and get TTY signals; in this mode, children of COMMAND will not be timed out"
      aliases:
        - -f
        - --foreground
    - name: kill-after
      type: string
      required: false
      description: "also send a KILL signal if COMMAND is still running this long after the initial signal was sent"
      aliases:
        - -k
        - --kill-after
    - name: preserve-status
      type: string
      required: false
      description: "exit with the same status as COMMAND, even when the command times out"
      aliases:
        - -p
        - --preserve-status
    - name: signal
      type: array
      required: false
      description: "specify the signal to be sent on timeout; SIGNAL may be a name like 'HUP' or a number; see 'kill -l' for a list of signals"
      aliases:
        - -s
        - --signal
    - name: verbose
      type: number
      required: false
      description: "diagnose to standard error any signal sent upon timeout --help display this help and exit --version output version information and exit"
      aliases:
        - -v
        - --verbose
execution:
  template: "timeout -f {foreground} -k {kill-after} -p {preserve-status} -s {signal} -v {verbose}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Display help message"
    command: "timeout --help"
install:
    - method: apt
      package_name: "coreutils"
      commands:
        - "apt-get install -y coreutils"
---

# timeout — Run a command with a time limit

## Overview

`timeout` is a command-line utility for run a command with a time limit.

## Usage

```
timeout -f {foreground} -k {kill-after} -p {preserve-status} -s {signal} -v {verbose}
```