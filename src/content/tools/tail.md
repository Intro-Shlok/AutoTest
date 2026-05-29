---
id: system-file-tail
namespace: system:file:tail
name: tail
description: Output the last part of files
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.file.tail
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
parameters:
  - name: bytes
    type: string
    required: false
    description: "output the last NUM bytes; or use -c +NUM to output starting with
      byte NUM of each file --debug indicate which --follow implementation is used"
    aliases:
      - -c
      - --bytes
  - name: follow
    type: string
    required: false
    description: "output appended data as the file grows; an absent option argument
      means 'descriptor'"
    aliases:
      - -f
      - --follow
  - name: flag-F
    template_key: flag-f
    type: string
    required: false
    description: "same as --follow=name --retry"
    aliases:
      - -F
  - name: lines
    type: string
    required: false
    description: "output the last NUM lines, instead of the last 10; or use -n +NUM
      to skip NUM-1 lines at the start --max-unchanged-stats=N with --follow=name,
      reopen a FILE which has not changed size after N (defa..."
    aliases:
      - -n
      - --lines
  - name: quiet
    type: string
    required: false
    description: "never output headers giving file names --retry keep trying to open
      a file if it is inaccessible"
    aliases:
      - -q
      - --quiet
      - --silent
  - name: sleep-interval
    type: integer
    required: false
    description: "with -f, sleep for approximately N seconds (default 1.0) between
      iterations; with inotify and --pid=P, check process P at least once every N
      seconds"
    aliases:
      - -s
      - --sleep-interval
  - name: verbose
    type: string
    required: false
    description: "always output headers giving file names"
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
  template: "tail -c {bytes} -f {follow} -F {flag-f} -n {lines} -q {quiet}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with bytes"
    command: "tail ${bytes}"
  - description: "Display help message"
    command: "tail --help"
related_tools:
  - system-file-head
install:
    - method: apt
      package_name: "coreutils"
      commands:
        - "apt-get install -y coreutils"
    - method: brew
      package_name: "coreutils"
      commands:
        - "brew install coreutils"
---

# tail — Output the last part of files

## Overview

`tail` is a command-line utility for output the last part of files.

## Usage

```
tail -c {bytes} -f {follow} -F {flag-f} -n {lines} -q {quiet}
```
