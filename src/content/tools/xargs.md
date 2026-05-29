---
id: system-file-xargs
namespace: system:file:xargs
name: xargs
description: Build and execute command lines from standard input
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.file.xargs
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
  - name: "null"
    type: string
    required: false
    description: "items are separated by a null, not whitespace"
    aliases:
      - "-0"
      - --null
  - name: arg-file
    type: file
    required: false
    description: "read arguments from FILE, not standard input"
    aliases:
      - -a
      - --arg-file
  - name: delimiter
    type: string
    required: false
    description: "items in input stream are separated by CHARACTER"
    aliases:
      - -d
      - --delimiter
  - name: flag-E
    template_key: flag-e
    type: string
    required: false
    description: "set logical EOF string; if END occurs as a line"
    aliases:
      - -E
  - name: eof
    type: string
    required: false
    description: "equivalent to -E END if END is specified"
    aliases:
      - -e
      - --eof
  - name: flag-I
    template_key: flag-i
    type: string
    required: false
    description: "same as --replace=R"
    aliases:
      - -I
  - name: replace
    type: string
    required: false
    description: "replace R in INITIAL-ARGS with names read"
    aliases:
      - -i
      - --replace
  - name: max-lines
    type: integer
    required: false
    description: "use at most MAX-LINES non-blank input lines per"
    aliases:
      - -L
      - -L
      - --max-lines
  - name: flag-l
    type: string
    required: false
    description: "similar to -L but defaults to at most one non-"
    aliases:
      - -l
      - -L
  - name: max-args
    type: integer
    required: false
    description: "use at most MAX-ARGS arguments per command line"
    aliases:
      - -n
      - -A
      - --max-args
  - name: open-tty
    type: string
    required: false
    description: "Reopen stdin as /dev/tty in the child process"
    aliases:
      - -o
      - --open-tty
  - name: max-procs
    type: integer
    required: false
    description: "run at most MAX-PROCS processes at a time"
    aliases:
      - -P
      - -P
      - --max-procs
  - name: interactive
    type: string
    required: false
    description: "prompt before running commands"
    aliases:
      - -p
      - --interactive
  - name: process-slot-var
    type: string
    required: false
    description: "set environment variable VAR in child processes"
    aliases:
      - --process-slot-var
  - name: no-run-if-empty
    type: string
    required: false
    description: "if there are no arguments, then do not run COMMAND"
    aliases:
      - -r
      - --no-run-if-empty
  - name: max-chars
    type: integer
    required: false
    description: "limit length of command line to MAX-CHARS"
    aliases:
      - -s
      - -C
      - --max-chars
  - name: show-limits
    type: string
    required: false
    description: "show limits on command-line length"
    aliases:
      - --show-limits
  - name: verbose
    type: string
    required: false
    description: "print commands before executing them"
    aliases:
      - -t
      - --verbose
  - name: exit
    type: string
    required: false
    description: "exit if the size (see -s) is exceeded"
    aliases:
      - -x
      - --exit
  - name: help
    type: string
    required: false
    description: "display this help and exit"
    aliases:
      - --help
  - name: version
    type: string
    required: false
    description: "output version information and exit"
    aliases:
      - --version
execution:
  template: "xargs -0 {null} -a {arg-file} -d {delimiter} -E {flag-e} -e {eof}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with null"
    command: "xargs ${null}"
  - description: "Display help message"
    command: "xargs --help"
  - description: Find all file names ending with .pdf, then remove them.
    command: find -name \*.pdf | xargs rm
  - description: 'The above, however, is better-written without xargs:'
    command: find -name \*.pdf -exec rm {} \+
  - description: Although it's best to use find's own functionality, in this situation.
    command: find -name \*.pdf -delete
  - description: Find all file names ending with '.pdf' and remove them. This approach
      also handles filenames with '\n' and skips '*.pdf' directories. The xargs(1)
      flag `-r` is equivalent to `--no-run-if-empty`, and the use of `-n` will in
      this case group execution by 10 files.
    command: find -name \*.pdf -type f -print0 | xargs -0 -r -n 10 rm
  - description: If file names may contains spaces, you can use the xargs(1) flag
      `-I` and its proceeding argument to specify the filename placeholder, as in
      find(1)'s use of `{}` in `-exec`. Although find(1)'s `{}` needs not be cuddled
      by quotes, - xargs(1) does.
    command: find -name \*.pdf | xargs -I {} rm -r '{}'
  - description: Print a list of files in the format of `*FILE=`. The use of xargs(1)
      flag `-n` here with its argument of `1` means to process the files one-by-one.
    command: find -name \*.pdf | xargs -I {} -n 1 echo '&{}='
  - description: The above is, however, much faster, more efficient, and easier without
      xargs.
    command: find -name \*.pdf -printf '&%f=\n'
  - description: Group words by three in a string.
    command: seq 1 10 | xargs -n 3
  - description: Alternatively, and more efficiently, use Bash brace expansion, if
      available.
    command: printf '%d ' {1..10} | xargs -n 3
related_tools:
  - system-file-find
install:
    - method: apt
      package_name: "findutils"
      commands:
        - "apt-get install -y findutils"
    - method: brew
      package_name: "findutils"
      commands:
        - "brew install findutils"
---

# xargs — Build and execute command lines from standard input

## Overview

`xargs` is a command-line utility for build and execute command lines from standard input.

## Usage

```
xargs -0 {null} -a {arg-file} -d {delimiter} -E {flag-e} -e {eof}
```
