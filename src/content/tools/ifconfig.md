---
id: network-config-ifconfig
namespace: network:config:ifconfig
name: ifconfig
description: Configure network interfaces
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.config.ifconfig
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
parameters: []
execution:
  template: "ifconfig"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Display help message"
    command: "ifconfig --help"
  - description: Display all network interfaces and their configuration
    command: ifconfig
  - description: View configuration details for a specific interface (e.g., eth0)
    command: ifconfig eth0
  - description: Enable a network interface (e.g., eth0)
    command: ifconfig eth0 up
  - description: Disable a network interface (e.g., eth0)
    command: ifconfig eth0 down
  - description: Assign an IP address to an interface (e.g., eth0)
    command: ifconfig eth0 192.168.1.10
  - description: Set a subnet mask on a network interface
    command: ifconfig eth0 netmask 255.255.255.0
  - description: Add an alias for a network interface with a separate IP address
    command: ifconfig eth0:0 192.168.1.20
  - description: Remove alias from a network interface
    command: ifconfig eth0:0 down
  - description: Set a broadcast address on a network interface
    command: ifconfig eth0 broadcast 192.168.1.255
  - description: Change the MAC address of a network interface
    command: ifconfig eth0 hw ether 00:11:22:33:44:55
related_tools:
  - network-config-ip
install:
    - method: apt
      package_name: "net-tools"
      commands:
        - "apt-get install -y net-tools"
---

# ifconfig — Configure network interfaces

## Overview

`ifconfig` is a command-line utility for configure network interfaces.

## Usage

```
ifconfig
```
