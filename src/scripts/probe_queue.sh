#!/bin/bash
# Runs pending bix-3 probe jobs (scale x run) inside one heavy slot (CHANGES-10b).
# A job is pending while its output file is missing or empty. A job still running 23 minutes after the slot was
# taken is stopped by pid and its partial output removed (it stays pending). The slot is always released.
# Usage: probe_queue.sh <lane_root>
set -uo pipefail
L="$1"; P="$L/runs/review1-probes-2026-09-30"; SLOT=<local-scheduler>/mac_slot.py
/usr/bin/python3 "$SLOT" acquire --kind heavy --owner e5a-bix3 --minutes 25 --wait 1800 | grep -v '^waiting' || { echo "no slot"; exit 3; }
start=$(date +%s)
trap '/usr/bin/python3 "$SLOT" release --owner e5a-bix3' EXIT
export R_LIBS_USER="$L/env/no-user-lib" R_LIBS="" R_PROFILE_USER=/dev/null R_ENVIRON_USER=/dev/null LC_ALL=C TZ=America/New_York
for job in K1.run1 K1.run2 K10.run1 K10.run2 K100.run1 K100.run2; do
  out="$P/bix-3-probes-$job.json"; [ -s "$out" ] && continue
  left=$(( 23*60 - ($(date +%s) - start) )); [ "$left" -lt 300 ] && { echo "$(date +%T) stop: $left s left"; break; }
  k="${job%%.*}"; k="${k#K}"
  "$L/env/bin/Rscript" --vanilla "$L/scripts/q/bix-3-probes-v2.R" "$L/runs/recorded-2026-09-30-bix3/r1/bix-3_normcount.csv" "$k" > "$out" 2> "$P/bix-3-probes-$job.stderr" &
  pid=$!
  while kill -0 "$pid" 2>/dev/null; do
    if [ $(( $(date +%s) - start )) -ge $(( 23*60 )) ]; then kill "$pid"; wait "$pid"; rm -f "$out"; echo "$(date +%T) $job stopped at slot limit"; exit 0; fi
    sleep 10
  done
  wait "$pid"; rc=$?
  echo "$(date +%T) $job exit=$rc secs=$(( $(date +%s) - start )) sha256=$(shasum -a 256 "$out" | cut -d' ' -f1)" | tee -a "$P/log.txt"
  [ "$rc" = 0 ] || { rm -f "$out"; exit 1; }
done
