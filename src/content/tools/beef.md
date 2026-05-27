---
id: security-exploit-beef
namespace: security:exploit:beef
name: beef
description: Browser Exploitation Framework for assessing browser security through client-side attack vectors and hooking.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - browser.exploitation
  - browser.attack
  - browser.hooking
  - credential.harvesting
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
  - metasploit
  - empire
  - setoolkit
workflow_edges:
  produces:
    - hooked-browsers
    - harvested-credentials
    - client-exploit
  consumes:
    - hook-url
    - target-browser
contract:
  inputs:
    - type: network.url
      description: Hook URL to serve to target
  outputs:
    - type: browser.session
      description: Hooked browser session
      mime: text/plain
    - type: credential.data
      description: Harvested credentials
      mime: application/json
  side_effects:
    - network_traffic
    - process_spawn
  resource_cost:
    cpu: medium
    memory_mb: 128
    network: medium
    disk_io: low
resource_profile:
  cpu: medium
  memory_mb: 128
  network: medium
  disk_io: low
allowed-tools:
  - beef
  - Bash
  - execFile
parameters:
  - name: flag-x
    type: string
    required: false
    description: "Config file path"
    aliases:
      - -x
      - --config
  - name: flag-p
    type: integer
    required: false
    description: "Bind port"
    aliases:
      - -p
      - --port
  - name: flag-H
    type: string
    required: false
    description: "Bind host/address"
    aliases:
      - -H
      - --host
  - name: flag-P
    type: string
    required: false
    description: "Admin UI password"
    aliases:
      - -P
      - --password
  - name: flag-c
    type: string
    required: false
    description: "Command to execute"
    aliases:
      - -c
      - --cmd
  - name: flag-d
    type: boolean
    required: false
    description: "Debug mode"
    aliases:
      - -d
      - --debug
  - name: flag-v
    type: boolean
    required: false
    description: "Verbose output"
    aliases:
      - -v
      - --verbose
  - name: flag-s
    type: boolean
    required: false
    description: "Enable SSL"
    aliases:
      - -s
      - --ssl
  - name: flag-D
    type: boolean
    required: false
    description: "Daemonize (run in background)"
    aliases:
      - -D
      - --daemon
  - name: flag-l
    type: string
    required: false
    description: "Log file path"
    aliases:
      - -l
      - --log
  - name: flag-ui
    type: integer
    required: false
    description: "UI server port"
    aliases:
      - --ui
      - --ui-port
  - name: flag-ui-host
    type: string
    required: false
    description: "UI server bind address"
    aliases:
      - --ui-host
execution:
  template: "beef -x config.yaml"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
global_vars:
  lhost: "0.0.0.0"
  lport: "3000"
examples:
  - description: "Start BeEF with default config"
    command: beef -x config.yaml
  - description: "Start BeEF on custom port"
    command: beef -x config.yaml -p 8080
  - description: "Start BeEF with SSL enabled"
    command: beef -x config.yaml -s -p 443
  - description: "Start BeEF daemonized"
    command: beef -x config.yaml -D
  - description: "Start BeEF with custom UI port"
    command: beef -x config.yaml --ui 8081
  - description: "Start BeEF in debug mode"
    command: beef -x config.yaml -d -v
  - description: "Start BeEF on specific interface"
    command: beef -x config.yaml -H 10.0.0.1 -p 3000
references:
  - label: "BeEF GitHub"
    url: "https://github.com/beefproject/beef"
  - label: "BeEF Wiki"
    url: "https://github.com/beefproject/beef/wiki"
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
# BeEF — Browser Exploitation Framework

BeEF (Browser Exploitation Framework) is a penetration testing tool focused on web browsers. It uses a client-side attack vector to assess browser security by hooking one or more browsers and using them as beachheads for launching further attacks.

## Key Capabilities

- **Browser hooking**: Hook target browsers via injected JavaScript
- **Module system**: Hundreds of modules for reconnaissance, exploitation, and persistence
- **Command chain**: Execute commands across hooked browsers
- **Tunneling**: Proxy traffic through hooked browsers to bypass network controls
- **Metasploit integration**: Pass hooked browser sessions to Metasploit

## Architecture

BeEF consists of:
- **Server**: Ruby-based C2 server with RESTful API
- **UI**: Web-based administration panel
- **Hook**: JavaScript payload delivered to target browsers
- **Modules**: Extensible module framework for browser attacks
