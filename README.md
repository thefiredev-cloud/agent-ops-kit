# Agent Ops Kit

A Claude Code plugin with three habits that keep an agent honest.

1. **Say what you checked.** Don't claim a service is running without the command output that shows it.
2. **Strip your data before you share.** A scrubber that fails the build when personal data survives into a public copy.
3. **Build both copies from one source.** A private version and a public version, generated — so they can't drift apart.

## Install

The repository is a plugin, not a marketplace, so load it by path or by URL:

```bash
# from a clone
git clone https://github.com/thefiredev-cloud/agent-ops-kit.git
claude --plugin-dir ./agent-ops-kit

# or straight from GitHub, for one session
claude --plugin-url https://github.com/thefiredev-cloud/agent-ops-kit/archive/refs/heads/main.zip
```

`claude plugin validate ./agent-ops-kit` checks the manifest.

## What you get

**Skills** load on their own when the work calls for them.

| Skill | Fires when |
|---|---|
| `evidence-gate` | You're about to claim something is deployed, running, passing, or fixed |
| `scrub-before-share` | Something is heading off the machine — a repo, a gist, a bug report |
| `two-variant-release` | You need a private build and a public build of the same project |

**Commands** you run yourself.

| Command | Does |
|---|---|
| `/scrub-check [path]` | Scans a directory for deny-listed data, reports the exit code |
| `/release-public` | Builds the public variant and stages it. Stops before publishing. |

**Agent** you delegate to.

`release-auditor` reads a build directory and returns `SAFE TO SHARE` or
`NOT SAFE` with file-and-line evidence. It never edits and never publishes.

## The scrubber

`scripts/scrub.py` scans file contents and filenames against a deny list and
exits nonzero on any hit.

```bash
python3 scripts/scrub.py --denylist my-denylist.json ./dist
echo "exit: $?"     # 0 clean, 1 findings, 2 bad usage
```

The engine ships with no patterns of its own. Copy
`scripts/denylist.example.json`, fill in your own values, and keep your copy out
of version control — a deny list is a tidy list of exactly what you're hiding.

Patterns belong to one of two groups:

- `secret` — API keys, tokens, private keys, filled-in `.env` lines. Fatal in
  any build, including private ones.
- `identity` — names, emails, phone numbers, hostnames, internal IP addresses,
  home directory paths. Fine in a private build, fatal in a public one.

```bash
# everything, for a public build
python3 scripts/scrub.py --denylist my-denylist.json ./dist/public

# credentials only, for a private build
python3 scripts/scrub.py --denylist my-denylist.json --groups secret ./dist/internal
```

Matches are masked in the output. You get the file, the line, and the pattern
name — enough to find it, not enough to reuse it.

## Test it before you trust it

A scrubber that has never failed might be matching nothing at all. Plant a deny
string in a file, build, and confirm it fails. Then remove it and confirm it
passes. Both runs, every time you change the deny list.

## Requirements

Claude Code with plugin support. Python 3.9 or newer for the scrubber. No third-party packages.

## Two things it does not do

It does not rewrite git history. A clean working tree says nothing about commit
40 — check with `git log -p -S '<string>'`.

It does not publish. The build is the output; the release is your call.

## Status

Version 0.1.0. Not listed in a plugin marketplace.

## License

MIT. See [LICENSE](LICENSE). Security policy in [SECURITY.md](SECURITY.md).
