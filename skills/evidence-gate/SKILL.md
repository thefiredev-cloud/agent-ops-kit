---
name: evidence-gate
description: >
  Blocks claims about system state that have no command output behind them. Use
  before saying anything is deployed, running, reachable, passing, fixed,
  installed, or earning - and whenever a report needs to distinguish what was
  verified from what was assumed. Triggers on "is it working", "did it deploy",
  "confirm", "verify", "prove it", "check that", or any status claim in a
  handoff or report.
---

# Evidence gate

A claim about state is a measurement, not a memory. If you did not run a command
this session and read its output, you do not know.

## The rule

Before writing that something is deployed, running, reachable, passing, fixed,
installed, or earning, ask: **which command proved that, and what did it print?**

No output, no claim. Say "unverified" instead. "Unverified" costs a follow-up
question. A wrong status claim costs a bad decision made downstream.

## What does not count as evidence

- An environment variable being set. It proves a value exists, not that anything read it.
- A config file saying a service is enabled.
- A successful build or deploy. Shipping is not running.
- Exit code 0 from a script that swallows its own errors.
- What the code says it does.
- What was true last session.

## What counts

| Claim | Evidence |
|---|---|
| Service is up | `systemctl --user status <unit>` showing `active (running)` |
| Port is listening | `ss -tlnp \| grep <port>` |
| Endpoint answers | `curl -sS -o /dev/null -w '%{http_code}' <url>` returning 200 |
| Tests pass | The runner's summary line |
| Package is installed | The version the binary itself prints |
| File changed | `git diff --stat`, or the file re-read after the edit |
| Nothing restarted | `ExecMainStartTimestamp` - restart counters miss manual bounces |

## Reporting

Show the command and what it returned. Not "the API is healthy" but:

```
$ curl -sS -o /dev/null -w '%{http_code}\n' http://10.0.0.1:3020/
200
```

When you could not verify, say so plainly and name the reason: "Could not check
the service - no access to host-a from here." That is a useful report.
A confident guess is not.

## Give yourself a check you can run

Before calling work done, name one command that fails if the change is broken,
then run it. A typecheck, one test, a curl that must return 200. Without it,
"looks done" is the only signal available, and the person you report to becomes
your test suite.

Keep it fast. A check that takes three minutes gets skipped.
