#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." >/dev/null 2>&1 && pwd)"
VENV_DIR="$PROJECT_ROOT/.venv"

echo "Bootstrapping project at: $PROJECT_ROOT"

if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment in $VENV_DIR"
  python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

python -m pip install --upgrade pip setuptools wheel build

if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
  echo "Installing requirements.txt"
  pip install -r "$PROJECT_ROOT/requirements.txt"
fi

if [ -f "$PROJECT_ROOT/requirements-dev.txt" ]; then
  echo "Installing requirements-dev.txt"
  pip install -r "$PROJECT_ROOT/requirements-dev.txt"
else
  echo "Installing git-filter-repo into the virtualenv"
  pip install git-filter-repo
fi

echo "Installing project in editable mode"
pip install -e "$PROJECT_ROOT"

echo "Building project distributions"
python -m build "$PROJECT_ROOT" --wheel --sdist
# Optionally run tests if pytest is available in the virtualenv
if python -m pytest --version > /dev/null 2>&1; then
  echo "Running test suite"
  python -m pytest -q
else
  echo "pytest not available in virtualenv; skipping tests"
fi

echo "Bootstrap complete."
