#!/usr/bin/env bash
# PodLens one-command setup.
# Creates a virtual environment, installs dependencies, and prepares config files.
set -euo pipefail

cd "$(dirname "$0")"

PYTHON="${PYTHON:-python3}"

echo "PodLens setup"
echo "-------------"

# 1. Virtual environment
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment (.venv)..."
  "$PYTHON" -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

# 2. Dependencies
echo "Installing dependencies..."
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt

# 3. Config files
if [ ! -f ".env" ]; then
  cp .env.example .env
  echo "Created .env  -> open it and paste your GEMINI_API_KEY"
fi

if [ ! -f "profile.md" ]; then
  cp profile.example.md profile.md
  echo "Created profile.md -> edit it with your own interests for personal mapping"
fi

echo ""
echo "Setup complete."
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your GEMINI_API_KEY (free: https://aistudio.google.com/apikey)"
echo "  2. (Optional) Edit profile.md with your interests"
echo "  3. Activate the env:   source .venv/bin/activate"
echo "  4. Try it:             python -m podlens examples/sample_transcript.txt"
echo ""
echo "No key yet? Inspect the pipeline without calling the API:"
echo "  python -m podlens examples/sample_transcript.txt --dry-run"
