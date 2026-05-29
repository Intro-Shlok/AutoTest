---
id: system-file-diff
namespace: system:file:diff
name: diff
description: Compare files line by line
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.file.diff
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
  - defense-evasion
parameters:
  - name: normal
    type: string
    required: false
    description: "output a normal diff (the default)"
    aliases:
      - --normal
  - name: brief
    type: string
    required: false
    description: "report only when files differ"
    aliases:
      - -q
      - --brief
  - name: report-identical-files
    type: string
    required: false
    description: "Set the report-identical-files parameter"
    aliases:
      - -s
      - --report-identical-files
  - name: context
    type: string
    required: false
    description: "output NUM (default 3) lines of copied context"
    aliases:
      - -c
      - -C
      - --context
  - name: unified
    type: string
    required: false
    description: "output NUM (default 3) lines of unified context"
    aliases:
      - -u
      - -U
      - --unified
  - name: ed
    type: string
    required: false
    description: "output an ed script"
    aliases:
      - -e
      - --ed
  - name: rcs
    type: string
    required: false
    description: "output an RCS format diff"
    aliases:
      - -n
      - --rcs
  - name: side-by-side
    type: string
    required: false
    description: "output in two columns"
    aliases:
      - -y
      - --side-by-side
  - name: width
    type: integer
    required: false
    description: "output at most NUM (default 130) print columns"
    aliases:
      - -W
      - --width
  - name: left-column
    type: string
    required: false
    description: "output only the left column of common lines"
    aliases:
      - --left-column
  - name: suppress-common-lines
    type: string
    required: false
    description: "do not output common lines"
    aliases:
      - --suppress-common-lines
  - name: show-c-function
    type: string
    required: false
    description: "show which C function each change is in"
    aliases:
      - -p
      - --show-c-function
  - name: show-function-line
    type: string
    required: false
    description: "show the most recent line matching RE"
    aliases:
      - -F
      - --show-function-line
  - name: label LABEL
    template_key: label-label
    type: string
    required: false
    description: "use LABEL instead of file name and timestamp"
    aliases:
      - --label LABEL
  - name: expand-tabs
    type: string
    required: false
    description: "expand tabs to spaces in output"
    aliases:
      - -t
      - --expand-tabs
  - name: initial-tab
    type: string
    required: false
    description: "make tabs line up by prepending a tab"
    aliases:
      - -T
      - --initial-tab
  - name: tabsize
    type: integer
    required: false
    description: "tab stops every NUM (default 8) print columns"
    aliases:
      - --tabsize
  - name: suppress-blank-empty
    type: string
    required: false
    description: "suppress space or tab before empty output lines"
    aliases:
      - --suppress-blank-empty
  - name: paginate
    type: string
    required: false
    description: "pass output through 'pr' to paginate it"
    aliases:
      - -l
      - --paginate
  - name: recursive
    type: string
    required: false
    description: "recursively compare any subdirectories found"
    aliases:
      - -r
      - --recursive
  - name: no-dereference
    type: string
    required: false
    description: "don't follow symbolic links"
    aliases:
      - --no-dereference
  - name: new-file
    type: string
    required: false
    description: "treat absent files as empty"
    aliases:
      - -N
      - --new-file
  - name: unidirectional-new-file
    type: string
    required: false
    description: "treat absent first files as empty"
    aliases:
      - --unidirectional-new-file
  - name: ignore-file-name-case
    type: string
    required: false
    description: "ignore case when comparing file names"
    aliases:
      - --ignore-file-name-case
  - name: no-ignore-file-name-case
    type: string
    required: false
    description: "Set the no-ignore-file-name-case parameter"
    aliases:
      - --no-ignore-file-name-case
  - name: exclude
    type: string
    required: false
    description: "exclude files that match PAT"
    aliases:
      - -x
      - --exclude
  - name: exclude-from
    type: file
    required: false
    description: "exclude files that match any pattern in FILE"
    aliases:
      - -X
      - --exclude-from
  - name: starting-file
    type: file
    required: false
    description: "start with FILE when comparing directories"
    aliases:
      - -S
      - --starting-file
  - name: from-file
    type: file
    required: false
    description: "compare FILE1 to all operands"
    aliases:
      - --from-file
  - name: to-file
    type: file
    required: false
    description: "compare all operands to FILE2"
    aliases:
      - --to-file
execution:
  template: "diff --normal {normal} -q {brief} -s {report-identical-files} -c {context}
    -u {unified}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with normal"
    command: "diff ${normal}"
  - description: "Display help message"
    command: "diff --help"
related_tools:
  - system-file-patch
install:
    - method: apt
      package_name: "diffutils"
      commands:
        - "apt-get install -y diffutils"
---

# diff — Compare files line by line

## Overview

`diff` is a command-line utility for compare files line by line.

## Usage

```
diff --normal {normal} -q {brief} -s {report-identical-files} -c {context} -u {unified}
```
