---
id: network-diagnostic-traceroute
namespace: network:diagnostic:traceroute
name: traceroute
description: Network diagnostic tool for displaying the route and measuring transit
  delays of packets across an IP network.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.diagnostic.route
  - network.diagnostic.hop
  - network.diagnostic.latency
  - network.discovery.path
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
  - mtr
  - ping
  - pathping
  - tracepath
artifacts:
  - type: network.diagnostic.route
    description: Hop-by-hop route trace results
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - route-trace
    - hop-latency
  consumes:
    - target-host
contract:
  inputs:
    - type: network.target.host
      description: Target hostname or IP address to trace
  outputs:
    - type: network.diagnostic.route
      description: Sequential list of hops with per-hop latency measurements
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
  - traceroute
  - Bash
  - execFile
parameters:
  - name: flag-4
    type: string
    required: false
    description: "Use IPv4"
    aliases:
      - "-4"
  - name: flag-6
    type: string
    required: false
    description: "Use IPv6"
    aliases:
      - "-6"
  - name: debug
    type: string
    required: false
    description: "Enable socket level debugging"
    aliases:
      - -d
      - --debug
  - name: dont-fragment
    type: string
    required: false
    description: "Do not fragment packets"
    aliases:
      - -F
      - --dont-fragment
  - name: first
    type: string
    required: false
    description: "Start from the first_ttl hop (instead from 1)"
    aliases:
      - -f
      - --first
  - name: gateway
    type: string
    required: false
    description: "Route packets through the specified gateway (maximum 8 for IPv4
      and 127 for IPv6)"
    aliases:
      - -g
      - --gateway
  - name: icmp
    type: string
    required: false
    description: "Use ICMP ECHO for tracerouting"
    aliases:
      - -I
      - --icmp
  - name: tcp
    type: string
    required: false
    description: "Use TCP SYN for tracerouting (default port is 80)"
    aliases:
      - -T
      - --tcp
  - name: interface
    type: string
    required: false
    description: "Specify a network interface to operate with"
    aliases:
      - -i
      - --interface
  - name: max-hops
    type: integer
    required: false
    description: "Set the max number of hops (max TTL to be reached). Default is 30"
    aliases:
      - -m
      - --max-hops
  - name: sim-queries
    type: integer
    required: false
    description: "Set the number of probes to be tried simultaneously (default is
      16)"
    aliases:
      - -N
      - --sim-queries
  - name: flag-n
    type: string
    required: false
    description: "Do not resolve IP addresses to their domain names"
    aliases:
      - -n
  - name: port
    type: string
    required: false
    description: "Set the destination port to use. It is either"
    aliases:
      - -p
      - --port
  - name: tos
    type: string
    required: false
    description: "Set the TOS (IPv4 type of service) or TC (IPv6"
    aliases:
      - -t
      - --tos
  - name: flowlabel
    type: string
    required: false
    description: "Use specified flow_label for IPv6 packets"
    aliases:
      - -l
      - --flowlabel
  - name: wait
    type: integer
    required: false
    description: "Wait for a probe no more than HERE (default 3) times longer than
      a response from the same hop, or no more than NEAR (default 10) times than some
      next hop, or MAX (default 5.0) seconds (float point ..."
    aliases:
      - -w
      - --wait
  - name: queries
    type: integer
    required: false
    description: "Set the number of probes per each hop. Default is 3"
    aliases:
      - -q
      - --queries
  - name: flag-r
    type: string
    required: false
    description: "Bypass the normal routing and send directly to a"
    aliases:
      - -r
  - name: source
    type: string
    required: false
    description: "Use source src_addr for outgoing packets"
    aliases:
      - -s
      - --source
  - name: sendwait
    type: integer
    required: false
    description: "Minimal time interval between probes (default 0). If the value is
      more than 10, then it specifies a number in milliseconds, else it is a number
      of seconds (float point values allowed too)"
    aliases:
      - -z
      - --sendwait
  - name: extensions
    type: string
    required: false
    description: "Show ICMP extensions (if present), including MPLS"
    aliases:
      - -e
      - --extensions
  - name: as-path-lookups
    type: string
    required: false
    description: "Perform AS path lookups in routing registries and"
    aliases:
      - -A
      - --as-path-lookups
  - name: module
    type: string
    required: false
    description: "Use specified module (either builtin or external)"
    aliases:
      - -M
      - --module
  - name: options
    type: string
    required: false
    description: "Use module-specific option OPTS for the traceroute module. Several
      OPTS allowed, separated by comma. If OPTS is \"help\", print info about available
      options"
    aliases:
      - -O
      - --options
  - name: sport
    type: string
    required: false
    description: "Use source port num for outgoing packets. Implies"
    aliases:
      - --sport
  - name: fwmark
    type: string
    required: false
    description: "Set firewall mark for outgoing packets"
    aliases:
      - --fwmark
  - name: udp
    type: string
    required: false
    description: "Use UDP to particular port for tracerouting"
    aliases:
      - -U
      - --udp
  - name: dccp
    type: string
    required: false
    description: "Use DCCP Request for tracerouting (default port"
    aliases:
      - -D
      - --dccp
  - name: protocol
    type: string
    required: false
    description: "Use raw packet of protocol prot for tracerouting"
    aliases:
      - -P
      - --protocol
  - name: mtu
    type: string
    required: false
    description: "Discover MTU along the path being traced. Implies"
    aliases:
      - --mtu
execution:
  template: "traceroute {flag-4} {flag-6} {debug} {dont-fragment} {first}"
  sandbox: execFile
  timeout_seconds: 120
  shell: false
global_vars:
  target: ip
examples:
  - description: "Standard route trace"
    command: "traceroute google.com"
  - description: "Trace with numeric addresses only (faster)"
    command: "traceroute -n google.com"
  - description: "Trace with custom max hops"
    command: "traceroute -m 15 google.com"
  - description: "TCP-based traceroute to specific port"
    command: "traceroute -T -p 443 google.com"
  - description: Basic usage to display the route taken by packets to reach a host
    command: traceroute hostname_or_IP_address
  - description: Specify the maximum number of hops (TTL) to be used
    command: traceroute -m max_ttl hostname_or_IP_address
  - description: Use a particular protocol (ICMP or UDP)
    command: 'traceroute -I hostname_or_IP_address   # For ICMP'
  - description: 'cheat.sheets: traceroute'
    command: 'traceroute -U hostname_or_IP_address  # For UDP'
  - description: Specify the number of probe packets per hop
    command: traceroute -q n_queries hostname_or_IP_address
  - description: Set the initial TTL (Time-To-Live)
    command: traceroute -f first_ttl hostname_or_IP_address
  - description: Specify the wait time for a response
    command: traceroute -w wait_time hostname_or_IP_address
  - description: Change the default port
    command: traceroute -p port_number hostname_or_IP_address
  - description: Specify the interface to be used
    command: traceroute -i interface hostname_or_IP_address
  - description: Display the IP addresses numerically without resolving hostnames
    command: traceroute -n hostname_or_IP_address
  - description: Set the source address
    command: traceroute -s source_address hostname_or_IP_address
references:
  - label: "traceroute man page"
    url: "https://linux.die.net/man/8/traceroute"
  - label: "RFC 1393 — Traceroute using IP Option"
    url: "https://datatracker.ietf.org/doc/html/rfc1393"
---

# traceroute — Network Path Discovery

Traceroute maps the network path between your machine and a target host by sending packets with incrementing TTL (Time To Live) values. Each router along the path decrements the TTL and sends back an ICMP Time Exceeded message, revealing the route.

## How It Works

1. Sends packet with TTL=1 — first router responds, TTL decremented to 0
2. Sends packet with TTL=2 — second router responds
3. Continues until target reached or max hops exceeded

## Output Interpretation

```
traceroute to google.com (142.250.80.14), 30 hops max, 60 byte packets
 1  192.168.1.1 (192.168.1.1)  1.234 ms  1.123 ms  1.456 ms
 2  10.0.0.1 (10.0.0.1)  5.678 ms  5.432 ms  6.012 ms
 3  * * *  (no response)
 4  72.14.237.194 (72.14.237.194)  15.234 ms  14.987 ms  15.567 ms
 5  142.250.80.14 (142.250.80.14)  12.345 ms  12.123 ms  11.987 ms
```

### What to Look For

| Indicator | Meaning |
|-----------|---------|
| **`* * *`** | Hop not responding (firewall, ICMP disabled) |
| **High latency** | Slow link, geographic distance, congestion |
| **Latency jump** | Likely where the geographic distance is crossed |
| **Request timeout** | Packet dropped or filtered at that hop |

## Related Tools

- **[mtr](../../diagnostic/mtr.md)** — Continuous trace with real-time statistics
- **[ping](../../diagnostic/ping.md)** — Basic reachability and latency testing
- **[pathping](../../diagnostic/pathping.md)** — Windows tool combining ping and traceroute
