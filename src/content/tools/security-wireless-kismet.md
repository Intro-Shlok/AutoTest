---
id: security-wireless-kismet
namespace: security:wireless:kismet
name: kismet
description: Wireless network detector, sniffer, and intrusion detection system for 802.11 networks.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.detect
  - network.sniff
  - network.intrusion.detect
  - network.enumerate
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
  - aircrack-ng
  - wifite
  - wireshark
artifacts:
  - type: wireless.capture.pcap
    description: Captured 802.11 packet data
    mime: application/vnd.tcpdump.pcap
    trust_level: verified
  - type: wireless.log
    description: Kismet alert and event log
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - network-map
    - packet-capture
    - alert-log
  consumes:
    - network-manipulation-interface
    - config-file
contract:
  inputs:
    - type: wireless.interface
      description: Wireless interface in monitor mode
    - type: config.file
      description: Kismet configuration file
    - type: wireless.gps.data
      description: GPS data for wardriving
  outputs:
    - type: wireless.capture.pcap
      description: Packet capture output
      mime: application/vnd.tcpdump.pcap
    - type: wireless.map.data
      description: Detected networks with GPS coordinates
      mime: text/plain
  side_effects:
    - raw_socket_access
    - network_traffic
  resource_cost:
    cpu: high
    memory_mb: 512
    network: medium
    disk_io: high
resource_profile:
  cpu: high
  memory_mb: 512
  network: medium
  disk_io: high
allowed-tools:
  - kismet
  - Bash
  - execFile
parameters:
  - name: config
    type: file
    required: false
    description: "Path to Kismet configuration file"
    aliases:
      - -c
      - --config
  - name: server
    type: string
    required: false
    description: "Kismet server address"
    aliases:
      - -s
      - --server
  - name: port
    type: integer
    required: false
    description: "Kismet server port"
    aliases:
      - -p
      - --port
  - name: verbose
    type: boolean
    required: false
    description: "Enable verbose logging"
    aliases:
      - -v
      - --verbose
  - name: daemonize
    type: boolean
    required: false
    description: "Run as background daemon"
    aliases:
      - --daemonize
  - name: logging
    type: string
    required: false
    description: "Set logging types"
    aliases:
      - -l
      - --logging
  - name: no-gps
    type: boolean
    required: false
    description: "Disable GPS support"
    aliases:
      - -n
      - --no-gps
  - name: server-args
    type: string
    required: false
    description: "Additional arguments for kismet server"
    aliases:
      - --server-args
execution:
  template: "kismet"
  sandbox: execFile
  timeout_seconds: 86400
  shell: false
global_vars: {}
examples:
  - description: "Start Kismet with default interface"
    command: kismet
  - description: "Start with custom config file"
    command: kismet -c /etc/kismet/kismet.conf
  - description: "Run as daemon"
    command: kismet --daemonize
  - description: "Start with verbose logging"
    command: kismet -v -l /var/log/kismet
  - description: "Connect to remote Kismet server"
    command: kismet -s 192.168.1.100 -p 2501
  - description: "Disable GPS on embedded device"
    command: kismet -n
  - description: "Log only specific packet types"
    command: kismet -l alert,packet,gps
  - description: "Specify server arguments for sources"
    command: kismet --server-args "-t wlan0"
references:
  - label: "Kismet Official Site"
    url: "https://www.kismetwireless.net/"
  - label: "Kismet Documentation"
    url: "https://www.kismetwireless.net/documentation/"
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
      package_name: "kismet"
      commands:
        - "apt-get install -y kismet"
---

# Kismet — Wireless Network Detector

Kismet is a wireless network detector, sniffer, and intrusion detection system. It works with WiFi (802.11), Bluetooth, and other wireless protocols.

## Key Capabilities

- **Network discovery**: Detects hidden and non-beaconing networks
- **Packet sniffing**: Captures 802.11 traffic for offline analysis
- **WIDS**: Wireless intrusion detection with alerting
- **Wardriving**: GPS integration for mapping networks
- **Multi-source**: Supports multiple interfaces simultaneously
