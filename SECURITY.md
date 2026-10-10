# Security policy

## Reporting a vulnerability

Use [private vulnerability reporting](https://github.com/thefiredev-cloud/agent-ops-kit/security/advisories/new) on this repository. Please don't open a public issue for a security problem. A public report is a working exploit until it's patched.

Include what you did, what happened, and what you expected. A short reproduction is worth more than a long description.

Expect an acknowledgement within three working days.

## What this tool does and does not protect

`scripts/scrub.py` is a deny-list scanner. It catches what you tell it to catch.

**It will not** find data you never listed. A deny list is a list of known
strings and shapes, not a classifier. New hostname, new alias, new account id:
if it isn't in the list, it passes.

**It will not** rewrite git history. A clean working tree says nothing about
earlier commits. Check with `git log -p -S '<string>'`, and rewrite with
`git filter-repo` if you find something.

**It will not** read binary formats. Files are decoded loosely, so a string in a
compiled artifact is usually caught, but metadata inside an image or a PDF is not
parsed. Strip those separately.

**It will not** scan past the first 8 MiB of a file, and it skips any path with a
directory named `.git`, `node_modules`, `__pycache__`, `.venv`, `venv` or
`.mypy_cache`, including those directories in the path of the scan target.

**It will not** make publishing reversible. Deleting a repository doesn't
retract forks, clones, or search engine caches. Treat any push as permanent.

Use it as one gate among several, not as proof that a tree is clean.

## Handling your deny list

Your deny list contains the exact strings you're trying to hide. Treat it as
sensitive:

- Keep it out of version control. Add it to `.gitignore`.
- Never commit it to the repository you're scrubbing.
- Never paste it into a bug report.

This is why the scanner holds no patterns of its own: the engine is safe to
share, the list is not.

## If a credential leaks

Rotate first, then clean up. Deleting a commit does not un-publish a key that was
already cloned or indexed.

1. Revoke the credential at the provider.
2. Issue a replacement.
3. Then remove it from the tree and from git history.

A `secret`-group match should be treated as compromised the moment it lands in a
repository, whether or not that repository was ever public.
