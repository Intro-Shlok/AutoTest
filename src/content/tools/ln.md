---
id: system-file-ln
namespace: system:file:ln
name: ln
description: Create hard and symbolic links
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.file.ln
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
  - name: backup
    type: string
    required: false
    description: "make a backup of each existing destination file"
    aliases:
      - --backup
  - name: flag-b
    type: string
    required: false
    description: "like --backup but does not accept an argument"
    aliases:
      - -b
  - name: directory
    type: string
    required: false
    description: "allow the superuser to attempt to hard link directories, if supported
      by the system"
    aliases:
      - -d
      - -F
      - --directory
  - name: force
    type: string
    required: false
    description: "remove existing destination files"
    aliases:
      - -f
      - --force
  - name: interactive
    type: string
    required: false
    description: "prompt whether to remove destinations"
    aliases:
      - -i
      - --interactive
  - name: logical
    type: string
    required: false
    description: "dereference TARGETs that are symbolic links"
    aliases:
      - -L
      - --logical
  - name: no-dereference
    type: file
    required: false
    description: "treat LINK_NAME as a normal file if it is a symbolic link to a directory"
    aliases:
      - -n
      - --no-dereference
  - name: physical
    type: string
    required: false
    description: "make hard links directly to symbolic links"
    aliases:
      - -P
      - --physical
  - name: relative
    type: string
    required: false
    description: "with -s, create links relative to link location"
    aliases:
      - -r
      - --relative
  - name: symbolic
    type: string
    required: false
    description: "make symbolic links instead of hard links"
    aliases:
      - -s
      - --symbolic
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
    description: "specify the DIRECTORY in which to create the links"
    aliases:
      - -t
      - --target-directory
  - name: no-target-directory
    type: string
    required: false
    description: "treat LINK_NAME as a normal file always"
    aliases:
      - -T
      - --no-target-directory
  - name: verbose
    type: string
    required: false
    description: "print name of each linked file --help display this help and exit
      --version output version information and exit"
    aliases:
      - -v
      - --verbose
execution:
  template: "ln --backup {backup} -b {flag-b} -d {directory} -f {force} -i {interactive}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with backup"
    command: "ln ${backup}"
  - description: "Display help message"
    command: "ln --help"
phase: enumeration
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

# ln — Create hard and symbolic links

## Overview

`ln` is a command-line utility for create hard and symbolic links.

## Usage

```
ln --backup {backup} -b {flag-b} -d {directory} -f {force} -i {interactive}
```
