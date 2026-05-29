---
id: security-crypto-openssl
namespace: security:crypto:openssl
name: openssl
description: Comprehensive cryptographic toolkit for SSL/TLS, certificate management,
  encryption, hashing, and key generation.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.crypto.hash
  - security.crypto.encrypt
  - security.crypto.decrypt
  - security.crypto.sign
  - security.crypto.verify
  - security.crypto.keygen
  - security.crypto.certificate
  - security.crypto.csr
  - security.tls.connect
  - security.tls.inspect
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
  - gnutls
  - certbot
  - cfssl
  - easyrsa
artifacts:
  - type: security.certificate.pem
    description: X.509 certificate (PEM or DER)
    mime: application/x-pem-file
    schema_version: "1.0.0"
    trust_level: verified
  - type: security.key.private
    description: Private key
    mime: application/x-pem-file
    trust_level: verified
  - type: security.key.public
    description: Public key
    mime: application/x-pem-file
    trust_level: verified
  - type: security.certificate.csr
    description: Certificate Signing Request
    mime: application/x-pem-file
    trust_level: verified
workflow_edges:
  produces:
    - certificate
    - private-key
    - csr
    - hash-output
  consumes:
    - input-data
    - private-key
contract:
  inputs:
    - type: data.raw
      description: Input data for hashing, encryption, or signing
    - type: security.key.private
      description: Private key for signing or decryption
  outputs:
    - type: data.hashed
      description: Hash or digest output
    - type: data.encrypted
      description: Encrypted data
    - type: security.certificate.pem
      description: Generated X.509 certificate
  side_effects:
    - filesystem_write
  resource_cost:
    cpu: medium
    memory_mb: 32
    network: none
    disk_io: low
resource_profile:
  cpu: medium
  memory_mb: 32
  network: none
  disk_io: low
allowed-tools:
  - openssl
  - Bash
  - execFile

features:
  - encryption
  - batch
techniques:
  - credential-access
  - encryption
  - privilege-escalation
execution:
  template: "openssl {action} {algorithm} {input} {output}"
  sandbox: execFile
  timeout_seconds: 60
  shell: false
global_vars:
  target: ip
  port: port
examples:
  - description: "Generate an RSA private key"
    command: "openssl genrsa -out private.pem 2048"
  - description: "Generate a self-signed certificate"
    command: "openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days
      365 -nodes"
  - description: "Compute SHA-256 hash of a file"
    command: "openssl dgst -sha256 file.txt"
  - description: "Encrypt a file with AES-256"
    command: "openssl enc -aes-256-cbc -salt -in plain.txt -out encrypted.enc"
  - description: "Connect to an HTTPS server and inspect certificate"
    command: "openssl s_client -connect example.com:443 -showcerts"
  - description: "View certificate details"
    command: "openssl x509 -in cert.pem -text -noout"
references:
  - label: "OpenSSL documentation"
    url: "https://www.openssl.org/docs/"
  - label: "OpenSSL Cookbook"
    url: "https://www.feistyduck.com/openssl-cookbook/"
install:
    - method: apt
      package_name: "openssl"
      commands:
        - "apt-get install -y openssl"
---

# OpenSSL — Cryptographic Toolkit

OpenSSL is the industry-standard cryptographic library that provides tools for SSL/TLS, certificate management, encryption, and hashing. It's essential for secure communications and data protection.

## Certificate Management

### Generate Certificate Authority
```bash
# Generate CA private key
openssl genrsa -out ca-key.pem 4096

# Generate CA certificate
openssl req -x509 -new -key ca-key.pem -out ca-cert.pem -days 3650
```

### Generate Server Certificate
```bash
# Generate server private key
openssl genrsa -out server-key.pem 2048

# Generate CSR
openssl req -new -key server-key.pem -out server.csr

# Sign with CA
openssl x509 -req -in server.csr -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial -out server-cert.pem -days 365
```

## Encryption & Decryption

```bash
# Encrypt a file with password
openssl enc -aes-256-cbc -salt -in secret.txt -out secret.enc -pbkdf2

# Decrypt
openssl enc -d -aes-256-cbc -in secret.enc -out secret.txt -pbkdf2

# Encrypt with key file
openssl rsautl -encrypt -pubin -inkey public.pem -in plain.txt -out encrypted.bin
```

## TLS Connection Testing

```bash
# Test HTTPS connection
openssl s_client -connect example.com:443 -servername example.com

# Show certificate chain
openssl s_client -connect example.com:443 -showcerts </dev/null

# Test TLS version support
openssl s_client -tls1_2 -connect example.com:443
```

## Hashing

```bash
# Compute hash of a file
openssl dgst -sha256 file.txt
openssl sha256 file.txt

# HMAC
echo -n "data" | openssl dgst -sha256 -hmac "key"
```

## Related Tools

- **[certbot](../../crypto/certbot.md)** — Let's Encrypt certificate automation
- **[cfssl](../../crypto/cfssl.md)** — CloudFlare's PKI toolkit
- **[easyrsa](../../crypto/easyrsa.md)** — Simple CA management
