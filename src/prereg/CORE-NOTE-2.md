# Correction to CORE-NOTE.md (30 Sep 2026, 22:15 EDT)

`CORE-NOTE.md` says every hash in `CORE.sha256` was taken from the hash list recorded at the time in the auditor's private plan; that is true of the first six lines only.
The plan never names `ADDENDUM-4.md`, which was written after the plan's last change: that line's hash comes from `prereg/SCRIPTS-16.sha256` (file time 21:04:54), written with the addendum.
Every hash in `CORE.sha256` matches its source and the file; what dates each freeze is that contemporaneous record (the plan for the first six, `SCRIPTS-16.sha256` for the seventh) and the file time shown.
The plan is a private file without its own version history, so for the first six lines "recorded at the time" rests on the auditor's record.
A portable form of the check command, for awk versions without interval expressions, run from `src/`:

    shasum -a 256 -c <(awk 'length($1) == 64 {print $1"  "$2}' prereg/CORE.sha256)

`SCRIPTS-5b.sha256` and `SCRIPTS-7b.sha256` list absolute paths on the auditor's machine, so they check only there; both match there and neither is superseded.
