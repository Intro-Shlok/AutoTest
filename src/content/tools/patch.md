---
id: system-file-patch
namespace: system:file:patch
name: patch
description: Apply diff patches to files
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.file.patch
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
  - process-manip
parameters:
  - name: strip
    type: integer
    required: false
    description: "Set the strip parameter"
    aliases:
      - -p
      - --strip
  - name: fuzz LINES
    template_key: fuzz-lines
    type: string
    required: false
    description: "Set the fuzz LINES parameter"
    aliases:
      - -F
      - --fuzz LINES
  - name: ignore-whitespace
    type: string
    required: false
    description: "Set the ignore-whitespace parameter"
    aliases:
      - -l
      - --ignore-whitespace
  - name: context
    type: string
    required: false
    description: "Set the context parameter"
    aliases:
      - -c
      - --context
  - name: ed
    type: string
    required: false
    description: "Set the ed parameter"
    aliases:
      - -e
      - --ed
  - name: normal
    type: string
    required: false
    description: "Set the normal parameter"
    aliases:
      - -n
      - --normal
  - name: unified
    type: string
    required: false
    description: "Set the unified parameter"
    aliases:
      - -u
      - --unified
  - name: forward
    type: string
    required: false
    description: "Set the forward parameter"
    aliases:
      - -N
      - --forward
  - name: reverse
    type: string
    required: false
    description: "Set the reverse parameter"
    aliases:
      - -R
      - --reverse
  - name: input
    type: string
    required: false
    description: "Set the input parameter"
    aliases:
      - -i
      - --input
  - name: output
    type: file
    required: false
    description: "Set the output parameter"
    aliases:
      - -o
      - --output
  - name: reject-file
    type: file
    required: false
    description: "Set the reject-file parameter"
    aliases:
      - -r
      - --reject-file
  - name: ifdef
    type: string
    required: false
    description: "Set the ifdef parameter"
    aliases:
      - -D
      - -t
      - -e
      - --ifdef
  - name: merge
    type: string
    required: false
    description: "Set the merge parameter"
    aliases:
      - --merge
  - name: remove-empty-files
    type: string
    required: false
    description: "Set the remove-empty-files parameter"
    aliases:
      - -E
      - --remove-empty-files
  - name: set-utc
    type: string
    required: false
    description: "Set the set-utc parameter"
    aliases:
      - -Z
      - --set-utc
  - name: set-time
    type: string
    required: false
    description: "Set the set-time parameter"
    aliases:
      - -T
      - --set-time
  - name: quoting-style
    type: file
    required: false
    description: "output file names using quoting style WORD"
    aliases:
      - --quoting-style
  - name: backup
    type: string
    required: false
    description: "Set the backup parameter"
    aliases:
      - -b
      - --backup
  - name: backup-if-mismatch
    type: string
    required: false
    description: "Set the backup-if-mismatch parameter"
    aliases:
      - --backup-if-mismatch
  - name: no-backup-if-mismatch
    type: string
    required: false
    description: "Set the no-backup-if-mismatch parameter"
    aliases:
      - --no-backup-if-mismatch
  - name: version-control
    type: string
    required: false
    description: "STYLE is either 'simple', 'numbered', or 'existing'"
    aliases:
      - -V
      - --version-control
  - name: prefix
    type: string
    required: false
    description: "Set the prefix parameter"
    aliases:
      - -B
      - --prefix
  - name: basename-prefix
    type: string
    required: false
    description: "Set the basename-prefix parameter"
    aliases:
      - -Y
      - --basename-prefix
  - name: suffix
    type: string
    required: false
    description: "Set the suffix parameter"
    aliases:
      - -z
      - --suffix
  - name: get
    type: integer
    required: false
    description: "Set the get parameter"
    aliases:
      - -g
      - --get
  - name: batch
    type: string
    required: false
    description: "Set the batch parameter"
    aliases:
      - -t
      - -P
      - --batch
  - name: force
    type: string
    required: false
    description: "Set the force parameter"
    aliases:
      - -f
      - -t
      - -P
      - --force
  - name: quiet
    type: string
    required: false
    description: "Set the quiet parameter"
    aliases:
      - -s
      - --quiet
      - --silent
  - name: verbose
    type: string
    required: false
    description: "Set the verbose parameter"
    aliases:
      - --verbose
execution:
  template: "patch -p {strip} -F {fuzz-lines} -l {ignore-whitespace} -c {context}
    -e {ed}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Display help message"
    command: "patch --help"
related_tools:
  - system-file-diff
install:
    - method: apt
      package_name: "patch"
      commands:
        - "apt-get install -y patch"
---

# patch — Apply diff patches to files

## Overview

`patch` is a command-line utility for apply diff patches to files.

## Usage

```
patch -p {strip} -F {fuzz-lines} -l {ignore-whitespace} -c {context} -e {ed}
```
