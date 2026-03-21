#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 3 ]; then
  echo "Usage: $0 <idea-id> <log-file> <command...>" >&2
  exit 1
fi

if ! command -v screen >/dev/null 2>&1; then
  echo "screen not found in PATH" >&2
  exit 1
fi

idea_id="$1"
log_file="$2"
shift 2
command_string="$*"

mkdir -p "$(dirname "$log_file")"

safe_id="$(printf '%s' "$idea_id" | tr -cs 'A-Za-z0-9._-' '-' | sed 's/^-*//; s/-*$//')"
if [ -z "$safe_id" ]; then
  safe_id="idea"
fi

session="idea-${safe_id}-$(date +%Y%m%d-%H%M%S)"
printf -v wrapped 'set -euo pipefail; exec > %q 2>&1; %s' "$log_file" "$command_string"

screen -dmS "$session" bash -lc "$wrapped"

echo "SCREEN_SESSION=$session"
echo "LOG_FILE=$log_file"
echo "COMMAND=$command_string"
