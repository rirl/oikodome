#!/usr/bin/env bash
set -euo pipefail

# Rewrite git history to remove .venv from all commits.
# This script only rewrites history and does not commit working-tree changes.
# Usage:
#   ./scripts/rewrite_remove_venv_history.sh

REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"

GIT_FILTER_REPO=.venv/bin/git-filter-repo
if [ ! -x "$GIT_FILTER_REPO" ]; then
  if command -v git-filter-repo >/dev/null 2>&1; then
    GIT_FILTER_REPO=git-filter-repo
  else
    echo 'Error: git-filter-repo is not installed.' >&2
    echo 'Install it in .venv or on PATH and rerun this script. Example:' >&2
    echo '  .venv/bin/python -m pip install git-filter-repo' >&2
    exit 1
  fi
fi

if [ ! -d .git ]; then
  echo 'Error: this script must be run from within a git repository.' >&2
  exit 1
fi

if [ -d .venv ] || git ls-files --error-unmatch .venv >/dev/null 2>&1; then
  echo 'Rewriting git history to remove .venv from all commits...'
  "$GIT_FILTER_REPO" --invert-paths --path .venv/ || {
    echo 'git-filter-repo failed.' >&2
    exit 1
  }
  echo 'History rewrite complete. You will likely need to force-push branches and notify collaborators.'
else
  echo 'No .venv path present in the repository history or working tree.'
fi
