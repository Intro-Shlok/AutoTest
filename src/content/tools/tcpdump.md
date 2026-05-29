---
id: network-capture-tcpdump
namespace: network:capture:tcpdump
name: tcpdump
description: Dump traffic on a network interface
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.capture.tcpdump
  - network.capture.packet
  - network.capture.sniff
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
  - requires-root
  - streaming
techniques:
  - network-sniffing
  - discovery
  - recon
  - command-and-control
parameters:
  - name: flag-r
    type: array
    required: false
    description: "read packets from a network interface. It can also be run with the
      -V flag, which causes it to read a list of saved packet files. In all cases,
      only packets that match expression will be processed ..."
    aliases:
      - -r
  - name: flag-b
    type: string
    required: false
    description: "Print the AS number in BGP packets in ASDOT notation rather than"
    aliases:
      - -b
  - name: flag-B
    template_key: flag-b
    type: string
    required: false
    description: "--buffer-size=buffer_size Set the operating system capture buffer
      size to buffer_size, in units of KiB (1024 bytes)"
    aliases:
      - -B
  - name: flag-c
    type: string
    required: false
    description: "Exit after receiving count packets"
    aliases:
      - -c
  - name: count
    type: string
    required: false
    description: "Print only on stdout the packet count when reading capture file(s)
      instead of parsing/printing the packets. If a filter is specified on the command
      line, tcpdump counts only packets that were match..."
    aliases:
      - --count
  - name: flag-C
    template_key: flag-c
    type: string
    required: false
    description: "Before writing a raw packet to a savefile, check whether the file
      is currently larger than file_size and, if so, close the current savefile and
      open a new one. Savefiles after the first savefile wi..."
    aliases:
      - -C
  - name: flag-d
    type: string
    required: false
    description: "Dump the compiled packet-matching code in a human readable form"
    aliases:
      - -d
  - name: flag-i
    type: string
    required: false
    description: "In this case the DLT defaults to EN10MB and can be set to"
    aliases:
      - -i
  - name: flag-d-2
    type: string
    required: false
    description: "Dump packet-matching code as a C program fragment"
    aliases:
      - -d
  - name: flag-d-3
    type: string
    required: false
    description: "Dump packet-matching code as decimal numbers (preceded with a"
    aliases:
      - -d
  - name: flag-D
    template_key: flag-d
    type: array
    required: false
    description: "--list-interfaces Print the list of the network interfaces available
      on the system and on which tcpdump can capture packets. For each network in‐
      terface, a number and an interface name, possibly f..."
    aliases:
      - -D
  - name: flag-a
    type: string
    required: false
    description: "where the interface name is a somewhat complex string"
    aliases:
      - -a
  - name: flag-e
    type: string
    required: false
    description: "Print the link-level header on each dump line. This can be used"
    aliases:
      - -e
  - name: flag-f
    type: integer
    required: false
    description: "Print `foreign' IPv4 addresses numerically rather than symboli‐"
    aliases:
      - -f
  - name: flag-F
    template_key: flag-f
    type: string
    required: false
    description: "Use file as input for the filter expression. An additional ex‐ pression
      given on the command line is ignored"
    aliases:
      - -F
  - name: flag-g
    type: string
    required: false
    description: "--ip-oneline Do not insert a line break after the IP header in verbose
      mode"
    aliases:
      - -g
  - name: flag-G
    template_key: flag-g
    type: file
    required: false
    description: "If specified, rotates the dump file specified with the -w option
      every rotate_seconds seconds. Savefiles will have the name spec‐ ified by -w
      which should include a time format as defined by strfti..."
    aliases:
      - -G
  - name: flag-h
    type: string
    required: false
    description: "--help Print the tcpdump and libpcap version strings, print a usage
      mes‐ sage, and exit"
    aliases:
      - -h
  - name: version
    type: string
    required: false
    description: "Print the tcpdump and libpcap version strings and exit"
    aliases:
      - --version
  - name: flag-i-2
    type: array
    required: false
    description: "--interface=interface Listen, report the list of link-layer types,
      report the list of time stamp types, or report the results of compiling a filter
      ex‐ pression on interface. If unspecified and if ..."
    aliases:
      - -i
  - name: flag-I
    template_key: flag-i
    type: string
    required: false
    description: "--monitor-mode Put the interface in \"monitor mode\"; this is supported
      only on IEEE 802.11 Wi-Fi interfaces, and supported only on some operat‐ ing
      systems"
    aliases:
      - -I
  - name: immediate-mode
    type: string
    required: false
    description: "Capture in \"immediate mode\". In this mode, packets are delivered
      to tcpdump as soon as they arrive, rather than being buffered for efficiency.
      This is the default when printing packets rather tha..."
    aliases:
      - --immediate-mode
  - name: flag-j
    type: string
    required: false
    description: "--time-stamp-type=tstamp_type Set the time stamp type for the capture
      to tstamp_type. The names to use for the time stamp types are given in pcap-tstamp(7);
      not all the types listed there will nece..."
    aliases:
      - -j
  - name: flag-J
    template_key: flag-j
    type: string
    required: false
    description: "--list-time-stamp-types List the supported time stamp types for
      the interface and exit. If the time stamp type cannot be set for the interface,
      no time stamp types are listed"
    aliases:
      - -J
  - name: time-stamp-precision
    type: number
    required: false
    description: "When capturing, set the time stamp precision for the capture to
      tstamp_precision. Note that availability of high precision time stamps (nanoseconds)
      and their actual accuracy is platform and hardwa..."
    aliases:
      - --time-stamp-precision
  - name: micro
    type: number
    required: false
    description: "--nano Shorthands for --time-stamp-precision=micro or --time-stamp-pre‐
      cision=nano, adjusting the time stamp precision accordingly. When reading packets
      from a savefile, using --micro truncates ti..."
    aliases:
      - --micro
  - name: flag-K
    template_key: flag-k
    type: string
    required: false
    description: "--dont-verify-checksums Don't attempt to verify IP, TCP, or UDP
      checksums. This is use‐ ful for interfaces that perform some or all of those
      checksum calculation in hardware; otherwise, all outgoin..."
    aliases:
      - -K
  - name: flag-l
    type: string
    required: false
    description: "Make stdout line buffered. Useful if you want to see the data"
    aliases:
      - -l
  - name: flag-U
    template_key: flag-u
    type: string
    required: false
    description: "be ``packet-buffered'', so that the output is written to stdout
      at the end of each packet rather than at the end of each line; this is buffered
      on all platforms, including Windows"
    aliases:
      - -U
      - -l
  - name: flag-L
    template_key: flag-l
    type: array
    required: false
    description: "--list-data-link-types List the known data link types for the interface,
      in the speci‐ fied mode, and exit. The list of known data link types may be
      dependent on the specified mode; for example, on..."
    aliases:
      - -L
execution:
  template: "tcpdump -r {flag-r} -b {flag-b} -B {flag-b} -c {flag-c} --count {count}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
global_vars:
  port: port
examples:
  - description: "Display help message"
    command: "tcpdump --help"
  - description: Capture packets from a specific network interface
    command: tcpdump -i eth0
  - description: Capture only a certain number of packets
    command: tcpdump -c 10
  - description: Capture and write packets to a file for later analysis
    command: tcpdump -w capture.pcap
  - description: Read packets from a file
    command: tcpdump -r capture.pcap
  - description: Capture packets from a specific host
    command: tcpdump host 192.168.1.1
  - description: Capture packets from a specific port
    command: tcpdump port 80
  - description: Capture packets based on a specific protocol (e.g., TCP)
    command: tcpdump tcp
  - description: Capture packets and filter for HTTP traffic
    command: tcpdump 'tcp port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2))
      != 0)'
  - description: Capture packets from a specific source IP
    command: tcpdump src 192.168.1.1
  - description: Capture packets to a specific destination IP
    command: tcpdump dst 192.168.1.2
  - description: Display captured packets with timestamp
    command: tcpdump -tttt
  - description: Capture packets and display with verbose output
    command: tcpdump -v
  - description: Capture packets and display with extra verbose output
    command: tcpdump -vv
  - description: Capture packets and resolve hostnames
    command: tcpdump -n
  - description: Capture packets and disable resolving hostnames
    command: tcpdump -nn
  - description: Capture packets and show link-layer headers
    command: tcpdump -e
  - description: Capture IPv6 packets
    command: tcpdump ip6
  - description: Capture packets larger than a specific size
    command: tcpdump greater 1024
install:
    - method: apt
      package_name: "tcpdump"
      commands:
        - "apt-get install -y tcpdump"
    - method: brew
      package_name: "tcpdump"
      commands:
        - "brew install tcpdump"
---

# tcpdump — Dump traffic on a network interface

## Overview

`tcpdump` is a command-line utility for dump traffic on a network interface.

## Usage

```
tcpdump -r {flag-r} -b {flag-b} -B {flag-b} -c {flag-c} --count {count}
```
