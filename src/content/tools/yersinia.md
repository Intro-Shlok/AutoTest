---
id: security-mitm-yersinia
namespace: security:mitm:yersinia
name: Yersinia
description: Layer 2 network protocol exploitation framework for attacking STP, CDP,
  DTP, VTP, HSRP, and other switching and routing protocols.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.attack.stp
  - security.attack.cdp
  - security.attack.dtp
  - security.attack.vtp
  - security.attack.hsrp
  - security.attack.dot1q
  - security.attack.dot1x
  - security.exploit.layer2
  - security.spoof.protocol
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
  - ettercap
  - bettercap
  - macof
contract:
  inputs:
    - type: network.interface
      description: Network interface for sending layer 2 frames
  outputs:
    - type: network.attack.stp
      description: STP topology change attack
    - type: network.spoof.cdp
      description: CDP packet injection
    - type: network.attack.vlan
      description: VLAN hopping via DTP
  side_effects:
    - network_traffic
    - raw_socket_access
    - network_traffic
resource_profile:
  cpu: low
  memory_mb: 32
  network: low
  disk_io: low
allowed-tools:
  - yersinia
parameters:
  - name: interface
    type: string
    required: true
    description: "Network interface to use"
    aliases:
      - -I
  - name: gui
    type: boolean
    required: false
    description: "Launch graphical (GTK) interface"
    aliases:
      - -G
  - name: daemon
    type: boolean
    required: false
    description: "Run in daemon mode (background)"
    aliases:
      - -d
  - name: interactive
    type: boolean
    required: false
    description: "Interactive curses-based text mode"
    aliases:
      - -i
  - name: show-networks
    type: boolean
    required: false
    description: "List available network interfaces"
    aliases:
      - -s
  - name: log
    type: file
    required: false
    description: "Log output to file"
    aliases:
      - -l
  - name: verbose
    type: boolean
    required: false
    description: "Verbose mode"
    aliases:
      - -v
  - name: help
    type: boolean
    required: false
    description: "Show help and exit"
    aliases:
      - -h
  - name: stp-attack
    type: string
    required: false
    description: "STP attack type (conf, root, bpdu)"
    aliases:
      - stp
  - name: cdp-spoof
    type: string
    required: false
    description: "CDP packet injection"
    aliases:
      - cdp
  - name: dtp-attack
    type: string
    required: false
    description: "DTP trunk negotiation attack"
    aliases:
      - dtp
  - name: vtp-attack
    type: string
    required: false
    description: "VTP domain attack"
    aliases:
      - vtp
execution:
  template: "yersinia -I {interface}"
  sandbox: execFile
  timeout_seconds: 86400
  shell: false
global_vars:
  interface: eth0
examples:
  - description: "Launch interactive mode on eth0"
    command: yersinia -I eth0 -i
  - description: "Launch GTK GUI for point-and-click attacks"
    command: yersinia -I eth0 -G
  - description: "Show available network interfaces"
    command: yersinia -s
  - description: "STP root role attack (become root bridge)"
    command: yersinia stp -attack 2
  - description: "CDP flooding attack"
    command: yersinia cdp -attack 1
  - description: "DTP trunk negotiation — enable trunking"
    command: yersinia dtp -attack 1
  - description: "VTP domain takeover"
    command: yersinia vtp -attack 1
  - description: "Run in daemon mode with logging"
    command: yersinia -I eth0 -d -l /tmp/yersinia.log
references:
  - label: "Yersinia GitHub"
    url: "https://github.com/tomac/yersinia"
  - label: "Yersinia documentation"
    url: "https://tools.kali.org/information-gathering/yersinia"
techniques:
  - credential-access
  - network-sniffing
attack_types:
  - CredentialAccess
  - Discovery
services:
  - SSH
  - DNS
  - HTTP
  - FTP
  - Kerberos
items:
  - NoCreds
workflow_edges:
  produces:
    - topology-attack
    - vlan-hop
    - protocol-spoof
  consumes:
    - network-interface
    - target-switch
phase: exploitation
features:
  - requires-root
install:
    - method: apt
      package_name: "yersinia"
      commands:
        - "apt-get install -y yersinia"
---

# Yersinia — Layer 2 Protocol Exploitation Framework

Yersinia is a framework for exploiting weaknesses in layer 2 network protocols. It implements attacks against STP (Spanning Tree Protocol), CDP (Cisco Discovery Protocol), DTP (Dynamic Trunking Protocol), VTP (VLAN Trunking Protocol), HSRP (Hot Standby Router Protocol), 802.1Q, and 802.1X.

## Protocol Attacks

| Protocol | Attacks |
|----------|---------|
| **STP** | BPDU floods, topology changes, root bridge hijacking |
| **CDP** | Device advertisement floods, fake device injection |
| **DTP** | Trunk negotiation, VLAN hopping |
| **VTP** | Domain takeover, configuration revision bumps |
| **HSRP** | Router impersonation, DoS |
| **802.1Q** | Double-tagging VLAN hopping |
| **802.1X** | EAPOL flooding, authentication bypass |

## Operational Modes

Yersinia offers three interfaces: interactive text mode (`-i`) for keyboard-driven attacks, GTK mode (`-G`) for mouse-driven point-and-click, and daemon mode (`-d`) for scripted headless operation.
