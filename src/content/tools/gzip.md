---
id: system-compress-gzip
namespace: system:compress:gzip
name: gzip
description: File compression utility using the DEFLATE algorithm for reducing file
  sizes with optional decompression and stream processing.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - filesystem.compress.gzip
  - filesystem.decompress.gzip
  - filesystem.compress.stream
  - filesystem.archive.compress
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
  - gunzip
  - zcat
  - bzip2
  - xz
  - zstd
artifacts:
  - type: filesystem.archive.gzip
    description: Gzip-compressed file
    mime: application/gzip
    schema_version: "1.0.0"
    trust_level: verified
  - type: filesystem.file.raw
    description: Decompressed file content
    trust_level: verified
workflow_edges:
  produces:
    - compressed-file
    - decompressed-output
  consumes:
    - input-file
    - compressed-file
contract:
  inputs:
    - type: filesystem.file.raw
      description: File to compress
    - type: filesystem.archive.gzip
      description: Gzip archive to decompress
  outputs:
    - type: filesystem.archive.gzip
      description: Compressed gzip archive
      mime: application/gzip
    - type: filesystem.file.raw
      description: Decompressed file content
  side_effects:
    - filesystem_write
  resource_cost:
    cpu: high
    memory_mb: 32
    network: none
    disk_io: high
resource_profile:
  cpu: high
  memory_mb: 32
  network: none
  disk_io: high
allowed-tools:
  - gzip
  - gunzip
  - zcat
  - Bash
  - execFile
parameters:
  - name: stdout
    type: string
    required: false
    description: "write on standard output, keep original files unchanged"
    aliases:
      - -c
      - --stdout
  - name: decompress
    type: string
    required: false
    description: "Set the decompress parameter"
    aliases:
      - -d
      - --decompress
  - name: force
    type: file
    required: false
    description: "force overwrite of output file and compress links"
    aliases:
      - -f
      - --force
  - name: help
    type: string
    required: false
    description: "give this help"
    aliases:
      - -h
      - --help
  - name: keep
    type: file
    required: false
    description: "keep (don't delete) input files"
    aliases:
      - -k
      - --keep
  - name: list
    type: string
    required: false
    description: "list compressed file contents"
    aliases:
      - -l
      - --list
  - name: license
    type: string
    required: false
    description: "display software license"
    aliases:
      - -L
      - --license
  - name: no-name
    type: string
    required: false
    description: "do not save or restore the original name and timestamp"
    aliases:
      - -n
      - --no-name
  - name: name
    type: string
    required: false
    description: "save or restore the original name and timestamp"
    aliases:
      - -N
      - --name
  - name: quiet
    type: string
    required: false
    description: "suppress all warnings"
    aliases:
      - -q
      - --quiet
  - name: recursive
    type: string
    required: false
    description: "operate recursively on directories"
    aliases:
      - -r
      - --recursive
  - name: rsyncable
    type: string
    required: false
    description: "make rsync-friendly archive"
    aliases:
      - --rsyncable
  - name: suffix
    type: string
    required: false
    description: "--synchronous synchronous output (safer if system crashes, but slower)"
    aliases:
      - -S
      - --suffix
    enum:
      - safer if system crashes
      - but slower
  - name: test
    type: string
    required: false
    description: "test compressed file integrity"
    aliases:
      - -t
      - --test
  - name: verbose
    type: string
    required: false
    description: "verbose mode"
    aliases:
      - -v
      - --verbose
  - name: version
    type: string
    required: false
    description: "display version number"
    aliases:
      - -V
      - --version
  - name: fast
    type: string
    required: false
    description: "compress faster"
    aliases:
      - "-1"
      - --fast
  - name: best
    type: string
    required: false
    description: "compress better"
    aliases:
      - "-9"
      - --best
execution:
  template: "gzip {stdout} {decompress} {force} {help} {keep}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
examples:
  - description: "Compress a file"
    command: "gzip file.txt"
  - description: "Decompress a .gz file"
    command: "gunzip file.txt.gz"
  - description: "Compress with maximum compression"
    command: "gzip -9 largefile.tar"
  - description: "Keep original file when compressing"
    command: "gzip -k file.txt"
  - description: "Stream compression in a pipeline"
    command: "cat largefile | gzip -c > output.gz"
  - description: "View compressed file contents"
    command: "zcat file.txt.gz"
references:
  - label: "Gzip documentation"
    url: "https://www.gnu.org/software/gzip/manual/"
  - label: "DEFLATE algorithm"
    url: "https://datatracker.ietf.org/doc/html/rfc1951"
techniques:
  - discovery
  - enumeration
---

# Gzip — File Compression

Gzip (GNU zip) is a widely used compression utility based on the DEFLATE algorithm. It provides a good balance of compression ratio and speed, making it the standard for text compression on Unix systems.

## Compression Levels

| Level | Flag | Speed | Size Reduction | Use Case |
|-------|------|-------|---------------|----------|
| 1 | `--fast` | Fastest | Lowest | Quick compression, already-compressed data |
| 6 | (default) | Good | Good | General purpose |
| 9 | `--best` | Slowest | Highest | Archival, distribution |

## Pipeline Usage

```bash
# Compress a tar archive
tar cf - directory/ | gzip -c > archive.tar.gz

# Decompress and extract
gunzip -c archive.tar.gz | tar xf -

# Search compressed files without decompressing to disk
zcat access.log.gz | grep 'ERROR'

# Count lines in compressed file
zcat data.txt.gz | wc -l

# Stream compression over pipe
mysqldump database | gzip -c > backup.sql.gz
```

## Compression Ratios

| File Type | Typical Ratio | Notes |
|-----------|---------------|-------|
| Text/Code | 60-80% | Highly compressible |
| Logs | 70-90% | Very high compression |
| JSON/XML | 70-85% | Repeated patterns compress well |
| Images (PNG) | 0-5% | Already compressed |
| Archives | 0-10% | Usually already compressed |

## Related Tools

- **[bzip2](../../compress/bzip2.md)** — Better compression ratio, slower
- **[xz](../../compress/xz.md)** — Best compression ratio, very slow
- **[zstd](../../compress/zstd.md)** — Modern, fast, good ratio
- **[tar](../../archive/tar.md)** — Often used together with gzip
