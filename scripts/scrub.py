#!/usr/bin/env python3
"""Scan a directory for deny-listed strings and fail loudly if any survive.

The engine holds no patterns of its own. Every pattern comes from a deny list
JSON file, so this file is safe to ship while your deny list stays private.

    scrub.py --denylist private.json dist/public
    scrub.py --denylist private.json --groups secret dist/internal

Exit codes:
    0  clean
    1  findings (something leaked)
    2  bad usage or unreadable deny list

Deny list format:
    {
      "patterns": [
        {"name": "owner-email", "group": "identity", "regex": "...",
         "flags": "i", "hint": "use contact@acme.example"}
      ]
    }

Groups let one list serve two jobs. "secret" patterns (API keys, private keys)
must never appear in ANY build. "identity" patterns (names, hosts, paths) are
fine internally and fatal in a public build.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Directories that are never part of a build output.
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", ".mypy_cache"}

# Read at most this much of any single file. A plugin ships text; anything
# larger is almost certainly a binary blob and gets a bytes scan instead.
MAX_BYTES = 8 * 1024 * 1024


def load_patterns(path, groups):
    """Compile deny patterns from JSON, optionally filtered to certain groups."""
    try:
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        sys.exit(f"scrub: deny list not found: {path}")
    except json.JSONDecodeError as exc:
        sys.exit(f"scrub: deny list is not valid JSON: {path}: {exc}")

    entries = raw.get("patterns")
    if not entries:
        # An empty deny list would silently pass everything. That is the exact
        # failure mode this tool exists to prevent, so refuse to run.
        sys.exit(f"scrub: deny list has no patterns: {path}")

    compiled = []
    for i, entry in enumerate(entries):
        name = entry.get("name") or f"pattern-{i}"
        group = entry.get("group", "identity")
        if groups and group not in groups:
            continue
        expr = entry.get("regex")
        if not expr:
            sys.exit(f"scrub: pattern {name!r} has no regex")
        flags = re.MULTILINE
        if "i" in entry.get("flags", ""):
            flags |= re.IGNORECASE
        try:
            compiled.append((name, group, re.compile(expr, flags), entry.get("hint", "")))
        except re.error as exc:
            sys.exit(f"scrub: pattern {name!r} is not a valid regex: {exc}")

    if not compiled:
        sys.exit(f"scrub: no patterns matched groups {sorted(groups)}")
    return compiled


def mask(text):
    """Show enough of a match to locate it, never enough to reuse it."""
    text = text.replace("\n", " ").strip()
    if len(text) <= 4:
        return "*" * len(text)
    return f"{text[:2]}{'*' * min(len(text) - 4, 12)}{text[-2:]}"


def walk(root):
    """Yield every file under root, skipping VCS and dependency noise."""
    for path in sorted(root.rglob("*")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file():
            yield path


def scan_text(text, rel, patterns, findings, kind):
    """Record every deny-pattern hit in text, with 1-indexed line numbers."""
    for name, group, rx, hint in patterns:
        for m in rx.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            findings.append(
                {
                    "file": rel,
                    "line": line,
                    "pattern": name,
                    "group": group,
                    "where": kind,
                    "match": mask(m.group(0)),
                    "hint": hint,
                }
            )


def scan(root, patterns):
    findings = []
    for path in walk(root):
        rel = str(path.relative_to(root))

        # A filename leaks just as loudly as file contents (jdoe-notes.md).
        scan_text(rel, rel, patterns, findings, "filename")

        try:
            data = path.read_bytes()[:MAX_BYTES]
        except OSError as exc:
            findings.append(
                {
                    "file": rel, "line": 0, "pattern": "unreadable", "group": "meta",
                    "where": "content", "match": str(exc), "hint": "cannot verify this file",
                }
            )
            continue

        # Decode loosely: a deny string embedded in an otherwise binary file
        # still needs to be caught.
        scan_text(data.decode("utf-8", errors="replace"), rel, patterns, findings, "content")
    return findings


def main():
    ap = argparse.ArgumentParser(description="Fail if deny-listed strings survive into a build.")
    ap.add_argument("target", help="directory to scan")
    ap.add_argument("--denylist", required=True, help="path to deny list JSON")
    ap.add_argument(
        "--groups",
        default="",
        help="comma-separated groups to enforce (default: all groups in the list)",
    )
    ap.add_argument("--json", action="store_true", help="emit findings as JSON")
    args = ap.parse_args()

    root = Path(args.target)
    if not root.is_dir():
        sys.exit(f"scrub: not a directory: {root}")

    groups = {g.strip() for g in args.groups.split(",") if g.strip()}
    patterns = load_patterns(args.denylist, groups)
    findings = scan(root, patterns)

    if args.json:
        print(json.dumps({"clean": not findings, "findings": findings}, indent=2))
    else:
        scope = ",".join(sorted(groups)) if groups else "all"
        print(f"scrub: {len(patterns)} patterns (groups: {scope}) over {root}")
        if not findings:
            print("scrub: CLEAN")
        else:
            print(f"scrub: FAILED - {len(findings)} finding(s)\n")
            for f in findings:
                print(f"  {f['file']}:{f['line']} [{f['pattern']}/{f['group']}/{f['where']}] {f['match']}")
                if f["hint"]:
                    print(f"      fix: {f['hint']}")

    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
