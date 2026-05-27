---
id: system-file-cp
namespace: system:file:cp
name: cp
description: Copy files and directories
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.file.cp
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
  - privilege-escalation
parameters:
  - name: archive
    type: string
    required: false
    description: "same as -dR --preserve=all --attributes-only don't copy the file
      data, just the attributes --backup[=CONTROL] make a backup of each existing
      destination file"
    aliases:
      - -a
      - --archive
  - name: flag-b
    type: string
    required: false
    description: "like --backup but does not accept an argument --copy-contents copy
      contents of special files when recursive"
    aliases:
      - -b
  - name: flag-d
    type: string
    required: false
    description: "same as --no-dereference --preserve=links --debug explain how a
      file is copied. Implies -v"
    aliases:
      - -d
  - name: force
    type: string
    required: false
    description: "if an existing destination file cannot be opened, remove it and
      try again (this option is ignored when the -n option is also used)"
    aliases:
      - -f
      - --force
  - name: interactive
    type: string
    required: false
    description: "prompt before overwrite (overrides a previous -n option)"
    aliases:
      - -i
      - --interactive
  - name: flag-H
    template_key: flag-h
    type: string
    required: false
    description: "follow command-line symbolic links in SOURCE"
    aliases:
      - -H
  - name: dereference
    type: string
    required: false
    description: "always follow symbolic links in SOURCE"
    aliases:
      - -L
      - --dereference
  - name: no-dereference
    type: file
    required: false
    description: "never follow symbolic links in SOURCE --keep-directory-symlink follow
      existing symlinks to directories"
    aliases:
      - -P
      - --no-dereference
  - name: link
    type: string
    required: false
    description: "hard link files instead of copying"
    aliases:
      - -l
      - --link
  - name: no-clobber
    type: string
    required: false
    description: "(deprecated) silently skip existing files. See also --update"
    aliases:
      - -n
      - --no-clobber
  - name: flag-p
    type: file
    required: false
    description: "same as --preserve=mode,ownership,timestamps --preserve[=ATTR_LIST]
      preserve the specified attributes --no-preserve=ATTR_LIST don't preserve the
      specified attributes --parents use full source file ..."
    aliases:
      - -p
  - name: recursive
    type: string
    required: false
    description: "copy directories recursively --reflink[=WHEN] control clone/CoW
      copies. See below --remove-destination remove each existing destination file
      before attempting to open it (contrast with --force) --s..."
    aliases:
      - -R
      - -r
      - --recursive
  - name: symbolic-link
    type: string
    required: false
    description: "make symbolic links instead of copying"
    aliases:
      - -s
      - --symbolic-link
  - name: suffix
    type: string
    required: false
    description: "override the usual backup suffix"
    aliases:
      - -S
      - --suffix
  - name: target-directory
    type: file
    required: false
    description: "copy all SOURCE arguments into DIRECTORY"
    aliases:
      - -t
      - --target-directory
  - name: no-target-directory
    type: string
    required: false
    description: "treat DEST as a normal file --update[=UPDATE] control which existing
      files are updated; UPDATE={all,none,none-fail,older(default)}"
    aliases:
      - -T
      - --no-target-directory
    enum:
      - all,none,none-fail,older(default)
  - name: flag-u
    type: string
    required: false
    description: "equivalent to --update[=older]. See below"
    aliases:
      - -u
  - name: verbose
    type: string
    required: false
    description: "explain what is being done"
    aliases:
      - -v
      - --verbose
  - name: one-file-system
    type: string
    required: false
    description: "stay on this file system"
    aliases:
      - -x
      - --one-file-system
  - name: flag-Z
    template_key: flag-z
    type: file
    required: false
    description: "set SELinux security context of destination file to default type
      --context[=CTX] like -Z, or if CTX is specified then set the SELinux or SMACK
      security context to CTX --help display this help and e..."
    aliases:
      - -Z
execution:
  template: "cp -a {archive} -b {flag-b} -d {flag-d} -f {force} -i {interactive}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with archive"
    command: "cp ${archive}"
  - description: "Display help message"
    command: "cp --help"
related_tools:
  - system-file-mv
  - system-file-rm
---

# cp — Copy files and directories

## Overview

`cp` is a command-line utility for copy files and directories.

## Usage

```
cp -a {archive} -b {flag-b} -d {flag-d} -f {force} -i {interactive}
```
