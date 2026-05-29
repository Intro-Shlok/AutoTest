---
id: security-mitm-ettercap
namespace: security:mitm:ettercap
name: Ettercap
description: Comprehensive MITM attack toolkit for ARP poisoning, DNS spoofing, and
  network traffic interception and analysis in switched LAN environments.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.mitm.arp
  - security.mitm.dns
  - security.poison.arp
  - security.intercept.traffic
  - security.spoof.dns
  - security.sniff.password
  - security.relay.ssl
  - security.hijack.session
platforms:
  - linux
  - cross-platform
risk_level: high
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies: []
related_tools:
  - bettercap
  - responder
  - yersinia
  - wireshark
contract:
  inputs:
    - type: network.interface
      description: Network interface for MITM operations
    - type: network.target.ip
      description: Target IP address for ARP poisoning
    - type: network.target.range
      description: Target IP range for network scan
  outputs:
    - type: security.credential.password
      description: Captured credentials from intercepted traffic
    - type: network.capture.pcap
      description: Captured network traffic
    - type: security.hash
      description: Captured authentication hashes
  side_effects:
    - network_traffic
    - raw_socket_access
    - network_traffic
resource_profile:
  cpu: low
  memory_mb: 64
  network: medium
  disk_io: low
allowed-tools:
  - ettercap
parameters:
  - name: interface
    type: string
    required: false
    description: "Network interface to use"
    aliases:
      - -i
  - name: text-mode
    type: boolean
    required: false
    description: "Use text-only interface (no GUI)"
    aliases:
      - -T
  - name: gui-mode
    type: boolean
    required: false
    description: "Use graphical interface"
    aliases:
      - -G
  - name: mitm-method
    type: string
    required: false
    description: "MITM attack method (arp, dhcp, port, ndp)"
    aliases:
      - -M
  - name: write
    type: file
    required: false
    description: "Write captured packets to pcap file"
    aliases:
      - -w
  - name: read
    type: file
    required: false
    description: "Read packets from pcap file"
    aliases:
      - -r
  - name: silent
    type: boolean
    required: false
    description: "Silent mode (no ARP flooding)"
    aliases:
      - -z
  - name: filter
    type: file
    required: false
    description: "Load a filter script (etter.filter)"
    aliases:
      - -F
  - name: plugin
    type: string
    required: false
    description: "Run a specific plugin"
    aliases:
      - -P
  - name: verbose
    type: boolean
    required: false
    description: "Enable verbose output"
    aliases:
      - -v
  - name: ssl
    type: boolean
    required: false
    description: "Enable SSL stripping (mitm-attack)"
    aliases:
      - -S
  - name: quiet
    type: boolean
    required: false
    description: "Suppress packet display"
    aliases:
      - -q
execution:
  template: "ettercap -T -i {interface} -M arp:remote"
  sandbox: execFile
  timeout_seconds: 86400
  shell: false
global_vars:
  interface: eth0
  target: remote
examples:
  - description: "ARP poisoning MITM attack in text mode"
    command: ettercap -T -i eth0 -M arp:remote /10.0.0.1/ /10.0.0.2/
  - description: "Passive network sniffing (no poisoning)"
    command: ettercap -T -i eth0 -s
  - description: "DNS spoofing with filter script"
    command: ettercap -T -i eth0 -M arp -F dns.spoof
  - description: "Capture traffic to pcap file"
    command: ettercap -T -i eth0 -M arp:remote -w capture.pcap
  - description: "Launch GUI mode for interactive analysis"
    command: ettercap -G
  - description: "Read and analyze existing pcap"
    command: ettercap -T -r capture.pcap
  - description: "SSL stripping attack"
    command: ettercap -T -i eth0 -M arp:remote -S
references:
  - label: "Ettercap Project"
    url: "https://www.ettercap-project.org/"
  - label: "Ettercap GitHub"
    url: "https://github.com/Ettercap/ettercap"
techniques:
  - credential-access
  - network-sniffing
attack_types:
  - CredentialAccess
  - Discovery
services:
  - HTTPS
  - FTP
  - SSH
  - SMB
  - LDAP
items:
  - NoCreds
  - Hash
workflow_edges:
  produces:
    - mitm-session
    - captured-traffic
    - intercepted-credentials
  consumes:
    - target-ip
    - target-range
    - network-interface
phase: exploitation
features:
  - requires-root
install:
    - method: apt
      package_name: "ettercap-graphical"
      commands:
        - "apt-get install -y ettercap-graphical"
---

# Ettercap — Comprehensive MITM Toolkit

Ettercap is a comprehensive suite for man-in-the-middle attacks on local area networks. It supports ARP poisoning, DNS spoofing, DHCP flooding, and passive sniffing with real-time traffic analysis, content filtering, and plugin-based extensibility.

## MITM Attack Methods

| Method | Flag | Description |
|--------|------|-------------|
| ARP poisoning | `-M arp:remote` | Classic ARP cache poisoning |
| DHCP spoofing | `-M dhcp` | Fake DHCP server |
| NDP poisoning | `-M ndp` | IPv6 neighbor discovery spoofing |
| Port stealing | `-M port` | Port stealing on switches |

## Plugins

Ettercap plugins extend functionality: `dns_spoof` (DNS response forgery), `chk_poison` (detect ARP poisoning), `find_conn` (find active connections), `gw_discover` (gateway discovery), `remote_browser` (inject HTML into HTTP streams).

## Filters

Content filtering allows real-time packet manipulation: replace text in HTTP streams, inject scripts, drop packets, or modify protocol headers using etterfilter-compiled filter scripts.
