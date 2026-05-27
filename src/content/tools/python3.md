---
id: dev-runtime-python3
namespace: dev:runtime:python3
name: python3
description: Python programming language interpreter
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - dev.runtime.python3
  - dev.runtime.execute
platforms:
  - linux
  - macos
  - windows
risk_level: low
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
parameters:
  - name: flag-b
    type: string
    required: false
    description: ": issue warnings about converting bytes/bytearray to str and comparing"
    aliases:
      - -b
  - name: flag-c
    type: string
    required: false
    description: "Set the flag-c parameter"
    aliases:
      - -c
  - name: flag-d
    type: string
    required: false
    description: ": turn on parser debugging output (for experts only, only works
      on"
    aliases:
      - -d
  - name: flag-h
    type: string
    required: false
    description: ": print this help message and exit (also -? or --help)"
    aliases:
      - -h
  - name: flag-i
    type: string
    required: false
    description: ": inspect interactively after running script; forces a prompt even"
    aliases:
      - -i
  - name: flag-m
    type: string
    required: false
    description: "Set the flag-m parameter"
    aliases:
      - -m
  - name: flag-q
    type: string
    required: false
    description: ": don't print version and copyright messages on interactive startup"
    aliases:
      - -q
  - name: flag-s
    type: file
    required: false
    description: ": don't add user site directory to sys.path; also PYTHONNOUSERSITE=x"
    aliases:
      - -s
  - name: flag-u
    type: string
    required: false
    description: ": force the stdout and stderr streams to be unbuffered"
    aliases:
      - -u
  - name: flag-v
    type: string
    required: false
    description: ": verbose (trace import statements); also PYTHONVERBOSE=x"
    aliases:
      - -v
  - name: flag-W
    template_key: flag-w
    type: string
    required: false
    description: "also PYTHONWARNINGS=arg"
    aliases:
      - -W
  - name: flag-x
    type: string
    required: false
    description: ": skip first line of source, allowing use of non-Unix forms of #!cmd"
    aliases:
      - -x
  - name: flag-X
    template_key: flag-x
    type: string
    required: false
    description: "Set the flag-X parameter"
    aliases:
      - -X
      - -s
  - name: check-hash-based-pycs
    type: string
    required: false
    description: "control how Python invalidates hash-based .pyc files"
    aliases:
      - --check-hash-based-pycs
  - name: help-env
    type: string
    required: false
    description: "Set the help-env parameter"
    aliases:
      - --help-env
  - name: help-xoptions
    type: string
    required: false
    description: "Set the help-xoptions parameter"
    aliases:
      - -s
      - -X
      - --help-xoptions
  - name: help-all
    type: string
    required: false
    description: "Set the help-all parameter"
    aliases:
      - --help-all
features:
  - local
  - batch
techniques:
  - analysis
  - defense-evasion
  - execution
  - credential-access
  - privilege-escalation
execution:
  template: "python3 {flag-b} {flag-c} {flag-d} {flag-h} {flag-i}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
global_vars:
  target: ip
  port: port
  user: user
  domain: domain
examples:
  - description: "Basic usage with flag_b"
    command: "python3 ${flag_b}"
  - description: "Display help message"
    command: "python3 --help"
  - description: NetRunners Active Directory/exploitation
    command: python3 targetedKerberoast.py -v -d {{DOMAIN}} -u {{USER}} -p '{{PASSWORD}}'
      --request-user TARGET_USER
  - description: NetRunners Active Directory/post-exploitation
    command: python3 gMSADumper.py -u {{USER}} -p '{{PASSWORD}}' -d {{DOMAIN}}
  - description: NetRunners KERBEROS/exploitation
    command: python3 targetedKerberoast.py -k --dc-host {{DC.DOMAIN}} -u {{USER}}
      -d {{DOMAIN}}
  - description: NetRunners web/exploitation
    command: python3 git_dumper.py {{URL}} git_dump
phase: exploitation
---

# python3 — Python programming language interpreter

## Overview

`python3` is a command-line utility for python programming language interpreter.

## Usage

```
python3 -b {{flag_b}} -c {{flag_c}} -d {{flag_d}} -h {{flag_h}} -i {{flag_i}}
```
