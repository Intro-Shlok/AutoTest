---
id: network-firewall-iptables
namespace: network:firewall:iptables
name: iptables
description: Administration tool for IPv4 firewall rules
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.firewall.iptables
platforms:
  - linux
risk_level: high
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
features:
  - remote
  - network-intensive
  - requires-root
techniques:
  - defense-evasion
  - network-manipulation
  - discovery
  - command-and-control
parameters:
  - name: append
    type: string
    required: false
    description: "Append to chain"
    aliases:
      - -A
      - --append
  - name: check
    type: string
    required: false
    description: "Check for the existence of a rule"
    aliases:
      - -C
      - --check
  - name: delete
    type: string
    required: false
    description: "Delete matching rule from chain"
    aliases:
      - -D
      - --delete
  - name: delete-2
    type: string
    required: false
    description: "Delete rule rulenum (1 = first) from chain"
    aliases:
      - -D
      - --delete
  - name: insert
    type: string
    required: false
    description: "Insert in chain as rulenum (default 1=first)"
    aliases:
      - -I
      - --insert
  - name: replace
    type: string
    required: false
    description: "Replace rule rulenum (1 = first) in chain"
    aliases:
      - -R
      - --replace
  - name: list
    type: string
    required: false
    description: "[chain [rulenum]]"
    aliases:
      - --list
  - name: list-rules
    type: string
    required: false
    description: "Print the rules in a chain or all chains"
    aliases:
      - -S
      - --list-rules
  - name: flush
    type: string
    required: false
    description: "Delete all rules in chain or all chains"
    aliases:
      - -F
      - --flush
  - name: zero
    type: string
    required: false
    description: "[chain [rulenum]]"
    aliases:
      - --zero
  - name: new
    type: string
    required: false
    description: "chain Create a new user-defined chain"
    aliases:
      - --new
  - name: delete-chain
    type: string
    required: false
    description: "[chain] Delete a user-defined chain"
    aliases:
      - --delete-chain
  - name: policy
    type: string
    required: false
    description: "Change policy on chain to target"
    aliases:
      - -P
      - --policy
  - name: rename-chain
    type: string
    required: false
    description: "old-chain new-chain Change chain name, (moving any references)"
    aliases:
      - --rename-chain
  - name: ipv4
    type: string
    required: false
    description: "Nothing (line is ignored by ip6tables-restore)"
    aliases:
      - --ipv4
  - name: ipv6
    type: string
    required: false
    description: "Error (line is ignored by iptables-restore)"
    aliases:
      - --ipv6
  - name: jump
    type: string
    required: false
    description: "target"
    aliases:
      - --jump
  - name: goto
    type: string
    required: false
    description: "chain"
    aliases:
      - --goto
  - name: match
    type: string
    required: false
    description: "match"
    aliases:
      - --match
  - name: numeric
    type: integer
    required: false
    description: "numeric output of addresses and ports"
    aliases:
      - --numeric
  - name: table
    type: string
    required: false
    default_value: "filter"
    description: "table table to manipulate"
    aliases:
      - --table
  - name: verbose
    type: string
    required: false
    description: "verbose mode"
    aliases:
      - --verbose
  - name: wait
    type: number
    required: false
    description: "[seconds] maximum wait to acquire xtables lock before give up"
    aliases:
      - --wait
  - name: line-numbers
    type: string
    required: false
    description: "print line numbers when listing"
    aliases:
      - --line-numbers
  - name: exact
    type: string
    required: false
    description: "expand numbers (display exact values)"
    aliases:
      - --exact
  - name: modprobe
    type: string
    required: false
    description: "try to insert modules using this command"
    aliases:
      - --modprobe
  - name: set-counters
    type: string
    required: false
    description: "set the counter during insert/append"
    aliases:
      - -c
      - --set-counters
execution:
  template: "iptables -A {append} -C {check} -D {delete} -D {delete-2} -I {insert}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Basic usage with append"
    command: "iptables ${append}"
  - description: "Display help message"
    command: "iptables --help"
---

# iptables — Administration tool for IPv4 firewall rules

## Overview

`iptables` is a command-line utility for administration tool for ipv4 firewall rules.

## Usage

```
iptables -A {append} -C {check} -D {delete} -D {delete-2} -I {insert}
```
