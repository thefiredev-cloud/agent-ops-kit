# Graph Report - agent-ops-kit  (2026-10-21)

## Corpus Check
- 11 files · ~4,963 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 2)

## Summary
- 79 nodes · 81 edges · 10 communities (8 shown, 2 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- scrub.py
- plugin.json
- Agent Ops Kit
- Security policy
- Evidence gate
- Scrub before share
- Two variants, one source
- release-auditor.md

## God Nodes (most connected - your core abstractions)
1. `Agent Ops Kit` - 8 edges
2. `load_patterns()` - 6 edges
3. `main()` - 6 edges
4. `Evidence gate` - 6 edges
5. `Scrub before share` - 6 edges
6. `Two variants, one source` - 6 edges
7. `Security policy` - 5 edges
8. `scan_text()` - 4 edges
9. `scan()` - 4 edges
10. `What you get` - 4 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Communities (10 total, 2 thin omitted)

### Community 0 - "scrub.py"
Cohesion: 0.20
Nodes (6): load_patterns(), main(), mask(), scan(), scan_text(), walk()

### Community 1 - "plugin.json"
Cohesion: 0.12
Nodes (15): agents, author, name, url, commands, description, displayName, homepage (+7 more)

### Community 2 - "Agent Ops Kit"
Cohesion: 0.17
Nodes (12): Agent, Agent Ops Kit, Commands, Install, License, Limits, Skills, Test it before you trust it (+4 more)

### Community 3 - "Security policy"
Cohesion: 0.29
Nodes (5): Handling your deny list, If a credential leaks, Reporting a vulnerability, Security policy, What this tool does and does not protect

### Community 4 - "Evidence gate"
Cohesion: 0.29
Nodes (6): Evidence gate, Give yourself a check you can run, Reporting, The rule, What counts, What does not count as evidence

### Community 5 - "Scrub before share"
Cohesion: 0.29
Nodes (6): Before publishing, Run the scrubber, Scrub before share, Two groups, two jobs, What people forget, When the scrubber fires

### Community 6 - "Two variants, one source"
Cohesion: 0.29
Nodes (6): Build, Choosing public values, Rules that make it work, The shape, Two variants, one source, Verify before you trust it

### Community 7 - "release-auditor.md"
Cohesion: 0.50
Nodes (3): Boundaries, Method, Report

## Knowledge Gaps
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Agent Ops Kit` connect `Agent Ops Kit` to `Security policy`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Should `plugin.json` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._