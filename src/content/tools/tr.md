---
id: system-file-tr
namespace: system:file:tr
name: tr
description: Translate or delete characters
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.file.tr
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
  - persistence
parameters:
  - name: complement
    type: string
    required: false
    description: "use the complement of ARRAY1"
    aliases:
      - -c
      - -C
      - --complement
  - name: delete
    type: string
    required: false
    description: "delete characters in ARRAY1, do not translate"
    aliases:
      - -d
      - --delete
  - name: squeeze-repeats
    type: string
    required: false
    description: "replace each sequence of a repeated character that is listed in
      the last specified ARRAY, with a single occurrence of that character"
    aliases:
      - -s
      - --squeeze-repeats
  - name: truncate-set1
    type: string
    required: false
    description: "first truncate ARRAY1 to length of ARRAY2 --help display this help
      and exit --version output version information and exit"
    aliases:
      - -t
      - --truncate-set1
  - name: flag-t
    type: string
    required: false
    description: "Set the flag-t parameter"
    aliases:
      - -t
execution:
  template: "tr -c {complement} -d {delete} -s {squeeze-repeats} -t {truncate-set1}
    -t {flag-t}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with complement"
    command: "tr ${complement}"
  - description: "Display help message"
    command: "tr --help"
phase: post-exploitation
related_tools:
  - text-process-awk
  - text-process-sed
  - text-search-grep
---

# tr — Translate or delete characters

## Overview

`tr` is a command-line utility for translate or delete characters.

## Usage

```
tr -c {complement} -d {delete} -s {squeeze-repeats} -t {truncate-set1} -t {flag-t}
```
