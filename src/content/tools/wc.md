---
id: system-file-wc
namespace: system:file:wc
name: wc
description: Print newline, word, and byte counts
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.file.wc
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
  - command-and-control
parameters:
  - name: bytes
    type: string
    required: false
    description: "print the byte counts"
    aliases:
      - -c
      - --bytes
  - name: chars
    type: string
    required: false
    description: "print the character counts"
    aliases:
      - -m
      - --chars
  - name: lines
    type: string
    required: false
    description: "print the newline counts --debug indicate what line count acceleration
      is used --files0-from=F read input from the files specified by NUL-terminated
      names in file F; If F is -, read names from stan..."
    aliases:
      - -l
      - --lines
  - name: max-line-length
    type: string
    required: false
    description: "print the maximum display width"
    aliases:
      - -L
      - --max-line-length
  - name: words
    type: string
    required: false
    description: "print the word counts --total=WHEN when to print a line with total
      counts; WHEN can be: auto, always, only, never --help display this help and
      exit --version output version information and exit"
    aliases:
      - -w
      - --words
execution:
  template: "wc -c {bytes} -m {chars} -l {lines} -L {max-line-length} -w {words}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with bytes"
    command: "wc ${bytes}"
  - description: "Display help message"
    command: "wc --help"
related_tools:
  - system-file-cat
  - system-file-comm
  - system-file-sort
  - system-file-uniq
---

# wc — Print newline, word, and byte counts

## Overview

`wc` is a command-line utility for print newline, word, and byte counts.

## Usage

```
wc -c {bytes} -m {chars} -l {lines} -L {max-line-length} -w {words}
```
