---
id: dev-build-make
namespace: dev:build:make
name: make
description: Build automation tool for compiling and managing project dependencies
  using Makefile-based rule definitions.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - dev.build.dependency
  - dev.build.compile
  - dev.build.clean
  - dev.build.automate
  - dev.build.test
  - dev.build.target
  - security.privilege-escalation.shell
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
  - cmake
  - ninja
  - meson
  - just
artifacts:
  - type: dev.build.artifact
    description: Built artifact (binary, library, or output)
    trust_level: verified
  - type: dev.build.log
    description: Build output log
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - build-artifact
    - build-log
  consumes:
    - makefile
    - source-code
contract:
  inputs:
    - type: dev.build.makefile
      description: Makefile with build rules
    - type: dev.source.code
      description: Source code to compile
  outputs:
    - type: dev.build.artifact
      description: Compiled binary or build artifact
  side_effects:
    - filesystem_write
  resource_cost:
    cpu: high
    memory_mb: 128
    network: none
    disk_io: high
resource_profile:
  cpu: high
  memory_mb: 128
  network: none
  disk_io: high
allowed-tools:
  - make
  - gmake
  - Bash
  - execFile

parameters:
  - name: flag-b
    type: string
    required: false
    description: "Ignored for compatibility"
    aliases:
      - -b
      - -m
  - name: always-make
    type: string
    required: false
    description: "Unconditionally make all targets"
    aliases:
      - -B
      - --always-make
  - name: directory
    type: file
    required: false
    description: "Change to DIRECTORY before doing anything"
    aliases:
      - -C
      - --directory
  - name: flag-d
    type: string
    required: false
    description: "Print lots of debugging information"
    aliases:
      - -d
  - name: debug
    type: string
    required: false
    description: "Print various types of debugging information"
    aliases:
      - --debug
  - name: environment-overrides
    type: string
    required: false
    description: "Environment variables override makefiles"
    aliases:
      - -e
      - --environment-overrides
  - name: eval
    type: string
    required: false
    description: "Evaluate STRING as a makefile statement"
    aliases:
      - -E
      - --eval
  - name: file
    type: file
    required: false
    description: "Read FILE as a makefile"
    aliases:
      - -f
      - --file
      - --makefile
  - name: help
    type: string
    required: false
    description: "Print this message and exit"
    aliases:
      - -h
      - --help
  - name: ignore-errors
    type: string
    required: false
    description: "Ignore errors from recipes"
    aliases:
      - -i
      - --ignore-errors
  - name: include-dir
    type: file
    required: false
    description: "Search DIRECTORY for included makefiles"
    aliases:
      - -I
      - --include-dir
  - name: jobs
    type: string
    required: false
    description: "Allow N jobs at once; infinite jobs with no arg"
    aliases:
      - -j
      - --jobs
  - name: jobserver-style
    type: string
    required: false
    description: "Select the style of jobserver to use"
    aliases:
      - --jobserver-style
  - name: keep-going
    type: string
    required: false
    description: "Keep going when some targets can't be made"
    aliases:
      - -k
      - --keep-going
  - name: load-average
    type: string
    required: false
    description: "Don't start multiple jobs unless load is below N"
    aliases:
      - -l
      - --load-average
      - --max-load
  - name: check-symlink-times
    type: string
    required: false
    description: "Use the latest mtime between symlinks and target"
    aliases:
      - -L
      - --check-symlink-times
  - name: just-print
    type: string
    required: false
    description: "Don't actually run any recipe; just print them"
    aliases:
      - -n
      - --just-print
      - --dry-run
      - --recon
  - name: old-file
    type: file
    required: false
    description: "Consider FILE to be very old and don't remake it"
    aliases:
      - -o
      - --old-file
      - --assume-old
  - name: output-sync
    type: string
    required: false
    description: "Synchronize output of parallel jobs by TYPE"
    aliases:
      - -O
      - --output-sync
  - name: print-data-base
    type: string
    required: false
    description: "Print make's internal database"
    aliases:
      - -p
      - --print-data-base
  - name: question
    type: string
    required: false
    description: "Run no recipe; exit status says if up to date"
    aliases:
      - -q
      - --question
  - name: no-builtin-rules
    type: string
    required: false
    description: "Disable the built-in implicit rules"
    aliases:
      - -r
      - --no-builtin-rules
  - name: no-builtin-variables
    type: string
    required: false
    description: "Set the no-builtin-variables parameter"
    aliases:
      - -R
      - -i
      - --no-builtin-variables
  - name: shuffle
    type: string
    required: false
    description: "Perform shuffle of prerequisites and goals"
    aliases:
      - --shuffle
  - name: silent
    type: string
    required: false
    description: "Don't echo recipes"
    aliases:
      - -s
      - --silent
      - --quiet
  - name: no-silent
    type: string
    required: false
    description: "Echo recipes (disable --silent mode)"
    aliases:
      - --no-silent
  - name: no-keep-going
    type: string
    required: false
    description: "Turns off -k"
    aliases:
      - -S
      - --no-keep-going
      - --stop
  - name: touch
    type: string
    required: false
    description: "Touch targets instead of remaking them"
    aliases:
      - -t
      - --touch
  - name: trace
    type: string
    required: false
    description: "Print tracing information"
    aliases:
      - --trace
  - name: version
    type: integer
    required: false
    description: "Print the version number of make and exit"
    aliases:
      - -v
      - --version
  - name: eval-expression
    description: Evaluate arbitrary make expression via $(shell cmd)
    type: string
  - name: include-file
    description: Include an arbitrary file into the Makefile parse
    type: string
features:
  - local
  - batch
  - process-manip
techniques:
  - execution
  - analysis
  - command-and-control
  - credential-access
  - defense-evasion
  - lateral-movement
  - persistence
  - privilege-escalation
  - process-manip
execution:
  template: "make {flag-b} {always-make} {directory} {flag-d} {debug}"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
examples:
  - description: "Build default target"
    command: "make"
  - description: "Build a specific target"
    command: "make clean build"
  - description: "Build with parallel jobs"
    command: "make -j$(nproc)"
  - description: "Build in a subdirectory"
    command: "make -C src/"
  - description: "Dry run to see what would be built"
    command: "make -n"
  - description: "Override compiler variable"
    command: "make CC=clang CFLAGS=-O3"
  - description: Can be used to execute arbitrary commands on a system and spawn shells
      either indirectly
    command: "make -s --eval=$'x:\\n\\t-'\"/bin/sh\"\n"
  - description: 'Argument injection: spawn interactive shell: Can be used to execute
      arbitrary commands on a system and spawn shells either indirectly'
    command: make -s --eval=$'x:\n\t-'"/bin/sh"
references:
  - label: "GNU Make manual"
    url: "https://www.gnu.org/software/make/manual/"
  - label: "Makefile tutorial"
    url: "https://makefiletutorial.com/"
install:
    - method: apt
      package_name: "make"
      commands:
        - "apt-get install -y make"
---

# Make — Build Automation

Make is one of the oldest and most widely used build automation tools. It reads a Makefile that specifies how to derive the target program from source files using rules with dependency tracking.

## Makefile Structure

```makefile
# Variables
CC     = gcc
CFLAGS = -Wall -O2
TARGET = myapp

# Default target
all: $(TARGET)

# Link target
$(TARGET): main.o util.o
	$(CC) $(CFLAGS) -o $@ $^

# Compile source files
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Clean build artifacts
clean:
	rm -f *.o $(TARGET)

# Phony targets
.PHONY: all clean
```

## Common Patterns

### Phony Targets Convention
```makefile
.PHONY: all clean install test lint format

all: build

build:
	go build -o bin/app .

test:
	go test ./...

lint:
	golangci-lint run

install:
	cp bin/app /usr/local/bin/

clean:
	rm -rf bin/
```

### Automatic Variables

| Variable | Meaning |
|----------|---------|
| `$@` | Target name |
| `$<` | First prerequisite |
| `$^` | All prerequisites |
| `$*` | Stem of the pattern match |
| `$?` | Changed prerequisites |

### Conditional Builds
```makefile
DEBUG ?= 0
ifeq ($(DEBUG), 1)
	CFLAGS += -g -DDEBUG
else
	CFLAGS += -O3
endif
```

## Related Tools

- **[cmake](../../build/cmake.md)** — Cross-platform build system generator
- **[ninja](../../build/ninja.md)** — Fast, small build system (often used with cmake)
- **[meson](../../build/meson.md)** — Modern build system
- **[just](../../build/just.md)** — Command runner (simpler alternative)
