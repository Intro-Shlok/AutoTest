---
id: system-file-find
namespace: system:file:find
name: find
description: Search for files in a directory hierarchy
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.file.find
  - system.file.delete
  - system.file.search
  - system.file.process
  - system.file.copy
  - system.file.move
  - security.execution.command
  - security.privilege-escalation.shell
  - system.file.read
  - system.file.write
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
  - output-json
  - process-manip
techniques:
  - defense-evasion
  - data-manipulation
  - process-manip
  - collection
  - enumeration
  - credential-access
  - discovery
  - lateral-movement
  - execution
  - persistence
  - privilege-escalation
parameters:
  - name: flag-d
    type: string
    required: false
    description: "Set the flag-d parameter"
    aliases:
      - -d
      - -f
      - -n
      - -r
      - -w
  - name: flag-d-2
    type: string
    required: false
    description: "-noleaf -xdev -ignore_readdir_race -noignore_readdir_race"
    aliases:
      - -d
      - -f
      - -f
      - -m
      - -m
  - name: flag-a
    type: string
    required: false
    description: "N -empty -false -fstype TYPE -gid N -group NAME -ilname PATTERN
      -iname PATTERN -inum N -iwholename PATTERN -iregex PATTERN -links N -lname PATTERN
      -mmin N -mtime N -name PATTERN -newer FILE -nouser..."
    aliases:
      - -a
      - -a
      - -a
      - -c
      - -c
      - -c
  - name: flag-d-3
    type: string
    required: false
    description: "FILE -fprint FILE -ls -fls FILE -prune -quit -exec COMMAND ; -exec
      COMMAND {} + -ok COMMAND ; -execdir COMMAND ; -execdir COMMAND {} + -okdir COMMAND"
    aliases:
      - -d
      - -p
      - -p
      - -f
      - -p
  - name: help
    type: string
    required: false
    description: "display this help and exit"
    aliases:
      - --help
  - name: version
    type: string
    required: false
    description: "output version information and exit"
    aliases:
      - --version
  - name: exec
    description: Execute a command on each matched file
    type: string
  - name: ok
    description: Like -exec but prompts before each execution
    type: string
  - name: execdir
    description: Execute command from the directory of the matched file
    type: string
  - name: fprintf
    description: Print formatted output to a file
    type: string
  - name: perm
    description: Find files with specific permissions (e.g., /4000 for SUID)
    type: string
  - name: user
    description: Find files owned by a specific user
    type: string
  - name: mmin
    description: Find files modified N minutes ago
    type: string
  - name: size
    description: Find files of a specific size
    type: string
execution:
  template: "find -d {flag-d} -d {flag-d-2} -a {flag-a} -d {flag-d-3} --help {help}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with flag-d"
    command: "find ${flag-d}"
  - description: "Display help message"
    command: "find --help"
  - description: Can be used to execute arbitrary commands on a system and spawn shells
      either indirectly
    command: "find . -name i_do_not_exist -or -exec perl -e 'exec sh' ; -quit\n"
  - description: or directly.
    command: "find . -exec /bin/sh ; -quit\n"
  - description: Can be used to execute arbitrary commands on a system.
    command: "find . -name i_do_not_exist -or -exec ls ; -quit\n"
  - description: Reading of files is possible by executing cat.
    command: "find /etc/passwd -exec cat {} ;\n"
  - description: Find has various capabilities to write to files and it is recommended
      to read the manual for more details, especially its fprintf and 'UNUSUAL FILENAMES'
      sections.
    command: "find . -fprintf /root/.authorized_keys 'ssh-rsa ...' -quit\n"
  - description: 'Argument injection: spawn interactive shell: Can be used to execute
      arbitrary commands on a system and spawn shells either indirectly'
    command: find . -name i_do_not_exist -or -exec perl -e 'exec sh' ; -quit
  - description: 'Argument injection: spawn interactive shell: or directly.'
    command: find . -exec /bin/sh ; -quit
  - description: 'Argument injection: execute arbitrary command: Can be used to execute
      arbitrary commands on a system.'
    command: find . -name i_do_not_exist -or -exec ls ; -quit
  - description: 'Argument injection: read local file: Reading of files is possible
      by executing cat.'
    command: find /etc/passwd -exec cat {} ;
  - description: "Argument injection: write to local file: Find has various capabilities
      to write to files and it is recommended to read the manual for more details,
      especially its fprintf and 'UNUSUAL FILENAMES' sections."
    command: find . -fprintf /root/.authorized_keys 'ssh-rsa ...' -quit
  - description: NetRunners usefull/shell
    command: find / -perm -4000 2>/dev/null
  - description: "Find files by case-insensitive extension, such as `.jpg`, `.JPG`,
      & `.jpG`). By default, find(1) uses glob pathname pattern matching. To avoid
      shell interpretation, the glob either must be expanded or the string quoted.
      Period is optional; it's implied unless a path is provided. find(1) works recursively
      unless otherwise directed (IE: `-maxdepth [N]`)."
    command: find . -iname '*.jpg'
  - description: Find directories.
    command: find . -type d
  - description: Find files. Specifically files; not directories, links, FIFOs, etc.
    command: find . -type f
  - description: Find files set to the provided octal mode (permissions).
    command: find . -type f -perm 777
  - description: Find files with setuid bit set, keeping to the same filesystem.
    command: find . -xdev \( -perm -4000 \) -type f -print0 | xargs -0 ls -l
  - description: "The above is a useful demonstration of some pitfalls into which
      a user can fall, where the below is the above but corrected. Here is why: *
      The `.` (current working directory) is assumed when no path is provided. * Group
      syntax (parentheses) was used, but nothing was actually grouped. * A lot of
      people have their ls(1) command aliased in many ways, - potentially causing
      problems with the output and how xargs(1) handles it. By escaping the command,
      we temporarily override any aliases and even functions by the same name. * At
      least in my experience, the prior xargs(1) is not as reliable. * The `-print0`
      and `xargs -0` is great, but unnecessary (except when?). However, it might be
      more preferred to simply use find(1)'s own `-printf` flag, in order to avoid
      the need for xargs(1) and ls(1), which should be many times faster, and allows
      for more specificity."
    command: find -perm -4000 -type f -print0 | xargs -I '{}' -0 \ls -l '{}'
  - description: Find and remove files with case-sensitive extension of `.txt`.
    command: find [PATH] -name '*.txt' -exec rm '{}' \;
  - description: The above is much more efficiently written as shown below, as find(1)
      has its own built-in delete function, not to mention a single rm(1) process
      was previously executed for each file processed, which is comparatively slow.
    command: find [PATH] -name '*.txt' -delete
  - description: Find files with extension '.txt' and look for a string into them.
    command: find ./path/ -name '*.txt' | xargs grep 'string'
  - description: Find files with size bigger than 5 Mb and sort them by size.
    command: find . -size +5M -type f -print0 | xargs -0 ls -Ssh | sort -z
  - description: Find files bigger thank 2 MB and list them.
    command: "find . -type f -size +20000k -exec ls -lh {} \\; | awk '{ print $9 \"\
      : \" $5 }'"
  - description: "Alternative, faster approach* to the above. Why it's faster: * No
      need for an external process, like ls(1). * The use of `;` with the `-exec`
      flag executes an ls(1) process for each file found, which is comparatively very
      slow. * The `printf` feature is built in and special to awk(1). That said, awk(1)
      or gawk(1) is doing a little more here, in order to get somewhat of a human-readable
      file size, but its impact is likely negligible."
    command: find -type f -size +20000k -printf '%s %P\n' |
  - description: 'cheat.sheets: find'
    command: awk "{printf(\"%'dM %s\n\", \$1 / (1024 * 1024), \$2)}"
  - description: Find files modified more than 7 days ago and list file information.
    command: find . -type f -mtime +7d -ls
  - description: Find symlinks owned by the given user, then list file information.
    command: find -type l -user [NAME] -ls
  - description: The following may be the syntax used on a Mac, however this is not
      valid on Linux, or at least version 4.7.0. All flags in GNU find(1) are one
      `-` only.
    command: find . -type l --user=[NAME] -ls
  - description: Search for and delete empty directories.
    command: find . -type d -empty -exec rmdir {} \;
  - description: A far more efficient approach to the above. If no path is provided,
      then the current working directory (CWD) is assumed, making the `.` superfluous.
    command: find -type d -empty -delete
  - description: Search for directories named `build` at a maximum depth of 2 directories.
      This means that find will not recursively search beyond two levels.
    command: find . -maxdepth 2 -name build -type d
  - description: Search all files which are not in a `.git` directory. Depending on
      the shell used, the bang (`!`) may need to be escaped, to avoid shell interpretation.
      Alternatively, although non-POSIX, the `-not` flag can be used.
    command: find . \! -iwholename '*.git*' -type f
  - description: Find all files that have the same inode (indicating hard link) as
      FILE. All output going to STDERR (typically error messages) will also be redirected
      to `/dev/null`, a special pseudo-file where data is sent to die.
    command: find . -type f -samefile [FILE] 2>/dev/null
  - description: Find all files in the current directory and modify their permissions.
    command: find . -type f -exec chmod 644 {} \;
  - description: Find files with extension `.txt` and edit all of them with vim(1).
      The use of `+` (escaped to avoid shell interpretation) with `-exec` means that
      only one process (in this case, `vim`) per `exec`ution is used. If `;` is instead
      used (would also need escaping), then one `vim` process would be used per file.
    command: find . -iname '*.txt' -exec vim {} \+
  - description: Find files with extension `.png`, then rename their extension to
      `.jpg`. It's highly important that `\;` is used here, instead of `\+`, otherwise
      it'd make a right mess of the files, due to the way in which mv(1) works.
    command: find . -type f -iname '*.png' -exec bash -c 'mv "$0" "${0%.*}.jpg"' {}
      \;
  - description: Use logic and grouping to delete extension-specific files.
    command: find \( -iname "*.jpg" -or -iname "*.sfv" -or -iname "*.xspf" \) -type
      f -delete
  - description: List executable files, by basename, found within PATH.
    command: find ${PATH//:/ } -type f -executable -printf "%P\n"
phase: enumeration
related_tools:
  - system-file-xargs
install:
    - method: apt
      package_name: "findutils"
      commands:
        - "apt-get install -y findutils"
    - method: brew
      package_name: "findutils"
      commands:
        - "brew install findutils"
---

# find — Search for files in a directory hierarchy

## Overview

`find` is a command-line utility for search for files in a directory hierarchy.

## Usage

```
find -d {flag-d} -d {flag-d-2} -a {flag-a} -d {flag-d-3} --help {help}
```
