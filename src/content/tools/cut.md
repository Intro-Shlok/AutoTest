---
id: system-file-cut
namespace: system:file:cut
name: cut
description: Remove sections from each line of files
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.file.cut
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
  - credential-access
parameters:
  - name: bytes
    type: array
    required: false
    description: "select only these bytes"
    aliases:
      - -b
      - --bytes
  - name: characters
    type: array
    required: false
    description: "select only these characters"
    aliases:
      - -c
      - --characters
  - name: delimiter
    type: string
    required: false
    description: "use DELIM instead of TAB for field delimiter"
    aliases:
      - -d
      - --delimiter
  - name: fields
    type: array
    required: false
    description: "select only these fields; also print any line that contains no delimiter
      character, unless the -s option is specified"
    aliases:
      - -f
      - --fields
  - name: flag-n
    type: string
    required: false
    description: "(ignored) --complement complement the set of selected bytes, characters
      or fields"
    aliases:
      - -n
  - name: only-delimited
    type: string
    required: false
    description: "do not print lines not containing delimiters --output-delimiter=STRING
      use STRING as the output delimiter; the default is to use the input delimiter"
    aliases:
      - -s
      - --only-delimited
  - name: zero-terminated
    type: string
    required: false
    description: "line delimiter is NUL, not newline --help display this help and
      exit --version output version information and exit"
    aliases:
      - -z
      - --zero-terminated
execution:
  template: "cut -b {bytes} -c {characters} -d {delimiter} -f {fields} -n {flag-n}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Display help message"
    command: "cut --help"
---

# cut — Remove sections from each line of files

## Overview

`cut` is a command-line utility for remove sections from each line of files.

## Usage

```
cut -b {bytes} -c {characters} -d {delimiter} -f {fields} -n {flag-n}
```
