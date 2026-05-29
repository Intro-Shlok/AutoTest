---
id: system-sync-rsync
namespace: system:sync:rsync
name: rsync
description: Fast, versatile file synchronization and transfer tool with delta encoding,
  compression, and remote sync over SSH.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - filesystem.sync.local
  - filesystem.sync.remote
  - filesystem.sync.incremental
  - filesystem.sync.archive
  - filesystem.transfer.delta
  - filesystem.backup
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
dependencies:
  - ssh
related_tools:
  - unison
  - tar
  - rclone
  - scp
  - network-remote-ssh
  - network-transfer-scp
  - network-transfer-sftp
artifacts:
  - type: filesystem.directory.synced
    description: Destination directory after rsync operation
    trust_level: verified
  - type: system.backup.archive
    description: Backup archive created via rsync
    trust_level: verified
workflow_edges:
  produces:
    - synced-directory
    - backup-archive
  consumes:
    - source-directory
    - destination-path
contract:
  inputs:
    - type: filesystem.directory.source
      description: Source directory or file path
    - type: filesystem.directory.destination
      description: Destination directory path
  outputs:
    - type: filesystem.directory.synced
      description: Synchronized destination directory
  side_effects:
    - filesystem_write
  resource_cost:
    cpu: low
    memory_mb: 32
    network: medium
    disk_io: high
resource_profile:
  cpu: low
  memory_mb: 32
  network: medium
  disk_io: high
allowed-tools:
  - rsync
  - Bash
  - execFile
parameters:
  - name: verbose
    type: string
    required: false
    description: "increase verbosity"
    aliases:
      - -v
      - --verbose
  - name: info
    type: string
    required: false
    description: "fine-grained informational verbosity"
    aliases:
      - --info
  - name: debug
    type: string
    required: false
    description: "fine-grained debug verbosity"
    aliases:
      - --debug
  - name: stderr
    type: string
    required: false
    default_value: "errors"
    description: "change stderr output mode"
    aliases:
      - --stderr
  - name: quiet
    type: string
    required: false
    description: "suppress non-error messages"
    aliases:
      - -q
      - --quiet
  - name: no-motd
    type: string
    required: false
    description: "suppress daemon-mode MOTD"
    aliases:
      - --no-motd
  - name: checksum
    type: string
    required: false
    description: "skip based on checksum, not mod-time & size"
    aliases:
      - -c
      - --checksum
  - name: archive
    type: string
    required: false
    description: "archive mode is -rlptgoD (no -A,-X,-U,-N,-H)"
    aliases:
      - -a
      - --archive
    enum:
      - no -A
      - -X
      - -U
      - -N
      - -H
  - name: no-OPTION
    template_key: no-option
    type: string
    required: false
    description: "turn off an implied OPTION (e.g. --no-D)"
    aliases:
      - --no-OPTION
  - name: recursive
    type: string
    required: false
    description: "recurse into directories"
    aliases:
      - -r
      - --recursive
  - name: relative
    type: string
    required: false
    description: "use relative path names"
    aliases:
      - -R
      - --relative
  - name: no-implied-dirs
    type: string
    required: false
    description: "don't send implied dirs with --relative"
    aliases:
      - --no-implied-dirs
  - name: backup
    type: string
    required: false
    description: "make backups (see --suffix & --backup-dir)"
    aliases:
      - -b
      - --backup
  - name: backup-dir
    type: file
    required: false
    description: "make backups into hierarchy based in DIR"
    aliases:
      - --backup-dir
  - name: suffix
    type: string
    required: false
    description: "backup suffix (default ~ w/o --backup-dir)"
    aliases:
      - --suffix
  - name: update
    type: string
    required: false
    description: "skip files that are newer on the receiver"
    aliases:
      - -u
      - --update
  - name: inplace
    type: string
    required: false
    description: "update destination files in-place"
    aliases:
      - --inplace
  - name: append
    type: string
    required: false
    description: "append data onto shorter files"
    aliases:
      - --append
  - name: append-verify
    type: string
    required: false
    description: "--append w/old data in file checksum"
    aliases:
      - --append-verify
  - name: dirs
    type: string
    required: false
    description: "transfer directories without recursing"
    aliases:
      - -d
      - --dirs
  - name: old-dirs
    type: string
    required: false
    description: "works like --dirs when talking to old rsync"
    aliases:
      - --old-dirs
      - --old-d
  - name: mkpath
    type: string
    required: false
    description: "create destination's missing path components"
    aliases:
      - --mkpath
  - name: links
    type: string
    required: false
    description: "copy symlinks as symlinks"
    aliases:
      - -l
      - --links
  - name: copy-links
    type: string
    required: false
    description: "transform symlink into referent file/dir"
    aliases:
      - -L
      - --copy-links
  - name: copy-unsafe-links
    type: string
    required: false
    description: "only \"unsafe\" symlinks are transformed"
    aliases:
      - --copy-unsafe-links
  - name: safe-links
    type: string
    required: false
    description: "ignore symlinks that point outside the tree"
    aliases:
      - --safe-links
  - name: munge-links
    type: string
    required: false
    description: "munge symlinks to make them safe & unusable"
    aliases:
      - --munge-links
  - name: copy-dirlinks
    type: string
    required: false
    description: "transform symlink to dir into referent dir"
    aliases:
      - -k
      - --copy-dirlinks
  - name: keep-dirlinks
    type: string
    required: false
    description: "treat symlinked dir on receiver as dir"
    aliases:
      - -K
      - --keep-dirlinks
  - name: hard-links
    type: string
    required: false
    description: "preserve hard links"
    aliases:
      - -H
      - --hard-links
execution:
  template: "rsync {verbose} {info} {debug} {stderr} {quiet}"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
global_vars:
  target: ip
  user: user
  port: port
examples:
  - description: "Local directory sync"
    command: "rsync -av /source/dir/ /backup/dir/"
  - description: "Remote sync over SSH"
    command: "rsync -avz /local/dir/ user@remote:/backup/dir/"
  - description: "Pull remote directory to local"
    command: "rsync -avz user@remote:/source/dir/ /local/dir/"
  - description: "Incremental backup with hardlinks"
    command: "rsync -av --link-dest=../previous /source/ /backup/current/"
  - description: "Dry run to preview changes"
    command: "rsync -avn /source/ /destination/"
  - description: "Sync with exclusions"
    command: "rsync -av --exclude='node_modules' --exclude='.git' /project/ /backup/"
references:
  - label: "Rsync documentation"
    url: "https://rsync.samba.org/documentation.html"
  - label: "Rsync tips and tricks"
    url: "https://linux.die.net/man/1/rsync"
install:
    - method: apt
      package_name: "rsync"
      commands:
        - "apt-get install -y rsync"
---

# Rsync — File Synchronization

Rsync is a fast, versatile file synchronization tool that transfers only the differences between source and destination (delta encoding), making repeated transfers extremely efficient.

## How It Works

1. **Scan** — Rsync examines source and destination files
2. **Delta** — Only the changed parts of files are transferred
3. **Apply** — Changes are written to the destination

## Key Features

| Feature | Description |
|---------|-------------|
| **Delta transfer** | Only transfers differences, not entire files |
| **Compression** | Optional `-z` flag for network-efficient transfer |
| **Preservation** | Maintains permissions, ownership, timestamps |
| **Remote sync** | Built-in SSH support for secure remote sync |
| **Incremental** | Hard-link based snapshots for backup rotation |

## Backup Strategies

### Simple Backup
```bash
rsync -av /home/user/ /backup/daily/
```

### Rotating Snapshots
```bash
# Create hardlink-based incremental backup
rsync -av --link-dest=../monday /source/ /backup/tuesday/

# Next day
rsync -av --link-dest=../tuesday /source/ /backup/wednesday/
```

### Remote Backup
```bash
# Push to remote
rsync -avz --delete /data/ user@backup-server:/backup/

# Pull from remote
rsync -avz user@server:/data/ /local/backup/
```

## Important Trailing Slash

```bash
# Copies the directory itself
rsync -av /source /destination  # → /destination/source/

# Copies the contents
rsync -av /source/ /destination  # → /destination/file1, ...
```

## Related Tools

- **[scp](../../remote/scp.md)** — Simple secure copy (simpler, no delta)
- **[rclone](../../sync/rclone.md)** — Cloud storage sync
- **[tar](../../archive/tar.md)** — Archive creation for offline transfer
