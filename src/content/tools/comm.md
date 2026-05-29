---
id: system-file-comm
namespace: system:file:comm
name: comm
description: Compare two sorted files line by line
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.file.comm
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
techniques:
  - collection
  - data-manipulation
  - defense-evasion
parameters:
  - name: flag-1
    type: string
    required: false
    description: "suppress column 1 (lines unique to FILE1)"
    aliases:
      - "-1"
  - name: flag-2
    type: string
    required: false
    description: "suppress column 2 (lines unique to FILE2)"
    aliases:
      - "-2"
  - name: flag-3
    type: string
    required: false
    description: "suppress column 3 (lines that appear in both files)"
    aliases:
      - "-3"
  - name: check-order
    type: string
    required: false
    description: "check that the input is correctly sorted, even if all input lines
      are pairable --nocheck-order do not check that the input is correctly sorted
      --output-delimiter=STR separate columns with STR --tot..."
    aliases:
      - --check-order
  - name: zero-terminated
    type: string
    required: false
    description: "line delimiter is NUL, not newline --help display this help and
      exit --version output version information and exit"
    aliases:
      - -z
      - --zero-terminated
execution:
  template: "comm -1 {flag-1} -2 {flag-2} -3 {flag-3} --check-order {check-order}
    -z {zero-terminated}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with flag-1"
    command: "comm ${flag-1}"
  - description: "Display help message"
    command: "comm --help"
related_tools:
  - system-file-cat
  - system-file-sort
  - system-file-uniq
  - system-file-wc
install:
    - method: apt
      package_name: "coreutils"
      commands:
        - "apt-get install -y coreutils"
---

# comm — Compare two sorted files line by line

## Overview

`comm` is a command-line utility for compare two sorted files line by line.

## Usage

```
comm -1 {flag-1} -2 {flag-2} -3 {flag-3} --check-order {check-order} -z {zero-terminated}
```
