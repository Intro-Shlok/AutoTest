---
id: system-process-kill
namespace: system:process:kill
name: kill
description: Send signals to processes
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.process.kill
  - system.process.list
  - system.process.signal
  - system.process.monitor
platforms:
  - linux
risk_level: high
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
  - process-termination
  - persistence
parameters:
  - name: flag-s
    type: string
    required: false
    description: "SIG is a signal name"
    aliases:
      - -s
  - name: flag-n
    type: string
    required: false
    description: "SIG is a signal number"
    aliases:
      - -n
  - name: flag-l
    type: string
    required: false
    description: "list the signal names; if arguments follow `-l' they are"
    aliases:
      - -l
execution:
  template: "kill -s {flag-s} -n {flag-n} -l {flag-l}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with flag-s"
    command: "kill ${flag-s}"
  - description: "Display help message"
    command: "kill --help"
related_tools:
  - system-process-ps
install:
    - method: apt
      package_name: "procps"
      commands:
        - "apt-get install -y procps"
---

# kill — Send signals to processes

## Overview

`kill` is a command-line utility for send signals to processes.

## Usage

```
kill -s {flag-s} -n {flag-n} -l {flag-l}
```
