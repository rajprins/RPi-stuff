#!/usr/bin/env bash
#
# deploy.sh — build (validate + test) and deploy the tank game to a Raspberry Pi Pico.
#
# Usage:
#   ./deploy.sh              # test, deploy, then run with console output (Ctrl-C to detach)
#   ./deploy.sh --no-run     # test and deploy only; game auto-starts on next power-up
#   ./deploy.sh --no-test    # skip the host-side smoke test
#   ./deploy.sh --device D   # use serial device D instead of auto-detection
#
set -euo pipefail

# --- Configuration ---
FILES=(main.py tank.py shell.py terrain.py)
SMOKE_TEST=".smoke_test.py"
PYTHON="${PYTHON:-python3}"

# --- Options ---
RUN_AFTER_DEPLOY=1
RUN_TESTS=1
DEVICE=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --no-run)  RUN_AFTER_DEPLOY=0 ;;
        --no-test) RUN_TESTS=0 ;;
        --device)  DEVICE="$2"; shift ;;
        -h|--help) grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
        *) echo "Unknown option: $1 (try --help)" >&2; exit 2 ;;
    esac
    shift
done

cd "$(dirname "$0")"

info()  { printf '\033[1;34m==>\033[0m %s\n' "$*"; }
error() { printf '\033[1;31mERROR:\033[0m %s\n' "$*" >&2; exit 1; }

# --- Preflight: tooling ---
command -v "$PYTHON" >/dev/null || error "$PYTHON not found"
"$PYTHON" -m mpremote version >/dev/null 2>&1 \
    || error "mpremote not installed. Install with: $PYTHON -m pip install --user mpremote"

# --- Build step 1: syntax-check every source file ---
info "Syntax-checking ${FILES[*]}"
"$PYTHON" -m py_compile "${FILES[@]}" || error "Syntax check failed"

# --- Build step 2: host-side smoke test (stubbed hardware) ---
if [[ $RUN_TESTS -eq 1 ]]; then
    if [[ -f "$SMOKE_TEST" ]]; then
        info "Running smoke tests ($SMOKE_TEST)"
        "$PYTHON" "$SMOKE_TEST" >/dev/null || error "Smoke tests failed — not deploying"
        info "Smoke tests passed"
    else
        info "No $SMOKE_TEST found, skipping tests"
    fi
fi

# --- Find the Pico ---
if [[ -z "$DEVICE" ]]; then
    # Prefer cu.* devices on macOS; fall back to Linux-style names.
    for d in /dev/cu.usbmodem* /dev/ttyACM*; do
        [[ -e "$d" ]] && DEVICE="$d" && break
    done
fi
[[ -n "$DEVICE" && -e "$DEVICE" ]] \
    || error "No Pico serial device found (looked for /dev/cu.usbmodem*, /dev/ttyACM*). Is it plugged in?"
info "Using device: $DEVICE"

# --- Free the port if a previous session is holding it ---
HOLDERS="$(lsof -t "$DEVICE" 2>/dev/null || true)"
if [[ -n "$HOLDERS" ]]; then
    info "Port is busy (PID(s): $HOLDERS) — terminating previous session(s)"
    kill $HOLDERS 2>/dev/null || true
    sleep 1
fi

# --- Deploy ---
info "Copying files to Pico"
"$PYTHON" -m mpremote connect "$DEVICE" fs cp "${FILES[@]}" : \
    || error "Copy failed"

info "Verifying files on device"
"$PYTHON" -m mpremote connect "$DEVICE" fs ls :

# --- Run ---
if [[ $RUN_AFTER_DEPLOY -eq 1 ]]; then
    info "Starting game (Ctrl-C to detach; game keeps running on the Pico)"
    exec "$PYTHON" -m mpremote connect "$DEVICE" run main.py
else
    info "Deploy complete. Resetting Pico so main.py auto-starts"
    "$PYTHON" -m mpremote connect "$DEVICE" reset || true
    info "Done"
fi
