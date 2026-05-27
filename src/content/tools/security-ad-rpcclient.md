---
id: security-ad-rpcclient
namespace: security:ad:rpcclient
name: rpcclient
description: Samba RPC client for executing MS-RPC functions against Windows systems
  for user, group, domain, and privilege enumeration.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.ad.enum.users
  - security.ad.enum.groups
  - security.ad.enum.domain
  - security.ad.enum.privileges
  - security.ad.rpc.samr
  - security.ad.rpc.lsarpc
  - security.ad.rpc.srvsvc
platforms:
  - linux
  - cross-platform
risk_level: high
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies: []
related_tools:
  - impacket
  - enum4linux-ng
  - smbclient
phase: exploitation
techniques:
  - credential-access
  - discovery
  - lateral-movement
items:
  - NoCreds
  - Hash
services:
  - SMB
  - Kerberos
attack_types:
  - Enumeration
  - CredentialAccess
  - LateralMovement
contract:
  inputs:
    - type: network.target.ip
      description: Target IP or hostname
    - type: credential.username
      description: Username for RPC authentication
    - type: credential.password
      description: Password for RPC authentication
  outputs:
    - type: security.ad.enum.users
      description: List of domain/local users with RIDs
    - type: security.ad.enum.groups
      description: Group membership information
    - type: security.ad.enum.domain
      description: Domain and trust information
  side_effects:
    - network_traffic
  resource_cost:
    cpu: low
    memory_mb: 16
    network: low
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 16
  network: low
  disk_io: low
allowed-tools:
  - rpcclient
parameters:
  - name: username
    type: string
    required: false
    description: "Username for RPC authentication"
    aliases:
      - -U
      - --user
      - --username
  - name: password
    type: string
    required: false
    description: "Password for RPC authentication"
    aliases:
      - -P
      - --password
  - name: no-pass
    type: boolean
    required: false
    default_value: false
    description: "Null session (no password)"
    aliases:
      - -N
      - --no-pass
  - name: workgroup
    type: string
    required: false
    default_value: WORKGROUP
    description: "Workgroup or domain name"
    aliases:
      - -W
      - --workgroup
  - name: ip
    type: string
    required: false
    description: "Target IP address"
    aliases:
      - -I
      - --ip
  - name: port
    type: integer
    required: false
    default_value: 445
    description: "SMB/RPC port number"
    aliases:
      - -p
      - --port
  - name: debug
    type: integer
    required: false
    default_value: 0
    description: "Debug level (0-10)"
    aliases:
      - -d
      - --debug
  - name: command
    type: string
    required: false
    description: "Execute RPC command non-interactively"
    aliases:
      - -c
      - --command
  - name: auth-file
    type: file
    required: false
    description: "File containing credentials"
    aliases:
      - -A
      - --auth-file
  - name: timeout
    type: integer
    required: false
    default_value: 30
    description: "Connection timeout in seconds"
    aliases:
      - -t
      - --timeout
  - name: kerberos
    type: boolean
    required: false
    default_value: false
    description: "Use Kerberos authentication"
    aliases:
      - -k
      - --kerberos
  - name: encrypt
    type: boolean
    required: false
    default_value: false
    description: "Require SMB encryption"
    aliases:
      - -e
      - --encrypt
execution:
  template: "rpcclient -U {username} {target}"
  sandbox: execFile
  timeout_seconds: 60
  shell: false
global_vars:
  target: ip
  username: user
examples:
  - description: "Null session connection to a domain controller"
    command: rpcclient -U "" -N 10.10.10.1
  - description: "Enumerate domain users via SAMR"
    command: rpcclient -U jdoe 10.10.10.1 -c "enumdomusers"
  - description: "Enumerate domain groups"
    command: rpcclient -U jdoe 10.10.10.1 -c "enumdomgroups"
  - description: "Get user information by RID"
    command: rpcclient -U jdoe 10.10.10.1 -c "queryuser 500"
  - description: "Enumerate SID for a domain user"
    command: rpcclient -U jdoe 10.10.10.1 -c "lookupsids S-1-5-21-..."
  - description: "List shares via SRVSVC"
    command: rpcclient -U jdoe 10.10.10.1 -c "netshareenumall"
  - description: "Get domain password policy"
    command: rpcclient -U jdoe 10.10.10.1 -c "getdompwinfo"
references:
  - label: "Samba rpcclient man page"
    url: "https://www.samba.org/samba/docs/current/man-html/rpcclient.1.html"
---

# rpcclient — MS-RPC Client

rpcclient is a command-line MS-RPC client from the Samba suite that allows direct interaction with Windows RPC services including SAMR (Security Account Manager), LSA (Local Security Authority), and SRVSVC (Server Service).

## Key RPC Commands

| Category | Command | Description |
|----------|---------|-------------|
| Users | `enumdomusers` | List all domain users |
| Users | `queryuser <rid>` | Get detailed user info |
| Users | `queryuser <rid> --sid` | Get user SID |
| Groups | `enumdomgroups` | List all domain groups |
| Groups | `querygroup <rid>` | Get group members |
| Domain | `lsaquery` | Get domain info |
| Domain | `getdompwinfo` | Get password policy |
| Shares | `netshareenumall` | List all shares |
| Shares | `netsharegetinfo <share>` | Get share details |
| SID | `lookupsids <sid>` | Resolve SID to name |
| SID | `lookupnames <name>` | Resolve name to SID |

## Authentication Methods

- **Null session**: `rpcclient -U "" -N <target>`
- **Guest session**: `rpcclient -U guest%"" <target>`
- **Authenticated**: `rpcclient -U user%pass <target>`
- **Kerberos**: `rpcclient -k -U user@DOMAIN <target>`
