#!/usr/bin/env bash
# Double-click this file to start the PodLens UI.
# It starts a local server and opens it in your browser. Leave the Terminal
# window open while you use it; close it (or Ctrl-C) when you're done.
cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
  echo "First run: setting up. This takes a minute..."
  bash setup.sh
fi

# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --quiet -r requirements.txt

PORT=8765

# Free the port if a previous server instance is still running, so we never
# end up talking to a stale server.
EXISTING=$(lsof -ti:${PORT} 2>/dev/null)
if [ -n "$EXISTING" ]; then
  echo "Stopping a previous server on port ${PORT}..."
  kill $EXISTING 2>/dev/null
  sleep 1
fi

echo ""
echo "PodLens UI -> http://127.0.0.1:${PORT}"
echo "(Keep this window open. Close it or press Ctrl-C to stop.)"
echo ""

# Open the browser shortly after the server starts.
( sleep 2; open "http://127.0.0.1:${PORT}" ) &

exec python -m uvicorn webui.server:app --host 127.0.0.1 --port "${PORT}" --reload --reload-dir webui --reload-dir podlens
