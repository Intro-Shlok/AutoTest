---
id: network-dns-dig
namespace: network:dns:dig
name: dig
description: DNS lookup utility for querying name servers and debugging DNS resolution
  issues.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.recon.dns
  - network.dns.query
  - network.dns.lookup
  - network.dns.reverse
  - network.dns.trace
  - system.file.read
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
  - cross-platform
dependencies: []
related_tools:
  - nslookup
  - host
  - whois
  - dnsrecon
artifacts:
  - type: network.dns.response
    description: DNS response data
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - dns-records
    - dns-trace
  consumes:
    - domain-name
contract:
  inputs:
    - type: network.target.domain
      description: Domain name to query
  outputs:
    - type: network.dns.response
      description: DNS query results with record details
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
  - dig
  - Bash
  - execFile
parameters:
  - name: flag-4
    type: string
    required: false
    description: "(use IPv4 query transport only)"
    aliases:
      - "-4"
  - name: flag-6
    type: string
    required: false
    description: "(use IPv6 query transport only)"
    aliases:
      - "-6"
  - name: flag-b
    type: string
    required: false
    description: "(bind to source address/port)"
    aliases:
      - -b
    enum:
      - bind to source address
      - port
  - name: flag-c
    type: string
    required: false
    description: "(specify query class)"
    aliases:
      - -c
  - name: flag-f
    type: string
    required: false
    description: "(batch mode)"
    aliases:
      - -f
  - name: flag-k
    type: string
    required: false
    description: "(specify tsig key file)"
    aliases:
      - -k
  - name: flag-m
    type: string
    required: false
    description: "(enable memory usage debugging)"
    aliases:
      - -m
  - name: flag-p
    type: integer
    required: false
    description: "(specify port number)"
    aliases:
      - -p
  - name: flag-q
    type: string
    required: false
    description: "(specify query name)"
    aliases:
      - -q
  - name: flag-r
    type: string
    required: false
    description: "(do not read ~/.digrc)"
    aliases:
      - -r
    enum:
      - do not read ~
      - .digrc
  - name: flag-t
    type: string
    required: false
    description: "(specify query type)"
    aliases:
      - -t
  - name: flag-u
    type: string
    required: false
    description: "(display times in usec instead of msec)"
    aliases:
      - -u
  - name: flag-x
    type: string
    required: false
    description: "(shortcut for reverse lookups)"
    aliases:
      - -x
      - -n
  - name: flag-y
    type: integer
    required: false
    description: "d-opt is of the form +keyword[=value], where keyword is: +[no]aaflag
      (Set AA flag in query (+[no]aaflag)) +[no]aaonly (Set AA flag in query (+[no]aaflag))
      +[no]additional (Control display of additi..."
    aliases:
      - -y
execution:
  template: "dig {flag-4} {flag-6} {flag-b} {flag-c} {flag-f}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
global_vars:
  target: ip
  domain: domain
examples:
  - description: "Standard A record lookup"
    command: "dig example.com A"
  - description: "Query MX records for mail servers"
    command: "dig example.com MX"
  - description: "Trace full DNS delegation path"
    command: "dig example.com +trace"
  - description: "Query a specific nameserver"
    command: "dig @8.8.8.8 example.com A"
  - description: "Reverse DNS lookup"
    command: "dig -x 142.250.80.14"
  - description: "Bulk domain transfer attempt (often disabled)"
    command: "dig example.com AXFR"
  - description: Read an arbitrary file by specifying it as a batch file. Note that
      this will leak lines of the file read as outbound DNS lookups.
    command: "dig -f /etc/passwd\n"
  - description: 'Argument injection: read local file: Read an arbitrary file by specifying
      it as a batch file. Note that this will leak lines of the file read as outbound
      DNS lookups.'
    command: dig -f /etc/passwd
  - description: Basic A record lookup
    command: dig example.com
  - description: Specify DNS server to use for the query
    command: dig @8.8.8.8 example.com
  - description: 'cheat.sheets: dig'
    command: dig example.com AAAA
  - description: Display only the answer section of the query
    command: dig +noquestion +noauthority +noadditional +noanswer example.com
  - description: Perform a reverse DNS lookup for an IP address
    command: dig -x 192.0.2.1
  - description: Use verbose output to display entire response
    command: dig +noall +answer +comment example.com
  - description: Query whois information using dig
    command: dig +short txt whois.example.com
  - description: Query DNS for specific port using SRV record
    command: dig _sip._tcp.example.com SRV
  - description: Conduct a trace from root to authoritative DNS server
    command: dig +trace example.com
  - description: Measure and display query time
    command: dig example.com +stats
  - description: Get list of name servers for a domain
    command: dig example.com NS
references:
  - label: "dig man page"
    url: "https://linux.die.net/man/1/dig"
  - label: "BIND documentation"
    url: "https://www.isc.org/bind/"
features:
  - output-json
  - file-system
techniques:
  - collection
---

# dig — DNS Lookup Utility

Dig (Domain Information Groper) is the most versatile DNS debugging tool available. It provides detailed information about DNS records, server responses, and resolution paths.

## Common Record Types

| Type | Purpose | Example Use |
|------|---------|-------------|
| **A** | IPv4 address mapping | `dig example.com A` |
| **AAAA** | IPv6 address mapping | `dig example.com AAAA` |
| **MX** | Mail exchange servers | `dig example.com MX` |
| **NS** | Authoritative name servers | `dig example.com NS` |
| **TXT** | Arbitrary text data (SPF, DKIM) | `dig example.com TXT` |
| **CNAME** | Canonical name alias | `dig www.example.com CNAME` |
| **SOA** | Start of Authority (zone metadata) | `dig example.com SOA` |

## Output Interpretation

```bash
; <<>> DiG 9.10.6 <<>> example.com A
;; QUESTION SECTION:
;example.com.           IN  A

;; ANSWER SECTION:
example.com.        3600    IN  A   93.184.216.34

;; Query time: 45 msec
;; SERVER: 192.168.1.1#53(192.168.1.1)
;; WHEN: Mon Jan 15 10:00:00 EDT 2026
;; MSG SIZE  rcvd: 56
```

| Field | Meaning |
|-------|---------|
| **3600** | TTL (seconds) — how long the record can be cached |
| **IN** | Internet class |
| **Query time** | Round-trip in milliseconds |

## Advanced Queries

```bash
# Get all record types
dig example.com ANY

# DNSSEC validation
dig example.com +dnssec

# Short output (just the values)
dig example.com +short

# Multiline output for readability
dig example.com +multiline

# Query specific EDNS options
dig example.com +edns=0
```

## Related Tools

- **[nslookup](../../dns/nslookup.md)** — Simpler DNS lookup (legacy)
- **[host](../../dns/host.md)** — Minimal DNS lookup
- **[whois](../../intel/whois.md)** — Domain registration information
- **[dnsrecon](../../recon/dnsrecon.md)** — DNS enumeration tool
