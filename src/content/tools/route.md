---
id: network-config-route
namespace: network:config:route
name: route
description: Show/manipulate the IP routing table
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.config.route
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
  - discovery
  - network-manipulation
parameters:
  - name: verbose
    type: string
    required: false
    description: "be verbose"
    aliases:
      - -v
      - --verbose
  - name: numeric
    type: string
    required: false
    description: "don't resolve names"
    aliases:
      - -n
      - --numeric
  - name: extend
    type: string
    required: false
    description: "display other/more information"
    aliases:
      - -e
      - --extend
  - name: fib
    type: string
    required: false
    description: "display Forwarding Information Base (default)"
    aliases:
      - -F
      - --fib
  - name: cache
    type: string
    required: false
    description: "display routing cache instead of FIB"
    aliases:
      - -C
      - --cache
execution:
  template: "route -v {verbose} -n {numeric} -e {extend} -F {fib} -C {cache}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with verbose"
    command: "route ${verbose}"
  - description: "Display help message"
    command: "route --help"
  - description: Display the IP routing table
    command: route
  - description: Add a new route to a specific network
    command: route add -net {network} netmask {netmask} gw {gateway} {interface}
  - description: Add a default gateway
    command: route add default gw {gateway} {interface}
  - description: Delete a route to a specific network
    command: route del -net {network} netmask {netmask} gw {gateway} {interface}
  - description: Delete the default gateway
    command: route del default
  - description: Add a route to a host
    command: route add -host {destination-host} gw {gateway} {interface}
  - description: Change the metric of a route
    command: route change -net {network} netmask {netmask} gw {gateway} {interface}
      metric {metric}
  - description: Show the routing table continuously with a delay
    command: watch -n 1 route -n
install:
    - method: apt
      package_name: "net-tools"
      commands:
        - "apt-get install -y net-tools"
---

# route — Show/manipulate the IP routing table

## Overview

`route` is a command-line utility for show/manipulate the ip routing table.

## Usage

```
route -v {verbose} -n {numeric} -e {extend} -F {fib} -C {cache}
```
