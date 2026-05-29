---
id: system-file-less
namespace: system:file:less
name: less
description: View file contents page by page
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.file.less
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
  - discovery
  - enumeration
  - execution
  - persistence
  - process-manip
parameters:
  - name: help
    type: string
    required: false
    description: "Display help (from command line)"
    aliases:
      - -?
      - --help
  - name: search-skip-screen
    type: string
    required: false
    description: "Search skips current screen"
    aliases:
      - -a
      - --search-skip-screen
  - name: SEARCH-SKIP-SCREEN
    template_key: search-skip-screen
    type: string
    required: false
    description: "Search starts just after target line"
    aliases:
      - -A
      - --SEARCH-SKIP-SCREEN
  - name: buffers
    type: integer
    required: false
    description: "Number of buffers"
    aliases:
      - -b
      - --buffers
  - name: auto-buffers
    type: string
    required: false
    description: "Don't automatically allocate buffers for pipes"
    aliases:
      - -B
      - --auto-buffers
  - name: clear-screen
    type: string
    required: false
    description: "Repaint by clearing rather than scrolling"
    aliases:
      - -c
      - --clear-screen
  - name: dumb
    type: string
    required: false
    description: "Dumb terminal"
    aliases:
      - -d
      - --dumb
  - name: color
    type: string
    required: false
    description: "Set screen colors"
    aliases:
      - -D
      - --color
  - name: quit-at-eof
    type: string
    required: false
    description: "Quit at end of file"
    aliases:
      - -e
      - -E
      - --quit-at-eof
      - --QUIT-AT-EOF
  - name: force
    type: string
    required: false
    description: "Force open non-regular files"
    aliases:
      - -f
      - --force
  - name: quit-if-one-screen
    type: string
    required: false
    description: "Quit if entire file fits on first screen"
    aliases:
      - -F
      - --quit-if-one-screen
  - name: hilite-search
    type: string
    required: false
    description: "Highlight only last match for searches"
    aliases:
      - -g
      - --hilite-search
  - name: HILITE-SEARCH
    template_key: hilite-search
    type: string
    required: false
    description: "Don't highlight any matches for searches"
    aliases:
      - -G
      - --HILITE-SEARCH
  - name: max-back-scroll
    type: integer
    required: false
    description: "Backward scroll limit"
    aliases:
      - -h
      - --max-back-scroll
  - name: ignore-case
    type: string
    required: false
    description: "Ignore case in searches that do not contain uppercase"
    aliases:
      - -i
      - --ignore-case
  - name: IGNORE-CASE
    template_key: ignore-case
    type: string
    required: false
    description: "Ignore case in all searches"
    aliases:
      - -I
      - --IGNORE-CASE
  - name: jump-target
    type: integer
    required: false
    description: "Screen position of target lines"
    aliases:
      - -j
      - --jump-target
  - name: status-column
    type: string
    required: false
    description: "Display a status column at left edge of screen"
    aliases:
      - -J
      - --status-column
  - name: lesskey-file
    type: string
    required: false
    description: "Use a compiled lesskey file"
    aliases:
      - -k
      - --lesskey-file
  - name: quit-on-intr
    type: string
    required: false
    description: "Exit less in response to ctrl-C"
    aliases:
      - -K
      - --quit-on-intr
  - name: no-lessopen
    type: string
    required: false
    description: "Ignore the LESSOPEN environment variable"
    aliases:
      - -L
      - --no-lessopen
  - name: long-prompt
    type: string
    required: false
    description: "Set prompt style"
    aliases:
      - -m
      - -M
      - --long-prompt
      - --LONG-PROMPT
  - name: line-numbers
    type: string
    required: false
    description: "Suppress line numbers in prompts and messages"
    aliases:
      - -n
      - --line-numbers
  - name: LINE-NUMBERS
    template_key: line-numbers
    type: string
    required: false
    description: "Display line number at start of each line"
    aliases:
      - -N
      - --LINE-NUMBERS
  - name: log-file
    type: file
    required: false
    description: "Copy to log file (standard input only)"
    aliases:
      - -o
      - --log-file
  - name: LOG-FILE
    template_key: log-file
    type: file
    required: false
    description: "Copy to log file (unconditionally overwrite)"
    aliases:
      - -O
      - --LOG-FILE
  - name: pattern
    type: string
    required: false
    description: "Start at pattern (from command line)"
    aliases:
      - -p
      - --pattern
  - name: flag-P
    template_key: flag-p
    type: string
    required: false
    description: "--prompt=[prompt]"
    aliases:
      - -P
  - name: quiet
    type: string
    required: false
    description: "Quiet the terminal bell"
    aliases:
      - -q
      - -Q
      - --quiet
      - --QUIET
      - --silent
      - --SILENT
  - name: raw-control-chars
    type: string
    required: false
    description: "Output \"raw\" control characters"
    aliases:
      - -r
      - -R
      - --raw-control-chars
      - --RAW-CONTROL-CHARS
execution:
  template: "less -? {help} -a {search-skip-screen} -A {search-skip-screen} -b {buffers}
    -B {auto-buffers}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with help"
    command: "less ${help}"
  - description: "Display help message"
    command: "less --help"
install:
    - method: apt
      package_name: "less"
      commands:
        - "apt-get install -y less"
---

# less — View file contents page by page

## Overview

`less` is a command-line utility for view file contents page by page.

## Usage

```
less -? {help} -a {search-skip-screen} -A {search-skip-screen} -b {buffers} -B {auto-buffers}
```
