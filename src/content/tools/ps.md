---
id: system-process-ps
namespace: system:process:ps
name: ps
description: Report process status
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.process.ps
  - system.process.list
  - system.process.signal
  - system.process.monitor
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
  - process-manip
techniques:
  - execution
  - impact
  - process-discovery
  - discovery
  - command-and-control
  - credential-access
  - defense-evasion
  - enumeration
  - exfiltration
  - lateral-movement
  - persistence
  - process-manip
parameters:
  - name: flag-A
    template_key: flag-a
    type: string
    required: false
    description: "all processes"
    aliases:
      - -A
      - -e
  - name: flag-a
    type: string
    required: false
    description: "all with tty, except session leaders"
    aliases:
      - -a
  - name: flag-d
    type: string
    required: false
    description: "all except session leaders"
    aliases:
      - -d
  - name: deselect
    type: string
    required: false
    description: "negate selection"
    aliases:
      - -N
      - --deselect
  - name: flag-C
    template_key: flag-c
    type: string
    required: false
    description: "command name"
    aliases:
      - -C
  - name: Group
    template_key: group
    type: string
    required: false
    description: "real group id or name"
    aliases:
      - -G
      - --Group <GID>
  - name: group
    type: string
    required: false
    description: "Set the group parameter"
    aliases:
      - -g
      - --group <group>
  - name: pid
    type: string
    required: false
    description: "process id"
    aliases:
      - -p
      - --pid <PID>
  - name: ppid
    type: string
    required: false
    description: "Set the ppid parameter"
    aliases:
      - --ppid <PID>
  - name: quick-pid
    type: string
    required: false
    description: "process id (quick mode)"
    aliases:
      - -q
      - --quick-pid <PID>
  - name: sid
    type: string
    required: false
    description: "Set the sid parameter"
    aliases:
      - -s
      - --sid <session>
  - name: tty
    type: string
    required: false
    description: "terminal"
    aliases:
      - -t
      - --tty <tty>
  - name: user
    type: string
    required: false
    description: "Set the user parameter"
    aliases:
      - -u
      - --user <UID>
  - name: User
    template_key: user
    type: string
    required: false
    description: "real user id or name"
    aliases:
      - -U
      - --User <UID>
  - name: flag-D
    template_key: flag-d
    type: string
    required: false
    description: "date format for lstart"
    aliases:
      - -D
  - name: flag-f
    type: string
    required: false
    description: "full-format, including command lines"
    aliases:
      - -f
  - name: flag-j
    type: string
    required: false
    description: "jobs format"
    aliases:
      - -j
  - name: flag-l
    type: string
    required: false
    description: "long format"
    aliases:
      - -l
  - name: flag-M
    template_key: flag-m
    type: string
    required: false
    description: "add security data (for SELinux)"
    aliases:
      - -M
  - name: flag-O
    template_key: flag-o
    type: string
    required: false
    description: "preloaded with default columns"
    aliases:
      - -O
  - name: format
    type: string
    required: false
    description: "user-defined format"
    aliases:
      - -o
      - --format <format>
  - name: flag-y
    type: string
    required: false
    description: "do not show flags, show rss vs. addr (used with -l)"
    aliases:
      - -y
  - name: context
    type: string
    required: false
    description: "display security context (for SELinux)"
    aliases:
      - --context
  - name: headers
    type: string
    required: false
    description: "repeat header lines, one per page"
    aliases:
      - --headers
  - name: no-headers
    type: string
    required: false
    description: "do not print header at all"
    aliases:
      - --no-headers
  - name: cols
    type: integer
    required: false
    description: "set screen width --rows, --lines <num> set screen height --signames
      display signal masks using signal names"
    aliases:
      - --cols
      - --columns
      - --width <num>
  - name: flag-m
    type: string
    required: false
    description: "after processes"
    aliases:
      - -m
  - name: flag-c
    type: string
    required: false
    description: "show scheduling class with -l option"
    aliases:
      - -c
  - name: flag-y-2
    type: string
    required: false
    description: "do not show flags, show rss (only with -l)"
    aliases:
      - -y
  - name: version
    type: string
    required: false
    description: "display version information and exit"
    aliases:
      - -V
      - --version
execution:
  template: "ps -A {flag-a} -a {flag-a} -d {flag-d} -N {deselect} -C {flag-c}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with flag-A"
    command: "ps ${flag-A}"
  - description: "Display help message"
    command: "ps --help"
phase: enumeration
related_tools:
  - system-process-kill
---

# ps — Report process status

## Overview

`ps` is a command-line utility for report process status.

## Usage

```
ps -A {flag-a} -a {flag-a} -d {flag-d} -N {deselect} -C {flag-c}
```
