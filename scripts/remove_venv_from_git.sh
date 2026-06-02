#!/usr/bin/env bash
set -euo pipefail

# Permanently remove .venv from git tracking.
# Usage:
#   ./scripts/remove_venv_from_git.sh        # remove from current index only
#   ./scripts/remove_venv_from_git.sh --history  # also rewrite history with git-filter-repo

REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"

if [ ! -f .gitignore ]; then
  touch .gitignore
fi

if ! grep -qxF '.venv/' .gitignore; then
  echo '.venv/' >> .gitignore
  echo 'Added .venv/ to .gitignore'
fi

TRACKED_COUNT=$(git ls-files .venv 2>/dev/null | wc -l)
if [ "$TRACKED_COUNT" -gt 0 ]; then
  echo 'Removing tracked .venv files from the index...'
  git rm -r --cached .venv
  echo 'Committing removal of .venv from the current branch...'
  git commit -m 'Remove .venv from repository and ignore it'
else
  echo 'No tracked .venv files found in the current index.'
fi

if [ "${1:-}" = '--history' ]; then
  if command -v git-filter-repo >/dev/null 2>&1; then
    echo 'Rewriting git history to remove .venv from all commits...'
    git filter-repo --invert-paths --path .venv/
    echo 'History rewritten. You may need to force-push branches and update collaborators.'
  else
    echo 'Error: git-filter-repo is not installed.' >&2
    echo 'Install git-filter-repo and rerun with --history to rewrite repository history.' >&2
    exit 1
  fi
fi
