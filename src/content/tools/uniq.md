---
id: system-file-uniq
namespace: system:file:uniq
name: uniq
description: Report or omit repeated lines
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.file.uniq
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
  - name: count
    type: integer
    required: false
    description: "prefix lines by the number of occurrences"
    aliases:
      - -c
      - --count
  - name: repeated
    type: string
    required: false
    description: "only print duplicate lines, one for each group"
    aliases:
      - -d
      - --repeated
  - name: flag-D
    template_key: flag-d
    type: string
    required: false
    description: "print all duplicate lines --all-repeated[=METHOD] like -D, but allow
      separating groups with an empty line; METHOD={none(default),prepend,separate}"
    aliases:
      - -D
    enum:
      - none(default),prepend,separate
  - name: skip-fields
    type: integer
    required: false
    description: "avoid comparing the first N fields --group[=METHOD] show all items,
      separating groups with an empty line; METHOD={separate(default),prepend,append,both}"
    aliases:
      - -f
      - --skip-fields
    enum:
      - separate(default),prepend,append,both
  - name: ignore-case
    type: string
    required: false
    description: "ignore differences in case when comparing"
    aliases:
      - -i
      - --ignore-case
  - name: skip-chars
    type: integer
    required: false
    description: "avoid comparing the first N characters"
    aliases:
      - -s
      - --skip-chars
  - name: unique
    type: string
    required: false
    description: "only print unique lines"
    aliases:
      - -u
      - --unique
  - name: zero-terminated
    type: string
    required: false
    description: "line delimiter is NUL, not newline"
    aliases:
      - -z
      - --zero-terminated
  - name: check-chars
    type: integer
    required: false
    description: "compare no more than N characters in lines --help display this help
      and exit --version output version information and exit"
    aliases:
      - -w
      - --check-chars
execution:
  template: "uniq -c {count} -d {repeated} -D {flag-d} -f {skip-fields} -i {ignore-case}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Display help message"
    command: "uniq --help"
related_tools:
  - system-file-cat
  - system-file-comm
  - system-file-sort
  - system-file-wc
---

# uniq — Report or omit repeated lines

## Overview

`uniq` is a command-line utility for report or omit repeated lines.

## Usage

```
uniq -c {count} -d {repeated} -D {flag-d} -f {skip-fields} -i {ignore-case}
```
