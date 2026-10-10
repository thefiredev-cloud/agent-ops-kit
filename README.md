# Agent Ops Kit

A Claude Code plugin for developers who let an AI agent ship code and want guardrails around what it claims and what it publishes. It bundles three skills, two slash commands, one review subagent and a Python scanner that fails when listed personal data or credentials survive into a build.

The plugin teaches three habits:

1. Say what you checked. Do not claim a service is running without the command output that shows it.
2. Strip your data before you share. The scanner exits nonzero when anything on your deny list is still in a public copy.
3. Build both copies from one source. A private and a public version are generated from one tree, so they cannot drift apart.

The kit does not include a build script. The `two-variant-release` skill describes the layout and rules, and you write the `build/build.py` that renders it (see [What you provide](#what-you-provide)).

Status: version 0.1.0, early. The scanner is a regex deny list. The repository has no automated test suite, and the plugin is not listed in a marketplace.

## Install

This repository is a plugin, not a marketplace. It has `.claude-plugin/plugin.json` and no `marketplace.json`, so `/plugin install` and `claude plugin marketplace add` do not work for it. Load it by path or by URL:

```bash
# from a clone
git clone https://github.com/thefiredev-cloud/agent-ops-kit.git
claude --plugin-dir ./agent-ops-kit

# or straight from GitHub
claude --plugin-url https://github.com/thefiredev-cloud/agent-ops-kit/archive/refs/heads/main.zip
```

Both flags apply to one session, so pass the flag each time you start Claude Code. `claude plugin validate ./agent-ops-kit` checks the manifest.

Requirements: Claude Code with plugin support, and Python 3.9 or newer for the scanner. The scanner uses only the standard library. The components below were loaded and listed on Claude Code 2.1.296.

## What you get

Plugin commands and agents are namespaced with the plugin name.

### Skills

Skills load on their own when the work calls for them.

| Skill | Fires when |
|---|---|
| `evidence-gate` | You are about to claim something is deployed, running, passing, or fixed |
| `scrub-before-share` | Something is heading off the machine: a repo, a gist, a bug report |
| `two-variant-release` | You need a private build and a public build of the same project |

### Commands

You run these yourself.

| Command | Does |
|---|---|
| `/agent-ops-kit:scrub-check [path]` | Runs the scanner over `path` (default `dist/public`) with `build/denylist.private.json` and reports the exit code and output |
| `/agent-ops-kit:release-public` | Runs `python3 build/build.py public`, lists `dist/public`, checks placeholders, `LICENSE` and `SECURITY.md`, then stops. It never publishes. |

Both commands call `scripts/scrub.py` or `build/build.py` relative to the directory Claude Code is working in. Copy `scripts/scrub.py` into your project, or run Claude Code from a clone of this repository.

### Agent

`agent-ops-kit:release-auditor` reads a build directory, runs the scanner first, then checks for what a regex cannot catch: hard-coded machine paths, filenames, fixtures, git history and look-alike placeholders. It returns `SAFE TO SHARE` or `NOT SAFE` with file-and-line evidence. Its instructions forbid editing and publishing. The agent file does not restrict its tools, so that rule is a prompt, not a permission.

## What you provide

- A deny list. Copy `scripts/denylist.example.json`, replace the example values with your own, and keep your copy out of version control. `/scrub-check` and the auditor look for it at `build/denylist.private.json`.
- A build script, if you want `/release-public`. The command runs `build/build.py public`, and `two-variant-release` describes the layout it expects: `src/` with `{{ TOKEN }}` placeholders, `values/internal.json`, `values/public.json`, `dist/internal/` and `dist/public/`.

## The scanner

`scripts/scrub.py` scans file contents and filenames against a deny list and exits nonzero on any hit.

```bash
python3 scripts/scrub.py --denylist my-denylist.json ./dist
echo "exit: $?"
```

| Option | Meaning |
|---|---|
| `target` | Directory to scan |
| `--denylist FILE` | Deny list JSON (required) |
| `--groups a,b` | Enforce only these groups. Default: every group in the list |
| `--json` | Print findings as JSON |

Exit codes: `0` clean, `1` findings, `2` missing or unparsable command-line arguments. A missing or invalid deny list, an empty deny list, an unknown group and a target that is not a directory also exit `1`, with a `scrub:` message on stderr. Read the output, not only the exit code.

The engine ships with no patterns of its own. A deny list is JSON with a `patterns` array. Each entry has:

- `name`: shown in findings
- `regex`: a Python regular expression, matched per file with `re.MULTILINE`
- `group`: `secret` or `identity`, default `identity`
- `flags`: `"i"` for case-insensitive
- `hint`: the fix suggestion shown next to a finding

An empty `patterns` list makes the scanner refuse to run, so an empty list cannot pass a build.

Patterns belong to one of two groups:

- `secret`: API keys, tokens, private keys, filled-in `.env` lines. Fatal in any build, including private ones.
- `identity`: names, emails, phone numbers, hostnames, internal IP addresses, home directory paths. Fine in a private build, fatal in a public one.

```bash
# everything, for a public build
python3 scripts/scrub.py --denylist my-denylist.json ./dist/public

# credentials only, for a private build
python3 scripts/scrub.py --denylist my-denylist.json --groups secret ./dist/internal
```

Matches are masked in the output. You get the file, the line, whether the hit was in the filename or the content, and the pattern name: enough to find it, not enough to reuse it.

### Limits

- It skips any path that has a directory named `.git`, `node_modules`, `__pycache__`, `.venv`, `venv` or `.mypy_cache`. The check includes the parent directories of the target, so a target that sits under a directory named `venv` is reported `CLEAN` without being scanned.
- It reads only the first 8 MiB of each file.
- It decodes files loosely as UTF-8, so a string inside a compiled artifact is usually found. Metadata inside images and PDFs is not parsed.
- It finds only what the deny list describes. A new hostname or alias passes.

## Test it before you trust it

A scanner that has never failed might be matching nothing at all. Plant a deny string in a file, run it, and confirm it fails. Then remove the string and confirm it passes. Repeat both runs every time you change the deny list.

## What it does not do

- It does not rewrite git history. A clean working tree says nothing about older commits. Check with `git log -p -S '<string>'`.
- It does not publish. The build is the output, and the release is your call.
- It does not make a push reversible. Forks, clones and caches outlive a deleted repository.

## License

MIT. See [LICENSE](LICENSE). Security policy in [SECURITY.md](SECURITY.md).
