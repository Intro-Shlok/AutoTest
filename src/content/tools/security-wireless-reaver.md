---
id: security-wireless-reaver
namespace: security:wireless:reaver
name: reaver
description: WiFi Protected Setup (WPS) PIN brute-force attack tool for recovering WPA/WPA2 passphrases.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.wps.bruteforce
  - network.crack.wpa
  - network.pin.attack
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
  - bully
  - aircrack-ng
  - wifite
artifacts:
  - type: wireless.wps.pin
    description: Recovered WPS PIN
    mime: text/plain
    trust_level: verified
  - type: wireless.wpa.psk
    description: Cracked WPA passphrase
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - wps-pin
    - wpa-passphrase
    - session-file
  consumes:
    - target-bssid
    - network-manipulation-interface
contract:
  inputs:
    - type: wireless.interface
      description: Wireless interface in monitor mode
    - type: wireless.bssid
      description: Target AP BSSID
    - type: wireless.channel
      description: Target channel
  outputs:
    - type: wireless.wps.pin
      description: Recovered WPS PIN
      mime: text/plain
    - type: wireless.wpa.psk
      description: WPA passphrase recovered via WPS
      mime: text/plain
  side_effects:
    - network_traffic
    - raw_socket_access
    - network_traffic
  resource_cost:
    cpu: medium
    memory_mb: 32
    network: low
    disk_io: low
resource_profile:
  cpu: medium
  memory_mb: 32
  network: low
  disk_io: low
allowed-tools:
  - reaver
  - Bash
  - execFile
parameters:
  - name: interface
    type: string
    required: true
    description: "Wireless interface name (monitor mode)"
    aliases:
      - -i
      - --interface
  - name: bssid
    type: string
    required: true
    description: "Target AP BSSID"
    aliases:
      - -b
      - --bssid
  - name: channel
    type: integer
    required: false
    description: "Wireless channel of target AP"
    aliases:
      - -c
      - --channel
  - name: pin
    type: string
    required: false
    description: "WPS PIN to test"
    aliases:
      - -p
      - --pin
  - name: lock-delay
    type: integer
    required: false
    description: "Delay in seconds after WPS lockout"
    aliases:
      - -l
      - --lock-delay
  - name: timeout
    type: integer
    required: false
    description: "Receive timeout in seconds"
    aliases:
      - -t
      - --timeout
  - name: session-file
    type: file
    required: false
    description: "Session file for resume support"
    aliases:
      - -s
      - --session
  - name: verbose
    type: boolean
    required: false
    description: "Enable verbose output"
    aliases:
      - -v
      - --verbose
  - name: quiet
    type: boolean
    required: false
    description: "Quiet mode, suppress output"
    aliases:
      - -q
      - --quiet
  - name: auto
    type: boolean
    required: false
    description: "Auto-detect best advanced options"
    aliases:
      - -a
      - --auto
  - name: no-associate
    type: boolean
    required: false
    description: "Do not associate with AP"
    aliases:
      - -A
      - --no-associate
  - name: exhaustive
    type: boolean
    required: false
    description: "Exhaustive PIN search"
    aliases:
      - -X
      - --exhaustive
execution:
  template: "reaver -i {interface} -b {bssid}"
  sandbox: execFile
  timeout_seconds: 86400
  shell: false
global_vars:
  interface: wlan0mon
  bssid: "00:11:22:33:44:55"
examples:
  - description: "Basic WPS PIN brute force"
    command: reaver -i wlan0mon -b 00:11:22:33:44:55
  - description: "With channel and verbose output"
    command: reaver -i wlan0mon -b 00:11:22:33:44:55 -c 6 -vv
  - description: "Resume from saved session"
    command: reaver -i wlan0mon -b 00:11:22:33:44:55 -s session.wpc
  - description: "Test specific PIN"
    command: reaver -i wlan0mon -b 00:11:22:33:44:55 -p 12345670
  - description: "With lockout delay and no association"
    command: reaver -i wlan0mon -b 00:11:22:33:44:55 -l 60 -A
  - description: "Exhaustive mode with auto options"
    command: reaver -i wlan0mon -b 00:11:22:33:44:55 -X -a
  - description: "Quiet mode with 30s timeout"
    command: reaver -i wlan0mon -b 00:11:22:33:44:55 -q -t 30
  - description: "Fixed channel with delay"
    command: reaver -i wlan0mon -b 00:11:22:33:44:55 -c 11 -d 5
references:
  - label: "Reaver GitHub"
    url: "https://github.com/t6x/reaver-wps-fork-t6x"
  - label: "WPS Attack Methodology"
    url: "https://github.com/t6x/reaver-wps-fork-t6x/wiki"
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
---

# Reaver — WPS PIN Attack Tool

Reaver performs a brute-force attack against WiFi Protected Setup (WPS) registrar PINs in order to recover WPA/WPA2 passphrases. It targets the WPS vulnerability in access points that have WPS enabled.

## How It Works

Reaver sends WPS PIN attempts to the target AP. When the correct PIN is found, the AP reveals the WPA/WPA2 passphrase. The default WPS PIN is often 8 digits, with the last digit being a checksum.

## Key Features

- **Session resume**: Saves progress so attacks can continue after interruption
- **Lockout detection**: Detects WPS lockout and waits before retrying
- **Auto mode**: Automatically selects optimal parameters
- **Exhaustive search**: Tries all possible PIN combinations
