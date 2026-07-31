---
description: Scan a directory for deny-listed personal data and credentials before it leaves the machine. Pass a path, or leave blank to check the public build.
argument-hint: [path-to-check]
---

Run the scrubber over a directory and report honestly on what it found.

Target: $ARGUMENTS (if empty, use `dist/public`)

Steps:

1. Locate the deny list. Prefer `build/denylist.private.json`. If it is missing,
   tell the user to copy `scripts/denylist.example.json` and fill it in — do not
   invent patterns and do not proceed with an empty list.

2. Run the scan and capture the exit code:

```bash
python3 scripts/scrub.py --denylist build/denylist.private.json <target>
echo "exit: $?"
```

3. Report the exit code and the command output verbatim. Exit 0 is clean, 1 is
   findings, 2 is a usage or config error. Do not summarize a nonzero exit as
   "mostly clean".

4. For each finding, name the file, the line, and the pattern. Propose the fix
   as a change to the source file or to `values/public.json`.

Never resolve a finding by adding an exception or loosening the pattern. If a
pattern is genuinely too broad, say so and propose a tighter regex — that is a
deliberate change the user approves, not something to slip in.
