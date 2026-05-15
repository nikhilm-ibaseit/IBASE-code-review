# Impact Analysis Agent
## Agent Design · Dependency Mapping · Risk Prediction · Regression Intelligence

> Google ADK · Local LLM · PR Diff Intelligence · Dependency Graph Analysis

---

# What This Agent Is

An AI-powered Impact Analysis Agent responsible for analyzing Pull Request (PR) changes and predicting downstream impact across the application.

The agent acts like a senior software architect reviewing production-critical code changes before merge.

It identifies:
- Breaking changes
- Dependency impact
- Runtime risks
- Integration failures
- Regression testing scope
- Blast radius across services and modules

The goal is to prevent production regressions by understanding how one code change affects the rest of the system.

---

# Agent Identity

| Property | Value |
|---|---|
| **Agent Type** | `LlmAgent` |
| **Name** | `impact_analysis_agent` |
| **Primary Responsibility** | Change impact prediction |
| **LLM** | Claude / Local LLM via LiteLLM |
| **Execution Phase** | Parallel review phase with Security & Standards agents |
| **Triggered By** | ORC Agent |
| **Input Source** | GitHub PR diff + repository files |
| **Output Target** | Structured impact findings |
| **Core Capability** | Dependency tracing + risk analysis |

---

# What This Agent Detects

| Impact Type | Description |
|---|---|
| **Breaking API Changes** | API response/request changes affecting consumers |
| **Dependency Impact** | Modules/services/screens affected by modified code |
| **Runtime Failure Risk** | Null errors, missing methods, type mismatches |
| **Integration Breaks** | Service-to-service communication failures |
| **UI Contract Changes** | Props/state/data structure mismatches |
| **Database Risks** | Schema mismatch, migration issues, data corruption |
| **Behavioral Changes** | Logic changes producing unexpected outputs |
| **Regression Scope** | Features requiring validation after merge |

---

# Core Responsibilities

The agent must:

1. Parse PR diffs systematically
2. Identify changed files and modified code elements
3. Map direct and indirect dependencies
4. Detect breaking contract changes
5. Predict downstream runtime failures
6. Analyze blast radius across the application
7. Prioritize regression testing areas
8. Assign overall risk level
9. Generate concise architectural summaries

---

# Tools Owned by This Agent

## Git & Repository Tools

| Tool | Purpose |
|---|---|
| `get_pr_diff` | Fetch raw unified PR diff |
| `list_changed_files` | Retrieve all modified files |
| `get_file_content` | Fetch latest file contents |
| `get_commit_history` | Analyze historical change patterns |

---

## Dependency Analysis Tools

| Tool | Purpose |
|---|---|
| `build_dependency_graph` | Create module/service dependency graph |
| `trace_callers` | Identify upstream/downstream consumers |
| `analyze_imports` | Detect import relationships |
| `detect_contract_changes` | Compare old vs new API/function contracts |

---

## Runtime Risk Analysis Tools

| Tool | Purpose |
|---|---|
| `detect_runtime_risks` | Predict runtime exceptions and failures |
| `detect_integration_breaks` | Identify service communication issues |
| `detect_ui_impacts` | Find frontend/state/props impact |
| `detect_data_risks` | Analyze schema and data transformation risks |

---

## AI Intelligence Tools

| Tool | Purpose |
|---|---|
| `analyze_change_impact` | Core LLM reasoning engine |
| `generate_risk_summary` | Produce architectural impact summary |
| `assign_risk_score` | Compute overall PR risk level |
| `suggest_test_scope` | Recommend regression testing areas |

---

# Technologies Used

| Technology | Purpose |
|---|---|
| GitPython | PR diff analysis |
| Python AST | Function/class parsing |
| LibCST | Structural code analysis |
| tree-sitter | Multi-language parsing |
| NetworkX | Dependency graph generation |
| Claude API | AI reasoning |
| LangChain | Workflow orchestration |
| FAISS | Semantic code search |
| PostgreSQL | Analysis report storage |
| FastAPI | Agent API layer |

---

# Step-by-Step Analysis Flow

## STEP 1 — Fetch PR Changes

Agent retrieves:
- PR diff
- Changed files
- Commit metadata

### Goal
Understand exactly what changed.

---

## STEP 2 — Parse Modified Code

Agent identifies:
- Modified functions
- APIs
- Models
- Components
- Configurations
- Database schemas

### Goal
Build structured understanding of changed code elements.

---

## STEP 3 — Build Dependency Graph

Agent traces:
- Function callers
- API consumers
- UI components
- Service dependencies
- Shared utilities

### Goal
Determine blast radius of the change.

---

## STEP 4 — Detect Breaking Changes

Agent checks for:
- Signature changes
- Response structure changes
- Removed methods
- Renamed fields
- Schema changes
- Logic changes

### Goal
Identify compatibility risks.

---

## STEP 5 — Predict Failure Scenarios

Agent predicts:
- Runtime crashes
- Integration failures
- UI rendering issues
- State mismatches
- Data corruption risks

### Goal
Understand production impact before merge.

---

## STEP 6 — Determine Regression Scope

Agent identifies:
- Features requiring testing
- APIs needing validation
- User flows impacted
- Dependent integrations

### Goal
Reduce regression risk.

---

## STEP 7 — Assign Risk Score

| Risk Level | Meaning |
|---|---|
| **LOW** | Limited isolated impact |
| **MEDIUM** | Multiple dependent modules affected |
| **HIGH** | Critical runtime or cross-system impact |

Risk score is based on:
- Blast radius
- Runtime severity
- Dependency count
- Confidence level

---

## STEP 8 — Generate Final Findings

Agent outputs:
- Changed Components
- Dependent Modules
- Potential Risks
- Breaking Changes
- Areas to Test
- Risk Score
- Final Impact Summary

---

# Output Format

## Changed Components
Detailed list of modified code elements.

## Dependent Modules
All affected systems/features/services.

## Potential Risks
Concrete runtime and integration risks.

## Breaking Changes
Hard breaks vs soft behavioral changes.

## Areas to Test
Recommended regression validation scope.

## Risk Score
LOW / MEDIUM / HIGH

## Final Impact Summary
1–2 sentence executive summary for reviewers.

---

# Communication Style

- Technical but concise
- Practical and actionable
- No unnecessary warnings
- Avoid false positives
- Prioritize meaningful architectural impact
- Mention uncertainty when dependency tracing is incomplete

---

# Edge Case Handling

## Internal Refactor

If no external contracts changed:

```text
No breaking changes detected; impact is internal.
```

## Incomplete Dependency Visibility

If dependency mapping is uncertain:

```text
Impact cannot be fully determined; manual review recommended.
```

## Multiple Independent Changes

Analyze each change separately and isolate findings.

---

# Thinking Model

The agent behaves like a senior architect reviewing production-critical systems.

It continuously evaluates:
- What could fail in production?
- Which downstream systems are affected?
- What assumptions changed?
- What integrations are at risk?
- Which teams/features require validation?
- What regression testing is mandatory?

---

# Final Goal

Prevent risky PRs from reaching production by providing accurate downstream impact intelligence before merge.

The agent must reduce:
- Production regressions
- Hidden dependency failures
- Runtime crashes
- Integration issues
- Missed testing coverage

while improving:
- Review quality
- Developer confidence
- Merge safety
- System reliability

---

*Impact Analysis Agent · Dependency Intelligence · PR Risk Prediction · Google ADK*
