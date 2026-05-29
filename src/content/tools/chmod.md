---
id: system-file-chmod
namespace: system:file:chmod
name: chmod
description: Change file mode bits
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.file.chmod
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
  - command-and-control
  - collection
  - execution
  - data-manipulation
  - credential-access
parameters:
  - name: changes
    type: string
    required: false
    description: "like verbose but report only when a change is made"
    aliases:
      - -c
      - --changes
  - name: silent
    type: string
    required: false
    description: "suppress most error messages"
    aliases:
      - -f
      - --silent
      - --quiet
  - name: verbose
    type: string
    required: false
    description: "output a diagnostic for every file processed --dereference affect
      the referent of each symbolic link, rather than the symbolic link itself"
    aliases:
      - -v
      - --verbose
  - name: no-dereference
    type: string
    required: false
    description: "affect each symbolic link, rather than the referent --no-preserve-root
      do not treat '/' specially (the default) --preserve-root fail to operate recursively
      on '/' --reference=RFILE use RFILE's mode..."
    aliases:
      - -h
      - --no-dereference
  - name: recursive
    type: string
    required: false
    description: "change files and directories recursively"
    aliases:
      - -R
      - --recursive
  - name: flag-H
    template_key: flag-h
    type: file
    required: false
    description: "if a command line argument is a symlink to a directory, traverse
      it"
    aliases:
      - -H
  - name: flag-L
    template_key: flag-l
    type: file
    required: false
    description: "traverse every symbolic link to a directory encountered"
    aliases:
      - -L
  - name: flag-P
    template_key: flag-p
    type: string
    required: false
    description: "do not traverse any symbolic links"
    aliases:
      - -P
  - name: help
    type: string
    required: false
    description: "display this help and exit --version output version information
      and exit"
    aliases:
      - --help
execution:
  template: "chmod -c {changes} -f {silent} -v {verbose} -h {no-dereference} -R {recursive}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with changes"
    command: "chmod ${changes}"
  - description: "Display help message"
    command: "chmod --help"
  - description: Give the [u]ser who owns a file the right to e[x]ecute it.
    command: chmod u+x PATH
  - description: Give the [u]ser rights to [r]ead and [w]rite to a file/directory.
    command: chmod u+rw PATH
  - description: Remove e[x]ecutable rights from the [g]roup.
    command: chmod g-x PATH
  - description: Give [a]ll users rights to [r]ead and e[x]ecute.
    command: chmod a+rx PATH
  - description: Give [o]thers (not in the file owner's group) the same rights as
      the [g]roup.
    command: chmod o=g PATH
  - description: Remove all rights from [o]thers.
    command: chmod o= PATH
  - description: Change permissions recursively, allowing [g]roup and [o]thers to
      [w]rite.
    command: chmod -R g+w,o+w PATH
  - description: Set access rights using numeric (octal) form.
    command: chmod 750 PATH
  - description: Add the execute permission bit to directories only. This works because
      the 'X' is uppercase, meaning only directories will be executable. However,
      if an existing file is executable, this bit will not be removed.
    command: chmod a+X PATH
  - description: Convert string representation of the access right into numeric form
      and back.
    command: curl cheat.sh/chmod/750
  - description: 'cheat.sheets: chmod'
    command: curl cheat.sh/chmod/rwxr-x
related_tools:
  - system-file-chown
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

---

# chmod — Change file mode bits

## Overview

`chmod` is a command-line utility for change file mode bits.

## Usage

```
chmod -c {changes} -f {silent} -v {verbose} -h {no-dereference} -R {recursive}
```
