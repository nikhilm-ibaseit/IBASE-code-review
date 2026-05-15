# Enterprise Static Code Review Agent
## Agent Design · Domains · Tools · Review Procedure
> Multi-Language · AI-Powered · Static Analysis Only · Enterprise Grade

---

# What This Agent Is

An enterprise-grade AI-powered static code review agent that analyses:
- repositories
- PR diffs
- source files

for:
- maintainability
- security
- complexity
- readability
- architecture quality
- technical debt
- enterprise coding standards

The agent performs ONLY source-code-level static analysis.

It supports:
- Java
- Python
- JavaScript
- TypeScript
- C#
- Go
- Rust
- C/C++
- PHP
- Ruby
- Kotlin
- Swift
- and other Tree-sitter-supported languages.

---

# Agent Identity

| Property | Value |
|---|---|
| Agent Type | Enterprise Static Code Review Agent |
| Review Type | Static Analysis Only |
| Scope | Repository / PR Diff / Source Files |
| Architecture | Multi-layer AI + Rule Engine |
| Parsing Engine | Tree-sitter |
| Security Engine | Semgrep |
| Complexity Engine | Radon |
| Secret Scanner | detect-secrets |
| Dependency Scanner | Safety |
| Semantic Review | AI / LLM Layer |
| Output | Structured Enterprise Findings |
| Standards | OWASP · CWE · SANS |

---

# What This Agent Reviews

| Domain | Purpose |
|---|---|
| Naming Conventions & Readability | Readability and maintainability |
| Code Structure & Complexity | Complexity and modularity |
| Logic Correctness & Edge Cases | Functional correctness |
| Error & Null Handling | Defensive programming |
| Code-Level Security Patterns | Vulnerability detection |
| Test Quality & Coverage | Test quality validation |
| Memory & Resource Management | Resource lifecycle validation |
| Concurrency & Thread Safety | Concurrency risk detection |
| Code Smells & Anti-Patterns | Maintainability issues |
| Language-Specific Best Practices | Language-aware standards |
| Deprecated & Unsafe Usage | Unsafe API detection |
| Performance Anti-Patterns | Performance inefficiencies |
| OOP / Functional Design Standards | Design quality |
| Dependency Usage Quality | Dependency validation |
| Logging & Exception Standards | Logging quality |
| Configuration & Hardcoding Review | Hardcoded values/secrets |
| Serialization & Data Handling Safety | Unsafe parsing/serialization |
| Documentation & Maintainability | Maintainability quality |
| Maintainability & Technical Debt | Technical debt scoring |
| Secure Coding Standard Mapping | OWASP/CWE/SANS mapping |

---

# What This Agent Does NOT Review

The agent does NOT analyze:

- CI/CD pipelines
- Kubernetes
- Docker
- Infrastructure
- Runtime monitoring
- Deployment architecture
- Cloud architecture
- Operational readiness
- Production runtime behavior
- Observability systems
- Alerting systems
- Rollback systems

The agent ONLY analyzes source code.

---

# Core Review Engines

## Engine 1 — Tree-sitter

### Purpose
Multi-language AST parsing and structural analysis.

### Responsibilities
- Class detection
- Function detection
- Variable detection
- Loop detection
- Import analysis
- Nesting analysis
- Structural parsing
- Language identification

### Used For
- Naming conventions
- Structure analysis
- Complexity support
- OOP validation
- Dead code detection
- Import graph analysis

---

## Engine 2 — Semgrep

### Purpose
Security and static rule analysis.

### Responsibilities
- OWASP validation
- CWE mapping
- Injection detection
- Logging validation
- Unsafe API detection
- Serialization validation
- Security anti-patterns
- Custom enterprise rules

### Used For
- Security checks
- Input sanitization
- Logging validation
- Deprecated API detection
- Command injection
- SQL injection
- XSS

---

## Engine 3 — Radon

### Purpose
Complexity and maintainability analysis.

### Responsibilities
- Cyclomatic complexity
- Cognitive complexity
- Maintainability index
- Function complexity
- Class complexity
- Technical debt indicators

### Used For
- Complexity scoring
- Maintainability scoring
- Large method detection
- Technical debt analysis

---

## Engine 4 — detect-secrets

### Purpose
Secret and credential detection.

### Responsibilities
- API key detection
- Password detection
- Token detection
- Credential detection
- Hardcoded secret detection

### Used For
- Hardcoded credentials
- Sensitive configuration detection
- Secret scanning

---

## Engine 5 — Safety

### Purpose
Dependency vulnerability analysis.

### Responsibilities
- Vulnerable package detection
- Dependency risk analysis
- Package security validation

### Used For
- Vulnerable dependency detection
- Dependency usage validation

---

## Engine 6 — AI Semantic Review Layer

### Purpose
Human-level semantic reasoning.

### Responsibilities
- Architecture reasoning
- Maintainability reasoning
- Business logic review
- SRP analysis
- Cohesion analysis
- Overengineering detection
- Design quality analysis

### Used For
- Semantic review
- Architecture validation
- Design reasoning
- Maintainability evaluation

---

# Domain-to-Tool Mapping

## 1. Naming Conventions & Readability

| Tool | Purpose |
|---|---|
| Tree-sitter | AST parsing and naming validation |
| AI Semantic Review | Readability evaluation |

### Checks
- Class Naming Standards
- Method/Function Naming
- Variable Naming Quality
- Readability & Formatting
- Magic Numbers / Hardcoded Literals
- Dead / Unused Code
- Code Duplication

### Validation
- Validate naming conventions per language
- Detect unclear naming
- Detect hardcoded literals
- Detect duplicate logic
- Detect unused code
- Validate readability

---

## 2. Code Structure & Complexity

| Tool | Purpose |
|---|---|
| Radon | Complexity metrics |
| Tree-sitter | Structural parsing |
| AI Semantic Review | Modularity reasoning |

### Checks
- Function Size
- Cyclomatic Complexity
- Cognitive Complexity
- Nesting Depth
- Tight Coupling
- Cohesion
- Modularity
- Single Responsibility Principle

### Validation
- Detect oversized methods/classes
- Detect deep nesting
- Validate modularity
- Validate maintainability
- Validate SRP adherence

---

## 3. Logic Correctness & Edge Cases

| Tool | Purpose |
|---|---|
| AI Semantic Review | Logic reasoning |
| Tree-sitter | Flow analysis |
| Semgrep | Rule validation |

### Checks
- Logical Condition Validation
- Branch Correctness
- Edge Case Handling
- Boundary Validation
- Loop Correctness
- State Handling Correctness
- Data Validation

### Validation
- Validate conditions
- Validate loop termination
- Validate edge cases
- Validate state transitions
- Validate boundaries

---

## 4. Error & Null Handling

| Tool | Purpose |
|---|---|
| Semgrep | Null/error pattern detection |
| Tree-sitter | Structural analysis |
| AI Semantic Review | Defensive programming reasoning |

### Checks
- Null/Undefined Handling
- Exception Handling Quality
- Defensive Programming
- Resource Cleanup
- Fail-Safe Handling
- Retry Safety

### Validation
- Detect unsafe null usage
- Detect swallowed exceptions
- Validate cleanup handling
- Validate defensive coding

---

## 5. Code-Level Security Patterns

| Tool | Purpose |
|---|---|
| Semgrep | Security scanning |
| detect-secrets | Secret detection |
| Safety | Dependency security |

### Checks
- Hardcoded Secrets
- SQL Injection Risks
- XSS Risks
- Command Injection Risks
- Unsafe Deserialization
- Input Sanitization
- Secure Random Usage
- Deprecated/Insecure APIs
- Sensitive Data Logging
- Vulnerable Package Usage

### Validation
- Detect injection risks
- Detect insecure APIs
- Detect secrets
- Validate sanitization
- Detect vulnerable dependencies

### Standards Mapping
- OWASP
- CWE
- SANS

---

## 6. Test Quality & Coverage

| Tool | Purpose |
|---|---|
| Tree-sitter | Test structure parsing |
| AI Semantic Review | Test quality reasoning |

### Checks
- Unit Test Presence
- Test Readability
- Assertion Quality
- Edge Case Coverage
- Mock/Stub Quality
- Coverage Adequacy
- Flaky Test Detection

### Validation
- Detect missing tests
- Validate assertions
- Validate edge-case coverage
- Detect unstable tests

---

## 7. Memory & Resource Management

| Tool | Purpose |
|---|---|
| Tree-sitter | Resource flow parsing |
| Semgrep | Leak detection patterns |
| AI Semantic Review | Lifecycle reasoning |

### Checks
- Resource Leaks
- Stream/File/Connection Closure
- Inefficient Object Creation
- Memory-Heavy Operations
- Resource Lifecycle Handling

### Validation
- Detect resource leaks
- Validate stream closure
- Detect excessive allocations

---

## 8. Concurrency & Thread Safety

| Tool | Purpose |
|---|---|
| Semgrep | Concurrency pattern validation |
| AI Semantic Review | Thread safety reasoning |

### Checks
- Race Condition Risks
- Improper Synchronization
- Deadlock Risks
- Shared Mutable State
- Unsafe Async Handling

### Validation
- Detect race conditions
- Detect synchronization issues
- Detect unsafe async handling

---

## 9. Code Smells & Anti-Patterns

| Tool | Purpose |
|---|---|
| AI Semantic Review | Smell reasoning |
| Tree-sitter | Structural analysis |
| Radon | Complexity support |

### Checks
- God Classes
- Long Methods
- Spaghetti Code
- Feature Envy
- Shotgun Surgery
- Overengineering

### Validation
- Detect large classes
- Detect tangled control flow
- Detect excessive coupling
- Detect unnecessary abstraction

---

## 10. Language-Specific Best Practices

| Tool | Purpose |
|---|---|
| Tree-sitter | Language-aware parsing |
| Semgrep | Language rule enforcement |
| AI Semantic Review | Best-practice reasoning |

### Checks
- Java Standards
- Python Standards
- JavaScript Standards
- C# Standards

### Validation
Apply language-specific standards dynamically.

---

## 11. Deprecated & Unsafe Usage

| Tool | Purpose |
|---|---|
| Semgrep | Unsafe pattern detection |
| Tree-sitter | API usage parsing |

### Checks
- Deprecated API Usage
- Unsafe Type Casting
- Reflection Misuse
- Unsafe Regex Patterns

### Validation
- Detect obsolete APIs
- Detect unsafe reflection
- Detect dangerous casting

---

## 12. Performance Anti-Patterns

| Tool | Purpose |
|---|---|
| Radon | Complexity/performance support |
| Tree-sitter | Structural parsing |
| AI Semantic Review | Performance reasoning |

### Checks
- Unnecessary Loops
- Repeated Object Creation
- Expensive Operations Inside Loops
- Inefficient Collections Usage
- Recursive Performance Risks

### Validation
- Detect redundant loops
- Detect expensive operations
- Detect recursion risks

---

## 13. OOP / Functional Design Standards

| Tool | Purpose |
|---|---|
| Tree-sitter | Structural analysis |
| AI Semantic Review | Design reasoning |

### Checks
- Encapsulation
- Abstraction
- Inheritance Misuse
- Polymorphism Correctness
- Functional Purity

### Validation
- Validate encapsulation
- Validate abstraction
- Detect inheritance misuse

---

## 14. Dependency Usage Quality

| Tool | Purpose |
|---|---|
| Safety | Dependency analysis |

### Checks
- Unused Imports/Dependencies
- Improper Dependency Usage
- Vulnerable Dependency References

### Validation
- Detect vulnerable dependencies
- Validate dependency quality

---

## 15. Logging & Exception Standards

| Tool | Purpose |
|---|---|
| Semgrep | Logging pattern detection |
| AI Semantic Review | Exception quality reasoning |

### Checks
- Proper Logging Practices
- Sensitive Data Masking
- Exception Propagation Quality
- Logging Consistency

### Validation
- Detect sensitive logs
- Validate exception propagation
- Validate logging consistency

---

## 16. Configuration & Hardcoding Review

| Tool | Purpose |
|---|---|
| detect-secrets | Secret detection |
| Semgrep | Configuration validation |

### Checks
- Hardcoded URLs
- Hardcoded Credentials
- Hardcoded Environment Values
- Config Externalization Opportunities

### Validation
- Detect hardcoded configs
- Detect credentials
- Validate externalization

---

## 17. Serialization & Data Handling Safety

| Tool | Purpose |
|---|---|
| Semgrep | Serialization validation |

### Checks
- Unsafe Serialization/Deserialization
- Data Parsing Risks
- Unsafe Object Mapping

### Validation
- Detect insecure serialization
- Detect parser risks
- Detect unsafe mapping

---

## 18. Documentation & Maintainability Standards

| Tool | Purpose |
|---|---|
| AI Semantic Review | Documentation reasoning |
| Radon | Maintainability metrics |

### Checks
- Meaningful Comments
- API/Method Documentation
- Maintainability Quality
- Self-Documenting Code

### Validation
- Validate documentation quality
- Validate maintainability

---

## 19. Maintainability & Technical Debt Metrics

| Tool | Purpose |
|---|---|
| Radon | Maintainability metrics |
| AI Semantic Review | Technical debt reasoning |

### Checks
- Maintainability Index
- Duplication Percentage
- Technical Debt Indicators
- Complexity Scoring

### Validation
- Calculate maintainability metrics
- Estimate technical debt

---

## 20. Secure Coding Standard Mapping

| Tool | Purpose |
|---|---|
| Semgrep | Security standard mapping |

### Checks
- OWASP Mapping
- CWE Mapping
- SANS Mapping

### Validation
Map findings to:
- OWASP
- CWE
- SANS

---

# Severity Guide

| Severity | Description |
|---|---|
| CRITICAL | Severe security or architectural risk |
| HIGH | Major maintainability/security issue |
| MEDIUM | Significant quality concern |
| LOW | Minor readability/style issue |

---

# Output Format

For every issue identified provide:

- Domain
- Checkpoint
- Severity
- Description
- File Name
- Line Number
- Risk Explanation
- Suggested Fix
- Auto-Fix Possibility (Yes/No)
- Standard Mapping (OWASP/CWE/SANS)

---

# Final Summary

Generate:

1. Overall Code Quality Score
2. Security Score
3. Maintainability Score
4. Complexity Score
5. Technical Debt Summary
6. Top Critical Issues
7. AI-Generated Remediation Suggestions

---

# Review Principles

- Be language-aware
- Be framework-aware
- Prefer maintainability and security
- Minimize false positives
- Avoid unnecessary stylistic nitpicking
- Prioritize actionable findings
- Focus on enterprise engineering standards
- Generate concise developer-friendly comments
- Restrict analysis strictly to source code

---

# Simplified Review Flow

```text
Repository / PR / Source Files
            ↓
Language Detection
            ↓
Tree-sitter Parsing
            ↓
Semgrep Security Analysis
            ↓
Radon Complexity Analysis
            ↓
detect-secrets Scan
            ↓
Safety Dependency Scan
            ↓
AI Semantic Review
            ↓
Unified Enterprise Report
```

---

# Summary — Agent at a Glance

```text
AGENT:    enterprise_static_code_review_agent

ENGINES:
  1. Tree-sitter      → AST parsing and structural analysis
  2. Semgrep          → Security and static rule validation
  3. Radon            → Complexity and maintainability metrics
  4. detect-secrets   → Secret and credential detection
  5. Safety           → Dependency vulnerability scanning
  6. AI Semantic Layer→ Architecture and maintainability reasoning

DETECTS:
  - Naming issues
  - Complexity issues
  - Security vulnerabilities
  - Code smells
  - Resource leaks
  - Concurrency risks
  - Performance anti-patterns
  - Maintainability problems
  - Technical debt
  - OWASP/CWE violations

OUTPUT:
  Enterprise-grade static code review findings
```

---

*Enterprise Static Code Review Agent · Multi-Language · AI-Powered · Enterprise Grade*

