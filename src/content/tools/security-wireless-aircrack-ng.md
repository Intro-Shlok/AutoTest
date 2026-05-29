---
id: security-wireless-aircrack-ng
namespace: security:wireless:aircrack-ng
name: aircrack-ng
description: Complete suite for monitoring, attacking, testing, and cracking WiFi networks, including WEP and WPA/WPA2-PSK.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.manipulation.sniff
  - network.crack.wep
  - network.crack.wpa
  - network.deauth
  - network.monitor
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
  - reaver
  - bully
  - kismet
  - wifite
artifacts:
  - type: wireless.crack.key
    description: Cracked WEP or WPA key
    mime: text/plain
    trust_level: verified
  - type: wireless.capture.pcap
    description: Captured wireless packets
    mime: application/vnd.tcpdump.pcap
    trust_level: verified
workflow_edges:
  produces:
    - cracked-key
    - handshake-capture
    - wep-key
  consumes:
    - capture-file
    - wordlist
contract:
  inputs:
    - type: wireless.capture.file
      description: Packet capture file (.cap or .pcap)
    - type: wordlist.file
      description: Dictionary file for password cracking
  outputs:
    - type: wireless.crack.key
      description: Cracked WPA passphrase or WEP key
      mime: text/plain
    - type: wireless.crack.hccapx
      description: Hashcat-compatible hash file
      mime: application/octet-stream
  side_effects:
    - network_traffic
    - network_traffic
    - raw_socket_access
  resource_cost:
    cpu: high
    memory_mb: 256
    network: low
    disk_io: medium
resource_profile:
  cpu: high
  memory_mb: 256
  network: low
  disk_io: medium
allowed-tools:
  - aircrack-ng
  - Bash
  - execFile
parameters:
  - name: wordlist
    type: file
    required: false
    description: "Path to dictionary file for WPA/WPA2-PSK cracking"
    aliases:
      - -w
      - --wordlist
  - name: attack-mode
    type: string
    required: false
    description: "Attack mode flag"
    aliases:
      - -a
      - --attack-mode
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
  - name: password
    type: string
    required: false
    description: "WPA password to test"
    aliases:
      - -p
      - --password
  - name: show
    type: boolean
    required: false
    description: "Show known keys in capture"
    aliases:
      - -s
      - --show
  - name: quiet
    type: boolean
    required: false
    description: "Quiet mode, suppress output"
    aliases:
      - -q
      - --quiet
  - name: korps
    type: boolean
    required: false
    description: "Enable KoreK attacks for WEP"
    aliases:
      - -K
      - --korps
  - name: strength
    type: integer
    required: false
    description: "WEP key strength in bits (40/104)"
    aliases:
      - -S
      - --strength
  - name: fudge
    type: integer
    required: false
    description: "Fudge factor for PTW attack"
    aliases:
      - -f
      - --fudge
execution:
  template: "aircrack-ng -w {wordlist} {capture-file}"
  sandbox: execFile
  timeout_seconds: 3600
  shell: false
global_vars:
  capture-file: handshake.cap
  wordlist: /usr/share/wordlists/rockyou.txt
examples:
  - description: "Crack WPA2 handshake using dictionary"
    command: aircrack-ng -w /usr/share/wordlists/rockyou.txt handshake.cap
  - description: "Crack WEP capture using PTW attack"
    command: aircrack-ng -a 1 -b 00:11:22:33:44:55 wep.cap
  - description: "Show known keys in capture file"
    command: aircrack-ng -s capture.cap
  - description: "Crack WPA with specific ESSID"
    command: aircrack-ng -w wordlist.txt -e MyNetwork handshake.cap
  - description: "Crack WEP with KoreK attacks"
    command: aircrack-ng -K -b 00:11:22:33:44:55 wep.cap
  - description: "Show all IVs and AP information"
    command: aircrack-ng capture.cap
  - description: "Convert capture to hccapx format"
    command: aircrack-ng -j hash.hccapx handshake.cap
  - description: "Crack with quiet mode and automatic detection"
    command: aircrack-ng -q -w wordlist.txt handshake.cap
references:
  - label: "Aircrack-ng Official Site"
    url: "https://www.aircrack-ng.org/"
  - label: "Aircrack-ng Documentation"
    url: "https://www.aircrack-ng.org/doku.php/documentation"
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
      package_name: "aircrack-ng"
      commands:
        - "apt-get install -y aircrack-ng"
---

# Aircrack-ng — WiFi Security Suite

Aircrack-ng is a complete suite of tools for assessing WiFi network security. It focuses on different areas of WiFi security: monitoring, attacking, testing, and cracking. It supports WEP and WPA/WPA2-PSK key recovery.

## Key Components

- **aircrack-ng**: WEP/WPA key cracker
- **airmon-ng**: Enable/disable monitor mode on wireless interfaces
- **airodump-ng**: Packet capture for raw 802.11 frames
- **aireplay-ng**: Packet injection for deauth and replay attacks
- **airdecap-ng**: Decrypt WEP/WPA captures with known key

## Cracking Modes

| Mode | Flag | Description |
|------|------|-------------|
| PTW | `-a 1` | Standard WEP cracking (PTW attack) |
| KoreK | `-a 1 -K` | KoreK attacks for difficult WEP |
| WPA-PSK | `-a 2 -w` | Dictionary attack on WPA handshake |
| WPA-PTK | `-a 2 -p` | WPA with known password test |

## Usage Workflow

```bash
# 1. Enable monitor mode
airmon-ng start wlan0

# 2. Capture handshake
airodump-ng -c 6 --bssid 00:11:22:33:44:55 -w capture wlan0mon

# 3. Crack the handshake
aircrack-ng -w /usr/share/wordlists/rockyou.txt capture-01.cap
```
