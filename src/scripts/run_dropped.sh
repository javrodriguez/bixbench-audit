#!/bin/bash
# CHANGES-14: runs bix-13-fit-dropped.R twice inside one heavy slot, then bix-13-classes.py on each fit (light).
# A job still running 23 minutes after the slot was taken is stopped by pid. The slot is always released.
# Usage: run_dropped.sh <lane_root>
set -uo pipefail
L="$1"; P="$L/runs/review5-probes-2026-09-30"; SLOT=<local-scheduler>/mac_slot.py
test ! -e "$P" || { echo "REFUSED: $P exists"; exit 2; }
mkdir -p "$P"
/usr/bin/python3 "$SLOT" acquire --kind heavy --owner e5a-bix3 --minutes 25 --wait 1800 | grep -v '^waiting' || { echo "no slot"; exit 3; }
start=$(date +%s)
trap '/usr/bin/python3 "$SLOT" release --owner e5a-bix3' EXIT
export R_LIBS_USER="$L/env/no-user-lib" R_LIBS="" R_PROFILE_USER=/dev/null R_ENVIRON_USER=/dev/null LC_ALL=C TZ=America/New_York PYTHONNOUSERSITE=1
for r in 1 2; do
  mkdir -p "$P/r$r"; t0=$(date +%s)
  "$L/env/bin/Rscript" --vanilla "$L/scripts/q/bix-13-fit-dropped.R" "$L/runs/pilot-2026-09-30/data" "$P/r$r/fits-dropped" > "$P/r$r/fit.log" 2> "$P/r$r/fit.stderr" &
  pid=$!
  while kill -0 "$pid" 2>/dev/null; do
    if [ $(( $(date +%s) - start )) -ge $(( 23*60 )) ]; then kill "$pid"; wait "$pid"; echo "$(date +%T) r$r fit stopped at slot limit" | tee -a "$P/log.txt"; exit 0; fi
    sleep 5
  done
  wait "$pid"; rc=$?
  (cd "$P/r$r/fits-dropped" && shasum -a 256 *.csv) > "$P/r$r/fits-dropped.sha256"
  "$L/env/bin/python" -s -P "$L/scripts/q/bix-13-classes.py" "$P/r$r/fits-dropped" > "$P/r$r/bix-13-classes-dropped.json" 2> "$P/r$r/classes.stderr"; rc2=$?
  echo "$(date '+%F %T %Z') r$r fit_exit=$rc classes_exit=$rc2 job_secs=$(( $(date +%s) - t0 )) fits=$(shasum -a 256 "$P/r$r/fits-dropped.sha256" | cut -d' ' -f1) classes=$(shasum -a 256 "$P/r$r/bix-13-classes-dropped.json" | cut -d' ' -f1)" | tee -a "$P/log.txt"
done
