---
id: system-file-chown
namespace: system:file:chown
name: chown
description: Change file owner and group
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.file.chown
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
  - name: changes
    type: string
    required: false
    description: "like verbose but report only when a change is made"
    aliases:
      - -c
      - --changes
  - name: silent
    type: string
    required: false
    description: "suppress most error messages"
    aliases:
      - -f
      - --silent
      - --quiet
  - name: verbose
    type: string
    required: false
    description: "output a diagnostic for every file processed --dereference affect
      the referent of each symbolic link (this is the default), rather than the symbolic
      link itself"
    aliases:
      - -v
      - --verbose
  - name: no-dereference
    type: string
    required: false
    description: "affect symbolic links instead of any referenced file; useful only
      on systems that can change the ownership of a symlink --from=CURRENT_OWNER:CURRENT_GROUP
      change the ownership of each file only if ..."
    aliases:
      - -h
      - --no-dereference
  - name: recursive
    type: string
    required: false
    description: "operate on files and directories recursively"
    aliases:
      - -R
      - --recursive
  - name: flag-H
    template_key: flag-h
    type: file
    required: false
    description: "if a command line argument is a symlink to a directory, traverse
      it"
    aliases:
      - -H
  - name: flag-L
    template_key: flag-l
    type: file
    required: false
    description: "traverse every symbolic link to a directory encountered"
    aliases:
      - -L
  - name: flag-P
    template_key: flag-p
    type: string
    required: false
    description: "do not traverse any symbolic links"
    aliases:
      - -P
  - name: help
    type: string
    required: false
    description: "display this help and exit --version output version information
      and exit"
    aliases:
      - --help
execution:
  template: "chown -c {changes} -f {silent} -v {verbose} -h {no-dereference} -R {recursive}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with changes"
    command: "chown ${changes}"
  - description: "Display help message"
    command: "chown --help"
related_tools:
  - system-file-chmod
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

# chown — Change file owner and group

## Overview

`chown` is a command-line utility for change file owner and group.

## Usage

```
chown -c {changes} -f {silent} -v {verbose} -h {no-dereference} -R {recursive}
```
