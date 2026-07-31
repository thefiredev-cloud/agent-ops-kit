---
name: two-variant-release
description: >
  Ship a private full-fidelity copy and a generic public copy of the same
  project from one source tree. Use when the user wants "an internal one and a
  public one", "a version without my data", a sanitized fork, a redistributable
  template, or an open-source release of something built for themselves.
  Triggers on "make it transferable", "generic version", "strip my data out",
  or "internal and external builds".
---

# Two variants, one source

The moment a project has a private copy and a public copy maintained by hand,
they start drifting. Then someone fixes a bug in one of them, and the fix goes
out with a home directory path attached.

Author once. Generate both.

## The shape

```
values/internal.json          real hosts, real paths, real names
values/public.json            generic substitutes
src/                          the project, with {{ TOKEN }} placeholders where values differ
build/denylist.private.json   deny patterns (never ships)
build/build.py                renders src -> dist/<variant>, then scrubs
dist/internal/                full fidelity
dist/public/                  safe to hand to a stranger
```

## Rules that make it work

1. **No owner data in `src/`.** Every host, path, email, and product name is a
   `{{ TOKEN }}` placeholder (no spaces in real usage). If it differs between
   variants, it is a token.
2. **The public build is generated, never hand-edited.** Editing a copy is how
   data leaks. If the public output is wrong, fix `src/` or `values/public.json`.
3. **The deny list lives outside `src/`.** It contains the very strings you are
   hiding, so shipping it would defeat the exercise. Keep the *engine* shippable
   and the *list* private.
4. **A failed scrub leaves no output.** Build into staging; promote to `dist/`
   only on a clean scrub. Never leave a half-built tree someone can publish.
5. **Unresolved tokens fail the build.** A token left unsubstituted in the
   output means a value is missing from the variant's values file, not that it
   can be ignored.

## Build

```bash
python3 build/build.py all        # or: internal | public
echo "exit: $?"
```

Internal enforces `secret` patterns only - it is *supposed* to contain real
hosts. Public enforces every pattern.

## Choosing public values

Make them obviously fake so nobody ships one by accident:

| Kind | Use |
|---|---|
| Domain / email | `acme.example`, `contact@acme.example` |
| IP address | `10.0.0.1`, or `192.0.2.1` (reserved for docs) |
| Phone | `555-0100` (reserved for examples) |
| Home path | `/home/user` |
| Company / product | `ExampleCo`, `ExampleApp` |
| Credential | `<your-key>` - angle brackets read as a blank to fill |

Avoid plausible-looking fakes. `acme-corp.com` is a real domain somebody owns.

## Verify before you trust it

Plant a deny string in `src/`, run the public build, and confirm it fails. A
scrubber that has never failed has never been tested - it may be matching
nothing at all. Remove the plant and confirm the build goes green again.
