---
id: system-file-file
namespace: system:file:file
name: file
description: Determine file type
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.file.delete
  - system.file.file
  - system.file.search
  - system.file.process
  - system.file.copy
  - system.file.move
  - system.file.read
platforms:
  - linux
risk_level: low
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
features:
  - file-system
  - local
  - output-json
techniques:
  - collection
  - data-manipulation
  - command-and-control
  - credential-access
  - defense-evasion
  - discovery
  - enumeration
  - execution
  - exfiltration
  - lateral-movement
  - persistence
  - privilege-escalation
  - process-manip
parameters:
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
      - -v
      - --version
  - name: magic-file LIST
    template_key: magic-file-list
    type: array
    required: false
    description: "use LIST as a colon-separated list of magic"
    aliases:
      - -m
      - --magic-file LIST
  - name: uncompress
    type: string
    required: false
    description: "try to look inside compressed files"
    aliases:
      - -z
      - --uncompress
  - name: uncompress-noreport
    type: string
    required: false
    description: "Set the uncompress-noreport parameter"
    aliases:
      - -Z
      - --uncompress-noreport
  - name: brief
    type: file
    required: false
    description: "do not prepend filenames to output lines"
    aliases:
      - -b
      - --brief
  - name: checking-printout
    type: string
    required: false
    description: "print the parsed form of the magic file, use in"
    aliases:
      - -c
      - --checking-printout
  - name: exclude TEST
    template_key: exclude-test
    type: array
    required: false
    description: "exclude TEST from the list of test to be"
    aliases:
      - -e
      - --exclude TEST
  - name: exclude-quiet TEST
    template_key: exclude-quiet-test
    type: string
    required: false
    description: "like exclude, but ignore unknown tests"
    aliases:
      - --exclude-quiet TEST
  - name: files-from FILE
    template_key: files-from-file
    type: file
    required: false
    description: "read the filenames to be examined from FILE"
    aliases:
      - -f
      - --files-from FILE
  - name: separator STRING
    template_key: separator-string
    type: string
    required: false
    description: "use string as separator instead of `:'"
    aliases:
      - -F
      - --separator STRING
  - name: mime
    type: string
    required: false
    description: "output MIME type strings (--mime-type and"
    aliases:
      - -i
      - --mime
  - name: mime-encoding
    type: array
    required: false
    description: "--apple output the Apple CREATOR/TYPE --extension output a slash-separated
      list of extensions --mime-type output the MIME type --mime-encoding output the
      MIME encoding"
    aliases:
      - --mime-encoding
  - name: keep-going
    type: string
    required: false
    description: "don't stop at the first match"
    aliases:
      - -k
      - --keep-going
  - name: list
    type: string
    required: false
    description: "list magic strength"
    aliases:
      - -l
      - --list
  - name: dereference
    type: string
    required: false
    description: "follow symlinks (default if POSIXLY_CORRECT is set)"
    aliases:
      - -L
      - --dereference
  - name: no-dereference
    type: string
    required: false
    description: "don't follow symlinks (default if POSIXLY_CORRECT is not set) (default)"
    aliases:
      - -h
      - --no-dereference
  - name: no-buffer
    type: string
    required: false
    description: "do not buffer output"
    aliases:
      - -n
      - --no-buffer
  - name: no-pad
    type: string
    required: false
    description: "do not pad output"
    aliases:
      - -N
      - --no-pad
  - name: print0
    type: file
    required: false
    description: "terminate filenames with ASCII NUL"
    aliases:
      - "-0"
      - --print0
  - name: preserve-date
    type: string
    required: false
    description: "preserve access times on files"
    aliases:
      - -p
      - --preserve-date
  - name: parameter
    type: string
    required: false
    description: "set file engine parameter limits"
    aliases:
      - -P
      - --parameter
  - name: raw
    type: string
    required: false
    description: "don't translate unprintable chars to \\ooo"
    aliases:
      - -r
      - --raw
  - name: special-files
    type: string
    required: false
    description: "treat special (block/char devices) files as"
    aliases:
      - -s
      - --special-files
  - name: no-sandbox
    type: string
    required: false
    description: "disable system call sandboxing"
    aliases:
      - -S
      - --no-sandbox
  - name: compile
    type: string
    required: false
    description: "compile file specified by -m"
    aliases:
      - -C
      - --compile
  - name: debug
    type: string
    required: false
    description: "print debugging messages"
    aliases:
      - -d
      - --debug
execution:
  template: "file --help {help} -v {version} -m {magic-file-list} -z {uncompress}
    -Z {uncompress-noreport}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with help"
    command: "file ${help}"
  - description: "Display help message"
    command: "file --help"
  - description: "Read an arbitrary file by specifying it as a magic file. This will\n
      result in errors containing the lines of the file. The argument parsing\ndone
      by file also means this can be specified as a single argument.\n"
    command: "file -m/etc/passwd\n"
  - description: "Argument injection: read local file: Read an arbitrary file by specifying
      it as a magic file. This will\nresult in errors containing the lines of the
      file. The argument parsing\ndone by file also means this can be specified as
      a single argument.\n"
    command: file -m/etc/passwd
phase: enumeration
---

# file — Determine file type

## Overview

`file` is a command-line utility for determine file type.

## Usage

```
file --help {help} -v {version} -m {magic-file-list} -z {uncompress} -Z {uncompress-noreport}
```
