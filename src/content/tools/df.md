---
id: system-storage-df
namespace: system:storage:df
name: df
description: Report filesystem disk space usage
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.storage.df
  - system.storage.usage
  - system.storage.mount
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
techniques:
  - discovery
parameters:
  - name: all
    type: string
    required: false
    description: "include pseudo, duplicate, inaccessible file systems"
    aliases:
      - -a
      - --all
  - name: block-size
    type: integer
    required: false
    description: "scale sizes by SIZE before printing them; see SIZE format below;
      E.g., '-BM' prints sizes in units of 1,048,576 bytes"
    aliases:
      - -B
      - --block-size
  - name: human-readable
    type: string
    required: false
    description: "print sizes in powers of 1024 (e.g., 1023M)"
    aliases:
      - -h
      - --human-readable
  - name: si
    type: string
    required: false
    description: "print sizes in powers of 1000 (e.g., 1.1G)"
    aliases:
      - -H
      - --si
  - name: inodes
    type: string
    required: false
    description: "list inode information instead of block usage"
    aliases:
      - -i
      - --inodes
  - name: flag-k
    type: string
    required: false
    description: "like --block-size=1K"
    aliases:
      - -k
  - name: local
    type: string
    required: false
    description: "limit listing to local file systems --no-sync do not invoke sync
      before getting usage info (default) --output[=FIELD_LIST] use the output format
      defined by FIELD_LIST, or print all fields if FIELD_..."
    aliases:
      - -l
      - --local
  - name: portability
    type: string
    required: false
    description: "use the POSIX output format --sync invoke sync before getting usage
      info --total elide all entries insignificant to available space, and produce
      a grand total"
    aliases:
      - -P
      - --portability
  - name: type
    type: string
    required: false
    description: "limit listing to file systems of type TYPE"
    aliases:
      - -t
      - --type
  - name: print-type
    type: string
    required: false
    description: "print file system type"
    aliases:
      - -T
      - --print-type
  - name: exclude-type
    type: string
    required: false
    description: "limit listing to file systems not of type TYPE"
    aliases:
      - -x
      - --exclude-type
  - name: flag-v
    type: string
    required: false
    description: "(ignored) --help display this help and exit --version output version
      information and exit"
    aliases:
      - -v
execution:
  template: "df -a {all} -B {block-size} -h {human-readable} -H {si} -i {inodes}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with all"
    command: "df ${all}"
  - description: "Display help message"
    command: "df --help"
  - description: Print free disk space in a [h]uman-readable format.
    command: df -h
  - description: Free disk space for [t]ype EXT2 file systems.
    command: df -t ext2
  - description: Free disk space for filesystems, e[x]cluding EXT2.
    command: df -x ext2
  - description: Show [i]node usage.
    command: df -i
  - description: Show information about a distinct filesystem path.
    command: df [PATH]
  - description: List [a]ll filesystems, + unreadable, duplicates, pseudo, and inaccessible.
    command: df -a
  - description: Fetch a grand total of disk usage.
    command: df --total
related_tools:
  - system-storage-du
---

# df — Report filesystem disk space usage

## Overview

`df` is a command-line utility for report filesystem disk space usage.

## Usage

```
df -a {all} -B {block-size} -h {human-readable} -H {si} -i {inodes}
```
