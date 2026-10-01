#!/bin/bash
# Runs the CHANGES-11 probes twice inside one heavy slot; a job still running 23 minutes after the slot was taken is
# stopped by pid and its partial output removed. The slot is always released.
# Usage: probe2_queue.sh <lane_root>
set -uo pipefail
L="$1"; P="$L/runs/review2-probes-2026-09-30"; SLOT=<local-scheduler>/mac_slot.py
mkdir -p "$P"
/usr/bin/python3 "$SLOT" acquire --kind heavy --owner e5a-bix3 --minutes 25 --wait 1800 | grep -v '^waiting' || { echo "no slot"; exit 3; }
start=$(date +%s)
trap '/usr/bin/python3 "$SLOT" release --owner e5a-bix3' EXIT
export R_LIBS_USER="$L/env/no-user-lib" R_LIBS="" R_PROFILE_USER=/dev/null R_ENVIRON_USER=/dev/null LC_ALL=C TZ=America/New_York
for job in b13.run1 b36.run1 b13.run2 b36.run2; do
  out="$P/$job.json"; [ -s "$out" ] && continue
  script="$L/scripts/q/bix-13-probes2.R"; [ "${job%%.*}" = b36 ] && script="$L/scripts/q/bix-36-origin.R"
  t0=$(date +%s)
  "$L/env/bin/Rscript" --vanilla "$script" "$L/runs/pilot-2026-09-30/data" > "$out" 2> "$P/$job.stderr" &
  pid=$!
  while kill -0 "$pid" 2>/dev/null; do
    if [ $(( $(date +%s) - start )) -ge $(( 23*60 )) ]; then kill "$pid"; wait "$pid"; rm -f "$out"; echo "$(date +%T) $job stopped at slot limit"; exit 0; fi
    sleep 5
  done
  wait "$pid"; rc=$?
  echo "$(date +%T) $job exit=$rc job_secs=$(( $(date +%s) - t0 )) sha256=$(shasum -a 256 "$out" | cut -d' ' -f1)" | tee -a "$P/log.txt"
  [ "$rc" = 0 ] || { rm -f "$out"; exit 1; }
done
