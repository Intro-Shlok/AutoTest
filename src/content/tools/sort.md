---
id: system-file-sort
namespace: system:file:sort
name: sort
description: Sort lines of text files
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.file.sort
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
  - credential-access
  - discovery
  - enumeration
  - execution
parameters:
  - name: ignore-leading-blanks
    type: string
    required: false
    description: "ignore leading blanks when finding sort keys in each line"
    aliases:
      - -b
      - --ignore-leading-blanks
  - name: dictionary-order
    type: integer
    required: false
    description: "consider only blanks and alphanumeric characters"
    aliases:
      - -d
      - --dictionary-order
  - name: ignore-case
    type: string
    required: false
    description: "fold lower case to upper case characters"
    aliases:
      - -f
      - --ignore-case
  - name: general-numeric-sort
    type: integer
    required: false
    description: "compare according to general numerical value"
    aliases:
      - -g
      - --general-numeric-sort
  - name: ignore-nonprinting
    type: string
    required: false
    description: "consider only printable characters"
    aliases:
      - -i
      - --ignore-nonprinting
  - name: month-sort
    type: string
    required: false
    description: "compare (unknown) < 'JAN' < ... < 'DEC'"
    aliases:
      - -M
      - --month-sort
  - name: human-numeric-sort
    type: string
    required: false
    description: "compare human readable numbers (e.g., 2K 1G)"
    aliases:
      - -h
      - --human-numeric-sort
  - name: numeric-sort
    type: integer
    required: false
    description: "compare according to string numerical value; see full documentation
      for supported strings"
    aliases:
      - -n
      - --numeric-sort
  - name: random-sort
    type: string
    required: false
    description: "shuffle, but group identical keys. See also shuf(1) --random-source=FILE
      get random bytes from FILE"
    aliases:
      - -R
      - --random-sort
  - name: reverse
    type: integer
    required: false
    description: "reverse the result of comparisons --sort=WORD sort according to
      WORD: general-numeric -g, human-numeric -h, month -M, numeric -n, random -R,
      version -V"
    aliases:
      - -r
      - --reverse
  - name: version-sort
    type: string
    required: false
    description: "natural sort of (version) numbers within text"
    aliases:
      - -V
      - --version-sort
  - name: batch-size
    type: string
    required: false
    description: "merge at most NMERGE inputs at once; for more use temp files"
    aliases:
      - --batch-size
  - name: check
    type: string
    required: false
    description: "check for sorted input; do not sort"
    aliases:
      - -c
      - -f
      - --check
      - --check
  - name: check-2
    type: string
    required: false
    description: "like -c, but do not report first bad line --compress-program=PROG
      compress temporaries with PROG; decompress them with PROG -d --debug annotate
      the part of the line used to sort, and warn about que..."
    aliases:
      - -C
      - --check
      - --check
  - name: key
    type: string
    required: false
    description: "sort via a key; KEYDEF gives location and type"
    aliases:
      - -k
      - --key
  - name: merge
    type: string
    required: false
    description: "merge already sorted files; do not sort"
    aliases:
      - -m
      - --merge
  - name: output
    type: file
    required: false
    description: "write result to FILE instead of standard output"
    aliases:
      - -o
      - --output
  - name: stable
    type: string
    required: false
    description: "stabilize sort by disabling last-resort comparison"
    aliases:
      - -s
      - --stable
  - name: buffer-size
    type: integer
    required: false
    description: "use SIZE for main memory buffer"
    aliases:
      - -S
      - --buffer-size
  - name: field-separator
    type: string
    required: false
    description: "use SEP instead of non-blank to blank transition"
    aliases:
      - -t
      - --field-separator
  - name: temporary-directory
    type: file
    required: false
    description: "use DIR for temporaries, not $TMPDIR or /tmp; multiple options specify
      multiple directories --parallel=N change the number of sorts run concurrently
      to N"
    aliases:
      - -T
      - --temporary-directory
  - name: unique
    type: string
    required: false
    description: "output only the first of lines with equal keys; with -c, check for
      strict ordering"
    aliases:
      - -u
      - --unique
  - name: zero-terminated
    type: string
    required: false
    description: "line delimiter is NUL, not newline --help display this help and
      exit --version output version information and exit"
    aliases:
      - -z
      - --zero-terminated
execution:
  template: "sort -b {ignore-leading-blanks} -d {dictionary-order} -f {ignore-case}
    -g {general-numeric-sort} -i {ignore-nonprinting}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with ignore-leading-blanks"
    command: "sort ${ignore-leading-blanks}"
  - description: "Display help message"
    command: "sort --help"
  - description: Return the contents of the British English dictionary, in reverse
      order.
    command: sort -r /usr/share/dict/british-english
  - description: The GNU sort(1) command can also filter out adjacent duplicate lines
      and can therefore overlap with the uniq(1) command. However, uniq(1) has some
      options that sort(1) cannot do so refer to the man page for you situation if
      you require something beyond a basic uniqueness check. In addition, there is
      the potential for parallizing the processing by piping sort(1) into uniq(1)
      for non trivial tasks. By default, sort(1) sorts lines or fields using the ASCII
      table. Here, we're essentially getting alphanumeric sorting, where case is handled
      separately; - this results in these words being adjacent to one another, thus
      duplicates are removed. If you need better uniq-ing, you could refer to AWK
      & its associative arrays.
    command: printf '%s\n' this is a list of of random words with duplicate words
      | sort -u
  - description: Sort numerically. If you don't provide the `-n` flag, sort(1) will
      instead sort by the ASCII table, as mentioned above, meaning it'll display as
      1, 10, - 11, 2, 3, 4, etc.
    command: printf '%d\n' {1..9} 10 11 | sort -n
  - description: You can even sort human-readable sizes. In this example, the 2nd
      column is being sorted, thanks to the use of the `-k` flag, and the sorting
      is reversed, so that the top-most storage space hungry filesystems are displayed
      from df(1).
    command: df -ht ext4 /dev/sd[a-z][1-9]* | sed '1d' | sort -rhk 2
related_tools:
  - system-file-cat
  - system-file-comm
  - system-file-uniq
  - system-file-wc
---

# sort — Sort lines of text files

## Overview

`sort` is a command-line utility for sort lines of text files.

## Usage

```
sort -b {ignore-leading-blanks} -d {dictionary-order} -f {ignore-case} -g {general-numeric-sort} -i {ignore-nonprinting}
```
