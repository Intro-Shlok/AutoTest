---
id: system-file-strings
namespace: system:file:strings
name: strings
description: Find printable strings in binary files
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.file.strings
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
  - defense-evasion
  - execution
  - persistence
  - privilege-escalation
  - process-manip
parameters:
  - name: all
    type: string
    required: false
    description: "Scan the entire file, not just the data section [default]"
    aliases:
      - -a
      - --all
  - name: data
    type: string
    required: false
    description: "Only scan the data sections in the file"
    aliases:
      - -d
      - --data
  - name: print-file-name
    type: string
    required: false
    description: "Print the name of the file before each string"
    aliases:
      - -f
      - --print-file-name
  - name: flag-n
    type: string
    required: false
    description: "Locate & print any sequence of at least <number>"
    aliases:
      - -n
  - name: bytes
    type: integer
    required: false
    description: "displayable characters. (The default is 4)"
    aliases:
      - --bytes
  - name: radix
    type: string
    required: false
    description: "Print the location of the string in base 8, 10 or 16"
    aliases:
      - -t
      - --radix
  - name: include-all-whitespace I
    template_key: include-all-whitespace-i
    type: string
    required: false
    description: "Set the include-all-whitespace I parameter"
    aliases:
      - -w
      - --include-all-whitespace I
  - name: flag-o
    type: string
    required: false
    description: "An alias for --radix=o"
    aliases:
      - -o
  - name: target
    type: string
    required: false
    description: "Specify the binary file format"
    aliases:
      - -T
      - --target
  - name: encoding
    type: string
    required: false
    description: "s = 7-bit, S = 8-bit, {b,l} = 16-bit, {B,L} = 32-bit"
    aliases:
      - -e
      - --encoding
    enum:
      - b,l
  - name: unicode
    type: string
    required: false
    description: "Set the unicode parameter"
    aliases:
      - --unicode
  - name: flag-U
    template_key: flag-u
    type: string
    required: false
    description: "Specify how to treat UTF-8 encoded unicode characters"
    aliases:
      - -U
  - name: output-separator
    type: string
    required: false
    description: "Set the output-separator parameter"
    aliases:
      - -s
      - --output-separator
  - name: help
    type: string
    required: false
    description: "Display this information"
    aliases:
      - -h
      - --help
  - name: version
    type: string
    required: false
    description: "Print the program's version number"
    aliases:
      - -v
      - -V
      - --version
execution:
  template: "strings -a {all} -d {data} -f {print-file-name} -n {flag-n} --bytes {bytes}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with all"
    command: "strings ${all}"
  - description: "Display help message"
    command: "strings --help"
mitre_ids:
  - T1191
---

# strings — Find printable strings in binary files

## Overview

`strings` is a command-line utility for find printable strings in binary files.

## Usage

```
strings -a {all} -d {data} -f {print-file-name} -n {flag-n} --bytes {bytes}
```
