---
id: security-wireless-hcxpcaptool
namespace: security:wireless:hcxpcaptool
name: hcxpcaptool
description: Converts packet capture files to hash formats compatible with hashcat and john for WPA cracking.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.convert.capture
  - network.hash.extract
  - network.hash.pmkid
  - network.hash.eapol
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
  - hcxdumptool
  - hashcat
  - john
artifacts:
  - type: wireless.hash.22000
    description: Hashcat mode 22000 hash file
    mime: text/plain
    trust_level: verified
  - type: wireless.hash.john
    description: John the Ripper hash file
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - hashcat-hashes
    - john-hashes
    - essid-list
  consumes:
    - packet-capture
contract:
  inputs:
    - type: wireless.capture.file
      description: Packet capture file (.pcap, .pcapng, .cap)
  outputs:
    - type: wireless.hash.22000
      description: Hashcat mode 22000 hashes
      mime: text/plain
    - type: wireless.hash.john
      description: John the Ripper hashes
      mime: text/plain
    - type: wireless.essid.list
      description: Extracted ESSID list
      mime: text/plain
  side_effects: []
  resource_cost:
    cpu: low
    memory_mb: 128
    network: none
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 128
  network: none
  disk_io: low
allowed-tools:
  - hcxpcaptool
  - Bash
  - execFile
parameters:
  - name: pmkid
    type: string
    required: false
    description: "Output PMKID hashes (hashcat mode 22000)"
    aliases:
      - -z
      - --pmkid
  - name: output
    type: string
    required: false
    description: "Output file path"
    aliases:
      - -o
      - --output
  - name: essid-list
    type: string
    required: false
    description: "Extract ESSID list to file"
    aliases:
      - -E
      - --essid-list
  - name: identity
    type: string
    required: false
    description: "Extract identities to file"
    aliases:
      - -I
      - --identity
  - name: username
    type: string
    required: false
    description: "Extract usernames to file"
    aliases:
      - -U
      - --username
  - name: hashcat
    type: string
    required: false
    description: "Output hashcat format hashes"
    aliases:
      - -j
      - --hashcat
  - name: john
    type: string
    required: false
    description: "Output John the Ripper hashes"
    aliases:
      - -J
      - --john
  - name: pmkid-eapol
    type: string
    required: false
    description: "Output PMKID+EAPOL hashes"
    aliases:
      - -k
      - --pmkid-eapol
  - name: verbose
    type: boolean
    required: false
    description: "Enable verbose output"
    aliases:
      - -v
      - --verbose
execution:
  template: "hcxpcaptool -z {pmkid-output} {capture-file}"
  sandbox: execFile
  timeout_seconds: 3600
  shell: false
global_vars:
  capture-file: capture.pcapng
  pmkid-output: hash.22000
examples:
  - description: "Convert capture to hashcat mode 22000"
    command: hcxpcaptool -z hash.22000 capture.pcapng
  - description: "Extract multiple hash formats"
    command: hcxpcaptool -z hash.22000 -j hash.john capture.pcapng
  - description: "Extract ESSID list from capture"
    command: hcxpcaptool -E essids.txt capture.pcapng
  - description: "Extract PMKID and identities"
    command: hcxpcaptool -z hash.22000 -I identities.txt capture.pcapng
  - description: "Extract PMKID+EAPOL combined"
    command: hcxpcaptool -k combined.22000 capture.pcapng
  - description: "Extract usernames from EAP"
    command: hcxpcaptool -U usernames.txt capture.pcapng
  - description: "Verbose conversion"
    command: hcxpcaptool -v -z hash.22000 capture.pcapng
  - description: "Full extraction of all data"
    command: hcxpcaptool -z hash.22000 -E essids.txt -I identities.txt -U usernames.txt capture.pcapng
references:
  - label: "hcxpcaptool GitHub"
    url: "https://github.com/ZerBea/hcxtools"
  - label: "Hashcat mode 22000"
    url: "https://hashcat.net/wiki/doku.php?id=cracking_wpawpa2"
phase: exploitation
techniques:
  - credential-access
  - network-manipulation
items:
  - Hash
services: []
attack_types:
  - Discovery
features: []
---

# hcxpcaptool — Capture to Hash Converter

hcxpcaptool (part of hcxtools) converts WLAN packet captures into hash formats suitable for offline cracking with hashcat (mode 22000) and John the Ripper.

## Supported Hash Formats

| Format | Flag | Cracker |
|--------|------|---------|
| PMKID | `-z` | hashcat -m 22000 |
| EAPOL | `-j` | hashcat -m 22000 |
| PMKID+EAPOL | `-k` | hashcat -m 22000 |
| John | `-J` | John the Ripper |
