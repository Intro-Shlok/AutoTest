---
id: security-recon-recon-ng
namespace: security:recon:recon-ng
name: recon-ng
description: Full-featured reconnaissance framework with modules for OSINT, social
  engineering, and target profiling across dozens of data sources.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.intel.osint
  - security.recon.passive
  - security.recon.framework
  - security.intel.email
  - network.discovery.subdomain
  - security.intel.contact
  - security.intel.geolocation
platforms:
  - linux
  - macos
  - cross-platform
risk_level: low
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies:
  - python3
related_tools:
  - spiderfoot
  - theharvester
  - maltego
artifacts:
  - type: security.recon.report
    description: Reconnaissance report and collected intelligence
    mime: text/html
    trust_level: community
  - type: security.recon.workspace
    description: Recon-ng workspace database
    mime: application/octet-stream
    trust_level: verified
workflow_edges:
  produces:
    - contacts
    - credentials
    - domains
    - hosts
    - leaked-data
  consumes:
    - domain
    - company-name
contract:
  inputs:
    - type: network.target.domain
      description: Target domain name
    - type: security.target.company
      description: Company name for profiling
  outputs:
    - type: security.recon.report
      description: Reconnaissance data
      mime: text/html
  side_effects:
    - network_traffic
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
  - recon-ng
  - Bash
  - execFile
parameters:
  - name: flag-w
    type: string
    required: false
    description: "Load/create a workspace"
    aliases:
      - -w
  - name: flag-r
    type: file
    required: false
    description: "Load commands from a resource file"
    aliases:
      - -r
  - name: no-version
    type: boolean
    required: false
    description: "Disable version check"
    aliases:
      - --no-version
  - name: no-analytics
    type: boolean
    required: false
    description: "Disable analytics reporting"
    aliases:
      - --no-analytics
  - name: no-marketplace
    type: boolean
    required: false
    description: "Disable remote module management"
    aliases:
      - --no-marketplace
  - name: stealth
    type: boolean
    required: false
    description: "Disable all passive requests"
    aliases:
      - --stealth
execution:
  template: "recon-ng -w {workspace}"
  sandbox: execFile
  timeout_seconds: 3600
  shell: true
global_vars:
  target: domain
  domain: "example.com"
  workspace: "default"
examples:
  - description: "Launch recon-ng with a specific workspace"
    command: recon-ng -w target-company
  - description: "Run commands from a resource file"
    command: recon-ng -w target-company -r commands.rc
  - description: "Launch in stealth mode (no passive requests)"
    command: recon-ng --stealth
  - description: "Interactive mode — create workspace and load modules"
    command: recon-ng -w example
  - description: "Marketplace module search via CLI args"
    command: recon-ng --no-marketplace
references:
  - label: "Recon-ng GitHub"
    url: "https://github.com/lanmaster53/recon-ng"
  - label: "Recon-ng documentation"
    url: "https://github.com/lanmaster53/recon-ng/wiki"
phase: enumeration
techniques:
  - discovery
  - enumeration
  - recon
items:
  - NoCreds
services: []
attack_types:
  - Enumeration
---

# Recon-ng — Reconnaissance Framework

Recon-ng is a powerful web reconnaissance framework that provides an interactive environment for open-source intelligence gathering. It features a modular architecture with modules for contact discovery, domain enumeration, credential harvesting, geolocation, and more.

## Framework Architecture

- **Workspaces**: Isolate reconnaissance data per target
- **Modules**: 100+ modules organized by category (discovery, exploitation, import, recon, reporting)
- **Marketplace**: Download community modules
- **Reporting**: Generate HTML, CSV, and other report formats

## Interactive Usage

```
$ recon-ng -w target
[recon-ng][target] > marketplace search shodan
[recon-ng][target] > modules load recon/domains-hosts/shodan_hostname
[recon-ng][target][shodan_hostname] > set SOURCE example.com
[recon-ng][target][shodan_hostname] > run
```
