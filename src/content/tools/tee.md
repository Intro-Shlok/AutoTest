---
id: system-io-tee
namespace: system:io:tee
name: tee
description: Reads from standard input and writes to both standard output and one
  or more files simultaneously.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - data.io.split
  - data.io.duplicate
  - filesystem.io.capture
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
  - cross-platform
dependencies: []
related_tools:
  - cat
  - dd
  - redirect
artifacts:
  - type: filesystem.directory.contents
    description: Captured output written to a file
    trust_level: verified
  - type: text.plain
    description: Passthrough stdout text
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - captured-output
  consumes:
    - stream-input
contract:
  inputs:
    - type: text.plain
      description: Input stream to duplicate
      mime: text/plain
  outputs:
    - type: filesystem.directory.contents
      description: Output captured to a file on disk
    - type: text.plain
      description: Pass-through copy of input to stdout
      mime: text/plain
  side_effects:
    - filesystem_write
  resource_cost:
    cpu: low
    memory_mb: 16
    network: none
    disk_io: medium
allowed-tools:
  - tee
  - Bash
  - execFile
parameters:
  - name: append
    type: string
    required: false
    description: "append to the given FILEs, do not overwrite"
    aliases:
      - -a
      - --append
  - name: ignore-interrupts
    type: string
    required: false
    description: "ignore interrupt signals"
    aliases:
      - -i
      - --ignore-interrupts
  - name: flag-p
    type: string
    required: false
    description: "operate in a more appropriate MODE with pipes --output-error[=MODE]
      set behavior on write error. See MODE below --help display this help and exit
      --version output version information and exit"
    aliases:
      - -p
execution:
  template: "tee {append} {ignore-interrupts} {flag-p}"
  sandbox: execFile
  timeout_seconds: 60
  shell: false
examples:
  - description: "Capture command output to a log file while viewing"
    command: "nmap -sS target | tee scan.log"
  - description: "Append output to an existing file"
    command: "curl https://api.example.com | tee -a results.txt"
  - description: Display `ls` output to the user, but also write it to the given file.
    command: ls | tee outfile.txt
  - description: As above, but append the data; previous file's data remains intact
      while new data is added at the end of the file.
    command: ls | tee -a outfile.txt
  - description: Pipe the standard output of a given command into `tee`, which then
      displays it to the user and sending the data to files `one`, `two`, and `three`.
    command: '[COMMAND] | tee one two three'
  - description: Workaround to output data to a file, with root privileges.
    command: echo 3 | sudo tee /proc/sys/vm/drop_caches
  - description: Pipe the current Vim buffer to a shell process, which in this case
      is `tee`. This is especially useful as a shortcut added to `.vimrc` or similar.
    command: :w !sudo tee %
references:
  - label: "GNU Coreutils tee"
    url: "https://www.gnu.org/software/coreutils/manual/html_node/tee-invocation.html"
techniques:
  - defense-evasion
install:
    - method: apt
      package_name: "coreutils"
      commands:
        - "apt-get install -y coreutils"
    - method: brew
      package_name: "coreutils"
      commands:
        - "brew install coreutils"
---

# tee — Duplicate Stream Content

tee reads from standard input and writes to both standard output and one or more files. It is the canonical Unix tool for simultaneously displaying and capturing command output — the essential bridge between `stdout`-producing tools and `file`-consuming tools.

## Pipeline Role

tee serves as the redirect transform in artifact pipelines:

```
tool producing stdout → tee → file on disk → tool consuming file
```

For example:

```bash
nmap -sS target.com | tee scan-output.txt
tar -czf archive.tar.gz scan-output.txt
```

This pattern: `nmap` (produces `network.scan.nmap.xml`) → `tee` (redirects to file `filesystem.directory.contents`) → `tar` (consumes `filesystem.directory.contents`) is the canonical transformation pipeline for artifact type mismatches.

## Common Usage

| Command | Effect |
|---------|--------|
| `cmd \| tee file` | Capture while viewing |
| `cmd \| tee -a file` | Append to existing log |
| `cmd \| tee file1 file2` | Duplicate to multiple files |
| `cmd \| tee /dev/tty` | Write to terminal directly |
