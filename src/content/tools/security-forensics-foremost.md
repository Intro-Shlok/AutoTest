---
id: security-forensics-foremost
namespace: security:forensics:foremost
name: foremost
description: File carving tool that recovers deleted files from disk images based on file headers and footers.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - forensics.file.carving
  - disk.recovery.deleted
  - forensics.header.signature
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
dependencies: []
related_tools:
  - binwalk
  - autopsy
  - volatility
  - scalpel
artifacts:
  - type: forensics.file.carved
    description: Recovered carved file
    mime: application/octet-stream
    trust_level: verified
  - type: forensics.report.text
    description: Carving audit log
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - carved-files
    - carving-report
  consumes:
    - disk-image
contract:
  inputs:
    - type: disk.image.file
      description: Path to the disk image or raw device
    - type: directory.path
      description: Output directory for carved files
    - type: forensics.config.file
      description: Custom configuration file for file types
  outputs:
    - type: forensics.file.carved
      description: Recovered files organized by type
      mime: application/octet-stream
    - type: forensics.report.text
      description: Carving summary and audit log
      mime: text/plain
  side_effects:
    - filesystem_write
    - filesystem_write
  resource_cost:
    cpu: medium
    memory_mb: 256
    network: none
    disk_io: high
resource_profile:
  cpu: medium
  memory_mb: 256
  network: none
  disk_io: high
allowed-tools:
  - foremost
  - Bash
  - execFile
parameters:
  - name: flag-i
    type: file
    required: true
    description: "Input file or disk image to carve"
    aliases:
      - -i
      - --input
  - name: flag-o
    type: string
    required: true
    description: "Output directory for carved files"
    aliases:
      - -o
      - --output
  - name: flag-q
    type: boolean
    required: false
    description: "Quiet mode — display only errors"
    aliases:
      - -q
      - --quiet
  - name: flag-v
    type: boolean
    required: false
    description: "Verbose mode — display detailed progress"
    aliases:
      - -v
      - --verbose
  - name: flag-b
    type: integer
    required: false
    description: "Block size in bytes (default: 512)"
    default_value: "512"
    aliases:
      - -b
      - --block-size
  - name: flag-c
    type: file
    required: false
    description: "Configuration file for carving types"
    aliases:
      - -c
      - --config
  - name: flag-t
    type: string
    required: false
    description: "File types to carve (e.g. jpg,png,pdf)"
    aliases:
      - -t
      - --type
  - name: flag-d
    type: boolean
    required: false
    description: "Debug mode — print internal operations"
    aliases:
      - -d
      - --debug
  - name: flag-s
    type: integer
    required: false
    description: "Skip N bytes at the start of the image"
    default_value: "0"
    aliases:
      - -s
      - --skip
  - name: flag-k
    type: boolean
    required: false
    description: "Keep temporary files after carving"
    aliases:
      - -k
      - --keep
  - name: flag-T
    type: integer
    required: false
    description: "Timeout in seconds per file type"
    aliases:
      - -T
      - --timeout
  - name: flag-V
    type: boolean
    required: false
    description: "Display version information"
    aliases:
      - -V
      - --version
  - name: flag-h
    type: boolean
    required: false
    description: "Display help message"
    aliases:
      - -h
      - --help
execution:
  template: "foremost -i {image-file} -o {output-dir}"
  sandbox: execFile
  timeout_seconds: 1800
  shell: false
global_vars:
  image-file: disk.raw
  output-dir: carved_output
examples:
  - description: "Recover all supported file types from a disk image"
    command: foremost -i disk.raw -o carved_output
  - description: "Recover only JPEG and PNG files"
    command: foremost -i disk.raw -o carved_output -t jpg,png
  - description: "Use custom configuration and block size"
    command: foremost -i disk.raw -o carved_output -c custom.conf -b 1024
  - description: "Skip first 1MB of the image and keep temp files"
    command: foremost -i disk.raw -o carved_output -s 1048576 -k
  - description: "Verbose carving with specific file types"
    command: foremost -v -i disk.raw -o carved_output -t pdf,doc,zip
  - description: "Display help"
    command: foremost -h
references:
  - label: "Foremost GitHub"
    url: "https://github.com/korczis/foremost"
  - label: "Foremost man page"
    url: "https://manpages.debian.org/testing/foremost/foremost.1.en.html"
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
      package_name: "foremost"
      commands:
        - "apt-get install -y foremost"
---
# Foremost — File Carving Tool

Foremost recovers deleted files from disk images by matching file headers and footers. It supports a wide range of file types including JPEG, PNG, PDF, ZIP, DOC, and many more through a configurable signature database.

## Key Features

- **Header/footer carving**: Matches known file signatures
- **Configurable types**: Custom carve configurations via config file
- **Audit logging**: Tracks every recovered file with metadata
- **Carving depth**: Recovers files from unallocated disk space
