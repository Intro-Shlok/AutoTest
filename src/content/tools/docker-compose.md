---
id: container-orchestrate-compose
namespace: container:orchestrate:compose
name: docker-compose
description: Multi-container orchestration tool for defining and running complex Docker
  application stacks.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - container.orchestrate.compose
  - container.orchestrate.stack
  - container.service.manage
  - container.network.multi
  - container.storage.volume
  - container.logs.tail
platforms:
  - linux
  - macos
  - windows
risk_level: low
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies:
  - docker
related_tools:
  - docker
  - docker-swarm
  - kubernetes
  - podman-compose
artifacts:
  - type: container.image.oci
    description: Built container image
    mime: application/vnd.oci.image.manifest.v1+json
    trust_level: verified
  - type: container.runtime.logs
    description: Container service logs
    mime: text/plain
    trust_level: verified
  - type: container.stack.config
    description: Docker Compose stack configuration
    mime: application/x-yaml
    trust_level: verified
workflow_edges:
  produces:
    - compose-stack
    - service-logs
  consumes:
    - compose-file
    - container-image
contract:
  inputs:
    - type: container.stack.composefile
      description: Docker Compose YAML file
      mime: application/x-yaml
    - type: container.image.oci
      description: Container images to use in the stack
  outputs:
    - type: container.stack.running
      description: Running container stack
    - type: container.runtime.logs
      description: Aggregated service logs
      mime: text/plain
  side_effects:
    - network_traffic
    - filesystem_write
    - process_spawn
  resource_cost:
    cpu: medium
    memory_mb: 128
    network: medium
    disk_io: medium
resource_profile:
  cpu: medium
  memory_mb: 128
  network: medium
  disk_io: medium
allowed-tools:
  - docker-compose
  - docker compose
  - Bash
  - execFile
parameters:
  - name: all-resources
    type: string
    required: false
    description: "Include all resources, even those not"
    aliases:
      - --all-resources
  - name: ansi
    type: string
    required: false
    description: "Control when to print ANSI control"
    aliases:
      - --ansi
  - name: compatibility
    type: string
    required: false
    description: "Run compose in backward compatibility mode"
    aliases:
      - --compatibility
  - name: dry-run
    type: string
    required: false
    description: "Execute command in dry run mode"
    aliases:
      - --dry-run
  - name: env-file
    type: string
    required: false
    description: "Specify an alternate environment file"
    aliases:
      - --env-file
  - name: file
    type: string
    required: false
    description: "Compose configuration files"
    aliases:
      - -f
      - --file
  - name: parallel
    type: string
    required: false
    description: "Control max parallelism, -1 for"
    aliases:
      - --parallel
  - name: profile
    type: file
    required: false
    description: "Specify a profile to enable"
    aliases:
      - --profile
  - name: progress
    type: string
    required: false
    description: "Set type of progress output (auto"
    aliases:
      - --progress
  - name: project-directory
    type: file
    required: false
    description: "Specify an alternate working directory"
    aliases:
      - --project-directory
  - name: project-name
    type: string
    required: false
    description: "Project name"
    aliases:
      - -p
      - --project-name
execution:
  template: "docker-compose {all-resources} {ansi} {compatibility} {dry-run} {env-file}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
examples:
  - description: "Start all services in background"
    command: "docker-compose up -d"
  - description: "Build and start services"
    command: "docker-compose up -d --build"
  - description: "View running services"
    command: "docker-compose ps"
  - description: "Tail logs from all services"
    command: "docker-compose logs -f"
  - description: "Execute command in a running service"
    command: "docker-compose exec web bash"
  - description: "Stop and remove all resources"
    command: "docker-compose down -v"
references:
  - label: "Docker Compose documentation"
    url: "https://docs.docker.com/compose/"
  - label: "Compose file reference"
    url: "https://docs.docker.com/compose/compose-file/"
techniques:
  - lateral-movement
---

# Docker Compose — Multi-Container Orchestration

Docker Compose is a tool for defining and running multi-container Docker applications. Using a YAML file, you configure all services, networks, and volumes, then start everything with a single command.

## Compose File Structure

```yaml
version: "3.8"
services:
  web:
    build: .
    ports:
      - "8080:80"
    depends_on:
      - db
  db:
    image: postgres:16
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Common Workflows

### Development
```bash
# Start development stack
docker-compose up -d

# Rebuild specific service
docker-compose build web

# View logs during development
docker-compose logs -f web

# Run one-off commands
docker-compose exec web pytest
```

### Production
```bash
# Pull latest images
docker-compose pull

# Graceful restart
docker-compose restart -t 30

# Scale a service
docker-compose up -d --scale worker=3
```

### Cleanup
```bash
# Stop containers
docker-compose stop

# Stop and remove everything
docker-compose down

# Remove everything including volumes
docker-compose down -v --rmi all
```

## Related Tools

- **[docker](../../runtime/docker.md)** — Container runtime
- **[kubernetes](../../orchestrate/kubernetes.md)** — Production container orchestration
- **[podman-compose](../../orchestrate/podman-compose.md)** — Rootless compose alternative
