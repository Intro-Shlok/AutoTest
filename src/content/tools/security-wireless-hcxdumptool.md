---
id: security-wireless-hcxdumptool
namespace: security:wireless:hcxdumptool
name: hcxdumptool
description: Tool for capturing WLAN traffic and dumping PMKID and handshake captures for offline WPA cracking with hashcat.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.capture.pmkid
  - network.capture.handshake
  - network.sniff
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
  - hcxpcaptool
  - aircrack-ng
  - hashcat
artifacts:
  - type: wireless.capture.pcapng
    description: Captured WLAN traffic
    mime: application/vnd.tcpdump.pcap
    trust_level: verified
  - type: wireless.capture.pmkid
    description: PMKID hashes for cracking
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - packet-capture
    - pmkid-hash
    - handshake-capture
  consumes:
    - network-manipulation-interface
contract:
  inputs:
    - type: wireless.interface
      description: Wireless interface in monitor mode
    - type: wireless.channel
      description: Target channel
    - type: wireless.bssid
      description: Target AP BSSID
  outputs:
    - type: wireless.capture.pcapng
      description: Raw packet capture
      mime: application/vnd.tcpdump.pcap
    - type: wireless.capture.pmkid
      description: PMKID hash file
      mime: text/plain
  side_effects:
    - raw_socket_access
    - network_traffic
  resource_cost:
    cpu: medium
    memory_mb: 128
    network: low
    disk_io: high
resource_profile:
  cpu: medium
  memory_mb: 128
  network: low
  disk_io: high
allowed-tools:
  - hcxdumptool
  - hcxpcaptool
  - Bash
  - execFile
parameters:
  - name: interface
    type: string
    required: true
    description: "Wireless interface in monitor mode"
    aliases:
      - -i
      - --interface
  - name: output
    type: string
    required: false
    description: "Output file path"
    aliases:
      - -o
      - --output
  - name: channel
    type: string
    required: false
    description: "Channel list to hop"
    aliases:
      - -c
      - --channel
  - name: timeout
    type: integer
    required: false
    description: "Timeout in seconds"
    aliases:
      - -t
      - --timeout
  - name: enable_status
    type: boolean
    required: false
    description: "Enable real-time status display"
    aliases:
      - --enable_status
  - name: disable_deauth
    type: boolean
    required: false
    description: "Disable deauth detection"
    aliases:
      - --disable_deauth
  - name: disable_assoc
    type: boolean
    required: false
    description: "Disable association detection"
    aliases:
      - --disable_assoc
  - name: disable_probe
    type: boolean
    required: false
    description: "Disable probe request capture"
    aliases:
      - --disable_probe
  - name: essid
    type: string
    required: false
    description: "Filter by ESSID"
    aliases:
      - -E
      - --essid
  - name: bssid
    type: string
    required: false
    description: "Filter by BSSID"
    aliases:
      - -B
      - --bssid
  - name: write
    type: string
    required: false
    description: "Write raw packets to file"
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
  template: "hcxdumptool -i {interface} -o {output}"
  sandbox: execFile
  timeout_seconds: 86400
  shell: false
global_vars:
  interface: wlan0mon
  output: capture.pcapng
examples:
  - description: "Capture on all channels"
    command: hcxdumptool -i wlan0mon -o capture.pcapng
  - description: "Capture specific channel with status"
    command: hcxdumptool -i wlan0mon -o capture.pcapng -c 6 --enable_status
  - description: "Filter by BSSID"
    command: hcxdumptool -i wlan0mon -o capture.pcapng -B 00:11:22:33:44:55
  - description: "Filter by ESSID"
    command: hcxdumptool -i wlan0mon -o capture.pcapng -E MyNetwork
  - description: "Disable deauth detection"
    command: hcxdumptool -i wlan0mon -o capture.pcapng --disable_deauth
  - description: "Capture with timeout"
    command: hcxdumptool -i wlan0mon -o capture.pcapng -t 300
  - description: "Read from existing capture"
    command: hcxdumptool -r capture.pcapng
  - description: "Disable unnecessary detections"
    command: hcxdumptool -i wlan0mon -o capture.pcapng --disable_deauth --disable_assoc --disable_probe
references:
  - label: "hcxdumptool GitHub"
    url: "https://github.com/ZerBea/hcxdumptool"
  - label: "Hashcat WPA Cracking"
    url: "https://hashcat.net/wiki/doku.php?id=cracking_wpawpa2"
phase: exploitation
techniques:
  - credential-access
  - network-manipulation
items:
  - Hash
services: []
attack_types:
  - Discovery
features:
  - requires-root
install:
    - method: apt
      package_name: "hcxdumptool"
      commands:
        - "apt-get install -y hcxdumptool"
---

# hcxdumptool — WLAN Capture Tool for PMKID

hcxdumptool captures WLAN traffic and extracts PMKID (RSN PMKID) hashes and WPA handshakes for offline cracking with hashcat or John the Ripper.

## PMKID Attack

The PMKID attack does not require a full EAPOL 4-way handshake — only a single packet from the AP is needed. This makes it faster and more reliable than traditional deauth-based handshake capture.
