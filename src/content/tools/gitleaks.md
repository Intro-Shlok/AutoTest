---
id: security-secrets-gitleaks
namespace: security:secrets:gitleaks
name: gitleaks
description: SAST tool for detecting secrets, passwords, API keys, tokens, and other sensitive data in git repositories.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - secrets.scan.repo
  - secrets.scan.diff
  - secrets.detect.api-key
  - secrets.detect.password
  - secrets.detect.token
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
  - trufflehog
  - gitrob
  - shhgit
artifacts:
  - type: secrets.scan.report
    description: Secret detection report
    mime: text/plain
    trust_level: verified
  - type: secrets.scan.json
    description: JSON format report
    mime: application/json
    trust_level: verified
workflow_edges:
  produces:
    - secrets-findings
    - scan-report
  consumes:
    - repo.path
contract:
  inputs:
    - type: git.repo.path
      description: Repository path or URL to scan
  outputs:
    - type: secrets.scan.report
      description: Detected secrets report
      mime: text/plain
    - type: secrets.scan.json
      description: JSON format findings
      mime: application/json
  side_effects: []
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
  - gitleaks
  - Bash
  - execFile
parameters:
  - name: flag-config
    type: string
    required: false
    description: "Config file path"
    aliases:
      - -c
      - --config
  - name: flag-repo-path
    type: string
    required: false
    description: "Repository path to scan"
    aliases:
      - -r
      - --repo-path
  - name: flag-repo-url
    type: string
    required: false
    description: "Repository URL to scan"
    aliases:
      - -u
      - --repo-url
  - name: flag-verbose
    type: boolean
    required: false
    description: "Verbose output"
    aliases:
      - -v
      - --verbose
  - name: flag-log-level
    type: string
    required: false
    description: "Log level (debug, info, warn, error)"
    aliases:
      - --log-level
  - name: flag-no-git
    type: boolean
    required: false
    description: "Scan a directory without git history"
    aliases:
      - --no-git
  - name: flag-format
    type: string
    required: false
    description: "Output format (json, csv, sarif)"
    aliases:
      - -f
      - --format
  - name: flag-exit-code
    type: boolean
    required: false
    description: "Non-zero exit code if leaks found"
    aliases:
      - --exit-code
  - name: flag-redact
    type: boolean
    required: false
    description: "Redact secrets from output"
    aliases:
      - --redact
execution:
  template: "gitleaks {flag-verbose} {flag-log-level} {flag-no-git} {flag-format} {flag-exit-code} {flag-redact} {flag-config} {flag-repo-path} {flag-repo-url}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
examples:
  - description: "Scan local repository"
    command: gitleaks -r /path/to/repo
  - description: "Scan remote repository URL"
    command: gitleaks -u https://github.com/user/repo
  - description: "Scan with JSON output"
    command: gitleaks -r /path/to/repo -f json -o findings.json
  - description: "Scan directory without git history"
    command: gitleaks --no-git -r /path/to/directory
  - description: "Scan with custom config and redact secrets"
    command: gitleaks -r /path/to/repo -c gitleaks.toml --redact
references:
  - label: "gitleaks GitHub"
    url: "https://github.com/gitleaks/gitleaks"
  - label: "gitleaks Documentation"
    url: "https://github.com/gitleaks/gitleaks?tab=readme-ov-file#configuration"
phase: enumeration
techniques:
  - discovery
  - credential-access
items:
  - Password
  - Hash
  - NoCreds
services: []
attack_types:
  - CredentialAccess
  - Discovery
---

# gitleaks — Secrets Scanner

gitleaks is a Static Application Security Testing (SAST) tool for detecting hardcoded secrets like passwords, API keys, tokens, and SSH keys in git repositories. It can scan local directories, git history, or remote repository URLs.

## Usage

```bash
# Scan local repository
gitleaks -r /path/to/repo

# Scan remote repository
gitleaks -u https://github.com/user/repo

# JSON output with exit code
gitleaks -r /path/to/repo -f json -o findings.json --exit-code

# Scan without git history
gitleaks --no-git -r /path/to/directory

# Scan with redaction
gitleaks -r /path/to/repo --redact
```