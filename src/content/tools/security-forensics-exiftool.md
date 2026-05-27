---
id: security-forensics-exiftool
namespace: security:forensics:exiftool
name: exiftool
description: Perl-based metadata reader and writer for extracting EXIF, IPTC, XMP, and other metadata from files.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - metadata.read.exif
  - metadata.read.iptc
  - metadata.read.xmp
  - metadata.write
  - forensics.metadata.extraction
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
  - strings
  - binwalk
  - file
artifacts:
  - type: metadata.exif
    description: EXIF metadata extracted from files
    mime: application/json
    trust_level: verified
  - type: metadata.report
    description: Metadata report in various formats
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - metadata
    - exif-data
    - metadata-report
  consumes:
    - target-file
    - target-directory
contract:
  inputs:
    - type: file.path
      description: File or directory to extract metadata from
    - type: output.format
      description: Output format (json, csv, tab, xml)
  outputs:
    - type: metadata.json
      description: Metadata as JSON
      mime: application/json
    - type: metadata.csv
      description: Metadata as CSV
      mime: text/csv
    - type: metadata.text
      description: Metadata as plain text
      mime: text/plain
  side_effects:
    - filesystem_write
  resource_cost:
    cpu: low
    memory_mb: 128
    network: none
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 128
  network: none
  disk_io: low
allowed-tools:
  - exiftool
  - Bash
  - execFile
parameters:
  - name: file
    type: string
    required: true
    description: "File(s) to read metadata from"
    aliases: []
  - name: flag-a
    type: boolean
    required: false
    description: "Show duplicate tags (all instances)"
    aliases:
      - -a
      - --duplicates
  - name: flag-r
    type: boolean
    required: false
    description: "Recursively process subdirectories"
    aliases:
      - -r
      - --recurse
  - name: flag-G
    type: boolean
    required: false
    description: "Print group name for each tag"
    aliases:
      - -G
      - --group
  - name: flag-j
    type: boolean
    required: false
    description: "JSON output format"
    aliases:
      - -j
      - --json
  - name: flag-t
    type: boolean
    required: false
    description: "Tab-delimited output format"
    aliases:
      - -t
      - --tab
  - name: flag-csv
    type: boolean
    required: false
    description: "CSV output format"
    aliases:
      - -csv
      - --csv
  - name: flag-p
    type: string
    required: false
    description: "Print format string for custom output"
    aliases:
      - -p
      - --print-format
  - name: flag-s
    type: boolean
    required: false
    description: "Short output — omit tag descriptions"
    aliases:
      - -s
      - --short
  - name: flag-n
    type: boolean
    required: false
    description: "Numeric values instead of descriptions"
    aliases:
      - -n
      - --numeric
  - name: flag-u
    type: boolean
    required: false
    description: "Include unknown tags"
    aliases:
      - -u
      - --unknown
  - name: flag-m
    type: boolean
    required: false
    description: "Ignore minor errors"
    aliases:
      - -m
      - --ignore-minor-errors
  - name: overwrite_original
    type: boolean
    required: false
    description: "Overwrite original file (backup as .original)"
    aliases:
      - --overwrite_original
  - name: flag-o
    type: string
    required: false
    description: "Output file or directory name"
    aliases:
      - -o
      - --output
  - name: flag-ext
    type: string
    required: false
    description: "Process only files with given extension"
    aliases:
      - -ext
      - --extension
  - name: flag-d
    type: string
    required: false
    description: "Date format string"
    aliases:
      - -d
      - --date-format
  - name: flag-v
    type: integer
    required: false
    description: "Verbose level (0-5)"
    default_value: "0"
    aliases:
      - -v
      - --verbose
  - name: list
    type: boolean
    required: false
    description: "List supported file types"
    aliases:
      - -list
      - --list
  - name: listx
    type: boolean
    required: false
    description: "List supported file types as XML"
    aliases:
      - -listx
      - --listx
  - name: charset
    type: string
    required: false
    description: "Character set for output encoding"
    aliases:
      - -charset
      - --charset
execution:
  template: "exiftool {file}"
  sandbox: execFile
  timeout_seconds: 120
  shell: false
global_vars:
  file: image.jpg
examples:
  - description: "Extract all metadata from a file"
    command: exiftool image.jpg
  - description: "Output metadata as JSON"
    command: exiftool -j image.jpg
  - description: "Recursively scan a directory for metadata"
    command: exiftool -r -j /path/to/photos/
  - description: "Extract only EXIF data from JPEG files recursively"
    command: exiftool -r -ext jpg -EXIF:All /path/to/photos/
  - description: "Tab-delimited output with group names"
    command: exiftool -G -t image.jpg
  - description: "Export metadata to CSV"
    command: exiftool -csv -r /path/to/photos/ > metadata.csv
  - description: "Remove all metadata from a file"
    command: exiftool -all= image.jpg --overwrite_original
  - description: "List all supported file types"
    command: exiftool -list
references:
  - label: "ExifTool Homepage"
    url: "https://exiftool.org/"
  - label: "ExifTool Documentation"
    url: "https://exiftool.org/exiftool_pod.html"
phase: enumeration
techniques:
  - discovery
items:
  - NoCreds
services: []
attack_types:
  - Discovery
---
# ExifTool — Metadata Reader/Writer

ExifTool is a powerful Perl-based utility for reading, writing, and manipulating metadata in a vast range of file formats. It supports EXIF, IPTC, XMP, GPS, and hundreds of other metadata types across images, audio, video, and documents.

## Key Features

- **Broad format support**: Hundreds of image, audio, video, and document formats
- **Multiple output formats**: JSON, CSV, XML, tab-delimited, custom print formats
- **Batch processing**: Recursive directory scanning with extension filtering
- **Metadata removal**: Bulk sanitization of sensitive metadata
