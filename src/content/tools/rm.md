---
id: system-file-rm
namespace: system:file:rm
name: rm
description: Remove files or directories
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.file.rm
  - system.file.search
  - system.file.process
  - system.file.copy
  - system.file.move
  - system.file.delete
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
  - file-system
techniques:
  - collection
  - data-manipulation
parameters:
  - name: force
    type: string
    required: false
    description: "ignore nonexistent files and arguments, never prompt"
    aliases:
      - -f
      - --force
  - name: flag-i
    type: string
    required: false
    description: "prompt before every removal"
    aliases:
      - -i
  - name: flag-I
    template_key: flag-i
    type: file
    required: false
    description: "prompt once before removing more than three files, or when removing
      recursively; less intrusive than -i, while still giving protection against most
      mistakes --interactive[=WHEN] prompt according to..."
    aliases:
      - -I
  - name: recursive
    type: string
    required: false
    description: "remove directories and their contents recursively"
    aliases:
      - -r
      - -R
      - --recursive
  - name: dir
    type: string
    required: false
    description: "remove empty directories"
    aliases:
      - -d
      - --dir
  - name: verbose
    type: string
    required: false
    description: "explain what is being done --help display this help and exit --version
      output version information and exit"
    aliases:
      - -v
      - --verbose
execution:
  template: "rm -f {force} -i {flag-i} -I {flag-i} -r {recursive} -d {dir}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with force"
    command: "rm ${force}"
  - description: "Display help message"
    command: "rm --help"
phase: exploitation
---

# rm — Remove files or directories

## Overview

`rm` is a command-line utility for remove files or directories.

## Usage

```
rm -f {force} -i {flag-i} -I {flag-i} -r {recursive} -d {dir}
```
