---
id: network-diagnostic-ping
namespace: network:diagnostic:ping
name: ping
description: Network utility for testing reachability and measuring round-trip latency
  to a remote host.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.diagnostic.reachability
  - network.diagnostic.latency
  - network.diagnostic.packetloss
  - network.discovery.host
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
  - cross-platform
dependencies: []
related_tools:
  - fping
  - hping3
  - mtr
  - traceroute
artifacts:
  - type: network.diagnostic.ping.result
    description: Ping statistics and round-trip times
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - ping-results
    - latency-stats
  consumes:
    - target-host
contract:
  inputs:
    - type: network.target.host
      description: Target hostname or IP address to ping
  outputs:
    - type: network.diagnostic.ping.result
      description: Ping response statistics including min/avg/max RTT and packet loss
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
  - ping
  - Bash
  - execFile
parameters:
  - name: flag-3
    type: string
    required: false
    description: "RTT precision (do not round up the result time)"
    aliases:
      - "-3"
  - name: flag-a
    type: string
    required: false
    description: "use audible ping"
    aliases:
      - -a
  - name: flag-c
    type: string
    required: false
    description: "stop after <count> replies"
    aliases:
      - -c
  - name: flag-d
    type: string
    required: false
    description: "use SO_DEBUG socket option"
    aliases:
      - -d
  - name: flag-e
    type: string
    required: false
    description: "define identifier for ping session, default is random for"
    aliases:
      - -e
  - name: flag-f
    type: string
    required: false
    description: "flood ping"
    aliases:
      - -f
  - name: flag-h
    type: string
    required: false
    description: "print help and exit"
    aliases:
      - -h
  - name: flag-I
    template_key: flag-i
    type: string
    required: false
    description: "either interface name or address"
    aliases:
      - -I
  - name: flag-i
    type: number
    required: false
    description: "seconds between sending each packet"
    aliases:
      - -i
  - name: flag-l
    type: integer
    required: false
    description: "send <preload> number of packages while waiting replies"
    aliases:
      - -l
  - name: flag-m
    type: string
    required: false
    description: "tag the packets going out"
    aliases:
      - -m
  - name: flag-M
    template_key: flag-m
    type: string
    required: false
    description: "define path MTU discovery, can be one of <do|dont|want|probe>"
    aliases:
      - -M
  - name: flag-n
    type: string
    required: false
    description: "no reverse DNS name resolution, override -H"
    aliases:
      - -n
  - name: flag-p
    type: string
    required: false
    description: "contents of padding byte"
    aliases:
      - -p
  - name: flag-q
    type: string
    required: false
    description: "quiet output"
    aliases:
      - -q
  - name: flag-Q
    template_key: flag-q
    type: string
    required: false
    description: "use quality of service <tclass> bits"
    aliases:
      - -Q
  - name: flag-s
    type: integer
    required: false
    description: "use <size> as number of data bytes to be sent"
    aliases:
      - -s
  - name: flag-S
    template_key: flag-s
    type: string
    required: false
    description: "use <size> as SO_SNDBUF socket option value"
    aliases:
      - -S
  - name: flag-t
    type: string
    required: false
    description: "define time to live"
    aliases:
      - -t
  - name: flag-v
    type: string
    required: false
    description: "verbose output"
    aliases:
      - -v
  - name: flag-w
    type: number
    required: false
    description: "reply wait <deadline> in seconds"
    aliases:
      - -w
  - name: flag-W
    template_key: flag-w
    type: string
    required: false
    description: "time to wait for response"
    aliases:
      - -W
  - name: flag-4
    type: string
    required: false
    description: "use IPv4"
    aliases:
      - "-4"
  - name: flag-b
    type: string
    required: false
    description: "allow pinging broadcast"
    aliases:
      - -b
  - name: flag-T
    template_key: flag-t
    type: string
    required: false
    description: "define timestamp, can be one of <tsonly|tsandaddr|tsprespec>"
    aliases:
      - -T
  - name: flag-6
    type: string
    required: false
    description: "use IPv6"
    aliases:
      - "-6"
  - name: flag-F
    template_key: flag-f
    type: string
    required: false
    description: "define flow label, default is random"
    aliases:
      - -F
  - name: flag-N
    template_key: flag-n
    type: string
    required: false
    description: "Set the flag-N parameter"
    aliases:
      - -N
execution:
  template: "ping {flag-3} {flag-a} {flag-c} {flag-d} {flag-e}"
  sandbox: execFile
  timeout_seconds: 60
  shell: false
global_vars:
  target: ip
examples:
  - description: "Standard connectivity test with 4 pings"
    command: "ping -c 4 google.com"
  - description: "Continuous ping with timestamp"
    command: "ping -D google.com"
  - description: "Flood ping for network stress testing"
    command: "sudo ping -f -c 1000 localhost"
  - description: "Custom packet size test"
    command: "ping -s 1472 -c 10 google.com"
  - description: Basic usage of ping to check connectivity to a host
    command: ping hostname_or_IP_address
  - description: Specify the number of echo requests to send
    command: ping -c 4 hostname_or_IP_address
  - description: Set the interval between sending each packet in seconds
    command: ping -i 2 hostname_or_IP_address
  - description: Flood ping, sending requests as fast as possible (requires root)
    command: ping -f hostname_or_IP_address
  - description: Ping with a specified packet size in bytes
    command: ping -s 100 hostname_or_IP_address
  - description: Set time to live to control the number of hops
    command: ping -t 64 hostname_or_IP_address
  - description: Use IPv4 explicitly (equivalent to ping)
    command: ping -4 hostname_or_IP_address
  - description: Use IPv6 explicitly
    command: ping -6 ipv6_address
  - description: Display the version of the ping command
    command: ping -V
references:
  - label: "ping man page"
    url: "https://linux.die.net/man/8/ping"
  - label: "ICMP protocol specification"
    url: "https://datatracker.ietf.org/doc/html/rfc792"
---

# ping — Network Reachability Testing

Ping is one of the most fundamental network diagnostic tools. It sends ICMP Echo Request packets and measures the time taken for Echo Reply responses, providing immediate feedback on network connectivity, latency, and packet loss.

## Interpreting Results

```
PING google.com (142.250.80.14): 56 data bytes
64 bytes from 142.250.80.14: icmp_seq=0 ttl=118 time=12.345 ms
64 bytes from 142.250.80.14: icmp_seq=1 ttl=118 time=11.892 ms
--- google.com ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max/stddev = 11.892/12.119/12.345/0.227 ms
```

### Key Metrics

| Metric | Interpretation |
|--------|---------------|
| **time** | Round-trip latency in milliseconds |
| **packet loss** | Percentage of packets not returned (should be 0%) |
| **ttl** | Time To Live — decremented by each router hop |
| **stddev** | Jitter — variance in round-trip time |

## Common Diagnoses

| Symptom | Possible Cause |
|---------|---------------|
| 100% packet loss | Host down, firewall blocking ICMP, network disconnected |
| High latency (>200ms) | Geographic distance, satellite link, congestion |
| Increasing latency | Network congestion, throttling, route flapping |
| Variable latency (jitter) | Wireless interference, bufferbloat, QoS issues |
| TTL expired in transit | Routing loop or hop count exceeded |

## Security Note

- Many hosts disable ICMP echo responses for security/privacy
- Packet loss may indicate firewalls rather than actual connectivity issues
- Flood ping can be considered a denial-of-service attack — use responsibly

## Related Tools

- **[mtr](../../diagnostic/mtr.md)** — Combines ping and traceroute for continuous path analysis
- **[traceroute](../../diagnostic/traceroute.md)** — Path discovery to target host
- **[hping3](../../diagnostic/hping3.md)** — Advanced packet crafting and testing
