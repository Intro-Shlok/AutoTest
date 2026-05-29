---
id: system-file-od
namespace: system:file:od
name: od
description: Dump files in octal and other formats
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.file.od
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
parameters:
  - name: address-radix
    type: string
    required: false
    description: "output format for file offsets; RADIX is one of [doxn], for Decimal,
      Octal, Hex or None --endian={big|little} swap input bytes according the specified
      order"
    aliases:
      - -A
      - --address-radix
    enum:
      - big
      - little
  - name: skip-bytes
    type: integer
    required: false
    description: "skip BYTES input bytes first"
    aliases:
      - -j
      - --skip-bytes
  - name: read-bytes
    type: integer
    required: false
    description: "limit dump to BYTES input bytes"
    aliases:
      - -N
      - --read-bytes
  - name: strings
    type: string
    required: false
    description: "show only NUL terminated strings of at least BYTES (default 3) printable
      characters"
    aliases:
      - -S
      - --strings
  - name: format
    type: string
    required: false
    description: "select output format or formats"
    aliases:
      - -t
      - --format
  - name: output-duplicates
    type: string
    required: false
    description: "do not use * to mark line suppression"
    aliases:
      - -v
      - --output-duplicates
  - name: width
    type: string
    required: false
    description: "output BYTES bytes per output line; 32 is implied when BYTES is
      not specified --traditional accept arguments in third form above --help display
      this help and exit --version output version informati..."
    aliases:
      - -w
      - --width
  - name: flag-a
    type: string
    required: false
    description: "same as -t a, select named characters, ignoring high-order bit"
    aliases:
      - -a
  - name: flag-b
    type: string
    required: false
    description: "same as -t o1, select octal bytes"
    aliases:
      - -b
  - name: flag-c
    type: string
    required: false
    description: "same as -t c, select printable characters or backslash escapes"
    aliases:
      - -c
  - name: flag-d
    type: string
    required: false
    description: "same as -t u2, select unsigned decimal 2-byte units"
    aliases:
      - -d
  - name: flag-f
    type: string
    required: false
    description: "same as -t fF, select floats"
    aliases:
      - -f
  - name: flag-i
    type: string
    required: false
    description: "same as -t dI, select decimal ints"
    aliases:
      - -i
  - name: flag-l
    type: string
    required: false
    description: "same as -t dL, select decimal longs"
    aliases:
      - -l
  - name: flag-o
    type: string
    required: false
    description: "same as -t o2, select octal 2-byte units"
    aliases:
      - -o
  - name: flag-s
    type: string
    required: false
    description: "same as -t d2, select decimal 2-byte units"
    aliases:
      - -s
  - name: flag-x
    type: string
    required: false
    description: "same as -t x2, select hexadecimal 2-byte units"
    aliases:
      - -x
execution:
  template: "od -A {address-radix} -j {skip-bytes} -N {read-bytes} -S {strings} -t
    {format}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with address-radix"
    command: "od ${address-radix}"
  - description: "Use address-radix flag"
    command: "od big"
  - description: "Display help message"
    command: "od --help"
phase: enumeration
related_tools:
  - system-file-hexdump
  - system-file-xxd
install:
    - method: apt
      package_name: "coreutils"
      commands:
        - "apt-get install -y coreutils"
---

# od — Dump files in octal and other formats

## Overview

`od` is a command-line utility for dump files in octal and other formats.

## Usage

```
od -A {address-radix} -j {skip-bytes} -N {read-bytes} -S {strings} -t {format}
```
