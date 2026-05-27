---
id: system-file-xxd
namespace: system:file:xxd
name: xxd
description: Hex dump or reverse hex dump
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.file.xxd
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
  - collection
  - data-manipulation
parameters:
  - name: flag-a
    type: string
    required: false
    description: "toggle autoskip: A single '*' replaces nul-lines. Default off"
    aliases:
      - -a
  - name: flag-b
    type: string
    required: false
    description: "binary digit dump (incompatible with -ps). Default hex"
    aliases:
      - -b
  - name: flag-c
    type: string
    required: false
    description: "format <cols> octets per line. Default 16 (-i: 12, -ps: 30)"
    aliases:
      - -c
  - name: flag-e
    type: string
    required: false
    description: "little-endian dump (incompatible with -ps,-i,-r)"
    aliases:
      - -e
  - name: flag-g
    type: integer
    required: false
    description: "number of octets per group in normal output. Default 2 (-e: 4)"
    aliases:
      - -g
  - name: flag-h
    type: string
    required: false
    description: "print this summary"
    aliases:
      - -h
  - name: flag-i
    type: string
    required: false
    description: "output in C include file style"
    aliases:
      - -i
  - name: flag-t
    type: string
    required: false
    description: "append terminating zero to C include output (-i)"
    aliases:
      - -t
  - name: flag-l
    type: string
    required: false
    description: "stop after <len> octets"
    aliases:
      - -l
  - name: flag-n
    type: string
    required: false
    description: "set the variable name used in C include output (-i)"
    aliases:
      - -n
  - name: flag-o
    type: string
    required: false
    description: "add <off> to the displayed file position"
    aliases:
      - -o
  - name: flag-p
    type: string
    required: false
    description: "output in postscript plain hexdump style"
    aliases:
      - -p
  - name: flag-r
    type: string
    required: false
    description: "reverse operation: convert (or patch) hexdump into binary"
    aliases:
      - -r
  - name: flag-r-2
    type: string
    required: false
    description: "revert with <off> added to file positions found in hexdump"
    aliases:
      - -r
      - -s
  - name: flag-d
    type: string
    required: false
    description: "show offset in decimal instead of hex"
    aliases:
      - -d
  - name: flag-s
    type: string
    required: false
    description: "Set the flag-s parameter"
    aliases:
      - -s
  - name: flag-u
    type: string
    required: false
    description: "use upper case hex letters"
    aliases:
      - -u
  - name: flag-R
    template_key: flag-r
    type: string
    required: false
    default_value: "auto"
    description: "colorize the output; <when> can be 'always', 'auto' or 'never'"
    aliases:
      - -R
  - name: flag-v
    type: string
    required: false
    description: "show version: \"xxd 2026-03-19 by Juergen Weigert et al.\""
    aliases:
      - -v
execution:
  template: "xxd -a {flag-a} -b {flag-b} -c {flag-c} -e {flag-e} -g {flag-g}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with flag-a"
    command: "xxd ${flag-a}"
  - description: "Display help message"
    command: "xxd --help"
related_tools:
  - system-file-hexdump
  - system-file-od
---

# xxd — Hex dump or reverse hex dump

## Overview

`xxd` is a command-line utility for hex dump or reverse hex dump.

## Usage

```
xxd -a {flag-a} -b {flag-b} -c {flag-c} -e {flag-e} -g {flag-g}
```
