---
description: Build the public variant, verify it is free of owner data, and stage it for release. Never publishes — publishing stays a human decision.
---

Produce the public build and report whether it is safe to release.

Steps:

1. Build the public variant and capture the exit code:

```bash
python3 build/build.py public
echo "exit: $?"
```

A nonzero exit means deny patterns survived and **no `dist/public` was written**.
Report the findings and stop. Do not retry with patterns disabled.

2. On a clean build, confirm what actually landed:

```bash
find dist/public -type f | sort
```

3. Read `dist/public/README.md` as a stranger would. Flag anything that assumes
   a machine, account, or directory only the owner has.

4. Check the placeholders are obviously fake — `acme.example`, `10.0.0.1`,
   `/home/user`, `<your-key>`. A realistic-looking fake gets copied into
   someone's production config.

5. Confirm `LICENSE` and `SECURITY.md` are present in the output.

6. Stop and report. Do **not** create a repository, push, tag, or publish to any
   registry or marketplace. End with the exact next step and who has to take it:

```
PENDING: publish the public plugin - awaiting your authorization
```

Publishing is irreversible in practice: forks, caches, and clones survive a
deleted repo. The build is the deliverable; the release is the owner's call.
