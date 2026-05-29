---
id: security-mitm-responder
namespace: security:mitm:responder
name: Responder
description: LLMNR, NBT-NS, and MDNS poisoner that captures NTLMv1/v2 hashes for
  offline cracking or relay attacks in Windows network environments.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.poison.llmnr
  - security.poison.nbtns
  - security.poison.mdns
  - security.capture.hash
  - security.mitm.responder
  - security.relay.ntlm
platforms:
  - linux
  - cross-platform
risk_level: high
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies:
  - python3
related_tools:
  - impacket
  - netexec
contract:
  inputs:
    - type: network.interface
      description: Network interface to listen on
  outputs:
    - type: security.credential.hash
      description: Captured NTLMv1/v2 hashes
  side_effects:
    - network_traffic
    - raw_socket_access
resource_profile:
  cpu: low
  memory_mb: 64
  network: medium
  disk_io: low
allowed-tools:
  - responder
parameters:
  - name: interface
    type: string
    required: true
    description: "Network interface to listen on"
  - name: analyze
    type: boolean
    required: false
    description: "Analyze mode (passive, no poisoning)"
  - name: wpad
    type: boolean
    required: false
    description: "Enable WPAD rogue proxy"
execution:
  template: "Responder -I {interface}"
  sandbox: execFile
  timeout_seconds: 86400
  shell: false
global_vars:
  target: ip
examples:
  - description: "Launch Responder in default poisoning mode"
    command: Responder -I eth0
  - description: "Analyze mode — passive listening without poisoning"
    command: Responder -I eth0 -A
  - description: "Enable WPAD rogue proxy server"
    command: Responder -I eth0 -w
  - description: "Disable HTTP and SMB servers (for relay attacks)"
    command: Responder -I eth0 -HTTP off -SMB off
  - description: "Multirelay attack — relay captured hashes to target"
    command: python3 Multirelay.py -t 10.10.10.1 -u ALL
references:
  - label: "Responder GitHub"
    url: "https://github.com/lgandx/Responder"
techniques:
  - credential-access
  - lateral-movement
attack_types:
  - CredentialAccess
  - LateralMovement
services:
  - LLMNR
  - NBT-NS
  - MDNS
items:
  - NoCreds
install:
    - method: apt
      package_name: "responder"
      commands:
        - "apt-get install -y responder"
---

# Responder — LLMNR/NBT-NS/MDNS Poisoner

Responder is an LLMNR, NBT-NS, and MDNS poisoner that responds to name resolution requests on a victim's network, causing victims to send authentication credentials to attacker-controlled services.

## Attack Flow

1. Victim mistypes a hostname or a service fails DNS resolution
2. Victim broadcasts LLMNR/NBT-NS asking "who has this name?"
3. Responder claims ownership and provides an attacker-controlled service (SMB, HTTP, etc.)
4. Victim sends NTLMv1/v2 hash to authenticate
5. Captured hash is cracked offline or relayed to a target server

## Key Options

| Option | Effect |
|--------|--------|
| `-I eth0` | Interface selection |
| `-A` | Analyze mode (no poisoning, just logging) |
| `-w` | Enable WPAD proxy |
| `-f` | Fingerprint victims |
| `-v` | Verbose output |
