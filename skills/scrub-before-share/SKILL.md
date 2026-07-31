---
name: scrub-before-share
description: >
  Strip personal and company data out of anything about to leave the machine -
  a repo going public, a gist, a bug report, a screenshot, a config sample, a
  plugin release. Use when the user says "make this public", "open source this",
  "share this", "sanitize", "redact", "scrub", "remove my data", or "safe to
  post". Also use before pasting logs or config into an issue tracker.
---

# Scrub before share

Assume every file leaving the machine will be read by a stranger and indexed by
a search engine. Publishing is not reversible: a deleted repo lives on in forks,
caches, and clones.

## Run the scrubber

`scripts/scrub.py` scans file contents *and filenames* against a deny list and
exits nonzero on any hit.

```bash
python3 scripts/scrub.py --denylist my-denylist.json ./dist
echo "exit: $?"     # 0 clean, 1 findings, 2 bad usage
```

The engine ships with no patterns of its own. Copy
`scripts/denylist.example.json`, fill in your values, and keep your copy out of
version control - a deny list is a tidy inventory of exactly what you are hiding.

## Two groups, two jobs

- **`secret`** - API keys, tokens, private keys, populated `.env` lines. Fatal
  anywhere, including private builds. A leaked key is leaked the moment it is
  committed.
- **`identity`** - names, emails, phone numbers, hostnames, internal IPs, home
  directory paths, account ids, product names. Fine in a private build, fatal in
  a public one.

Enforce both on anything public; enforce `secret` on everything:

```bash
python3 scripts/scrub.py --denylist my-denylist.json --groups secret ./private-build
```

## What people forget

Contents are the easy part. These get missed:

1. **Filenames and directory names.** `notes-for-dave.md` names Dave.
2. **Git history.** Scrubbing the working tree leaves every past commit intact.
   Check with `git log -p -S '<string>'` before you conclude it is gone.
3. **Absolute paths in tracebacks, lockfiles, and `.map` files.** `/home/<you>/`
   appears in build output nobody reads.
4. **Sample config and fixtures.** Test data is real data surprisingly often.
5. **Screenshots.** A terminal title bar carries a hostname and a username.

## When the scrubber fires

Do not add an exception. Fix the file. An allowlist entry is a permanent hole
punched in the one check standing between private data and the internet.

If a pattern is genuinely too broad - it matches an ordinary English word -
tighten the regex, do not skip the path.

## Before publishing

1. Build the public variant. The build fails if anything survives.
2. Read the rendered README as a stranger would. Does it assume a machine only
   you have?
3. Confirm placeholders look obviously fake: `contact@acme.example`, `10.0.0.1`,
   `/home/user`, `<your-key>`. A realistic-looking fake gets copied into
   production by someone.
4. Publishing is the owner's call, never the agent's. Stage it and ask.
