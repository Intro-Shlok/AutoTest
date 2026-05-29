---
id: security-forensics-autopsy
namespace: security:forensics:autopsy
name: autopsy
description: GUI-based digital forensics platform built on The Sleuth Kit for disk image analysis, file carving, and timeline generation.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - disk.analysis.image
  - forensics.file.carving
  - forensics.timeline.generation
  - forensics.keyword.search
  - forensics.hash.analysis
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
  - sleuthkit
  - volatility
  - foremost
  - binwalk
artifacts:
  - type: disk.image.raw
    description: Raw disk image for analysis
    mime: application/octet-stream
    trust_level: verified
  - type: forensics.report.html
    description: Autopsy analysis report in HTML
    mime: text/html
    trust_level: verified
  - type: forensics.case.database
    description: Autopsy case database (SQLite)
    mime: application/x-sqlite3
    trust_level: verified
workflow_edges:
  produces:
    - disk-analysis
    - carved-files
    - timeline
    - keyword-hits
    - hash-sets
  consumes:
    - disk-image
    - case-directory
contract:
  inputs:
    - type: disk.image.file
      description: Path to the disk image to analyze
    - type: directory.path
      description: Case directory for storing results
    - type: forensics.ingest.module
      description: Ingest module configuration
  outputs:
    - type: forensics.report.html
      description: HTML analysis report
      mime: text/html
    - type: forensics.file.carved
      description: Recovered carved files
      mime: application/octet-stream
  side_effects:
    - filesystem_write
    - filesystem_write
  resource_cost:
    cpu: medium
    memory_mb: 1024
    network: low
    disk_io: high
resource_profile:
  cpu: medium
  memory_mb: 1024
  network: low
  disk_io: high
allowed-tools:
  - autopsy
  - Bash
  - execFile
parameters:
  - name: help
    type: boolean
    required: false
    description: "Display help message"
    aliases:
      - --help
  - name: version
    type: boolean
    required: false
    description: "Display version information"
    aliases:
      - --version
  - name: no-browser
    type: boolean
    required: false
    description: "Do not open the browser on startup"
    aliases:
      - --no-browser
  - name: flag-p
    type: integer
    required: false
    description: "Port to bind the web interface"
    default_value: "9999"
    aliases:
      - -p
      - --port
  - name: flag-H
    type: string
    required: false
    description: "Host address to bind"
    default_value: "127.0.0.1"
    aliases:
      - -H
      - --host
  - name: admin-pass
    type: string
    required: false
    description: "Administrator password for first-run setup"
    aliases:
      - --admin-pass
  - name: ingest-modules
    type: string
    required: false
    description: "Comma-separated list of ingest modules to run"
    aliases:
      - --ingest-modules
  - name: keyword-list
    type: file
    required: false
    description: "File containing keywords to search"
    aliases:
      - --keyword-list
  - name: hash-db
    type: file
    required: false
    description: "Hash database for known file matching"
    aliases:
      - --hash-db
  - name: flag-version
    type: boolean
    required: false
    description: "Show Autopsy version"
    aliases:
      - -version
      - --version
execution:
  template: "autopsy"
  sandbox: execFile
  timeout_seconds: 3600
  shell: false
global_vars: {}
examples:
  - description: "Start Autopsy web interface on default port"
    command: autopsy
  - description: "Start Autopsy on a custom port without opening browser"
    command: autopsy --no-browser -p 9999
  - description: "Bind to all network interfaces"
    command: autopsy -H 0.0.0.0
  - description: "Start with specific ingest modules"
    command: autopsy --ingest-modules "RecentActivity,HashLookup,KeywordSearch"
  - description: "Display help"
    command: autopsy --help
  - description: "Show version"
    command: autopsy --version
references:
  - label: "Autopsy Documentation"
    url: "https://www.autopsy.com/documentation/"
  - label: "Sleuth Kit GitHub"
    url: "https://github.com/sleuthkit/sleuthkit"
phase: enumeration
techniques:
  - discovery
items:
  - NoCreds
services: []
attack_types:
  - Discovery
install:
    - method: apt
      package_name: "autopsy"
      commands:
        - "apt-get install -y autopsy"
---
# Autopsy — Digital Forensics Platform

Autopsy is a GUI-based digital forensics platform built on The Sleuth Kit. It provides disk image analysis, file carving, keyword search, timeline generation, and hash set analysis through an intuitive web interface.

## Key Features

- **Multi-user**: Web-based interface supports collaborative cases
- **Modular ingest**: Pluggable ingest modules for extensible analysis
- **Timeline analysis**: Visual timeline of file system activity
- **Keyword search**: Indexed text search across disk images
- **File carving**: Recovers deleted files using file signatures
