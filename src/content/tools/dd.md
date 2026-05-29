---
id: system-file-dd
namespace: system:file:dd
name: dd
description: Convert and copy a file
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.file.dd
  - system.file.search
  - system.file.process
  - system.file.copy
  - system.file.move
  - system.file.delete
platforms:
  - linux
risk_level: high
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
  - credential-access
  - execution
  - process-manip
parameters:
  - name: help
    type: string
    required: false
    description: "display this help and exit --version output version information
      and exit"
    aliases:
      - --help
execution:
  template: "dd --help {help}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with help"
    command: "dd ${help}"
  - description: "Display help message"
    command: "dd --help"
  - description: 'Read from `/dev/urandom`, 2*512 Bytes, and put it into `/tmp/test.txt`.
      Note: each iteration reads 512 bytes (the selected block size).'
    command: dd if=/dev/urandom of=/tmp/test.txt count=2 bs=512
  - description: Watch the progress of dd(1).
    command: dd if=/dev/zero of=/dev/null bs=4KB &
  - description: 'cheat.sheets: dd'
    command: export dd_pid=`pgrep '^dd'`
  - description: 'cheat.sheets: dd'
    command: while [[ -d /proc/$dd_pid ]]; do
  - description: 'cheat.sheets: dd'
    command: kill -USR1 $dd_pid && sleep 1
  - description: 'cheat.sheets: dd'
    command: clear
  - description: 'cheat.sheets: dd'
    command: done
  - description: 'Watch the progress of dd(1) with pv(1) and dialog(1), both of which
      can be installed with the following command: apt-get install pv dialog'
    command: (
  - description: 'cheat.sheets: dd'
    command: pv -n /dev/zero | dd of=/dev/null bs=128M conv=notrunc,noerror
  - description: 'cheat.sheets: dd'
    command: ) 2>&1 | dialog --gauge "Running dd command (cloning), please wait..."
      10 70 0
  - description: 'Watch the progress of dd(1) with pv(1) and zenity(1), both of which
      can be installed with the following command: apt-get install pv zenity'
    command: (
  - description: 'cheat.sheets: dd'
    command: pv -n /dev/zero | dd of=/dev/null bs=128M conv=notrunc,noerror
  - description: 'cheat.sheets: dd'
    command: ) 2>&1 | zenity --title 'Cloning with dd(1) -- please wait...' --progress
  - description: Watch the progress of dd(1) with the built-in `progress` functionality,
      - introduced in CoreUtils v8.24.
    command: dd if=/dev/zero of=/dev/null bs=128M status=progress
  - description: DD with "graphical" return
    command: dcfldd if=/dev/zero of=/dev/null bs=500K
  - description: This will output the sound from your microphone port to the ssh target
      computer's speaker port. The sound quality is very bad, so you will hear a lot
      of hissing.
    command: dd if=/dev/dsp | ssh -c arcfour -C username@host dd of=/dev/dsp
  - description: Show current progress without interruption (USR1)
    command: dd if=/dev/zero of=/dev/null & pid=$!
  - description: 'cheat.sheets: dd'
    command: kill -USR1 $pid
  - description: Create a 1GiB file with nothing but zeros, ready to mkswap(8) it.
    command: dd if=/dev/zero of=/swapfile count=1048576 bs=1024 status=progress
phase: exploitation
install:
    - method: apt
      package_name: "coreutils"
      commands:
        - "apt-get install -y coreutils"
---

# dd — Convert and copy a file

## Overview

`dd` is a command-line utility for convert and copy a file.

## Usage

```
dd --help {help}
```
