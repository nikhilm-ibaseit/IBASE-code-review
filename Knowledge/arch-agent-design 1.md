# Architecture Pattern Analyser Agent
## Agent Design · Tools · Actions · Step-by-Step Procedure
> Google ADK · Local LLM · mem0 · No code / No pseudo code

---

## What This Agent Is

A **Google ADK LlmAgent** that analyses a GitHub PR diff for architectural violations.
It is the only agent in the system with **persistent memory across PR runs**.
It autonomously decides whether to do a full codebase discovery or an incremental diff-only analysis — based on what it finds in mem0.

---

## Agent Identity

| Property | Value |
|---|---|
| **ADK Type** | `LlmAgent` |
| **Name** | `arch_pattern_agent` |
| **LLM** | Local model via LiteLLM (Ollama-compatible) |
| **Memory** | mem0 OSS — local Qdrant + Ollama embeddings |
| **Runs in** | Phase 2 — parallel with Security, Impact, Standards agents |
| **Triggered by** | ORC Agent via ADK ParallelAgent |
| **Reads from** | GitHub directly via its own git tools + mem0 |
| **Writes to** | ADK session state → `findings` list |
| **Git tools owned** | `get_pr_diff`, `get_file_content`, `list_changed_files` |

---

## What Violations It Detects

| Violation Type | What It Means |
|---|---|
| **Layering violation** | Code crosses architectural layer boundaries in the wrong direction — e.g. database query inside a route handler, HTTP call inside a model class |
| **God class / god module** | A class or module has grown to do too many things — too many methods spanning multiple concerns, or a utility file imported by too many others |
| **Circular dependency** | File A imports B, B imports C, C imports A — a cycle introduced or extended by this PR |

---

## Memory Design (mem0)

### What gets stored per repo

- Inferred architecture style (e.g. "layered MVC", "clean architecture")
- Layer map — which file belongs to which layer
- Module roles — what each file/folder is responsible for
- Known patterns in use (Repository, DTO, Factory, etc.)
- Class and module sizes at last scan
- Import dependency graph snapshot
- History of past violations (titles only — for recurrence detection)

### How mem0 is used

- **Search** — at the start of every run, query mem0 with the repo name to retrieve stored architectural knowledge
- **Add** — after Discovery Mode, save the full inferred architecture as a mem0 memory scoped to the repo
- **Update** — after every PR analysis, append new violation history and updated class sizes
- **Scope** — `user_id = repo_full_name` (e.g. `"org/repo"`) so each repo has its own isolated memory

### mem0 configuration

- LLM provider: Ollama (same local model as the agent)
- Embedder: Ollama (`nomic-embed-text` or `bge-m3`)
- Vector store: local on-disk Qdrant (no server needed)
- No API key required — fully offline

---

## Tools This Agent Owns (8 tools)

### Git Tools (3) — owned directly, no separate Git Agent

---

### Tool 1 — `get_pr_diff`

**What it does:**
Fetches the raw unified diff for the PR from GitHub.
This is the primary input for violation analysis — every other analysis tool depends on it.
Called first, before any analysis begins.

**Input:** PR URL (from session state — passed by ORC on trigger)
**Output:** raw unified diff string
**Calls:** GitHub API via git action

---

### Tool 2 — `list_changed_files`

**What it does:**
Fetches the list of all files changed in the PR — with change type (added / modified / deleted).
Used to know which files to fetch in full, and to scope the import graph and cycle detection to relevant files only.

**Input:** PR URL (from session state)
**Output:** list of changed file paths with change types
**Calls:** GitHub API via git action

---

### Tool 3 — `get_file_content`

**What it does:**
Fetches the full content of a specific file at HEAD.
Called for each changed file and their immediate import neighbours.
In Discovery Mode — called for all repo files to build a complete picture.
In Incremental Mode — called only for changed files + files they import.

**Input:** repo name + file path + ref (HEAD SHA from PR)
**Output:** full file content as string
**Calls:** GitHub API via git action

---

### Analysis Tools (5) — owned by this agent

---

### Tool 4 — `check_knowledge_exists`

**What it does:**
Searches mem0 for any stored architectural knowledge about this specific repo.
This is the decision gate — the result determines which mode the agent runs in.
Called after git tools have fetched the diff and file list.

**Input:** repo full name
**Output:** `true` (knowledge found — Incremental Mode) or `false` (no knowledge — Discovery Mode)
**Calls:** mem0 `search()` scoped to repo

---

### Tool 5 — `infer_architecture`

**What it does:**
Used in **Discovery Mode only**.
Sends all fetched file contents to the local LLM to analyse the entire codebase structure.
LLM infers: architecture style, layer boundaries, module responsibilities, patterns in use, class sizes, and import dependency structure.
Result is saved to mem0 automatically via the `after_run` lifecycle hook — not a tool call.

**Input:** all file contents fetched via Tool 3
**Output:** structured ArchKnowledge — layer map, module roles, inferred style, patterns, class sizes
**Calls:** local LLM with full file contents + architecture inference prompt

---

### Tool 6 — `build_import_graph`

**What it does:**
Parses import statements from the fetched file contents.
Builds a directed graph of who imports whom.
Pure logic — no LLM call.
In Discovery Mode: built from all fetched files.
In Incremental Mode: built from changed files + their immediate neighbours only.

**Input:** fetched file contents (from Tool 3)
**Output:** directed import graph — file → list of files it imports
**Calls:** nothing external — pure parsing logic

---

### Tool 7 — `detect_cycles`

**What it does:**
Runs depth-first search on the import graph.
Finds circular dependency chains.
Only reports cycles that touch at least one changed file — avoids flagging pre-existing cycles the PR didn't introduce.

**Input:** import graph from Tool 6 + changed file list from Tool 2
**Output:** list of cycles — each cycle is the full chain of files involved
**Calls:** nothing external — pure graph traversal

---

### Tool 8 — `analyse_arch_violations`

**What it does:**
The core intelligence of the agent.
Takes the PR diff, recalled architectural knowledge from mem0, the predefined ruleset, and detected cycles.
Asks the local LLM to find all three violation types: layering, god class, circular deps.
Returns one structured finding per violation found.

**Input:**
- PR diff from Tool 1
- Recalled knowledge from mem0 (injected by `before_run` hook)
- Architecture ruleset (predefined — in system prompt)
- Cycle list from Tool 7

**Output:** list of ArchFinding — each with file, line, severity, category, explanation, suggestion
**Calls:** local LLM with diff + knowledge + ruleset as context

---

## Lifecycle Hooks (not tools — always run automatically)

### `before_run`
- Reads `repo` from session state
- Calls mem0 `search()` to retrieve stored architectural knowledge
- Injects recalled knowledge into session state so tools can access it
- Agent does not decide this — it always happens before any tool is called

### `after_run`
- Reads findings produced by the agent
- Calls mem0 `add()` to append violation history and updated class sizes
- Keeps memory fresh without a full re-scan next time
- Agent does not decide this — it always happens after the agent finishes

---

## Step-by-Step Procedure

### Every Run — Regardless of Mode

```
STEP 1 — before_run hook fires (automatic)
         mem0.search("architecture knowledge", user_id=repo)
         → recalled knowledge injected into agent context
         → if nothing found, recalled knowledge is empty string
```

```
STEP 2 — Agent calls: get_pr_diff(pr_url)
         → fetches raw unified diff from GitHub
         → diff stored for use by analyse_arch_violations later
```

```
STEP 3 — Agent calls: list_changed_files(pr_url)
         → fetches list of all changed file paths + change types
         → used to know which files to fetch and to scope cycle detection
```

```
STEP 4 — Agent calls: check_knowledge_exists(repo)
         → queries mem0 result from STEP 1
         → if result has content → INCREMENTAL MODE
         → if result is empty   → DISCOVERY MODE
```

---

### Discovery Mode (first run on this repo)

```
STEP 5a — Agent calls: get_file_content() for ALL repo files
           → fetches full content of every file in the repo
           → this is the expensive step — only runs once per repo ever
           → files collected into a dict: path → content
```

```
STEP 6a — Agent calls: infer_architecture(all_file_contents)
           → sends all file contents to local LLM
           → LLM produces:
               - architecture style label (e.g. "layered MVC")
               - layer map: which file belongs to which layer
               - module roles: what each file is responsible for
               - known patterns in use (Repository, DTO, etc.)
               - class sizes: class name → method count
           → result will be saved to mem0 by after_run hook automatically
```

```
STEP 7a — Agent calls: build_import_graph(all_file_contents)
           → parses ALL import statements across all fetched files
           → builds full directed import graph for the repo
```

```
STEP 8a — Agent calls: detect_cycles(full_graph, changed_files)
           → DFS on full import graph
           → returns only cycles that touch at least one changed file
```

```
STEP 9a — Agent calls: analyse_arch_violations(diff, inferred_knowledge, ruleset, cycles)
           → diff from STEP 2
           → inferred_knowledge from STEP 6a
           → ruleset from system prompt
           → cycles from STEP 8a
           → local LLM checks all three violation types:
               LAYERING   — does diff introduce cross-layer imports or calls?
               GOD CLASS  — does diff grow a class/module beyond single responsibility?
               CIRCULAR   — are any detected cycles architecturally harmful?
           → returns list of ArchFinding
```

---

### Incremental Mode (knowledge already in mem0)

```
STEP 5b — Agent calls: get_file_content() for changed files + their import neighbours ONLY
           → much smaller fetch than Discovery Mode
           → import neighbours = files that changed files import from
```

```
STEP 6b — No infer_architecture call
           → recalled knowledge from mem0 (STEP 1) is used directly
           → layer map, module roles, patterns already known
```

```
STEP 7b — Agent calls: build_import_graph(changed_files_contents + neighbours)
           → parses import statements from changed files + their neighbours only
           → builds partial import graph — faster than full repo scan
```

```
STEP 8b — Agent calls: detect_cycles(partial_graph, changed_files)
           → DFS on partial graph
           → returns cycles touching changed files
```

```
STEP 9b — Agent calls: analyse_arch_violations(diff, recalled_knowledge, ruleset, cycles)
           → same as STEP 9a but recalled_knowledge comes from mem0
           → LLM compares diff against stored architectural understanding
           → returns list of ArchFinding
```

---

### Final Steps — Both Modes

```
STEP 10 — Agent appends findings to session_state["findings"]
          → ORC Agent reads this along with Security + Impact findings
          → Comment Agent formats and posts all findings to GitHub PR
```

```
STEP 11 — after_run hook fires (automatic)
          mem0.add(violation_history + updated_class_sizes, user_id=repo)
          → new violation titles appended to repo memory
          → updated class sizes saved if god class findings were produced
          → inferred architecture saved if this was Discovery Mode
          → memory stays fresh for next PR — no full re-scan needed
```

---

## Decision Logic — Discovery vs Incremental

```
Agent triggered by ORC (PR URL in session state)
         ↓
before_run: mem0.search(repo) → recalled knowledge
         ↓
get_pr_diff(pr_url)          → raw diff
list_changed_files(pr_url)   → changed file paths
         ↓
check_knowledge_exists(repo)
         ↓
    recalled empty?
    ┌── YES — DISCOVERY ──────────────────── NO — INCREMENTAL ──┐
    │                                                             │
    │  get_file_content() ALL repo files    get_file_content()   │
    │                                       changed + neighbours  │
    │  infer_architecture()                 (skip infer)         │
    │  → saves to mem0 via after_run        use recalled memory  │
    │                                                             │
    │  build_import_graph (full)            build_import_graph   │
    │                                       (partial)            │
    └──────────────────────────────────────────────────────────--┘
         ↓                                          ↓
    detect_cycles(graph, changed_files)    detect_cycles(graph, changed_files)
         ↓                                          ↓
    analyse_arch_violations()             analyse_arch_violations()
         ↓                                          ↓
    append to session_state.findings      append to session_state.findings
         ↓                                          ↓
    after_run: mem0.add(arch + violations) after_run: mem0.add(violations)
```

---

## Architecture Ruleset (injected into system prompt)

Five rules passed as context on every `analyse_arch_violations` call:

| Rule | Description |
|---|---|
| **Layer Integrity** | Dependencies flow inward only. Higher layers call lower layers. Lower layers must never import higher layers. |
| **Single Responsibility** | A class with more than one primary concern is a violation. Flag classes growing beyond 10 methods across multiple domains. |
| **No Circular Dependencies** | No file may transitively import itself through any chain. Flag any cycle introduced or extended by the diff. |
| **Pattern Consistency** | If the codebase uses a pattern (Repository, DTO, Factory), all new code must follow it. Flag deviations. |
| **Boundary Enforcement** | Infrastructure concerns (DB, HTTP, filesystem) must not appear in domain/business logic layers. |

---

## Severity Guide

| Severity | When to use |
|---|---|
| **CRITICAL** | Breaks the core architectural contract — e.g. data layer imports presentation layer |
| **HIGH** | Introduces a new cycle, or significant god class growth spanning 3+ concerns |
| **MED** | Pattern inconsistency, growing god class, minor layer blur |
| **LOW** | Small style deviation, utility file gaining one more importer |

---

## What This Agent Does NOT Do

- Does not rely on any other agent to fetch data — it fetches its own diff and files via git tools
- Does not post comments — Comment Agent handles all posting
- Does not track security issues — Security Agent's job
- Does not compute blast radius — Impact Agent's job
- Does not enforce a specific named architecture — infers and enforces the repo's own style
- Does not re-scan the full repo on every PR — only on first run or forced reset

---

## Summary — Agent at a Glance

```
AGENT:    arch_pattern_agent  (Google ADK LlmAgent)
LLM:      local model via LiteLLM / Ollama
MEMORY:   mem0 OSS — local Qdrant + Ollama embeddings — scoped per repo

GIT TOOLS (3) — agent fetches its own data:
  1. get_pr_diff              → fetch raw unified diff from GitHub
  2. list_changed_files       → fetch list of changed file paths
  3. get_file_content         → fetch full file content per path

ANALYSIS TOOLS (5):
  4. check_knowledge_exists   → gate: discovery or incremental?
  5. infer_architecture       → discovery only: full repo LLM analysis
  6. build_import_graph       → pure logic: parse imports → directed graph
  7. detect_cycles            → pure logic: DFS → find harmful cycles
  8. analyse_arch_violations  → core LLM call: diff + memory + ruleset → findings

HOOKS (2, automatic — not tools):
  before_run  → mem0.search → inject recalled knowledge into agent context
  after_run   → mem0.add   → save architecture + violation history + class sizes

DETECTS:
  - Layering violations
  - God class / god module growth
  - Circular dependencies

OUTPUT:
  list[ArchFinding] appended to session_state["findings"]
  Each finding: file · line · severity · category · explanation · suggestion
```

---

*Architecture Pattern Analyser · Google ADK · Local LLM · mem0 OSS*
