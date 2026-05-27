---
id: system-storage-du
namespace: system:storage:du
name: du
description: Estimate file space usage
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.storage.du
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
  - defense-evasion
  - execution
  - process-manip
parameters:
  - name: "null"
    type: string
    required: false
    description: "end each output line with NUL, not newline"
    aliases:
      - "-0"
      - --null
  - name: all
    type: string
    required: false
    description: "write counts for all files, not just directories"
    aliases:
      - -a
      - --all
  - name: apparent-size
    type: string
    required: false
    description: "print apparent sizes rather than device usage; although the apparent
      size is usually smaller, it may be larger due to holes in ('sparse') files,
      internal fragmentation, indirect blocks, etc"
    aliases:
      - -A
      - --apparent-size
  - name: block-size
    type: integer
    required: false
    description: "scale sizes by SIZE before printing them; See SIZE format below;
      E.g., '-BM' prints sizes in units of 1,048,576 bytes"
    aliases:
      - -B
      - --block-size
  - name: bytes
    type: string
    required: false
    description: "equivalent to '--apparent-size --block-size=1'"
    aliases:
      - -b
      - --bytes
  - name: total
    type: string
    required: false
    description: "produce a grand total"
    aliases:
      - -c
      - --total
  - name: dereference-args
    type: string
    required: false
    description: "dereference only symlinks that are listed on the command line"
    aliases:
      - -D
      - --dereference-args
  - name: max-depth
    type: integer
    required: false
    description: "print the total for a directory (or file, with --all) only if it
      is N or fewer levels below the command line argument; --max-depth=0 is the same
      as --summarize --files0-from=F summarize device usag..."
    aliases:
      - -d
      - --max-depth
  - name: flag-H
    template_key: flag-h
    type: string
    required: false
    description: "equivalent to --dereference-args (-D)"
    aliases:
      - -H
  - name: human-readable
    type: string
    required: false
    description: "print sizes in human readable format (e.g., 1K 234M 2G) --inodes
      list inode usage information instead of block usage"
    aliases:
      - -h
      - --human-readable
  - name: flag-k
    type: string
    required: false
    description: "like --block-size=1K"
    aliases:
      - -k
  - name: dereference
    type: string
    required: false
    description: "dereference all symbolic links"
    aliases:
      - -L
      - --dereference
  - name: count-links
    type: string
    required: false
    description: "count sizes many times if hard linked"
    aliases:
      - -l
      - --count-links
  - name: flag-m
    type: string
    required: false
    description: "like --block-size=1M"
    aliases:
      - -m
  - name: no-dereference
    type: string
    required: false
    description: "don't follow any symbolic links (this is the default)"
    aliases:
      - -P
      - --no-dereference
  - name: separate-dirs
    type: string
    required: false
    description: "for directories do not include size of subdirectories --si like
      -h, but use powers of 1000 not 1024"
    aliases:
      - -S
      - --separate-dirs
  - name: summarize
    type: string
    required: false
    description: "display only a total for each argument"
    aliases:
      - -s
      - --summarize
  - name: threshold
    type: integer
    required: false
    description: "exclude entries smaller than SIZE if positive, or entries greater
      than SIZE if negative --time show time of the last modification of any file
      in the directory, or any of its subdirectories --time=W..."
    aliases:
      - -t
      - --threshold
  - name: exclude-from
    type: file
    required: false
    description: "exclude files that match any pattern in FILE --exclude=PATTERN exclude
      files that match PATTERN"
    aliases:
      - -X
      - --exclude-from
  - name: one-file-system
    type: string
    required: false
    description: "skip directories on different file systems --help display this help
      and exit --version output version information and exit"
    aliases:
      - -x
      - --one-file-system
execution:
  template: "du -0 {null} -a {all} -A {apparent-size} -B {block-size} -b {bytes}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with null"
    command: "du ${null}"
  - description: "Display help message"
    command: "du --help"
  - description: With 'root' privileges, use du(1), sort(1), and head(1) to display
      a list of the top 20 space-consuming files in whichever storage medium '/' is
      mounted. Here, du(1) is using the `-x` flag to keep to the one filesystem, which
      is important for getting accurate results on the filesystem on which you might,
      for example, be needing to free space. In order to sort the human-readable file
      sizes, sort(1) is using the `-h` flag, the `-k` flag to specify the column to
      sort (first), and its using the `-r` flag to reverse the sorting, so we see
      the highest size first. To then show the top-20 lines, we use head(1) and specify
      the number of lines via the `-n` flag. The default number of lines displayed
      by head(1) and tail(1) is 10. Root privileges are gained for this task by using
      sudo(8) on bash(1) in order to have a new root-owned BASH session, which then
      executes the commands proceeding the `-c` flag.
    command: sudo bash -c 'du -xh / | sort -rhk 1 | head -n 20'
  - description: Display just the total human-readable size of the current working
      directory.
    command: du -sh
  - description: Display the total human-readable size of the three provided directories,
      as well as the grand total of the combined directories.
    command: du -chs ~/Desktop ~/Pictures ~/Videos
  - description: You could potentially make this task a bit easier with BASH brace
      expansion.
    command: du -chs ~/{Desktop,Pictures,Videos}
phase: exploitation
related_tools:
  - system-storage-df
---

# du — Estimate file space usage

## Overview

`du` is a command-line utility for estimate file space usage.

## Usage

```
du -0 {null} -a {all} -A {apparent-size} -B {block-size} -b {bytes}
```
