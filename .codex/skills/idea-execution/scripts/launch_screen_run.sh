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
log_dir="$(cd "$(dirname "$log_file")" && pwd -P)"
log_file_abs="${log_dir}/$(basename "$log_file")"

safe_id="$(printf '%s' "$idea_id" | tr -cs 'A-Za-z0-9._-' '-' | sed 's/^-*//; s/-*$//')"
if [ -z "$safe_id" ]; then
  safe_id="idea"
fi

session="idea-${safe_id}-$(date +%Y%m%d-%H%M%S)"
command_b64="$(printf '%s' "$command_string" | base64 | tr -d '\n')"
runner_file="$(mktemp "${TMPDIR:-/tmp}/idea-launch-${safe_id}.XXXXXX.sh")"

cat > "$runner_file" <<'EOF_RUNNER'
#!/usr/bin/env bash
set -euo pipefail

: "${IDEA_LAUNCH_LOG_FILE:?}"
: "${IDEA_LAUNCH_IDEA_ID:?}"
: "${IDEA_LAUNCH_SESSION:?}"
: "${IDEA_LAUNCH_COMMAND_B64:?}"

exec > "$IDEA_LAUNCH_LOG_FILE" 2>&1

GPU_MONITOR_ID="${GPU_MONITOR_ID:-${DEVICE:-0}}"
GPU_BUSY_CHECK_INTERVAL_SECONDS="${GPU_BUSY_CHECK_INTERVAL_SECONDS:-180}"
GPU_IDLE_CHECK_INTERVAL_SECONDS="${GPU_IDLE_CHECK_INTERVAL_SECONDS:-10}"
GPU_IDLE_CONFIRM_COUNT="${GPU_IDLE_CONFIRM_COUNT:-4}"
GPU_IDLE_UTIL_THRESHOLD="${GPU_IDLE_UTIL_THRESHOLD:-5}"
GPU_IDLE_MEM_THRESHOLD_MB="${GPU_IDLE_MEM_THRESHOLD_MB:-500}"
SKIP_GPU_IDLE_WAIT="${SKIP_GPU_IDLE_WAIT:-0}"

cleanup_runner() {
  rm -f -- "$0"
}

wait_for_gpu_idle() {
  echo "[gpu-wait] gpu=${GPU_MONITOR_ID} busy_interval=${GPU_BUSY_CHECK_INTERVAL_SECONDS}s idle_interval=${GPU_IDLE_CHECK_INTERVAL_SECONDS}s idle_confirm_count=${GPU_IDLE_CONFIRM_COUNT} util<=${GPU_IDLE_UTIL_THRESHOLD}% mem<=${GPU_IDLE_MEM_THRESHOLD_MB}MB skip_wait=${SKIP_GPU_IDLE_WAIT}"
  if [[ "$SKIP_GPU_IDLE_WAIT" == "1" ]]; then
    echo "[gpu-wait] skip because SKIP_GPU_IDLE_WAIT=1"
    return 0
  fi
  if ! command -v nvidia-smi >/dev/null 2>&1 || ! nvidia-smi -i "$GPU_MONITOR_ID" >/dev/null 2>&1; then
    echo "[gpu-wait] nvidia-smi/GPU unavailable, skip wait"
    return 0
  fi

  local idle_hits=0
  while true; do
    local stat_line util mem sleep_seconds
    stat_line="$(nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader,nounits -i "$GPU_MONITOR_ID")"
    util="${stat_line%%,*}"
    util="${util//[[:space:]]/}"
    mem="${stat_line##*,}"
    mem="${mem//[[:space:]]/}"
    if (( util <= GPU_IDLE_UTIL_THRESHOLD && mem <= GPU_IDLE_MEM_THRESHOLD_MB )); then
      idle_hits=$(( idle_hits + 1 ))
      if (( idle_hits >= GPU_IDLE_CONFIRM_COUNT )); then
        echo "[gpu-wait] GPU ${GPU_MONITOR_ID} idle ${idle_hits}/${GPU_IDLE_CONFIRM_COUNT} times, start run"
        return 0
      fi
      sleep_seconds="$GPU_IDLE_CHECK_INTERVAL_SECONDS"
      echo "[gpu-wait] idle util=${util}% mem=${mem}MB, confirm ${idle_hits}/${GPU_IDLE_CONFIRM_COUNT}, recheck in ${sleep_seconds}s"
    else
      if (( idle_hits > 0 )); then
        echo "[gpu-wait] idle streak broken at ${idle_hits}/${GPU_IDLE_CONFIRM_COUNT}, reset"
      fi
      idle_hits=0
      sleep_seconds="$GPU_BUSY_CHECK_INTERVAL_SECONDS"
      echo "[gpu-wait] busy util=${util}% mem=${mem}MB, recheck in ${sleep_seconds}s"
    fi
    sleep "$sleep_seconds"
  done
}

trap cleanup_runner EXIT

command_string="$(printf '%s' "$IDEA_LAUNCH_COMMAND_B64" | base64 --decode)"
echo "[launch] idea_id=$IDEA_LAUNCH_IDEA_ID session=$IDEA_LAUNCH_SESSION"
echo "[launch] command=$command_string"
wait_for_gpu_idle
bash -lc "$command_string"
EOF_RUNNER

chmod +x "$runner_file"
screen -dmS "$session" env \
  IDEA_LAUNCH_LOG_FILE="$log_file_abs" \
  IDEA_LAUNCH_IDEA_ID="$idea_id" \
  IDEA_LAUNCH_SESSION="$session" \
  IDEA_LAUNCH_COMMAND_B64="$command_b64" \
  bash "$runner_file"

echo "SCREEN_SESSION=$session"
echo "LOG_FILE=$log_file_abs"
echo "COMMAND=$command_string"
