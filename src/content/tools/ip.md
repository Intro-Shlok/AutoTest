---
id: network-config-ip
namespace: network:config:ip
name: ip
description: Show/manipulate routing, devices, policy routing and tunnels
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.config.ip
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
techniques:
  - defense-evasion
  - network-manipulation
  - discovery
  - command-and-control
  - enumeration
  - execution
  - exfiltration
  - lateral-movement
parameters:
  - name: flag-h
    type: file
    required: false
    description: "-f[amily] { inet | inet6 | mpls | bridge | link } | -4 | -6 | -M
      | -B | -0 | -l[oops] { maximum-addr-flush-attempts } | -echo | -br[ief] | -o[neline]
      | -t[imestamp] | -ts[hort] | -b[atch] [filename..."
    aliases:
      - -h
      - -r
      - -i
      - -j
      - -p
    enum:
      - inet
      - inet6
      - mpls
      - bridge
      - link
execution:
  template: "ip -h {flag-h}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Use flag-h flag"
    command: "ip inet"
  - description: "Display help message"
    command: "ip --help"
  - description: Display the current IP addresses and network interfaces
    command: ip addr show
  - description: Display the routing table
    command: ip route show
  - description: Add a new IP address to an interface
    command: ip addr add 192.168.1.100/24 dev eth0
  - description: Delete an IP address from an interface
    command: ip addr del 192.168.1.100/24 dev eth0
  - description: Bring an interface up
    command: ip link set dev eth0 up
  - description: Bring an interface down
    command: ip link set dev eth0 down
  - description: Show network interfaces and link status
    command: ip link show
  - description: Add a new default gateway
    command: ip route add default via 192.168.1.1
  - description: Delete the default gateway
    command: ip route del default
  - description: Flush all IP addresses on an interface
    command: ip addr flush dev eth0
  - description: Change the MAC address of an interface
    command: ip link set dev eth0 address 00:11:22:33:44:55
  - description: Show information about tunnels
    command: ip tunnel show
  - description: 'Shortcut: Show brief information about IP addresses and devices'
    command: ip -brief addr show
  - description: 'Shortcut: Show brief information about link status'
    command: ip -brief link show
phase: enumeration
related_tools:
  - network-config-ifconfig
install:
    - method: apt
      package_name: "iproute2"
      commands:
        - "apt-get install -y iproute2"
---

# ip — Show/manipulate routing, devices, policy routing and tunnels

## Overview

`ip` is a command-line utility for show/manipulate routing, devices, policy routing and tunnels.

## Usage

```
ip -h {flag-h}
```
