---
id: network-remote-telnet
namespace: network:remote:telnet
name: telnet
description: Telnet protocol client for remote connections
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.remote.telnet
  - network.remote.shell
platforms:
  - linux
risk_level: low
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
features:
  - remote
  - network-intensive
techniques:
  - command-and-control
  - lateral-movement
parameters:
  - name: ipv4
    type: string
    required: false
    description: "use only IPv4"
    aliases:
      - "-4"
      - --ipv4
  - name: ipv6
    type: string
    required: false
    description: "use only IPv6"
    aliases:
      - "-6"
      - --ipv6
  - name: binary
    type: string
    required: false
    description: "use an 8-bit data transmission"
    aliases:
      - "-8"
      - --binary
  - name: login
    type: string
    required: false
    description: "attempt automatic login"
    aliases:
      - -a
      - --login
  - name: bind
    type: string
    required: false
    description: "bind to specific local ADDRESS"
    aliases:
      - -b
      - --bind
  - name: no-rc
    type: string
    required: false
    description: "do not read the user's .telnetrc file"
    aliases:
      - -c
      - --no-rc
  - name: debug
    type: string
    required: false
    description: "turn on debugging"
    aliases:
      - -d
      - --debug
  - name: escape
    type: string
    required: false
    description: "use CHAR as an escape character"
    aliases:
      - -e
      - --escape
  - name: no-escape
    type: string
    required: false
    description: "use no escape character"
    aliases:
      - -E
      - --no-escape
  - name: no-login
    type: string
    required: false
    description: "do not automatically login to the remote system"
    aliases:
      - -K
      - --no-login
  - name: user
    type: string
    required: false
    description: "attempt automatic login as USER"
    aliases:
      - -l
      - --user
  - name: binary-output
    type: string
    required: false
    description: "use an 8-bit data transmission for output only"
    aliases:
      - -L
      - --binary-output
  - name: trace
    type: file
    required: false
    description: "record trace information into FILE"
    aliases:
      - -n
      - --trace
  - name: rlogin
    type: string
    required: false
    description: "use a user-interface similar to rlogin"
    aliases:
      - -r
      - --rlogin
  - name: encrypt
    type: string
    required: false
    description: "encrypt the data stream, if possible"
    aliases:
      - -x
      - --encrypt
  - name: realm
    type: string
    required: false
    description: "obtain tickets for the remote host in REALM"
    aliases:
      - -k
      - --realm
  - name: disable-auth
    type: string
    required: false
    description: "disable type ATYPE authentication"
    aliases:
      - -X
      - --disable-auth
  - name: help
    type: string
    required: false
    description: "give this help list"
    aliases:
      - -?
      - --help
  - name: usage
    type: string
    required: false
    description: "give a short usage message"
    aliases:
      - --usage
  - name: version
    type: string
    required: false
    description: "print program version"
    aliases:
      - -V
      - --version
execution:
  template: "telnet -4 {ipv4} -6 {ipv6} -8 {binary} -a {login} -b {bind}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
global_vars:
  target: ip
  port: port
examples:
  - description: "Basic usage with ipv4"
    command: "telnet ${ipv4}"
  - description: "Display help message"
    command: "telnet --help"
  - description: Connect to a remote host on a specified port
    command: telnet hostname port
  - description: Open a telnet session without specifying a port (default to port
      23)
    command: telnet hostname
  - description: Open a telnet session with option for terminal type
    command: telnet -l username hostname
  - description: Interrupt a running command or return to the telnet prompt
    command: Ctrl + ] (Escape sequence, type this combo while in a telnet session)
  - description: Display telnet’s internal help
    command: telnet help
  - description: Telnet quit command to exit the session
    command: quit (Type this command within the telnet session to exit)
  - description: Set or show telnet options
    command: telnet set option (Enter this within the telnet command line to configure
      options)
  - description: Send special telnet sequence to the host
    command: send set_sequence_name (Enter this within a telnet session to send specific
      sequences such as break)
install:
    - method: apt
      package_name: "telnet"
      commands:
        - "apt-get install -y telnet"
---

# telnet — Telnet protocol client for remote connections

## Overview

`telnet` is a command-line utility for telnet protocol client for remote connections.

## Usage

```
telnet -4 {ipv4} -6 {ipv6} -8 {binary} -a {login} -b {bind}
```
