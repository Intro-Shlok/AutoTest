---
id: system-file-stat
namespace: system:file:stat
name: stat
description: Display file or filesystem status
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.file.stat
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
  - name: dereference
    type: string
    required: false
    description: "follow links"
    aliases:
      - -L
      - --dereference
  - name: file-system
    type: string
    required: false
    description: "display file system status instead of file status --cached=MODE
      specify how to use cached attributes; useful on remote file systems. See MODE
      below"
    aliases:
      - -f
      - --file-system
  - name: format
    type: string
    required: false
    description: "use the specified FORMAT instead of the default; output a newline
      after each use of FORMAT --printf=FORMAT like --format, but interpret backslash
      escapes, and do not output a mandatory trailing new..."
    aliases:
      - -c
      - --format
  - name: terse
    type: string
    required: false
    description: "print the information in terse form --help display this help and
      exit --version output version information and exit"
    aliases:
      - -t
      - --terse
  - name: terse-2
    type: string
    required: false
    description: "Set the terse-2 parameter"
    aliases:
      - --terse
  - name: terse-3
    type: string
    required: false
    description: "Set the terse-3 parameter"
    aliases:
      - --terse
      - --file-system
execution:
  template: "stat -L {dereference} -f {file-system} -c {format} -t {terse} --terse
    {terse-2}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with dereference"
    command: "stat ${dereference}"
  - description: "Display help message"
    command: "stat --help"
  - description: display numerical values for file permissions
    command: stat -c '%a %n' *
  - description: Display only the octal permissions for the given directory. Great
      for tests.
    command: stat --format='%a' /boot
phase: enumeration
---

# stat — Display file or filesystem status

## Overview

`stat` is a command-line utility for display file or filesystem status.

## Usage

```
stat -L {dereference} -f {file-system} -c {format} -t {terse} --terse {terse-2}
```
