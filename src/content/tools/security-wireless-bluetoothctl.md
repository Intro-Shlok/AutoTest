---
id: security-wireless-bluetoothctl
namespace: security:wireless:bluetoothctl
name: bluetoothctl
description: Command-line Bluetooth controller for device scanning, pairing, and management via BlueZ.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - bluetooth.scan
  - bluetooth.pair
  - bluetooth.discover
  - bluetooth.manage
platforms:
  - linux
risk_level: medium
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies: []
related_tools:
  - btlejack
  - hcitool
  - gatttool
artifacts:
  - type: bluetooth.device.list
    description: List of discovered Bluetooth devices
    mime: text/plain
    trust_level: verified
  - type: bluetooth.device.info
    description: Detailed device information
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - device-list
    - device-info
    - paired-devices
  consumes:
    - bluetooth-adapter
contract:
  inputs:
    - type: bluetooth.adapter
      description: Bluetooth adapter index
  outputs:
    - type: bluetooth.device.list
      description: Discovered Bluetooth devices
      mime: text/plain
    - type: bluetooth.device.info
      description: Detailed device attribute information
      mime: text/plain
  side_effects:
    - network_traffic
    - network_traffic
  resource_cost:
    cpu: low
    memory_mb: 16
    network: none
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 16
  network: none
  disk_io: low
allowed-tools:
  - bluetoothctl
  - Bash
  - execFile
parameters:
  - name: scan
    type: boolean
    required: false
    description: "Scan for Bluetooth devices"
    aliases:
      - scan
      - --scan
  - name: advertise
    type: boolean
    required: false
    description: "Enable advertising"
    aliases:
      - advertise
      - --advertise
  - name: discoverable
    type: boolean
    required: false
    description: "Make adapter discoverable"
    aliases:
      - discoverable
      - --discoverable
  - name: pairable
    type: boolean
    required: false
    description: "Make adapter pairable"
    aliases:
      - pairable
      - --pairable
  - name: power
    type: string
    required: false
    description: "Power control (on/off)"
    aliases:
      - power
      - --power
  - name: agent
    type: string
    required: false
    description: "Register agent type"
    aliases:
      - agent
      - --agent
  - name: default-agent
    type: boolean
    required: false
    description: "Set as default agent"
    aliases:
      - default-agent
      - --default-agent
  - name: pair
    type: string
    required: false
    description: "Pair with device by MAC"
    aliases:
      - pair
      - --pair
  - name: trust
    type: string
    required: false
    description: "Trust device by MAC"
    aliases:
      - trust
      - --trust
  - name: connect
    type: string
    required: false
    description: "Connect to device by MAC"
    aliases:
      - connect
      - --connect
  - name: info
    type: string
    required: false
    description: "Show device info by MAC"
    aliases:
      - info
      - --info
execution:
  template: "bluetoothctl"
  sandbox: execFile
  timeout_seconds: 3600
  shell: true
global_vars: {}
examples:
  - description: "Start interactive bluetoothctl session"
    command: bluetoothctl
  - description: "Enable scanning and power on"
    command: echo -e "power on\nscan on" | bluetoothctl
  - description: "List paired devices"
    command: bluetoothctl devices
  - description: "Show adapter information"
    command: bluetoothctl show
  - description: "Pair with a device"
    command: echo -e "pair AA:BB:CC:DD:EE:FF\nconnect AA:BB:CC:DD:EE:FF" | bluetoothctl
  - description: "Trust and connect"
    command: echo -e "trust AA:BB:CC:DD:EE:FF\nconnect AA:BB:CC:DD:EE:FF" | bluetoothctl
  - description: "Show device information"
    command: bluetoothctl info AA:BB:CC:DD:EE:FF
  - description: "Register agent and make pairable"
    command: echo -e "agent on\ndefault-agent\npairable on" | bluetoothctl
references:
  - label: "BlueZ Bluetoothctl"
    url: "https://github.com/bluez/bluez/tree/master/client"
  - label: "BlueZ Documentation"
    url: "http://www.bluez.org/documentation/"
phase: enumeration
techniques:
  - discovery
  - network-manipulation
items:
  - NoCreds
services: []
attack_types:
  - Discovery
features:
  - requires-root
install:
    - method: apt
      package_name: "bluez"
      commands:
        - "apt-get install -y bluez"
---

# bluetoothctl — Bluetooth Device Controller

bluetoothctl is the primary command-line interface for BlueZ, the official Linux Bluetooth protocol stack. It provides interactive and non-interactive control over Bluetooth adapters and devices.

## Common Commands

| Command | Description |
|---------|-------------|
| `scan on/off` | Enable/disable device discovery |
| `pair <mac>` | Pair with a Bluetooth device |
| `connect <mac>` | Connect to a paired device |
| `trust <mac>` | Mark device as trusted |
| `info <mac>` | Show detailed device information |
| `devices` | List all known devices |
| `show` | Show adapter information |
