---
id: security-sniff-wireshark
namespace: security:sniff:wireshark
name: Wireshark
description: World's most popular network protocol analyzer for live traffic capture
  and offline pcap analysis with deep inspection of hundreds of protocols.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.sniff.packet
  - network.analyze.protocol
  - network.capture.live
  - network.capture.offline
  - security.forensics.pcap
  - network.filter.display
  - network.filter.capture
platforms:
  - linux
  - macos
  - windows
  - cross-platform
risk_level: medium
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies: []
related_tools:
  - tcpdump
  - tshark
  - ettercap
contract:
  inputs:
    - type: network.interface
      description: Network interface to capture on
    - type: file.pcap
      description: PCAP file for offline analysis
  outputs:
    - type: file.pcap
      description: Captured packet data
    - type: network.analysis.json
      description: Parsed packet analysis output
  side_effects:
    - network_traffic
    - raw_socket_access
resource_profile:
  cpu: medium
  memory_mb: 256
  network: high
  disk_io: high
allowed-tools:
  - wireshark
  - tshark
parameters:
  - name: interface
    type: string
    required: false
    description: "Network interface to capture on"
    aliases:
      - -i
      - --interface
  - name: read-file
    type: file
    required: false
    description: "Read packet data from pcap file"
    aliases:
      - -r
      - --read-file
  - name: start-capture
    type: boolean
    required: false
    description: "Start capturing immediately"
    aliases:
      - -k
  - name: write-file
    type: file
    required: false
    description: "Write captured packets to file"
    aliases:
      - -w
      - --write-file
  - name: capture-filter
    type: string
    required: false
    description: "Capture filter expression (pcap-filter syntax)"
    aliases:
      - -f
  - name: display-filter
    type: string
    required: false
    description: "Display filter expression"
    aliases:
      - -Y
      - --display-filter
  - name: packet-count
    type: integer
    required: false
    description: "Stop after capturing count packets"
    aliases:
      - -c
  - name: output-format
    type: string
    required: false
    description: "Output format (fields, pdml, psml, json)"
    aliases:
      - -T
      - --output-format
  - name: verbose
    type: boolean
    required: false
    description: "Verbose output"
    aliases:
      - -V
  - name: hex
    type: boolean
    required: false
    description: "Display hex dump of packet data"
    aliases:
      - -x
  - name: quiet
    type: boolean
    required: false
    description: "Suppress packet output"
    aliases:
      - -q
  - name: list-interfaces
    type: boolean
    required: false
    description: "List available network interfaces"
    aliases:
      - -D
      - --list-interfaces
execution:
  template: "wireshark -i {interface} -k"
  sandbox: execFile
  timeout_seconds: 86400
  shell: false
global_vars:
  interface: eth0
examples:
  - description: "Start live capture on eth0"
    command: wireshark -i eth0 -k
  - description: "Analyze offline pcap file"
    command: wireshark -r capture.pcap
  - description: "Capture with display filter for HTTP traffic"
    command: wireshark -i eth0 -k -Y "http"
  - description: "Write capture to output file"
    command: wireshark -i eth0 -w output.pcap -k
  - description: "Capture with BPF filter for port 80 only"
    command: wireshark -i eth0 -f "port 80" -k
  - description: "List available capture interfaces"
    command: wireshark -D
  - description: "Open pcap with specific display filter"
    command: wireshark -r capture.pcap -Y "tcp.port==443"
references:
  - label: "Wireshark Official Site"
    url: "https://www.wireshark.org/"
  - label: "Wireshark Documentation"
    url: "https://www.wireshark.org/docs/"
phase: enumeration
techniques:
  - network-sniffing
  - credential-access
items:
  - NoCreds
  - Hash
services: []
attack_types:
  - Discovery
  - CredentialAccess
workflow_edges:
  produces:
    - pcap-capture
    - packet-analysis
  consumes:
    - target-interface
    - pcap-file
features:
  - requires-root
install:
    - method: apt
      package_name: "wireshark"
      commands:
        - "apt-get install -y wireshark"
---

# Wireshark — Network Protocol Analyzer

Wireshark is the world's foremost network protocol analyzer, enabling live capture and offline inspection of hundreds of protocols. It provides deep packet inspection, advanced filtering, and rich analysis capabilities for network troubleshooting, security analysis, and forensic investigation.

## Capture Modes

| Mode | Command | Description |
|------|---------|-------------|
| Live | `wireshark -i eth0 -k` | Capture live traffic on interface |
| Offline | `wireshark -r file.pcap` | Analyze existing pcap file |
| Filtered | `wireshark -f "port 80"` | Capture with BPF filter |

## Display Filters

Wireshark display filters are powerful expressions for isolating packets of interest:

- `http` — Show only HTTP traffic
- `tcp.port == 443` — Show traffic on port 443
- `ip.addr == 10.0.0.1` — Filter by IP address
- `dns.qry.name contains "example"` — DNS query filtering
- `tcp.flags.syn == 1 and tcp.flags.ack == 0` — SYN packets only

## Protocol Support

Wireshark decodes hundreds of protocols including TCP/IP, HTTP, DNS, TLS, SMB, DHCP, ARP, ICMP, SNMP, FTP, SSH, Kerberos, and many more. Protocol dissection can be extended via Lua plugins.
