---
id: system-file-md5sum
namespace: system:file:md5sum
name: md5sum
description: Compute and check MD5 message digest
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.file.md5sum
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
  - name: binary
    type: string
    required: false
    description: "read in binary mode"
    aliases:
      - -b
      - --binary
  - name: check
    type: string
    required: false
    description: "read checksums from the FILEs and check them --tag create a BSD-style
      checksum"
    aliases:
      - -c
      - --check
  - name: text
    type: string
    required: false
    description: "read in text mode (default)"
    aliases:
      - -t
      - --text
  - name: zero
    type: string
    required: false
    description: "end each output line with NUL, not newline, and disable file name
      escaping"
    aliases:
      - -z
      - --zero
  - name: ignore-missing
    type: string
    required: false
    description: "don't fail or report status for missing files --quiet don't print
      OK for each successfully verified file --status don't output anything, status
      code shows success --strict exit non-zero for imprope..."
    aliases:
      - --ignore-missing
  - name: warn
    type: string
    required: false
    description: "warn about improperly formatted checksum lines --help display this
      help and exit --version output version information and exit"
    aliases:
      - -w
      - --warn
execution:
  template: "md5sum -b {binary} -c {check} -t {text} -z {zero} --ignore-missing {ignore-missing}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with binary"
    command: "md5sum ${binary}"
  - description: "Display help message"
    command: "md5sum --help"
related_tools:
  - system-file-sha1sum
  - system-file-sha256sum
install:
    - method: apt
      package_name: "coreutils"
      commands:
        - "apt-get install -y coreutils"
---

# md5sum — Compute and check MD5 message digest

## Overview

`md5sum` is a command-line utility for compute and check md5 message digest.

## Usage

```
md5sum -b {binary} -c {check} -t {text} -z {zero} --ignore-missing {ignore-missing}
```
