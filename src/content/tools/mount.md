---
id: system-storage-mount
namespace: system:storage:mount
name: mount
description: Mount a filesystem
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.storage.mount
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
  - credential-access
  - privilege-escalation
parameters:
  - name: all
    type: string
    required: false
    description: "mount all filesystems mentioned in fstab"
    aliases:
      - -a
      - --all
  - name: no-canonicalize
    type: string
    required: false
    description: "don't canonicalize paths"
    aliases:
      - -c
      - --no-canonicalize
  - name: fake
    type: string
    required: false
    description: "dry run; skip the mount(2) syscall"
    aliases:
      - -f
      - --fake
  - name: fork
    type: string
    required: false
    description: "fork off for each device (use with -a)"
    aliases:
      - -F
      - --fork
  - name: fstab
    type: file
    required: false
    description: "alternative file to /etc/fstab"
    aliases:
      - -T
      - --fstab <path>
  - name: internal-only
    type: string
    required: false
    description: "don't call the mount.<type> helpers"
    aliases:
      - -i
      - --internal-only
  - name: show-labels
    type: string
    required: false
    description: "show also filesystem labels"
    aliases:
      - -l
      - --show-labels
  - name: map-groups
    type: string
    required: false
    description: "add the specified GID map to an ID-mapped mount --map-users <inner>:<outer>:<count>
      add the specified UID map to an ID-mapped mount --map-users /proc/<pid>/ns/user
      specify the user namespace for an..."
    aliases:
      - --map-groups <inner>
  - name: mkdir
    type: string
    required: false
    description: "alias to '-o X-mount.mkdir[=<mode>]'"
    aliases:
      - -m
      - --mkdir
  - name: no-mtab
    type: string
    required: false
    description: "don't write to /etc/mtab"
    aliases:
      - -n
      - --no-mtab
  - name: options-mode
    type: string
    required: false
    description: "what to do with options loaded from fstab --options-source <source>
      mount options source --options-source-force force use of options from fstab/mtab
      --onlyonce check if filesystem is already mounted"
    aliases:
      - --options-mode <mode>
  - name: options
    type: array
    required: false
    description: "comma-separated list of mount options"
    aliases:
      - -o
      - --options <list>
  - name: test-opts
    type: array
    required: false
    description: "Set the test-opts parameter"
    aliases:
      - -O
      - -a
      - --test-opts <list>
  - name: read-only
    type: string
    required: false
    description: "mount the filesystem read-only (same as -o ro)"
    aliases:
      - -r
      - --read-only
  - name: types
    type: array
    required: false
    description: "limit the set of filesystem types"
    aliases:
      - -t
      - --types <list>
  - name: source
    type: string
    required: false
    description: "explicitly specifies source (path, label, uuid)"
    aliases:
      - --source <src>
    enum:
      - path
      - label
      - uuid
  - name: target
    type: string
    required: false
    description: "explicitly specifies mountpoint"
    aliases:
      - --target <target>
  - name: target-prefix
    type: file
    required: false
    description: "specifies path used for all mountpoints"
    aliases:
      - --target-prefix <path>
  - name: verbose
    type: string
    required: false
    description: "say what is being done"
    aliases:
      - -v
      - --verbose
  - name: rw
    type: string
    required: false
    description: "Set the rw parameter"
    aliases:
      - -w
      - -w
      - --rw
      - --read-write
  - name: namespace
    type: string
    required: false
    description: "perform mount in another namespace"
    aliases:
      - -N
      - --namespace <ns>
  - name: help
    type: string
    required: false
    description: "display this help"
    aliases:
      - -h
      - --help
  - name: version
    type: string
    required: false
    description: "display version"
    aliases:
      - -V
      - --version
  - name: label
    type: string
    required: false
    description: "synonym for LABEL=<label>"
    aliases:
      - -L
      - --label <label>
  - name: uuid
    type: string
    required: false
    description: "synonym for UUID=<uuid>"
    aliases:
      - -U
      - --uuid <uuid>
  - name: bind
    type: string
    required: false
    description: "mount a subtree somewhere else (same as -o bind)"
    aliases:
      - -B
      - --bind
  - name: move
    type: string
    required: false
    description: "move a subtree to some other place"
    aliases:
      - -M
      - --move
  - name: rbind
    type: string
    required: false
    description: "mount a subtree and all submounts somewhere else"
    aliases:
      - -R
      - --rbind
  - name: make-shared
    type: string
    required: false
    description: "mark a subtree as shared"
    aliases:
      - --make-shared
  - name: make-slave
    type: string
    required: false
    description: "mark a subtree as slave"
    aliases:
      - --make-slave
execution:
  template: "mount -a {all} -c {no-canonicalize} -f {fake} -F {fork} -T {fstab}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with all"
    command: "mount ${all}"
  - description: "Display help message"
    command: "mount --help"
  - description: Mount a temporary filesystem (TMPFS) of 4GB to '/mnt'. The contents
      will vanish when you reboot, but this can be very useful when working with things
      like bootstrap tarballs or temporary storages for sensitive data.
    command: mount -t tmpfs -o mode=755,size=4096M tmpfs /mnt
install:
    - method: apt
      package_name: "mount"
      commands:
        - "apt-get install -y mount"
---

# mount — Mount a filesystem

## Overview

`mount` is a command-line utility for mount a filesystem.

## Usage

```
mount -a {all} -c {no-canonicalize} -f {fake} -F {fork} -T {fstab}
```
