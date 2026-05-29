---
id: security-ad-ldapsearch
namespace: security:ad:ldapsearch
name: ldapsearch
description: LDAP directory search tool for querying Active Directory to enumerate
  users, groups, computers, organizational units, and domain policies.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.ad.enum.users
  - security.ad.enum.groups
  - security.ad.enum.computers
  - security.ad.enum.ous
  - security.ad.enum.gpos
  - security.ad.ldap.query
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
  - windapsearch
  - ad-ldap-enum
phase: exploitation
techniques:
  - credential-access
  - discovery
  - lateral-movement
items:
  - NoCreds
  - Hash
services:
  - LDAP
attack_types:
  - Enumeration
  - CredentialAccess
  - LateralMovement
contract:
  inputs:
    - type: network.target.uri
      description: LDAP server URI (ldap:// or ldaps://)
    - type: credential.binddn
      description: Distinguished name for LDAP bind
    - type: credential.password
      description: Password for LDAP bind
    - type: ldap.basedn
      description: Base DN for search scope
  outputs:
    - type: security.ad.enum.results
      description: LDAP query results in LDIF format
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
  - ldapsearch
parameters:
  - name: simple
    type: boolean
    required: false
    default_value: false
    description: "Use simple authentication (not SASL)"
    aliases:
      - -x
      - --simple
  - name: uri
    type: string
    required: false
    description: "LDAP server URI (ldap://host:port)"
    aliases:
      - -H
      - --uri
  - name: bind-dn
    type: string
    required: false
    description: "Distinguished name to bind as"
    aliases:
      - -D
      - --bind-dn
  - name: password
    type: string
    required: false
    description: "Password for LDAP bind"
    aliases:
      - -w
      - --password
  - name: base-dn
    type: string
    required: false
    description: "Base DN for search"
    aliases:
      - -b
      - --base-dn
  - name: scope
    type: string
    required: false
    default_value: sub
    description: "Search scope (base, one, sub, children)"
    aliases:
      - -s
      - --scope
  - name: filter
    type: string
    required: false
    default_value: "(objectClass=*)"
    description: "LDAP search filter"
    aliases:
      - -f
      - --filter
  - name: format
    type: boolean
    required: false
    default_value: false
    description: "LDIF format with comments only"
    aliases:
      - -LLL
  - name: time-limit
    type: integer
    required: false
    default_value: 0
    description: "Time limit in seconds for search"
    aliases:
      - -l
      - --time-limit
  - name: size-limit
    type: integer
    required: false
    default_value: 0
    description: "Maximum number of entries to return"
    aliases:
      - -z
      - --size-limit
  - name: host
    type: string
    required: false
    description: "LDAP server hostname"
    aliases:
      - -h
      - --host
  - name: port
    type: integer
    required: false
    default_value: 389
    description: "LDAP server port"
    aliases:
      - -p
      - --port
  - name: starttls
    type: boolean
    required: false
    default_value: false
    description: "Use STARTTLS to upgrade to TLS"
    aliases:
      - -Z
      - --starttls
execution:
  template: "ldapsearch -x -H {uri} -b {base-dn}"
  sandbox: execFile
  timeout_seconds: 60
  shell: false
global_vars:
  uri: string
  base-dn: string
examples:
  - description: "Anonymous LDAP query to retrieve base DSE"
    command: ldapsearch -x -H ldap://10.10.10.1 -b "" -s base
  - description: "Enumerate all users in the domain"
    command: ldapsearch -x -H ldap://10.10.10.1 -D jdoe@evilcorp.local -w Pass123 -b dc=evilcorp,dc=local "(objectClass=user)"
  - description: "Enumerate all domain groups"
    command: ldapsearch -x -H ldap://10.10.10.1 -D jdoe@evilcorp.local -w Pass123 -b dc=evilcorp,dc=local "(objectClass=group)"
  - description: "Find domain admins group members"
    command: ldapsearch -x -H ldap://10.10.10.1 -D jdoe@evilcorp.local -w Pass123 -b dc=evilcorp,dc=local "(&(objectClass=group)(cn=Domain Admins))" member
  - description: "Enumerate all computers in the domain"
    command: ldapsearch -x -H ldap://10.10.10.1 -D jdoe@evilcorp.local -w Pass123 -b dc=evilcorp,dc=local "(objectClass=computer)"
  - description: "Search for users with SPNs (kerberoast target)"
    command: ldapsearch -x -H ldap://10.10.10.1 -D jdoe@evilcorp.local -w Pass123 -b dc=evilcorp,dc=local "(&(objectClass=user)(servicePrincipalName=*))" servicePrincipalName
  - description: "Find users with Kerberos pre-auth disabled (AS-REP roast)"
    command: ldapsearch -x -H ldap://10.10.10.1 -D jdoe@evilcorp.local -w Pass123 -b dc=evilcorp,dc=local "(&(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=4194304))" samaccountname
references:
  - label: "OpenLDAP ldapsearch man page"
    url: "https://www.openldap.org/software/man.cgi?query=ldapsearch"
install:
    - method: apt
      package_name: "ldap-utils"
      commands:
        - "apt-get install -y ldap-utils"
---

# ldapsearch — LDAP Directory Query Tool

ldapsearch is the standard command-line LDAP search tool from OpenLDAP, used to query Active Directory and other LDAP-compliant directory services.

## Common AD LDAP Filters

| Query | LDAP Filter |
|-------|-------------|
| All users | `(objectClass=user)` |
| All groups | `(objectClass=group)` |
| All computers | `(objectClass=computer)` |
| Domain Admins | `(&(objectClass=group)(cn=Domain Admins))` |
| Users with SPNs | `(&(objectClass=user)(servicePrincipalName=*))` |
| Users without pre-auth | `(&(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=4194304))` |
| Locked out users | `(&(objectClass=user)(lockoutTime>=1))` |
| Disabled users | `(&(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=2))` |

## Anonymous Access

If the domain controller allows anonymous LDAP queries, you can enumerate significant AD information without any credentials using `ldapsearch -x -H ldap://DC_IP -b dc=domain,dc=local -s sub "(objectClass=*)"`.
