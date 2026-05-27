---
id: system-file-base64
namespace: system:file:base64
name: base64
description: Base64 encode/decode data
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.file.base64
  - system.file.search
  - system.file.process
  - system.file.copy
  - system.file.move
  - system.file.delete
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
  - file-system
  - encryption
  - batch
techniques:
  - lateral-movement
  - data-manipulation
  - execution
  - command-and-control
  - persistence
  - credential-access
  - defense-evasion
  - exfiltration
  - collection
  - privilege-escalation
parameters:
  - name: decode
    type: string
    required: false
    description: "decode data"
    aliases:
      - -d
      - --decode
  - name: ignore-garbage
    type: string
    required: false
    description: "when decoding, ignore non-alphabet characters"
    aliases:
      - -i
      - --ignore-garbage
  - name: wrap
    type: string
    required: false
    description: "wrap encoded lines after COLS character (default 76). Use 0 to disable
      line wrapping --help display this help and exit --version output version information
      and exit"
    aliases:
      - -w
      - --wrap
execution:
  template: "base64 -d {decode} -i {ignore-garbage} -w {wrap}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with decode"
    command: "base64 ${decode}"
  - description: "Display help message"
    command: "base64 --help"
mitre_ids:
  - T1027
  - T1140
---

# base64 — Base64 encode/decode data

## Overview

`base64` is a command-line utility for base64 encode/decode data.

## Usage

```
base64 -d {decode} -i {ignore-garbage} -w {wrap}
```
