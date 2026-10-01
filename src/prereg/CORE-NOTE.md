# About CORE.sha256

`CORE.sha256` was compiled on 30 Sep 2026 at 21:57 EDT (its final version, with exact file times, is stamped 21:57:54), from the hash list recorded at the time in the auditor's private plan (`plans/e5a-bixbench-audit.md`, "Pre-registration" section); every hash in it matches that list and the files.
A hash published then attests that the file has not changed since; what dates each freeze is the plan's contemporaneous entry and the file modification time shown.
Its lines carry notes after the path, so check them from the `src/` folder with:

    shasum -a 256 -c <(awk '$1 ~ /^[0-9a-f]{64}$/ {print $1"  "$2}' prereg/CORE.sha256)
