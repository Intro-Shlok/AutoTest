---
id: security-web-owasp-zap
namespace: security:web:zap
name: owasp-zap
description: OWASP Zed Attack Proxy — open-source web application security scanner for
  finding vulnerabilities in web applications and APIs.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.proxy.intercept
  - web.scan.active
  - web.scan.passive
  - web.fuzzing
  - web.spider
  - web.api.scan
  - web.session.handling
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
dependencies: []
related_tools:
  - burpsuite
  - nikto
  - wpscan
artifacts:
  - type: web.scan.report
    description: ZAP scan report in HTML or JSON
    mime: text/html
    trust_level: verified
  - type: web.scan.session
    description: ZAP session file
    mime: application/octet-stream
    trust_level: verified
workflow_edges:
  produces:
    - scan-results
    - alerts
    - spider-results
  consumes:
    - target-url
    - target-context
contract:
  inputs:
    - type: web.target.url
      description: Target application URL to scan
    - type: web.target.context
      description: Context definition for authenticated scanning
  outputs:
    - type: web.scan.report
      description: HTML or JSON scan report
      mime: text/html
    - type: web.scan.alerts
      description: Security alerts found during scan
      mime: application/json
  side_effects:
    - network_traffic
    - network_traffic
  resource_cost:
    cpu: high
    memory_mb: 512
    network: medium
    disk_io: low
resource_profile:
  cpu: high
  memory_mb: 512
  network: medium
  disk_io: low
allowed-tools:
  - zap
  - zap-cli
  - Bash
  - execFile
parameters:
  - name: daemon
    type: boolean
    required: false
    description: "Run ZAP in daemon mode (headless)"
    aliases:
      - -daemon
  - name: port
    type: integer
    required: false
    description: "Port to listen on (default 8080)"
    default_value: "8080"
    aliases:
      - -port
  - name: host
    type: string
    required: false
    description: "Host address to bind to (default 127.0.0.1)"
    default_value: "127.0.0.1"
    aliases:
      - -host
  - name: config
    type: string
    required: false
    description: "Configuration key=value pairs"
    aliases:
      - -config
  - name: cmd
    type: boolean
    required: false
    description: "Run ZAP in command-line mode without GUI"
    aliases:
      - -cmd
  - name: suppressinfo
    type: boolean
    required: false
    description: "Suppress informational messages in output"
    aliases:
      - -suppressinfo
  - name: newsession
    type: string
    required: false
    description: "Create new session at specified path"
    aliases:
      - -newsession
  - name: session
    type: string
    required: false
    description: "Open existing session file"
    aliases:
      - -session
execution:
  template: "zap -daemon -port {port} -host {host}"
  sandbox: execFile
  timeout_seconds: 3600
  shell: false
global_vars:
  target: url
  port: "8080"
  host: "127.0.0.1"
examples:
  - description: "Start ZAP in daemon mode on default port"
    command: zap -daemon -port 8080
  - description: "Run ZAP in command-line mode with config"
    command: zap -cmd -config api.disablekey=true
  - description: "Start daemon with custom host binding"
    command: zap -daemon -host 0.0.0.0 -port 9090
  - description: "Load existing session and suppress info messages"
    command: zap -session session.session -suppressinfo
  - description: "Create new session in daemon mode"
    command: zap -daemon -newsession /tmp/zap-session
  - description: "Full automated scan using zap-cli"
    command: zap-cli --port 8080 quick-scan --self-contained -r report.html https://target.com
references:
  - label: "OWASP ZAP Documentation"
    url: "https://www.zaproxy.org/docs/"
  - label: "ZAP API Reference"
    url: "https://www.zaproxy.org/docs/api/"
phase: exploitation
techniques:
  - discovery
  - discovery
  - discovery
  - discovery
items:
  - NoCreds
services: []
attack_types:
  - Exploitation
install:
    - method: apt
      package_name: "zaproxy"
      commands:
        - "apt-get install -y zaproxy"
---

# OWASP ZAP — Zed Attack Proxy

OWASP ZAP (Zed Attack Proxy) is one of the world's most popular free web application security scanners. It helps automatically find security vulnerabilities in web applications and APIs.

## Key Features

- **Intercepting Proxy**: Inspect and modify HTTP/HTTPS traffic
- **Active Scanner**: Automatically find vulnerabilities
- **Passive Scanner**: Identify issues without modifying requests
- **Spider**: Crawl web applications to map content
- **API Scanning**: Test REST and GraphQL APIs
- **Authentication Support**: Form-based, NTLM, OAuth, etc.

## Modes

| Mode | Command | Description |
|------|---------|-------------|
| GUI | `zap` | Standard graphical interface |
| Daemon | `zap -daemon` | Headless mode (API accessible) |
| Command-line | `zap -cmd` | CLI mode for scripting |

## Basic Usage

```bash
# Start daemon mode for automated scanning
zap -daemon -port 8080

# Use zap-cli for headless scanning
zap-cli --port 8080 quick-scan -r report.html https://target.com

# Run with custom configuration
zap -cmd -config api.disablekey=true -config scanner.attackOnStart=true
```

## Operational Security

- Set `api.disablekey=true` for local-only API access
- Use `-host 127.0.0.1` to bind to localhost only
- Scanning without authorization is illegal in many jurisdictions
