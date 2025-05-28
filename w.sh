#!/bin/bash

A="a"
B="b"
VIMDIFF_PID=""

# Get initial modification time
LAST_MOD=$(stat -c %Y "$B")

start_vimdiff() {
  # Kill previous vimdiff if running
  if [ -n "$VIMDIFF_PID" ] && kill -9 "$VIMDIFF_PID" 2>/dev/null; then
    kill "$VIMDIFF_PID"
    wait "$VIMDIFF_PID" 2>/dev/null
  fi
  # Start new vimdiff in the foreground
  vimdiff "$A" "$B" &
  VIMDIFF_PID=$!
}

# Start the first vimdiff
start_vimdiff

while true; do
  sleep 1
  NEW_MOD=$(stat -c %Y "$B")
  if [ "$NEW_MOD" != "$LAST_MOD" ]; then
    LAST_MOD=$NEW_MOD
    start_vimdiff
  fi
done

