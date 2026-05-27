---
id: security-recon-maltego
namespace: security:recon:maltego
name: maltego
description: Graphical link analysis and data mining tool for OSINT investigations,
  entity correlation, and relationship mapping.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.intel.osint
  - security.recon.graph
  - security.intel.correlation
  - security.intel.link-analysis
  - security.recon.passive
platforms:
  - linux
  - macos
  - windows
  - cross-platform
risk_level: low
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies: []
related_tools:
  - recon-ng
  - spiderfoot
  - theharvester
artifacts:
  - type: security.recon.graph
    description: Maltego graph visualization
    mime: application/xml
    trust_level: verified
  - type: security.recon.report
    description: Maltego export report
    mime: text/html
    trust_level: community
workflow_edges:
  produces:
    - entity-graph
    - relationship-map
    - intelligence-report
  consumes:
    - domain
    - ip-address
    - email
    - person-name
contract:
  inputs:
    - type: network.target.domain
      description: Target domain name
    - type: network.target.ip
      description: Target IP address
    - type: security.target.email
      description: Email address
    - type: security.target.person
      description: Person name
  outputs:
    - type: security.recon.graph
      description: Link analysis graph
      mime: application/xml
    - type: security.recon.report
      description: Export report
      mime: text/html
  side_effects:
    - network_traffic
    - network_traffic
  resource_cost:
    cpu: high
    memory_mb: 1024
    network: medium
    disk_io: medium
resource_profile:
  cpu: high
  memory_mb: 1024
  network: medium
  disk_io: medium
allowed-tools:
  - maltego
  - Bash
  - execFile
parameters:
  - name: flag-g
    type: string
    required: false
    description: "Run in GUI mode with specified graph file"
    aliases:
      - -g
  - name: flag-c
    type: string
    required: false
    description: "Run in CLI mode with specified transform"
    aliases:
      - -c
  - name: flag-i
    type: string
    required: false
    description: "Import configuration"
    aliases:
      - -i
  - name: flag-e
    type: string
    required: false
    description: "Export graph to file"
    aliases:
      - -e
execution:
  template: "maltego"
  sandbox: execFile
  timeout_seconds: 86400
  shell: false
global_vars:
  target: domain
  domain: "example.com"
examples:
  - description: "Launch Maltego GUI"
    command: maltego
  - description: "Launch with a specific graph file"
    command: maltego -g /path/to/graph.mtgx
  - description: "Run a transform from the command line"
    command: maltego -c "maltego.TransformName" -e output.mtgx
references:
  - label: "Maltego Official Site"
    url: "https://www.maltego.com/"
  - label: "Maltego Transform Hub"
    url: "https://www.maltego.com/transform-hub/"
phase: enumeration
techniques:
  - discovery
  - recon
  - enumeration
items:
  - NoCreds
services: []
attack_types:
  - Enumeration
---

# Maltego — Link Analysis & OSINT

Maltego is a graphical link analysis tool for OSINT investigations. It provides an interactive environment for mining and correlating information from various public data sources, presenting results as entity graphs that reveal relationships between domains, IP addresses, email addresses, people, and organizations.

## Key Concepts

- **Entities**: Represent pieces of data (domains, IPs, emails, people)
- **Transforms**: Plugins that query data sources and return related entities
- **Graphs**: Visual representation of entity relationships
- **Machines**: Automated sequences of transforms for common investigations

## Common Use Cases

- Domain infrastructure mapping
- Email address correlation
- Social network footprinting
- Company organizational charting
- Person-of-interest profiling
