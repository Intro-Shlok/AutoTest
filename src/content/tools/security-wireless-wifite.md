---
id: security-wireless-wifite
namespace: security:wireless:wifite
name: wifite
description: Automated wireless attack tool that orchestrates aircrack-ng, reaver, and other tools to audit WiFi networks.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.audit
  - network.crack.wep
  - network.crack.wpa
  - network.wps.bruteforce
  - network.deauth
  - network.pmkid
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
  - reaver
  - bully
  - kismet
artifacts:
  - type: wireless.crack.key
    description: Cracked WPA/WEP key
    mime: text/plain
    trust_level: verified
  - type: wireless.capture.handshake
    description: Captured WPA handshake
    mime: application/vnd.tcpdump.pcap
    trust_level: verified
workflow_edges:
  produces:
    - cracked-key
    - handshake-capture
    - pmkid-hash
  consumes:
    - network-manipulation-interface
    - wordlist
contract:
  inputs:
    - type: wireless.interface
      description: Wireless interface name
    - type: wordlist.file
      description: Dictionary file for cracking
  outputs:
    - type: wireless.crack.key
      description: Cracked wireless key
      mime: text/plain
    - type: wireless.capture.handshake
      description: Captured handshake
      mime: application/vnd.tcpdump.pcap
  side_effects:
    - network_traffic
    - raw_socket_access
    - network_traffic
  resource_cost:
    cpu: medium
    memory_mb: 128
    network: low
    disk_io: low
resource_profile:
  cpu: medium
  memory_mb: 128
  network: low
  disk_io: low
allowed-tools:
  - wifite
  - Bash
  - execFile
parameters:
  - name: interface
    type: string
    required: false
    description: "Wireless interface name"
    aliases:
      - -i
      - --interface
  - name: essid
    type: string
    required: false
    description: "Target network ESSID"
    aliases:
      - -e
      - --essid
  - name: bssid
    type: string
    required: false
    description: "Target network BSSID"
    aliases:
      - -b
      - --bssid
  - name: channel
    type: string
    required: false
    description: "Target channel"
    aliases:
      - -c
      - --channel
  - name: wep
    type: boolean
    required: false
    description: "Attack only WEP networks"
    aliases:
      - -w
      - --wep
  - name: wpa
    type: boolean
    required: false
    description: "Attack only WPA networks"
    aliases:
      - -t
      - --wpa
  - name: verbose
    type: boolean
    required: false
    description: "Enable verbose output"
    aliases:
      - -v
      - --verbose
  - name: no-wps
    type: boolean
    required: false
    description: "Skip WPS PIN attacks"
    aliases:
      - --no-wps
  - name: no-deauth
    type: boolean
    required: false
    description: "Skip deauth attacks"
    aliases:
      - --no-deauth
  - name: pmkid
    type: boolean
    required: false
    description: "Use PMKID attack"
    aliases:
      - --pmkid
  - name: handshake-dir
    type: string
    required: false
    description: "Directory to save handshakes"
    aliases:
      - --handshake-dir
  - name: wordlist
    type: file
    required: false
    description: "Dictionary file for cracking"
    aliases:
      - --wordlist
execution:
  template: "wifite -i {interface}"
  sandbox: execFile
  timeout_seconds: 86400
  shell: false
global_vars:
  interface: wlan0
examples:
  - description: "Attack all visible WiFi networks automatically"
    command: wifite -i wlan0
  - description: "Attack only WPA networks"
    command: wifite -i wlan0 --wpa --no-wep
  - description: "Attack specific BSSID"
    command: wifite -i wlan0 -b 00:11:22:33:44:55
  - description: "Use only PMKID attack"
    command: wifite -i wlan0 --pmkid --no-wps --no-deauth
  - description: "Skip deauth and WPS attacks"
    command: wifite -i wlan0 --no-deauth --no-wps
  - description: "With custom wordlist"
    command: wifite -i wlan0 --wordlist /usr/share/wordlists/rockyou.txt
  - description: "Attack 5GHz networks"
    command: wifite -i wlan0 -5 --no-wep
  - description: "Use random MAC and cloaking"
    command: wifite -i wlan0 --random-mac --cloaking
references:
  - label: "Wifite GitHub"
    url: "https://github.com/derv82/wifite2"
  - label: "Wifite Documentation"
    url: "https://github.com/derv82/wifite2/wiki"
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
      package_name: "wifite"
      commands:
        - "apt-get install -y wifite"
---

# Wifite — Automated Wireless Auditor

Wifite automates WiFi auditing by orchestrating aircrack-ng, reaver, bully, and hcxdumptool. It targets WEP, WPA, and WPS-enabled networks with minimal user interaction.

## Attack Modes

| Mode | Description |
|------|-------------|
| WEP | ARP replay + packet injection, crack when enough IVs |
| WPA | Deauth + handshake capture, crack with dictionary |
| WPS | PIN brute-force via reaver/bully |
| PMKID | PMKID capture via hcxdumptool |
