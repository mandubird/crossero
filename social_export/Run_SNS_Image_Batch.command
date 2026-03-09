#!/bin/bash
set -e
cd "$(dirname "$0")"

if [ ! -x "../.venv/bin/python" ]; then
  echo "Python venv not found: ../.venv/bin/python"
  read -p "Press Enter to close..." _
  exit 1
fi

echo "[SNS Batch] Start"
../.venv/bin/python social_batch_export.py || true

echo ""
echo "Done. Check output folder:"
echo "$(pwd)/output"
echo ""
read -p "Press Enter to close..." _
