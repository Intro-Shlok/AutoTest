---
id: system-file-head
namespace: system:file:head
name: head
description: Output the first part of files
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.file.head
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
  - pipes-stdin
  - pipes-stdout
techniques:
  - collection
  - data-manipulation
  - execution
  - process-manip
parameters:
  - name: bytes
    type: string
    required: false
    description: "print the first NUM bytes of each file; with the leading '-', print
      all but the last NUM bytes of each file"
    aliases:
      - -c
      - --bytes
  - name: lines
    type: string
    required: false
    description: "print the first NUM lines instead of the first 10; with the leading
      '-', print all but the last NUM lines of each file"
    aliases:
      - -n
      - --lines
  - name: quiet
    type: string
    required: false
    description: "never print headers giving file names"
    aliases:
      - -q
      - --quiet
      - --silent
  - name: verbose
    type: string
    required: false
    description: "always print headers giving file names"
    aliases:
      - -v
      - --verbose
  - name: zero-terminated
    type: string
    required: false
    description: "line delimiter is NUL, not newline --help display this help and
      exit --version output version information and exit"
    aliases:
      - -z
      - --zero-terminated
execution:
  template: "head -c {bytes} -n {lines} -q {quiet} -v {verbose} -z {zero-terminated}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with bytes"
    command: "head ${bytes}"
  - description: "Display help message"
    command: "head --help"
related_tools:
  - system-file-tail
---

# head — Output the first part of files

## Overview

`head` is a command-line utility for output the first part of files.

## Usage

```
head -c {bytes} -n {lines} -q {quiet} -v {verbose} -z {zero-terminated}
```
