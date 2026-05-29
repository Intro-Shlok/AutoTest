---
id: system-process-nice
namespace: system:process:nice
name: nice
description: Run a program with modified scheduling priority
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.process.nice
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
  - command-and-control
  - credential-access
  - defense-evasion
  - lateral-movement
  - process-manip
parameters:
  - name: flag-2
    type: string
    required: false
    description: "Set the flag-2 parameter"
    aliases:
      - "-2"
  - name: adjustment
    type: integer
    required: false
    description: "add integer N to the niceness (default 10) --help display this help
      and exit --version output version information and exit"
    aliases:
      - -n
      - --adjustment
execution:
  template: "nice -2 {flag-2} -n {adjustment}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with flag-2"
    command: "nice ${flag-2}"
  - description: "Display help message"
    command: "nice --help"
related_tools:
  - system-process-ionice
install:
    - method: apt
      package_name: "coreutils"
      commands:
        - "apt-get install -y coreutils"
---

# nice — Run a program with modified scheduling priority

## Overview

`nice` is a command-line utility for run a program with modified scheduling priority.

## Usage

```
nice -2 {flag-2} -n {adjustment}
```
