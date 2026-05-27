---
id: security-intel-whois
namespace: security:intel:whois
name: whois
description: Domain registration and IP address lookup service for querying WHOIS
  databases for ownership and metadata.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.intel.whois
  - security.intel.domain
  - security.intel.ip
  - security.recon.passive
  - network.dns.lookup
platforms:
  - linux
  - macos
  - cross-platform
risk_level: low
trust_level: community
execution_policy: enabled
architectures:
  - amd64
  - arm64
  - cross-platform
dependencies: []
related_tools:
  - dig
  - host
  - dnsrecon
  - theHarvester
artifacts:
  - type: security.intel.whois.record
    description: WHOIS record data for domain or IP
    mime: text/plain
    trust_level: community
workflow_edges:
  produces:
    - whois-record
    - domain-registration
  consumes:
    - domain-name
    - ip-address
contract:
  inputs:
    - type: network.target.domain
      description: Domain name to query
    - type: network.target.ip
      description: IP address to query
  outputs:
    - type: security.intel.whois.record
      description: Domain or IP registration details
      mime: text/plain
  side_effects:
    - network_traffic
  resource_cost:
    cpu: low
    memory_mb: 8
    network: low
    disk_io: none
resource_profile:
  cpu: low
  memory_mb: 8
  network: low
  disk_io: none
allowed-tools:
  - whois
  - Bash
  - execFile
parameters:
  - name: host HOST
    template_key: host-host
    type: string
    required: false
    description: "connect to server HOST"
    aliases:
      - -h
      - --host HOST
  - name: port PORT
    template_key: port-port
    type: integer
    required: false
    description: "connect to PORT"
    aliases:
      - -p
      - --port PORT
  - name: verbose
    type: string
    required: false
    description: "explain what is being done"
    aliases:
      - --verbose
  - name: no-recursion
    type: string
    required: false
    description: "disable recursion from registry to registrar servers"
    aliases:
      - --no-recursion
  - name: help
    type: string
    required: false
    description: "display this help and exit"
    aliases:
      - --help
  - name: version
    type: string
    required: false
    description: "output version information and exit"
    aliases:
      - --version
  - name: flag-l
    type: string
    required: false
    description: "find the one level less specific match"
    aliases:
      - -l
  - name: flag-m
    type: string
    required: false
    description: "find all one level more specific matches"
    aliases:
      - -m
  - name: flag-c
    type: string
    required: false
    description: "find the smallest match containing a mnt-irt attribute"
    aliases:
      - -c
  - name: flag-x
    type: string
    required: false
    description: "exact match"
    aliases:
      - -x
  - name: flag-b
    type: string
    required: false
    description: "return brief IP address ranges with abuse contact"
    aliases:
      - -b
  - name: flag-d
    type: string
    required: false
    description: "return DNS reverse delegation objects too"
    aliases:
      - -d
  - name: flag-i
    type: string
    required: false
    description: "do an inverse look-up for specified ATTRibutes"
    aliases:
      - -i
  - name: flag-T
    template_key: flag-t
    type: string
    required: false
    description: "only look for objects of TYPE"
    aliases:
      - -T
  - name: flag-r
    type: string
    required: false
    description: "turn off recursive look-ups for contact information"
    aliases:
      - -r
  - name: flag-a
    type: string
    required: false
    description: "also search all the mirrored databases"
    aliases:
      - -a
  - name: flag-s
    type: string
    required: false
    description: "Set the flag-s parameter"
    aliases:
      - -s
  - name: flag-g
    type: string
    required: false
    description: "find updates from SOURCE from serial FIRST to LAST"
    aliases:
      - -g
      - -L
  - name: flag-t
    type: string
    required: false
    description: "request template for object of TYPE"
    aliases:
      - -t
  - name: flag-v
    type: string
    required: false
    description: "request verbose template for object of TYPE"
    aliases:
      - -v
  - name: flag-q
    type: string
    required: false
    description: "Set the flag-q parameter"
    aliases:
      - -q
execution:
  template: "whois {host-host} {port-port} {verbose} {no-recursion} {help}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
global_vars:
  host-host: ip
  port-port: port
examples:
  - description: "Query domain registration information"
    command: "whois example.com"
  - description: "Query IP address ownership"
    command: "whois 8.8.8.8"
  - description: "Query a specific WHOIS server"
    command: "whois -h whois.verisign-grs.com example.com"
  - description: "Get raw server response"
    command: "whois -v example.com"
  - description: Retrieve registration details of an IP address
    command: whois 192.0.2.1
  - description: Query a specific WHOIS server for domain information
    command: whois -h whois.nic.xyz example.xyz
  - description: Display command usage information in case of errors or unsure use
    command: whois -h
  - description: Use specific WHOIS server on a non-standard port
    command: whois -h whois.example.com -p 43 example.com
  - description: Format output to be more readable by human
    command: whois -H example.com
  - description: Display help and additional options
    command: whois --help
references:
  - label: "WHOIS protocol specification"
    url: "https://datatracker.ietf.org/doc/html/rfc3912"
  - label: "ICANN WHOIS service"
    url: "https://whois.icann.org/"
---

# Whois — Domain and IP Registration Lookup

WHOIS is a query and response protocol for querying databases that store registered users or assignees of domain names and IP address blocks. It's an essential tool for passive reconnaissance and domain research.

## Key Information Retrieved

| Data Point | Description |
|------------|-------------|
| **Registrar** | Company where domain was registered |
| **Registrant** | Domain owner name and organization |
| **Creation Date** | When the domain was registered |
| **Expiration Date** | When registration expires |
| **Name Servers** | DNS servers for the domain |
| **Admin/Tech Contacts** | Administrative and technical contacts |

## Use Cases

### Security Research
- Identify domain ownership for threat intelligence
- Discover related domains via shared registrant info
- Verify domain age and legitimacy

### Network Administration
- Find contact info for abuse reporting
- Identify IP address block ownership
- Check domain expiration for renewal planning

## Limitations

- WHOIS privacy services often mask registrant details
- Rate-limited by many WHOIS servers
- Different TLDs use different WHOIS servers
- GDPR has reduced WHOIS data availability in Europe

## Related Tools

- **[dig](../../dns/dig.md)** — DNS record lookup
- **[dnsrecon](../../recon/dnsrecon.md)** — Automated DNS enumeration
- **[theHarvester](../../recon/theHarvester.md)** — Email and subdomain discovery
