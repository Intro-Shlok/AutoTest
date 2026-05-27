---
id: security-graphql-clairvoyance
namespace: security:graphql:clairvoyance
name: clairvoyance
description: GraphQL schema enumeration tool that uses introspection queries and field suggestion brute-force to recover API schema definitions.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - graphql.enum.schema
  - graphql.discovery.field
  - graphql.introspection
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
  - burpsuite
  - owasp-zap
  - nmap
artifacts:
  - type: graphql.schema.json
    description: Reconstructed GraphQL schema
    mime: application/json
    trust_level: verified
  - type: report.txt
    description: Schema enumeration results
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - graphql-schema
  consumes:
    - target-url
contract:
  inputs:
    - type: web.target.url
      description: GraphQL endpoint URL
  outputs:
    - type: graphql.schema.json
      description: Reconstructed GraphQL schema as JSON
      mime: application/json
  side_effects:
    - network_traffic
  resource_cost:
    cpu: low
    memory_mb: 64
    network: low
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 64
  network: low
  disk_io: low
allowed-tools:
  - clairvoyance
  - python3
  - Bash
  - execFile
parameters:
  - name: url
    type: string
    required: true
    description: "GraphQL endpoint URL"
    aliases:
      - -u
      - --url
  - name: flag-json
    type: string
    required: false
    description: "Output file for the reconstructed schema JSON"
    aliases:
      - -j
      - --json
  - name: flag-wordlist
    type: string
    required: false
    description: "Wordlist file for field name bruteforce"
    aliases:
      - -w
      - --wordlist
  - name: flag-threads
    type: integer
    required: false
    description: "Number of threads for field discovery"
    aliases:
      - -t
      - --threads
  - name: flag-header
    type: string
    required: false
    description: "Custom HTTP header (name:value)"
    aliases:
      - -H
      - --header
  - name: flag-proxy
    type: string
    required: false
    description: "HTTP proxy to use"
    aliases:
      - -p
      - --proxy
execution:
  template: "clairvoyance {flag-json} {flag-wordlist} {flag-threads} {flag-header} {flag-proxy} -u {url}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
examples:
  - description: "Basic GraphQL schema enumeration"
    command: clairvoyance -u https://api.example.com/graphql
  - description: "Save schema to file with custom wordlist"
    command: clairvoyance -u https://api.example.com/graphql -j schema.json -w wordlist.txt
  - description: "Use proxy and custom header"
    command: 'clairvoyance -u https://api.example.com/graphql -p http://127.0.0.1:8080 -H "Authorization: Bearer token"'
references:
  - label: "Clairvoyance GitHub"
    url: "https://github.com/nicholasaleks/clairvoyance"
phase: enumeration
techniques:
  - discovery
  - enumeration
items:
  - NoCreds
services:
  - HTTP
attack_types:
  - Discovery
  - Enumeration
---

# Clairvoyance — GraphQL Schema Enumeration

Clairvoyance is a Python-based tool for GraphQL schema enumeration that uses introspection queries combined with field suggestion brute-force to recover API schema definitions even when introspection is partially restricted.

## Usage

```bash
# Basic enumeration
clairvoyance -u https://api.example.com/graphql

# Save schema JSON
clairvoyance -u https://api.example.com/graphql -j schema.json

# Use wordlist for field discovery
clairvoyance -u https://api.example.com/graphql -w common_fields.txt

# Authenticated scan
clairvoyance -u https://api.example.com/graphql -H "Cookie: session=abc123"
```
