---
id: container-runtime-docker
namespace: container:runtime:docker
name: docker
description: Container platform for developing, shipping, and running applications
  in isolated environments.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - container.runtime.execute
  - container.image.build
  - container.image.publish
  - container.orchestration.compose
  - container.storage.volume
  - container.network.manage
platforms:
  - linux
  - macos
  - windows
risk_level: medium
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies: []
related_tools:
  - podman
  - containerd
  - nerdctl
artifacts:
  - type: container.image.oci
    description: Built or pulled OCI container image
    mime: application/vnd.oci.image.manifest.v1+json
    schema_version: "1.0.0"
    trust_level: verified
  - type: container.runtime.logs
    description: Log output from container execution
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - container-image
    - container-logs
  consumes:
    - dockerfile
    - base-image
contract:
  inputs:
    - type: container.image.dockerfile
      description: Dockerfile for image build
    - type: container.image.oci
      description: Base container image
  outputs:
    - type: container.image.oci
      description: Built or pulled container image
      mime: application/vnd.oci.image.manifest.v1+json
    - type: container.runtime.logs
      description: Container execution logs
      mime: text/plain
  side_effects:
    - network_traffic
    - filesystem_write
    - process_spawn
  resource_cost:
    cpu: high
    memory_mb: 1024
    network: high
    disk_io: high
resource_profile:
  cpu: high
  memory_mb: 1024
  network: high
  disk_io: high
allowed-tools:
  - docker
  - Bash
  - execFile
parameters:
  - name: config
    type: string
    required: false
    description: "Location of client config files (default"
    aliases:
      - --config
  - name: context
    type: string
    required: false
    description: "Name of the context to use to connect to the"
    aliases:
      - -c
      - --context
  - name: debug
    type: string
    required: false
    description: "Enable debug mode"
    aliases:
      - -D
      - --debug
  - name: host
    type: string
    required: false
    description: "Daemon socket to connect to"
    aliases:
      - -H
      - --host
  - name: log-level
    type: string
    required: false
    description: "Set the logging level (\"debug\", \"info\""
    aliases:
      - -l
      - --log-level
  - name: tls
    type: string
    required: false
    description: "Use TLS; implied by --tlsverify"
    aliases:
      - --tls
  - name: tlscacert
    type: string
    required: false
    description: "Trust certs signed only by this CA (default"
    aliases:
      - --tlscacert
  - name: tlscert
    type: file
    required: false
    description: "Path to TLS certificate file (default"
    aliases:
      - --tlscert
  - name: tlskey
    type: file
    required: false
    description: "Path to TLS key file (default"
    aliases:
      - --tlskey
  - name: tlsverify
    type: string
    required: false
    description: "Use TLS and verify the remote"
    aliases:
      - --tlsverify
  - name: version
    type: string
    required: false
    description: "Print version information and quit"
    aliases:
      - -v
      - --version
execution:
  template: "docker {config} {context} {debug} {host} {log-level}"
  sandbox: docker
  timeout_seconds: 300
  shell: false
global_vars:
  host: ip
examples:
  - description: "Run an interactive container"
    command: "docker run -it --rm ubuntu:latest bash"
  - description: "Build an image from Dockerfile"
    command: "docker build -t myapp:latest ."
  - description: "Run a web server with port mapping"
    command: "docker run -d -p 80:80 --name web nginx:alpine"
  - description: "Execute command in running container"
    command: "docker exec -it mycontainer ps aux"
  - description: 'Darkiros UTILS: Remove docker image'
    command: docker image rm [image_id]
  - description: 'Darkiros UTILS: Delete an image from the local image store'
    command: docker rmi [image_id]
  - description: 'Darkiros UTILS: List all images that are locally stored with the
      Docker Engine'
    command: docker images
  - description: 'Darkiros UTILS: List all containers that are locally stored with
      the Docker Engine'
    command: docker ps -a
  - description: 'Darkiros UTILS: List all containers that are currently running'
    command: docker ps -q
  - description: 'Darkiros UTILS: Stop a running container'
    command: docker stop [container_id]
  - description: 'Darkiros UTILS: Stop all running containers'
    command: docker stop $(docker ps -a -q)
  - description: 'Darkiros UTILS: Build an image from the Dockerfile in the current
      directory and tag the image'
    command: docker build -t [image_name] .
  - description: 'Darkiros UTILS: Pull an image from a registry'
    command: docker pull [image_name]:[tag]
  - description: 'Darkiros UTILS: Create a new bash process inside the container and
      connect it to the terminal'
    command: docker exec -it [container_id] bash
  - description: 'Darkiros UTILS: Print the last lines of a container’s logs'
    command: docker logs --tail 100 [container_id] | less
  - description: 'Darkiros UTILS: Print the last lines of a container’s logs and follow'
    command: docker logs -f --tail 100 [container_id]
  - description: 'Darkiros UTILS: Create new network'
    command: docker network create [network_name]
  - description: 'Darkiros UTILS: List all networks'
    command: docker network ls
  - description: 'Darkiros UTILS: Builds, (re)creates, starts, and attaches to containers
      for all services'
    command: docker-compose up
  - description: 'Darkiros UTILS: Builds, (re)creates, starts, and dettaches to containers
      for all services'
    command: docker-compose up -d
  - description: 'Darkiros UTILS: Stops containers and removes containers, networks,
      volumes, and images created by up'
    command: docker-compose down
references:
  - label: "Docker documentation"
    url: "https://docs.docker.com/"
  - label: "Dockerfile reference"
    url: "https://docs.docker.com/engine/reference/builder/"
  - label: "Docker CLI reference"
    url: "https://docs.docker.com/engine/reference/commandline/cli/"
techniques:
  - command-and-control
  - lateral-movement
---

# Docker — Container Platform

Docker is the industry-standard container platform that enables developers to package applications and their dependencies into lightweight, portable containers that run consistently across any environment.

## Core Architecture

Docker uses a client-server architecture:

- **Docker Daemon** (`dockerd`): Background service managing containers, images, networks, and volumes
- **Docker CLI** (`docker`): Command-line interface that communicates with the daemon via REST API
- **Docker Registry**: Storage and distribution system for container images (default: Docker Hub)

## Container Lifecycle

```mermaid
flowchart LR
    A[Dockerfile] -->|docker build| B[Image]
    B -->|docker push| C[Registry]
    C -->|docker pull| B
    B -->|docker run| D[Container]
    D -->|docker stop| E[Stopped]
    E -->|docker start| D
    E -->|docker rm| F[Removed]
```

## Docker Compose

For multi-container applications, `docker compose` defines services, networks, and volumes in a YAML file:

```yaml
# docker-compose.yml
version: "3.9"
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
  database:
    image: postgres:15
    environment:
      POSTGRES_DB: myapp
      POSTGRES_PASSWORD: secret
    volumes:
      - db-data:/var/lib/postgresql/data
volumes:
  db-data:
```

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Tear down
docker compose down -v
```

## Security Best Practices

- Never run containers with `--privileged` in production
- Use read-only root filesystems (`--read-only`)
- Drop unnecessary Linux capabilities (`--cap-drop ALL`)
- Scan images for vulnerabilities (`docker scan` or Trivy)
- Use distroless or scratch base images to reduce attack surface

## Related Tools

- **[podman](../../container/image/podman.md)** — Daemonless container engine (drop-in Docker replacement)
- **[kubernetes](../../container/orchestration/kubernetes.md)** — Container orchestration platform
- **[docker-compose](../../container/orchestration/docker-compose.md)** — Multi-container application definition
