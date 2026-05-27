---
id: security-wireless-bettercap
namespace: security:wireless:bettercap
name: bettercap
description: Powerful MITM framework for WiFi, Bluetooth, and wired network attacks with an interactive command console.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.mitm
  - network.sniff
  - network.deauth
  - network.proxy
  - network.dns.spoof
  - network.arp.spoof
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
  - ettercap
  - responder
  - yersinia
artifacts:
  - type: network.capture.pcap
    description: Captured network traffic
    mime: application/vnd.tcpdump.pcap
    trust_level: verified
  - type: network.log.sniffed
    description: Sniffed credentials and data
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - captured-traffic
    - sniffed-credentials
    - spoofed-dns
  consumes:
    - network-interface
    - target-ip
    - gateway-ip
contract:
  inputs:
    - type: network.interface
      description: Network interface
    - type: network.target.ip
      description: Target IP address
    - type: network.gateway.ip
      description: Gateway IP address
  outputs:
    - type: network.capture.pcap
      description: Packet capture file
      mime: application/vnd.tcpdump.pcap
    - type: network.log.credentials
      description: Captured credentials
      mime: text/plain
  side_effects:
    - network_traffic
    - network_traffic
    - network_traffic
  resource_cost:
    cpu: medium
    memory_mb: 256
    network: high
    disk_io: medium
resource_profile:
  cpu: medium
  memory_mb: 256
  network: high
  disk_io: medium
allowed-tools:
  - bettercap
  - Bash
  - execFile
parameters:
  - name: interface
    type: string
    required: false
    description: "Network interface name"
    aliases:
      - -I
      - --interface
  - name: target
    type: string
    required: false
    description: "Target IP address"
    aliases:
      - -T
      - --target
  - name: gateway
    type: string
    required: false
    description: "Gateway IP address"
    aliases:
      - -G
      - --gateway
  - name: spoof
    type: boolean
    required: false
    description: "Enable ARP spoofing"
    aliases:
      - -S
      - --spoof
  - name: sniffer
    type: boolean
    required: false
    description: "Enable sniffer"
    aliases:
      - -X
      - --sniffer
  - name: proxy
    type: boolean
    required: false
    description: "Enable HTTP/HTTPS proxy"
    aliases:
      - -P
      - --proxy
  - name: log
    type: string
    required: false
    description: "Log file path"
    aliases:
      - -L
      - --log
  - name: output
    type: string
    required: false
    description: "Output directory"
    aliases:
      - -O
      - --output
  - name: caplet
    type: file
    required: false
    description: "Caplet script file to execute"
    aliases:
      - --caplet
  - name: eval
    type: string
    required: false
    description: "Evaluate a bettercap command"
    aliases:
      - -eval
      - --eval
  - name: no-http
    type: boolean
    required: false
    description: "Disable HTTP server"
    aliases:
      - --no-http
  - name: no-https
    type: boolean
    required: false
    description: "Disable HTTPS server"
    aliases:
      - --no-https
execution:
  template: "bettercap -I {interface} -X"
  sandbox: execFile
  timeout_seconds: 86400
  shell: false
global_vars:
  interface: eth0
examples:
  - description: "Start sniffer on interface"
    command: bettercap -I eth0 -X
  - description: "ARP spoof target with sniffer"
    command: bettercap -I eth0 -T 192.168.1.100 -X --spoof
  - description: "MITM with proxy and logging"
    command: bettercap -I eth0 -T 192.168.1.100 -G 192.168.1.1 -P --proxy -L cap.log
  - description: "Run a caplet script"
    command: bettercap -I eth0 --caplet /path/to/caplet.cap
  - description: "Evaluate commands inline"
    command: bettercap -eval "net.sniff on; set arp.spoof.targets 192.168.1.100; arp.spoof on"
  - description: "Sniffer with DNS spoofing"
    command: bettercap -I eth0 -X --dns example.com=10.0.0.1
  - description: "Capture output to file"
    command: bettercap -I eth0 -X -O /tmp/capture
  - description: "Disable HTTP/HTTPS servers"
    command: bettercap -I eth0 -X --no-http --no-https
references:
  - label: "Bettercap Official Site"
    url: "https://www.bettercap.org/"
  - label: "Bettercap GitHub"
    url: "https://github.com/bettercap/bettercap"
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

# Bettercap — MITM Framework

Bettercap is a powerful, modular, and portable MITM framework capable of attacking WiFi, Bluetooth Low Energy, and wired networks. It features an interactive console with real-time monitoring.

## Key Modules

- **net.sniff**: Passive network sniffer
- **arp.spoof**: ARP poisoning for MITM
- **dns.spoof**: DNS response spoofing
- **http.proxy**: HTTP/HTTPS proxy with SSL stripping
- **wifi**: WiFi monitoring, deauth, and WPA handshake capture
- **ble**: Bluetooth Low Energy attacks
