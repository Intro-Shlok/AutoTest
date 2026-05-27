---
id: security-reverse-strace
namespace: security:reverse:strace
name: strace
description: System call tracer for monitoring syscalls made by a process, useful for debugging and reverse engineering.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - trace.syscall
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
  - ltrace
  - gdb
  - trace-cmd
workflow_edges:
  produces:
    - syscall-log
    - trace-summary
  consumes:
    - binary
    - pid
contract:
  inputs:
    - type: file.binary
      description: Binary to trace system calls
    - type: system.pid
      description: Process ID to attach to
  outputs:
    - type: trace.syscall
      description: System call trace log
      mime: text/plain
    - type: trace.summary
      description: Syscall count summary
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
  - strace
  - Bash
  - execFile
parameters:
  - name: count
    type: boolean
    required: false
    description: "Count syscalls and print summary"
    aliases:
      - -c
  - name: follow
    type: boolean
    required: false
    description: "Trace child processes (fork)"
    aliases:
      - -f
  - name: expr
    type: string
    required: false
    description: "Filter syscalls by expression"
    aliases:
      - -e
  - name: output
    type: string
    required: false
    description: "Write trace to file"
    aliases:
      - -o
  - name: pid
    type: integer
    required: false
    description: "Attach to running process by PID"
    aliases:
      - -p
  - name: strsize
    type: integer
    required: false
    description: "Max string size to print per string"
    aliases:
      - -s
  - name: timestamp
    type: boolean
    required: false
    description: "Prefix each line with timestamp"
    aliases:
      - -t
  - name: timecalls
    type: boolean
    required: false
    description: "Show time spent in syscalls"
    aliases:
      - -T
  - name: verbose
    type: boolean
    required: false
    description: "Verbose mode (decode structures)"
    aliases:
      - -v
  - name: hex
    type: boolean
    required: false
    description: "Print non-ascii strings in hex"
    aliases:
      - -x
  - name: relative
    type: boolean
    required: false
    description: "Print relative timestamps"
    aliases:
      - -r
  - name: instrPointer
    type: boolean
    required: false
    description: "Print instruction pointer"
    aliases:
      - -i
execution:
  template: "strace -c {binary}"
  sandbox: execFile
  timeout_seconds: 120
  shell: false
global_vars:
  binary: ""
examples:
  - description: "Count system calls with summary"
    command: strace -c /bin/ls
  - description: "Filter specific syscalls"
    command: strace -e trace=open,read,write /bin/ls
  - description: "Attach to running process"
    command: strace -p 1234
  - description: "Follow child processes"
    command: strace -f -o trace.log ./server
  - description: "Trace with timestamps"
    command: strace -t -T /bin/ls
  - description: "Print instruction pointer with each syscall"
    command: strace -i /bin/ls
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

# strace — System Call Tracer

strace intercepts and records system calls made by a process. It is an indispensable tool for reverse engineering, debugging, and understanding program behavior at the kernel interface level.

## Common Filters

| Expression | Effect |
|------------|--------|
| `-e trace=file` | Only file-related syscalls |
| `-e trace=network` | Only network syscalls |
| `-e trace=process` | Only process-related syscalls |
| `-e trace=signal` | Only signal syscalls |
| `-e read=3` | Show data read from fd 3 |

## Example Output (Count Mode)

```
% time     seconds  usecs/call     calls    errors syscall
------ ----------- ----------- --------- --------- ----------------
 43.28    0.000211           5        40           write
 28.69    0.000140           5        28           read
 15.78    0.000077           3        28           openat
  6.97    0.000034           1        29           close
```
