---
id: system-file-mv
namespace: system:file:mv
name: mv
description: Move/rename files and directories
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.file.mv
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
  - defense-evasion
  - execution
  - persistence
parameters:
  - name: backup
    type: string
    required: false
    description: "make a backup of each existing destination file"
    aliases:
      - --backup
  - name: flag-b
    type: string
    required: false
    description: "like --backup but does not accept an argument --debug explain how
      a file is copied. Implies -v --exchange exchange source and destination"
    aliases:
      - -b
  - name: force
    type: string
    required: false
    description: "do not prompt before overwriting"
    aliases:
      - -f
      - --force
  - name: interactive
    type: string
    required: false
    description: "prompt before overwrite"
    aliases:
      - -i
      - --interactive
  - name: no-clobber
    type: string
    required: false
    description: "do not overwrite an existing file"
    aliases:
      - -n
      - --no-clobber
  - name: no-copy
    type: string
    required: false
    description: "do not copy if renaming fails --strip-trailing-slashes remove any
      trailing slashes from each SOURCE argument"
    aliases:
      - --no-copy
  - name: suffix
    type: string
    required: false
    description: "override the usual backup suffix"
    aliases:
      - -S
      - --suffix
  - name: target-directory
    type: file
    required: false
    description: "move all SOURCE arguments into DIRECTORY"
    aliases:
      - -t
      - --target-directory
  - name: no-target-directory
    type: string
    required: false
    description: "treat DEST as a normal file --update[=UPDATE] control which existing
      files are updated; UPDATE={all,none,none-fail,older(default)}"
    aliases:
      - -T
      - --no-target-directory
    enum:
      - all,none,none-fail,older(default)
  - name: flag-u
    type: string
    required: false
    description: "equivalent to --update[=older]. See below"
    aliases:
      - -u
  - name: verbose
    type: string
    required: false
    description: "explain what is being done"
    aliases:
      - -v
      - --verbose
  - name: context
    type: file
    required: false
    description: "set SELinux security context of destination file to default type
      --help display this help and exit --version output version information and exit"
    aliases:
      - -Z
      - --context
execution:
  template: "mv --backup {backup} -b {flag-b} -f {force} -i {interactive} -n {no-clobber}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with backup"
    command: "mv ${backup}"
  - description: "Display help message"
    command: "mv --help"
related_tools:
  - system-file-cp
  - system-file-rm
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

# mv — Move/rename files and directories

## Overview

`mv` is a command-line utility for move/rename files and directories.

## Usage

```
mv --backup {backup} -b {flag-b} -f {force} -i {interactive} -n {no-clobber}
```
