---
id: security-web-wpscan
namespace: security:web:wpscan
name: wpscan
description: Black-box WordPress vulnerability scanner that detects themes, plugins, users, and security misconfigurations.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.scan.wordpress
  - web.discovery.plugin
  - web.discovery.theme
  - web.discovery.user
  - security.vulnerability.scan
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
  - joomscan
  - cmsmap
artifacts:
  - type: web.wpscan.report
    description: WordPress vulnerability scan report
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - wp-scan-results
    - wp-vulnerabilities
    - wp-users
  consumes:
    - target-url
contract:
  inputs:
    - type: web.target.url
      description: Target WordPress URL
  outputs:
    - type: web.wpscan.results
      description: Vulnerability scan results
      mime: text/plain
  side_effects:
    - network_traffic
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
  - wpscan
  - Bash
  - execFile
parameters:
  - name: url
    type: string
    required: true
    description: "Target WordPress URL (--url)"
    aliases:
      - --url
  - name: enumerate
    type: string
    required: false
    description: "Enumeration options (-e)"
    default_value: "vp,vt"
    aliases:
      - -e
  - name: plugins-detection
    type: string
    required: false
    description: "Plugin detection mode (--plugins-detection)"
    default_value: "passive"
    aliases:
      - --plugins-detection
  - name: api-token
    type: string
    required: false
    description: "WPScan API token (--api-token)"
    aliases:
      - --api-token
  - name: passwords
    type: string
    required: false
    description: "Password file for brute force (--passwords)"
    aliases:
      - --passwords
  - name: usernames
    type: string
    required: false
    description: "Username file (--usernames)"
    aliases:
      - --usernames
  - name: threads
    type: integer
    required: false
    description: "Number of threads (-t)"
    default_value: "5"
    aliases:
      - -t
  - name: verbose
    type: boolean
    required: false
    description: "Verbose output (-v)"
    aliases:
      - -v
  - name: batch
    type: boolean
    required: false
    description: "Never ask for user input (--batch)"
    aliases:
      - --batch
  - name: random-user-agent
    type: boolean
    required: false
    description: "Random User-Agent (--random-user-agent)"
    aliases:
      - --random-user-agent
  - name: proxy
    type: string
    required: false
    description: "Proxy URL (--proxy)"
    aliases:
      - --proxy
  - name: cookie
    type: string
    required: false
    description: "Cookie string (--cookie)"
    aliases:
      - --cookie
  - name: headers
    type: string
    required: false
    description: "Custom HTTP headers (--headers)"
    aliases:
      - --headers
  - name: detection-mode
    type: string
    required: false
    description: "Detection mode (--detection-mode)"
    default_value: "mixed"
    aliases:
      - --detection-mode
  - name: force
    type: boolean
    required: false
    description: "Force scan even if not WordPress (--force)"
    aliases:
      - --force
execution:
  template: "wpscan --url {target} -e"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
global_vars:
  target: url
examples:
  - description: "Basic WordPress scan"
    command: wpscan --url http://target.com --batch
  - description: "Enumerate vulnerabilities and users"
    command: wpscan --url http://target.com -e vp,vt,u --batch
  - description: "Brute force user passwords"
    command: wpscan --url http://target.com --usernames users.txt --passwords rockyou.txt
  - description: "Use stealthy mode"
    command: wpscan --url http://target.com --stealthy
  - description: "With API token for vulnerability database"
    command: wpscan --url http://target.com --api-token YOUR_TOKEN -e vp,vt
references:
  - label: "WPScan GitHub"
    url: "https://github.com/wpscanteam/wpscan"
  - label: "WPScan website"
    url: "https://wpscan.com/"
phase: enumeration
techniques:
  - discovery
  - enumeration
  - discovery
items:
  - NoCreds
services: []
attack_types:
  - Enumeration
---

# WPScan — WordPress Vulnerability Scanner

WPScan is a black-box WordPress vulnerability scanner that identifies security issues by enumerating themes, plugins, users, and checking for known vulnerabilities.

## Basic Usage

```bash
# Basic scan
wpscan --url http://target.com --batch

# Enumerate vulnerable plugins, themes, and users
wpscan --url http://target.com -e vp,vt,u --batch
```

## Enumeration Options

| Flag | Description |
|------|-------------|
| `-e vp` | Vulnerable plugins |
| `-e vt` | Vulnerable themes |
| `-e u` | Users |
| `-e ap` | All plugins |
| `-e at` | All themes |
| `-e cb` | Config backups |
| `-e tt` | Timthumb files |
| `-e dbe` | Database exports |

## Modes

```bash
# Stealthy (low and slow)
wpscan --url http://target.com --stealthy

# Aggressive detection
wpscan --url http://target.com --detection-mode aggressive

# Force scan non-WordPress sites
wpscan --url http://target.com --force
```
