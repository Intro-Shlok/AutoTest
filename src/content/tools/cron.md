---
id: system-scheduler-cron
namespace: system:scheduler:cron
name: cron
description: Daemon to execute scheduled commands
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - system.scheduler.cron
  - system.scheduler.cron
platforms:
  - linux
risk_level: medium
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
features:
  - local
  - requires-root
techniques:
  - execution
  - persistence
  - command-and-control
parameters:
  - name: flag-f
    type: string
    required: false
    description: "Stay in foreground mode, don't daemonize"
    aliases:
      - -f
  - name: flag-l
    type: string
    required: false
    description: "Enable LSB compliant names for /etc/cron.d files. This setting,
      however, does not affect the parsing of files under /etc/cron.hourly, /etc/cron.daily,
      /etc/cron.weekly or /etc/cron.monthly"
    aliases:
      - -l
  - name: flag-n
    type: string
    required: false
    description: "Include the FQDN in the subject when sending mails. By default,
      cron will abbreviate the hostname"
    aliases:
      - -n
  - name: flag-N
    template_key: flag-n
    type: string
    required: false
    description: "Run cron jobs Now, immediately, and exit. This option is useful
      to perform tests"
    aliases:
      - -N
  - name: flag-L
    template_key: flag-l
    type: string
    required: false
    description: "Tell cron what to log about jobs (errors are logged regardless of
      this value) as the sum of the following values:"
    aliases:
      - -L
  - name: flag-x
    type: string
    required: false
    description: "Tell cron to be more verbose and output debugging information; debugflags
      is the sum of those values:"
    aliases:
      - -x
execution:
  template: "cron -f {flag-f} -l {flag-l} -n {flag-n} -N {flag-n} -L {flag-l}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with flag-f"
    command: "cron ${flag-f}"
  - description: "Display help message"
    command: "cron --help"
---

# cron — Daemon to execute scheduled commands

## Overview

`cron` is a command-line utility for daemon to execute scheduled commands.

## Usage

```
cron -f {flag-f} -l {flag-l} -n {flag-n} -N {flag-n} -L {flag-l}
```
