---
id: system-process-free
namespace: system:process:free
name: free
description: Display amount of free and used memory
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.process.free
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
  - defense-evasion
  - lateral-movement
  - process-manip
parameters:
  - name: bytes
    type: string
    required: false
    description: "show output in bytes"
    aliases:
      - -b
      - --bytes
  - name: kilo
    type: string
    required: false
    description: "show output in kilobytes"
    aliases:
      - --kilo
  - name: mega
    type: string
    required: false
    description: "show output in megabytes"
    aliases:
      - --mega
  - name: giga
    type: string
    required: false
    description: "show output in gigabytes"
    aliases:
      - --giga
  - name: tera
    type: string
    required: false
    description: "show output in terabytes"
    aliases:
      - --tera
  - name: peta
    type: string
    required: false
    description: "show output in petabytes"
    aliases:
      - --peta
  - name: kibi
    type: string
    required: false
    description: "show output in kibibytes"
    aliases:
      - -k
      - --kibi
  - name: mebi
    type: string
    required: false
    description: "show output in mebibytes"
    aliases:
      - -m
      - --mebi
  - name: gibi
    type: string
    required: false
    description: "show output in gibibytes"
    aliases:
      - -g
      - --gibi
  - name: tebi
    type: string
    required: false
    description: "show output in tebibytes"
    aliases:
      - --tebi
  - name: pebi
    type: string
    required: false
    description: "show output in pebibytes"
    aliases:
      - --pebi
  - name: human
    type: string
    required: false
    description: "show human-readable output"
    aliases:
      - -h
      - --human
  - name: si
    type: string
    required: false
    description: "use powers of 1000 not 1024"
    aliases:
      - --si
  - name: lohi
    type: string
    required: false
    description: "show detailed low and high memory statistics"
    aliases:
      - -l
      - --lohi
  - name: line
    type: string
    required: false
    description: "show output on a single line"
    aliases:
      - -L
      - --line
  - name: total
    type: string
    required: false
    description: "show total for RAM + swap"
    aliases:
      - -t
      - --total
  - name: committed
    type: string
    required: false
    description: "show committed memory and commit limit"
    aliases:
      - -v
      - --committed
  - name: seconds N
    template_key: seconds-n
    type: integer
    required: false
    description: "repeat printing every N seconds"
    aliases:
      - -s
      - --seconds N
  - name: count N
    template_key: count-n
    type: integer
    required: false
    description: "repeat printing N times, then exit"
    aliases:
      - -c
      - --count N
  - name: wide
    type: string
    required: false
    description: "wide output"
    aliases:
      - -w
      - --wide
  - name: help
    type: string
    required: false
    description: "display this help and exit"
    aliases:
      - --help
  - name: version
    type: string
    required: false
    description: "Set the version parameter"
    aliases:
      - -V
      - --version
execution:
  template: "free -b {bytes} --kilo {kilo} --mega {mega} --giga {giga} --tera {tera}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with bytes"
    command: "free ${bytes}"
  - description: "Display help message"
    command: "free --help"
phase: post-exploitation
install:
    - method: apt
      package_name: "procps"
      commands:
        - "apt-get install -y procps"
---

# free — Display amount of free and used memory

## Overview

`free` is a command-line utility for display amount of free and used memory.

## Usage

```
free -b {bytes} --kilo {kilo} --mega {mega} --giga {giga} --tera {tera}
```
