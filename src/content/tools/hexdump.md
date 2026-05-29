---
id: system-file-hexdump
namespace: system:file:hexdump
name: hexdump
description: Display file contents in hexadecimal
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.file.hexdump
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
  - execution
  - process-manip
parameters:
  - name: one-byte-octal
    type: string
    required: false
    description: "one-byte octal display"
    aliases:
      - -b
      - --one-byte-octal
  - name: one-byte-hex
    type: string
    required: false
    description: "one-byte hexadecimal display"
    aliases:
      - -X
      - --one-byte-hex
  - name: one-byte-char
    type: string
    required: false
    description: "one-byte character display"
    aliases:
      - -c
      - --one-byte-char
  - name: canonical
    type: string
    required: false
    description: "canonical hex+ASCII display"
    aliases:
      - -C
      - --canonical
  - name: two-bytes-decimal
    type: string
    required: false
    description: "two-byte decimal display"
    aliases:
      - -d
      - --two-bytes-decimal
  - name: two-bytes-octal
    type: string
    required: false
    description: "two-byte octal display"
    aliases:
      - -o
      - --two-bytes-octal
  - name: two-bytes-hex
    type: string
    required: false
    description: "two-byte hexadecimal display"
    aliases:
      - -x
      - --two-bytes-hex
  - name: color
    type: string
    required: false
    description: "interpret color formatting specifiers"
    aliases:
      - -L
      - --color
  - name: format
    type: string
    required: false
    description: "format string to be used for displaying data"
    aliases:
      - -e
      - --format <format>
  - name: format-file
    type: file
    required: false
    description: "Set the format-file parameter"
    aliases:
      - -f
      - --format-file <file>
  - name: length
    type: string
    required: false
    description: "interpret only length bytes of input"
    aliases:
      - -n
      - --length <length>
  - name: skip
    type: string
    required: false
    description: "skip offset bytes from the beginning"
    aliases:
      - -s
      - --skip <offset>
  - name: no-squeezing
    type: string
    required: false
    description: "output identical lines"
    aliases:
      - -v
      - --no-squeezing
  - name: help
    type: string
    required: false
    description: "display this help"
    aliases:
      - -h
      - --help
  - name: version
    type: string
    required: false
    description: "display version"
    aliases:
      - -V
      - --version
execution:
  template: "hexdump -b {one-byte-octal} -X {one-byte-hex} -c {one-byte-char} -C {canonical}
    -d {two-bytes-decimal}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with one-byte-octal"
    command: "hexdump ${one-byte-octal}"
  - description: "Display help message"
    command: "hexdump --help"
  - description: side-by-side hexadecimal and ASCII view of the first 128 bytes of
      a file
    command: hexdump -C -n128 /etc/passwd
  - description: Convert a binary file to C Array
    command: hexdump -v -e '16/1 "0x%02X, "' -e '"\n"' file.bin > hexarray.h
  - description: Convert a binary file to Shell code
    command: hexdump -v -e '"\\""x" 1/1 "%02x" ""'
  - description: Generate random MAC address
    command: hexdump -n6 -e '/1 ":%02X"' /dev/random|sed s/^://g
related_tools:
  - system-file-od
  - system-file-xxd
install:
    - method: apt
      package_name: "bsdmainutils"
      commands:
        - "apt-get install -y bsdmainutils"
---

# hexdump — Display file contents in hexadecimal

## Overview

`hexdump` is a command-line utility for display file contents in hexadecimal.

## Usage

```
hexdump -b {one-byte-octal} -X {one-byte-hex} -c {one-byte-char} -C {canonical} -d {two-bytes-decimal}
```
