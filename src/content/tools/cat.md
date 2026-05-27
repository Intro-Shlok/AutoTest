---
id: system-file-cat
namespace: system:file:cat
name: cat
description: Concatenate files and print to standard output
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.file.cat
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
  - command-and-control
  - credential-access
  - execution
  - persistence
  - process-manip
parameters:
  - name: show-all
    type: string
    required: false
    description: "equivalent to -vET"
    aliases:
      - -A
      - --show-all
  - name: number-nonblank
    type: string
    required: false
    description: "number nonempty output lines, overrides -n"
    aliases:
      - -b
      - --number-nonblank
  - name: flag-e
    type: string
    required: false
    description: "equivalent to -vE"
    aliases:
      - -e
  - name: show-ends
    type: string
    required: false
    description: "display $ or ^M$ at end of each line"
    aliases:
      - -E
      - --show-ends
  - name: number
    type: string
    required: false
    description: "number all output lines"
    aliases:
      - -n
      - --number
  - name: squeeze-blank
    type: string
    required: false
    description: "suppress repeated empty output lines"
    aliases:
      - -s
      - --squeeze-blank
  - name: flag-t
    type: string
    required: false
    description: "equivalent to -vT"
    aliases:
      - -t
  - name: show-tabs
    type: string
    required: false
    description: "display TAB characters as ^I"
    aliases:
      - -T
      - --show-tabs
  - name: flag-u
    type: string
    required: false
    description: "(ignored)"
    aliases:
      - -u
  - name: show-nonprinting
    type: string
    required: false
    description: "use ^ and M- notation, except for LFD and TAB"
    aliases:
      - -v
      - --show-nonprinting
  - name: help
    type: string
    required: false
    description: "display this help and exit --version output version information
      and exit"
    aliases:
      - --help
execution:
  template: "cat -A {show-all} -b {number-nonblank} -e {flag-e} -E {show-ends} -n
    {number}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with show-all"
    command: "cat ${show-all}"
  - description: "Display help message"
    command: "cat --help"
  - description: POSIX way in which to cat(1); see cat(1posix).
    command: cat -u [FILE_1 [FILE_2] ...]
  - description: Output a file, expanding any escape sequences (default). Using this
      short one-liner let's you view the boot log how it was show at boot-time.
    command: cat /var/log/boot.log
  - description: This is an ever-popular useless use of cat.
    command: cat /etc/passwd | grep '^root'
  - description: 'The sane way:'
    command: grep '^root' /etc/passwd
  - description: If in bash(1), this is often (but not always) a useless use of cat(1).
    command: Buffer=`cat /etc/passwd`
  - description: 'The sane way:'
    command: Buffer=`< /etc/passwd`
related_tools:
  - system-file-comm
  - system-file-sort
  - system-file-uniq
  - system-file-wc
---

# cat — Concatenate files and print to standard output

## Overview

`cat` is a command-line utility for concatenate files and print to standard output.

## Usage

```
cat -A {show-all} -b {number-nonblank} -e {flag-e} -E {show-ends} -n {number}
```
