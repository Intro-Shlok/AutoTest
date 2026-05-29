---
id: security-forensics-steghide
namespace: security:forensics:steghide
name: steghide
description: Steganography tool for embedding and extracting hidden data within image and audio files.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - steganography.embed
  - steganography.extract
  - steganography.info
  - forensics.data.hiding
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
  - foremost
  - zsteg
  - strings
artifacts:
  - type: steganography.embedded.file
    description: File with embedded hidden data
    mime: application/octet-stream
    trust_level: verified
  - type: steganography.extracted.file
    description: Extracted hidden data from stego file
    mime: application/octet-stream
    trust_level: verified
workflow_edges:
  produces:
    - stego-file
    - extracted-data
  consumes:
    - cover-file
    - embed-file
    - stego-file
contract:
  inputs:
    - type: file.path
      description: Cover file (image/audio) to embed data into
    - type: file.path
      description: Data file to embed
    - type: string
      description: Passphrase for encryption
  outputs:
    - type: file.path
      description: Stego file with embedded data
      mime: application/octet-stream
    - type: file.path
      description: Extracted data file
      mime: application/octet-stream
  side_effects:
    - filesystem_write
    - filesystem_write
  resource_cost:
    cpu: low
    memory_mb: 64
    network: none
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 64
  network: none
  disk_io: low
allowed-tools:
  - steghide
  - Bash
  - execFile
parameters:
  - name: subcommand
    type: string
    required: true
    description: "Subcommand: embed, extract, or info"
    aliases:
      - embed
      - extract
      - info
  - name: flag-cf
    type: file
    required: false
    description: "Cover file (JPEG, BMP, WAV, AU) to hide data in"
    aliases:
      - -cf
      - --cover-file
  - name: flag-ef
    type: file
    required: false
    description: "File to embed into the cover file"
    aliases:
      - -ef
      - --embed-file
  - name: flag-p
    type: string
    required: false
    description: "Passphrase for embedding or extraction"
    aliases:
      - -p
      - --passphrase
  - name: flag-sf
    type: file
    required: false
    description: "Stego file (output for embed, input for extract)"
    aliases:
      - -sf
      - --stego-file
  - name: flag-xf
    type: file
    required: false
    description: "File to write extracted data to"
    aliases:
      - -xf
      - --extract-file
  - name: flag-z
    type: integer
    required: false
    description: "Compression level (1-9) before embedding"
    default_value: "1"
    aliases:
      - -z
      - --compress
  - name: flag-e
    type: string
    required: false
    description: "Encryption algorithm to use (e.g. aes256, twofish)"
    aliases:
      - -e
      - --encryption
  - name: flag-a
    type: string
    required: false
    description: "Embedding algorithm"
    aliases:
      - -a
      - --algorithm
  - name: flag-v
    type: boolean
    required: false
    description: "Verbose output"
    aliases:
      - -v
      - --verbose
  - name: flag-q
    type: boolean
    required: false
    description: "Quiet mode — suppress warnings"
    aliases:
      - -q
      - --quiet
  - name: info
    type: boolean
    required: false
    description: "Display information about a stego file"
    aliases:
      - --info
execution:
  template: "steghide embed -cf {cover} -ef {data} -p {passphrase}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
global_vars:
  cover: cover.jpg
  data: secret.txt
  passphrase: ""
examples:
  - description: "Embed a file into a JPEG image"
    command: steghide embed -cf cover.jpg -ef secret.txt -p mypassphrase
  - description: "Extract hidden data from a stego image"
    command: steghide extract -sf stego.jpg -p mypassphrase
  - description: "Embed with encryption and compression"
    command: steghide embed -cf cover.wav -ef secret.txt -p mypass -e aes256 -z 9
  - description: "Display info about a stego file"
    command: steghide info stego.jpg
  - description: "Extract hidden data to a specific output file"
    command: steghide extract -sf stego.jpg -p mypass -xf extracted.txt
  - description: "Embed using quiet mode"
    command: steghide embed -q -cf cover.bmp -ef data.zip -p mypass
references:
  - label: "Steghide SourceForge"
    url: "https://steghide.sourceforge.net/"
  - label: "Steghide man page"
    url: "https://manpages.debian.org/testing/steghide/steghide.1.en.html"
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
      package_name: "steghide"
      commands:
        - "apt-get install -y steghide"
---
# Steghide — Steganography Tool

Steghide embeds and extracts hidden data in JPEG, BMP, WAV, and AU files. It uses a passphrase for encryption and supports compression and various encryption algorithms.

## Key Features

- **Multiple formats**: JPEG, BMP, WAV, AU cover files
- **Encryption**: AES, Twofish, and other algorithms via -e flag
- **Compression**: Pre-embedding compression with adjustable level
- **Stego detection**: The `info` subcommand reveals embedded data metadata
