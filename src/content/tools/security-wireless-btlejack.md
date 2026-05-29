---
id: security-wireless-btlejack
namespace: security:wireless:btlejack
name: btlejack
description: Bluetooth Low Energy (BLE) sniffing and jamming tool for security assessments of BLE devices.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - ble.sniff
  - ble.jam
  - ble.scan
  - ble.capture
platforms:
  - linux
risk_level: medium
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies:
  - python3
related_tools:
  - bluetoothctl
  - bettercap
  - hcitool
artifacts:
  - type: ble.capture.dump
    description: Captured BLE traffic dump
    mime: application/octet-stream
    trust_level: verified
  - type: ble.device.list
    description: Discovered BLE devices
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - device-list
    - capture-dump
    - jammed-devices
  consumes:
    - ble-interface
contract:
  inputs:
    - type: ble.interface
      description: BLE interface (hciX)
    - type: ble.channel
      description: BLE channel to monitor
  outputs:
    - type: ble.capture.dump
      description: Captured BLE traffic
      mime: application/octet-stream
    - type: ble.device.list
      description: Discovered BLE devices
      mime: text/plain
  side_effects:
    - raw_socket_access
    - network_traffic
  resource_cost:
    cpu: medium
    memory_mb: 64
    network: low
    disk_io: medium
resource_profile:
  cpu: medium
  memory_mb: 64
  network: low
  disk_io: medium
allowed-tools:
  - btlejack
  - Bash
  - execFile
parameters:
  - name: interface
    type: string
    required: false
    description: "BLE interface (hciX)"
    aliases:
      - -i
      - --interface
  - name: debug
    type: boolean
    required: false
    description: "Enable debug output"
    aliases:
      - -d
      - --debug
  - name: sniff
    type: boolean
    required: false
    description: "Sniff BLE connections"
    aliases:
      - -s
      - --sniff
  - name: follow
    type: boolean
    required: false
    description: "Follow a BLE connection"
    aliases:
      - -f
      - --follow
  - name: jam
    type: boolean
    required: false
    description: "Jam BLE connections"
    aliases:
      - -j
      - --jam
  - name: timeout
    type: integer
    required: false
    description: "Timeout in seconds"
    aliases:
      - -t
      - --timeout
  - name: channel
    type: string
    required: false
    description: "BLE channel (0-39)"
    aliases:
      - -c
      - --channel
  - name: output
    type: string
    required: false
    description: "Output file path"
    aliases:
      - -o
      - --output
  - name: verbose
    type: boolean
    required: false
    description: "Enable verbose output"
    aliases:
      - -v
      - --verbose
  - name: advertisements
    type: boolean
    required: false
    description: "Sniff advertisements only"
    aliases:
      - -a
      - --advertisements
  - name: write
    type: string
    required: false
    description: "Write capture to file"
    aliases:
      - -w
      - --write
  - name: read
    type: file
    required: false
    description: "Read from capture file"
    aliases:
      - -r
      - --read
execution:
  template: "btlejack -s"
  sandbox: execFile
  timeout_seconds: 86400
  shell: false
global_vars: {}
examples:
  - description: "Scan for BLE devices"
    command: btlejack -s
  - description: "Sniff on specific interface"
    command: btlejack -i hci0 -s
  - description: "Jam active BLE connections"
    command: btlejack -j
  - description: "Follow existing BLE connection"
    command: btlejack -f
  - description: "Sniff with output to file"
    command: btlejack -s -o capture.dump
  - description: "Sniff advertisements only"
    command: btlejack -a -o ads.dump
  - description: "Sniff with debug and verbose"
    command: btlejack -i hci0 -s -d -v
  - description: "Specific channel sniffing"
    command: btlejack -c 37 -s
references:
  - label: "Btlejack GitHub"
    url: "https://github.com/virtualabs/btlejack"
  - label: "BLE Security Research"
    url: "https://github.com/virtualabs/btlejack/wiki"
phase: exploitation
techniques:
  - credential-access
  - network-manipulation
items:
  - NoCreds
services: []
attack_types:
  - Discovery
features:
  - requires-root
install:
    - method: pip
      package_name: "btlejack"
      commands:
        - "pip install btlejack"
---

# Btlejack — Bluetooth Low Energy Sniffer

Btlejack is a Bluetooth Low Energy (BLE) sniffing and jamming tool. It can capture BLE packets, follow connections, and jam BLE devices for security assessment purposes.

## Capabilities

- **Sniffing**: Passive capture of BLE advertising and data channels
- **Jamming**: Active jamming of BLE connections
- **Connection following**: Decrypt and follow established BLE connections
- **Dump reading**: Offline analysis of captured BLE traffic
