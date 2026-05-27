---
id: network-analysis-scapy
namespace: network:analysis:scapy
name: scapy
description: Python-based packet crafting and network manipulation framework for packet generation, sniffing, protocol analysis, and network attack development.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.packet.craft
  - network.sniff.traffic
  - network.protocol.analyze
  - network.attack.arp
  - network.attack.dns
  - network.attack.dhcp
  - network.manipulation.ip
platforms:
  - linux
  - macos
  - cross-platform
risk_level: medium
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies:
  - python3
related_tools:
  - wireshark
  - tcpdump
  - nmap
  - bettercap
artifacts:
  - type: network.capture.pcap
    description: Captured network packets in PCAP format
    mime: application/vnd.tcpdump.pcap
    trust_level: verified
  - type: network.analysis.json
    description: Packet analysis results as JSON
    mime: application/json
    trust_level: verified
workflow_edges:
  produces:
    - crafted-packets
    - captured-traffic
    - pcap-output
  consumes:
    - target-ip
    - target-port
    - network-interface
contract:
  inputs:
    - type: network.target.ip
      description: Target IP address for packet destination
    - type: network.interface
      description: Network interface to use
    - type: network.port.number
      description: Target port number
  outputs:
    - type: network.capture.pcap
      description: Captured or crafted packet data
      mime: application/vnd.tcpdump.pcap
    - type: network.analysis.json
      description: Protocol analysis results
      mime: application/json
  side_effects:
    - raw_socket_access
    - network_traffic
  resource_cost:
    cpu: low
    memory_mb: 64
    network: medium
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 64
  network: medium
  disk_io: low
allowed-tools:
  - scapy
  - python3
  - Bash
  - execFile
parameters:
  - name: script
    type: string
    required: false
    description: "Python script file containing Scapy commands"
  - name: flag-i
    type: string
    required: false
    description: "Network interface"
    aliases:
      - -i
      - --interface
  - name: flag-t
    type: string
    required: false
    description: "Target IP or hostname"
    aliases:
      - -t
      - --target
  - name: count
    type: integer
    required: false
    description: "Number of packets to send or capture"
    aliases:
      - -c
      - --count
execution:
  template: "python3 {script} {flags}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
examples:
  - description: "ICMP ping sweep"
    command: 'python3 -c "from scapy.all import *; sr1(IP(dst=\"10.0.0.1\")/ICMP(), timeout=2)"'
  - description: "TCP SYN scan"
    command: 'python3 -c "from scapy.all import *; sr1(IP(dst=\"10.0.0.1\")/TCP(dport=80, flags=\"S\"), timeout=2)"'
  - description: "ARP scan local network"
    command: 'python3 -c "from scapy.all import *; arp_request = ARP(pdst=\"10.0.0.0/24\"); result = srp(arp_request, timeout=2)[0]; result.summary()"'
  - description: "Sniff traffic on interface"
    command: 'python3 -c "from scapy.all import *; packets = sniff(iface=\"eth0\", count=10); wrpcap(\"capture.pcap\", packets)"'
  - description: "DNS query"
    command: 'python3 -c "from scapy.all import *; sr1(IP(dst=\"8.8.8.8\")/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=\"example.com\")), timeout=2)"'
references:
  - label: "Scapy Official Site"
    url: "https://scapy.net/"
  - label: "Scapy Documentation"
    url: "https://scapy.readthedocs.io/"
  - label: "Scapy GitHub"
    url: "https://github.com/secdev/scapy/"
phase: discovery
techniques:
  - network-sniffing
  - discovery
items:
  - NoCreds
services: []
attack_types:
  - Discovery
  - Exploitation
---

# Scapy — Packet Crafting and Network Manipulation

Scapy is a powerful Python library for packet manipulation, protocol analysis, and network attack development. It can craft arbitrary packets, sniff traffic, perform network scans, and implement custom protocols.

## Basic Examples

```python
from scapy.all import *

# TCP SYN scan
ans = sr1(IP(dst="10.0.0.1")/TCP(dport=80, flags="S"), timeout=2)
print(ans.summary())

# ARP request
ans = srp(ARP(pdst="10.0.0.1"), timeout=2)[0]
for req, res in ans:
    print(f"{res.psrc} - {res.hwsrc}")

# Simple packet sniffer
pkts = sniff(filter="tcp port 80", count=10)
wrpcap("http.pcap", pkts)
```

## Common Use Cases

- Custom packet generation
- Network scanning and discovery
- Protocol fuzzing
- ARP spoofing / MITM
- DNS manipulation
- Traffic sniffing and analysis
- Packet crafting for exploitation
