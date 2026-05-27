---
id: security-reverse-ltrace
namespace: security:reverse:ltrace
name: ltrace
description: Library call tracer for monitoring dynamic library calls made by a running program.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - trace.library.call
  - reverse.analysis
  - debug.tracing
platforms:
  - linux
  - macos
  - cross-platform
risk_level: low
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies: []
related_tools:
  - strace
  - gdb
  - trace-cmd
workflow_edges:
  produces:
    - library-call-log
    - trace-summary
  consumes:
    - binary
    - pid
contract:
  inputs:
    - type: file.binary
      description: Binary to trace library calls
    - type: system.pid
      description: Process ID to attach to
  outputs:
    - type: trace.library
      description: Library call trace log
      mime: text/plain
    - type: trace.summary
      description: Library call summary
      mime: text/plain
  side_effects:
    - process_spawn
  resource_cost:
    cpu: low
    memory_mb: 32
    network: low
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 32
  network: low
  disk_io: low
allowed-tools:
  - ltrace
  - Bash
  - execFile
parameters:
  - name: count
    type: boolean
    required: false
    description: "Count library calls and print summary"
    aliases:
      - -c
  - name: follow
    type: boolean
    required: false
    description: "Trace child processes (fork)"
    aliases:
      - -f
  - name: library
    type: string
    required: false
    description: "Only trace calls from specific library"
    aliases:
      - -l
  - name: output
    type: string
    required: false
    description: "Write trace to file instead of stderr"
    aliases:
      - -o
  - name: pid
    type: integer
    required: false
    description: "Attach to a running process by PID"
    aliases:
      - -p
  - name: syscalls
    type: boolean
    required: false
    description: "Show system calls in addition to library calls"
    aliases:
      - -S
  - name: timestamp
    type: boolean
    required: false
    description: "Add timestamp to each trace line"
    aliases:
      - -t
  - name: timecalls
    type: boolean
    required: false
    description: "Show time spent inside each call"
    aliases:
      - -T
  - name: filter
    type: string
    required: false
    description: "Filter calls by name pattern"
    aliases:
      - -e
  - name: strsize
    type: integer
    required: false
    description: "Max string display size"
    aliases:
      - -s
execution:
  template: "ltrace -c {binary}"
  sandbox: execFile
  timeout_seconds: 120
  shell: false
global_vars:
  binary: ""
examples:
  - description: "Count library calls with summary"
    command: ltrace -c /bin/ls
  - description: "Trace specific library only"
    command: ltrace -l libc.so.6 /bin/ls
  - description: "Attach to running process"
    command: ltrace -p 1234
  - description: "Show syscalls and library calls"
    command: ltrace -S /bin/ls
  - description: "Trace with timestamps and call durations"
    command: ltrace -t -T /bin/ls
  - description: "Write trace to file"
    command: ltrace -o trace.log /bin/ls
phase: exploitation
techniques:
  - discovery
  - execution
items:
  - NoCreds
services: []
attack_types:
  - Exploitation
  - Discovery
---

# ltrace — Library Call Tracer

ltrace intercepts and logs dynamic library calls made by a program. It is essential for understanding program behavior during reverse engineering, particularly for identifying library function usage patterns.

## Common Use Cases

- Identify which library functions a binary calls
- Analyze encryption routines by tracing crypto library calls
- Reverse engineer file I/O operations
- Profile program execution without source code

## Example Output

```
__libc_start_main(0x4026c0, 1, 0x7ffcdb2a6f58, 0x404540, 0x4045b0 <unfinished ...>
strlen(".")                                    = 1
malloc(3)                                      = 0x55d4c8a0c260
strcpy(0x55d4c8a0c260, ".")                    = 0x55d4c8a0c260
```
