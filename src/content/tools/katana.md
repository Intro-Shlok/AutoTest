---
id: security-web-katana
namespace: security:web:katana
name: katana
description: Fast web crawler and spider from ProjectDiscovery for discovering endpoints,
  assets, and attack surface.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.discovery.endpoint
  - web.crawl.spider
  - web.enumeration.asset
  - web.discovery.js-source
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
  - gospider
  - hakrawler
  - aquatone
artifacts:
  - type: crawl.json
    description: Crawl results as JSON lines
    mime: application/json
    trust_level: verified
  - type: crawl.txt
    description: Crawl results as text output
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - endpoint-list
    - url-list
    - js-files
    - known-files
  consumes:
    - target-url
    - target-domain
contract:
  inputs:
    - type: web.target.url
      description: Target URL to crawl
    - type: web.target.domain
      description: Target domain to scope the crawl
    - type: web.crawl.depth
      description: Maximum crawl depth
  outputs:
    - type: crawl.json
      description: Discovered endpoints as JSON
      mime: application/json
    - type: crawl.txt
      description: Discovered endpoints as text
      mime: text/plain
  side_effects:
    - network_traffic
    - network_traffic
  resource_cost:
    cpu: low
    memory_mb: 128
    network: medium
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 128
  network: medium
  disk_io: low
allowed-tools:
  - katana
  - Bash
  - execFile
parameters:
  - name: url
    type: string
    required: true
    description: "Target URL to crawl"
    aliases:
      - -u
      - --url
  - name: depth
    type: integer
    required: false
    description: "Maximum crawl depth"
    default_value: "3"
    aliases:
      - -d
      - --depth
  - name: js-crawl
    type: boolean
    required: false
    description: "Enable JavaScript parsing and crawling"
    aliases:
      - -jc
      - --js-crawl
  - name: extension-match
    type: string
    required: false
    description: "Only crawl URLs matching extensions"
    aliases:
      - -em
      - --extension-match
  - name: extension-filter
    type: string
    required: false
    description: "Filter out URLs matching extensions"
    aliases:
      - -ef
      - --extension-filter
  - name: known-files
    type: string
    required: false
    description: "Check for known files (robots.txt, sitemap.xml)"
    aliases:
      - -kf
      - --known-files
  - name: max-response-size
    type: integer
    required: false
    description: "Maximum response body size in bytes"
    default_value: "5242880"
    aliases:
      - -mrs
      - --max-response-size
  - name: output
    type: string
    required: false
    description: "Write output to file"
    aliases:
      - -o
      - --output
  - name: json
    type: boolean
    required: false
    description: "Write output in JSON lines format"
    aliases:
      - -oJ
      - --json
  - name: status-code
    type: string
    required: false
    description: "Filter by status code (e.g. 200,302)"
    aliases:
      - -sc
      - --status-code
  - name: content-type
    type: string
    required: false
    description: "Filter by content type"
    aliases:
      - -ct
      - --content-type
  - name: headers
    type: string
    required: false
    description: "Custom HTTP headers"
    aliases:
      - -H
      - --headers
  - name: proxy
    type: string
    required: false
    description: "HTTP proxy address"
    aliases:
      - -p
      - --proxy
  - name: threads
    type: integer
    required: false
    description: "Number of concurrent threads"
    default_value: "10"
    aliases:
      - -t
      - --threads
  - name: rate-limit
    type: integer
    required: false
    description: "Maximum requests per second"
    aliases:
      - -rl
      - --rate-limit
  - name: timeout
    type: integer
    required: false
    description: "Request timeout in seconds"
    default_value: "10"
    aliases:
      - -timeout
      - --timeout
  - name: silent
    type: boolean
    required: false
    description: "Suppress output banner and progress"
    aliases:
      - -silent
      - --silent
  - name: verbose
    type: boolean
    required: false
    description: "Verbose output"
    aliases:
      - -v
      - --verbose
  - name: field
    type: string
    required: false
    description: "Fields to display in output"
    default_value: "url"
    aliases:
      - -f
      - --field
  - name: automatic-form-fill
    type: boolean
    required: false
    description: "Automatically fill forms for crawling"
    aliases:
      - -aff
      - --automatic-form-fill
  - name: insecure
    type: boolean
    required: false
    description: "Skip TLS certificate verification"
    aliases:
      - -k
      - --insecure
  - name: no-headless
    type: boolean
    required: false
    description: "Disable headless browser crawling"
    aliases:
      - -nh
      - --no-headless
execution:
  template: "katana -u {target} -d {depth}"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
global_vars:
  target: url
  depth: "3"
examples:
  - description: "Basic crawl with default depth"
    command: katana -u http://target.com
  - description: "Deep crawl with JavaScript parsing"
    command: katana -u http://target.com -d 5 -jc
  - description: "Filter by specific extensions"
    command: katana -u http://target.com -em php,asp,js
  - description: "Output crawled URLs as JSON"
    command: katana -u http://target.com -oJ -o endpoints.json
  - description: "Crawl with proxy and rate limiting"
    command: katana -u http://target.com -p http://127.0.0.1:8080 -rl 50
  - description: "Silent mode with filtered status codes"
    command: katana -u http://target.com -silent -sc 200,302
references:
  - label: "Katana GitHub"
    url: "https://github.com/projectdiscovery/katana"
  - label: "ProjectDiscovery Katana"
    url: "https://projectdiscovery.io/tools/katana"
phase: enumeration
techniques:
  - discovery
  - discovery
  - discovery
items:
  - NoCreds
services: []
attack_types:
  - Enumeration
install:
    - method: go
      repo_url: "github.com/projectdiscovery/katana/cmd/katana"
      commands:
        - "go install -v github.com/projectdiscovery/katana/cmd/katana@latest"
---

# Katana — Web Crawler and Spider

Katana is a fast web crawler from ProjectDiscovery designed for discovering endpoints, JavaScript sources, and hidden assets. It supports both standard HTTP crawling and headless browser-based crawling for JavaScript-heavy applications.

## Basic Usage

```bash
# Basic crawl
katana -u http://target.com

# Deep crawl with JS parsing
katana -u http://target.com -d 5 -jc

# Output as JSON
katana -u http://target.com -oJ -o crawl.json

# Crawl with rate limiting
katana -u http://target.com -rl 50 -t 5
```

## Crawl Modes

| Mode | Flag | Description |
|------|------|-------------|
| Standard | (default) | HTTP-based crawling |
| JS Crawl | `-jc` | Parse JavaScript for URLs |
| Headless | (default) | Headless browser for JS-heavy sites |
| Form Fill | `-aff` | Auto-fill forms during crawl |
