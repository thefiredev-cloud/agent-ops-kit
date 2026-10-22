# Graph Report - agent-ops-kit  (2026-10-21)

## Corpus Check
- 14 files · ~190,520 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 10 file(s) not represented in the graph (top: .mmd 8, (none) 2)

## Summary
- 113 nodes · 128 edges · 10 communities
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 6 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- scrub.py
- plugin.json
- ARCHITECTURE.md
- Agent Ops Kit
- Agent Ops Kit: architecture
- Communities (10 total, 2 thin omitted)
- Graph Report - agent-ops-kit  (2026-10-21)
- Evidence gate
- Scrub before share
- Two variants, one source

## God Nodes (most connected - your core abstractions)
1. `Agent Ops Kit: architecture` - 11 edges
2. `Graph Report - agent-ops-kit  (2026-10-21)` - 10 edges
3. `Agent Ops Kit` - 9 edges
4. `Communities (10 total, 2 thin omitted)` - 9 edges
5. `load_patterns()` - 8 edges
6. `main()` - 8 edges
7. `Evidence gate` - 6 edges
8. `Scrub before share` - 6 edges
9. `Two variants, one source` - 6 edges
10. `scan_text()` - 5 edges

## Surprising Connections (you probably didn't know these)
- `10. Evidence` --references--> `load_patterns()`  [INFERRED]
  docs/ARCHITECTURE.md → scripts/scrub.py
- `God Nodes (most connected - your core abstractions)` --references--> `load_patterns()`  [INFERRED]
  docs/architecture/graphify/GRAPH_REPORT.md → scripts/scrub.py
- `God Nodes (most connected - your core abstractions)` --references--> `scan_text()`  [INFERRED]
  docs/architecture/graphify/GRAPH_REPORT.md → scripts/scrub.py
- `God Nodes (most connected - your core abstractions)` --references--> `scan()`  [INFERRED]
  docs/architecture/graphify/GRAPH_REPORT.md → scripts/scrub.py
- `10. Evidence` --references--> `main()`  [INFERRED]
  docs/ARCHITECTURE.md → scripts/scrub.py

## Import Cycles
- None detected.

## Communities (10 total, 0 thin omitted)

### Community 0 - "scrub.py"
Cohesion: 0.19
Nodes (8): 10. Evidence, God Nodes (most connected - your core abstractions), load_patterns(), main(), mask(), scan(), scan_text(), walk()

### Community 1 - "plugin.json"
Cohesion: 0.12
Nodes (15): agents, author, name, url, commands, description, displayName, homepage (+7 more)

### Community 2 - "ARCHITECTURE.md"
Cohesion: 0.14
Nodes (8): Boundaries, Method, Report, Handling your deny list, If a credential leaks, Reporting a vulnerability, Security policy, What this tool does and does not protect

### Community 3 - "Agent Ops Kit"
Cohesion: 0.15
Nodes (13): Agent, Agent Ops Kit, Architecture, Commands, Install, License, Limits, Skills (+5 more)

### Community 4 - "Agent Ops Kit: architecture"
Cohesion: 0.17
Nodes (12): 1. Purpose, 2. Whiteboard view, 3. System context (C4 level 1), 4. Containers and components (C4 level 2), 5.1 /scrub-check before sharing a build, 5.2 /release-public stops before publishing, 5. Key runtime sequences, 6. Data flow and stores (+4 more)

### Community 5 - "Communities (10 total, 2 thin omitted)"
Cohesion: 0.22
Nodes (9): Communities (10 total, 2 thin omitted), Community 0 - "scrub.py", Community 1 - "plugin.json", Community 2 - "Agent Ops Kit", Community 3 - "Security policy", Community 4 - "Evidence gate", Community 5 - "Scrub before share", Community 6 - "Two variants, one source" (+1 more)

### Community 6 - "Graph Report - agent-ops-kit  (2026-10-21)"
Cohesion: 0.25
Nodes (8): Community Hubs (Navigation), Corpus Check, Graph Report - agent-ops-kit  (2026-10-21), Import Cycles, Knowledge Gaps, Suggested Questions, Summary, Surprising Connections (you probably didn't know these)

### Community 7 - "Evidence gate"
Cohesion: 0.29
Nodes (6): Evidence gate, Give yourself a check you can run, Reporting, The rule, What counts, What does not count as evidence

### Community 8 - "Scrub before share"
Cohesion: 0.29
Nodes (6): Before publishing, Run the scrubber, Scrub before share, Two groups, two jobs, What people forget, When the scrubber fires

### Community 9 - "Two variants, one source"
Cohesion: 0.29
Nodes (6): Build, Choosing public values, Rules that make it work, The shape, Two variants, one source, Verify before you trust it

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Graph Report - agent-ops-kit  (2026-10-21)` connect `Graph Report - agent-ops-kit  (2026-10-21)` to `scrub.py`, `ARCHITECTURE.md`, `Communities (10 total, 2 thin omitted)`?**
  _High betweenness centrality (0.287) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `load_patterns()` (e.g. with `10. Evidence` and `God Nodes (most connected - your core abstractions)`) actually correct?**
  _`load_patterns()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `plugin.json` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._
- **Why does `Agent Ops Kit: architecture` connect `Agent Ops Kit: architecture` to `scrub.py`, `ARCHITECTURE.md`?**
  _High betweenness centrality (0.241) - this node is a cross-community bridge._
- **Should `ARCHITECTURE.md` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._
- **Why does `Agent Ops Kit` connect `Agent Ops Kit` to `ARCHITECTURE.md`?**
  _High betweenness centrality (0.172) - this node is a cross-community bridge._