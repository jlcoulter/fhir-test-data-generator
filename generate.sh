#!/bin/bash

set -euo pipefail

VENV_DIR="venv"
PYTHON_BIN="$VENV_DIR/bin/python"

if [ ! -d "$VENV_DIR" ]; then
  echo "Creating Python virtual environment..."
  python3 -m venv "$VENV_DIR"
fi

echo "Installing dependencies..."
"$PYTHON_BIN" -m pip install -r requirements.txt

echo -e "\nCommand: $PYTHON_BIN generate.py $*"
echo ""

exec "$PYTHON_BIN" generate.py "$@"