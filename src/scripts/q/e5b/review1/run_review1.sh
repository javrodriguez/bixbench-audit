#!/bin/bash
# E5B-CHANGES-5: reruns adversarial review 1's six probes (copied unchanged from the reviewer's scratch folder) twice
# under the lane's hashing (E5B-SCRIPTS-5.sha256), isolated as run_e5b.py; outputs r1/ and r2/, compared byte for byte.
# Usage: run_review1.sh <repo_root> <run_dir> <conda_env> <env2_venv> <data_root>
set -uo pipefail
REPO=$1; RUN=$2; ENV=$3; PY2=$4; DATA=$5
while read -r h f; do [ "$(shasum -a 256 "$REPO/$f" | cut -d' ' -f1)" = "$h" ] || { echo "REFUSED: $f differs"; exit 2; }; done < "$REPO/src/prereg/E5B-SCRIPTS-5.sha256"
[ ! -e "$RUN/r1" ] || { echo "REFUSED: $RUN has outputs"; exit 2; }
export PYTHONNOUSERSITE=1 LC_ALL=C TZ=America/New_York
Q="$REPO/src/scripts/q/e5b/review1"
for rep in 1 2; do
  mkdir -p "$RUN/r$rep"
  for p in p3 p52 p52b p52c p53; do
    "$ENV/bin/python" -s -P "$Q/$p.py" > "$RUN/r$rep/$p.txt" 2> "$RUN/r$rep/$p.stderr"
    echo "$(date '+%H:%M:%S') $p rep=$rep exit=$? sha256=$(shasum -a 256 "$RUN/r$rep/$p.txt" | cut -d' ' -f1)" >> "$RUN/log.txt"
  done
  "$PY2/bin/python" -s -P "$Q/p27.py" "$DATA" 0 34 > "$RUN/r$rep/p27.json" 2> "$RUN/r$rep/p27.stderr"
  echo "$(date '+%H:%M:%S') p27 rep=$rep exit=$? sha256=$(shasum -a 256 "$RUN/r$rep/p27.json" | cut -d' ' -f1)" >> "$RUN/log.txt"
done
for f in p3.txt p52.txt p52b.txt p52c.txt p53.txt p27.json; do cmp -s "$RUN/r1/$f" "$RUN/r2/$f" && echo "$f identical" || echo "$f DIFFERENT"; done | tee -a "$RUN/log.txt"
