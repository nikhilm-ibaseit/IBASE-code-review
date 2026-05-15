TITLE Code Review Agent - Agent Design Tools Actions Step-by-Step Procedure --- Google ADK LlmAgent Python no code no pseudo code ---

TITLE Code Review Agent - What This Agent Is...
Property            | Value
--------------------|------
ADK Type            | LlmAgent
Name                | codereviewagent
LLM                 | gemini-flash-latest or equivalent fast review model
Memory              | none persistent, session-state only
Runs in             | Phase 1 as the primary entry point for PR review pipeline
Triggered by        | ORC Agent upon new PR event or manual review request
Reads from          | session state PR metadata, diff hunks, file list, language context
Writes to           | session state raw findings handed off to downstream analysis agents
Git tools owned     | none, consumes prepared diff and PR metadata
Parsing tools owned | none, consumes structured diff and file context
Output              | list of RawFinding objects each tied to file, line, category, severity, explanation, and suggestion

TITLE Code Review Agent - Agent Identity...
Field             | Value
------------------|------
Purpose           | Perform a structured first-pass review of pull request changes and surface candidate findings
Role in system    | Primary review layer, feeds structured findings to security, standards, architecture, and impact agents
Language support  | Language agnostic, compatible with Python, Java, JavaScript, Go, CSharp, and others
Primary focus     | Detecting code smells, logic issues, missing tests, readability problems, and obvious bugs
Non goals         | Does not perform deep security analysis, does not compute blast radius, does not post PR comments itself

TITLE Code Review Agent - What It Detects From Input...
Input Type                  | What It Means
----------------------------|------
Changed file diff hunk      | The modified lines of code submitted as part of the pull request
PR title and description    | Context for intent, linked issues, and scope of the change
File language metadata      | Programming language to guide review heuristics
Symbol and AST context      | Function, class, or module boundaries to understand scope of change
Test file presence flag     | Whether corresponding unit or integration tests exist for changed code
Prior finding context       | Existing known issues from the same file or module to avoid duplicates

TITLE Code Review Agent - Required Input Schema...
- repo_id               repository identifier
- pr_id                 pull request identifier
- file_path             exact path of changed file
- language              detected programming language
- diff_hunk             changed code snippet
- line_start            first affected line number
- line_end              last affected line number
- symbol_name           function, class, or module name if known
- node_type             AST node type if known
- pr_title              title of the pull request
- pr_description        body text of the pull request description
- has_tests             boolean indicating whether test files are included in the PR
- prior_findings        optional list of findings already recorded for this file

TITLE Code Review Agent - Output Schema...
- finding_id            unique id for the raw finding record
- file_path             target file path
- line_start            first affected line
- line_end              last affected line
- symbol_name           function, class, or module if resolved
- category              bug, smell, readability, missing_test, logic, performance, style
- severity              critical, high, medium, low
- summary               short one-line description of the finding
- evidence              the specific code snippet supporting the finding
- suggested_fix         recommended correction or improvement
- confidence            confidence score from 0.0 to 1.0
- source_agent          always codereviewagent
- needs_deep_analysis   boolean flag for whether downstream agents should inspect this finding further

TITLE Code Review Agent - Tools This Agent Owns 4 tools...
What it does    | Validates that the incoming PR payload follows the expected schema and contains all required fields
Used at         | Entry boundary before any analysis begins
Input           | structured PR diff payload
Output          | validation pass or field error list
Result          | prevents malformed or incomplete PR data from reaching the review pipeline

TITLE Code Review Agent - Tool 1 prschemachecker...
What it does    | Maps each diff hunk to a resolved file path and confirmed line span using the PR file manifest
Used after      | schema validation and before code analysis
Input           | file list, diff hunk, raw line numbers
Output          | confirmed file path and exact line range per hunk
Result          | ensures findings reference real changed lines and not stale or out-of-scope code

TITLE Code Review Agent - Tool 2 difflinemapper...
What it does    | Detects the programming language of each changed file and extracts relevant symbol context such as function or class boundaries
Used when       | the finding has file path and hunk but no language or symbol context yet
Input           | file path, diff hunk, language hint if available
Output          | confirmed language, symbol name, node type, and context window
Result          | enables language-aware review heuristics and improves finding precision

TITLE Code Review Agent - Tool 3 languagecontextdetector...
What it does    | Analyzes the mapped and language-resolved diff hunk and produces a list of raw candidate findings with category, severity, evidence, and suggestion
Used after      | location mapping and language detection and before output ranking
Input           | file path, language, diff hunk, symbol context, PR description
Output          | list of RawFinding candidates
Result          | produces the core review output ready for deduplication and downstream handoff

TITLE Code Review Agent - Tool 4 codeanalyzerfinder...
What it does    | Removes duplicate findings or merges nearby overlapping findings into a single record before output
Used after      | finding generation and before writing to session state
Input           | generated raw finding list
Output          | deduplicated and ranked finding list
Result          | keeps findings concise and reduces noise for downstream agents and reviewers

TITLE Code Review Agent - Lifecycle Hooks not tools always run automatically...
BEFORERUN
- Reads session state PR metadata and diff payload
- Loads file list and language context for the PR
- Initializes empty finding buffer
- Does not generate findings yet

AFTERRUN
- Writes final raw findings to session state for downstream agents
- Sets needs_deep_analysis flags for security, architecture, and impact agents
- No persistent memory required
- Does not update security knowledge or architecture knowledge bases

TITLE Code Review Agent - Step-by-Step Procedure...
STEP 1   ORC Agent triggers this agent when a new PR event arrives or a manual review is requested
STEP 2   Agent reads session state and receives PR metadata, diff hunks, and file context
STEP 3   prschemachecker validates required fields and rejects malformed or incomplete PR payloads
STEP 4   difflinemapper maps each diff hunk to its confirmed file path and exact changed line range
STEP 5   languagecontextdetector identifies the programming language and resolves symbol boundaries for each changed file
STEP 6   codeanalyzerfinder analyzes the mapped and language-resolved hunks and produces raw candidate findings
STEP 7   codeanalyzerfinder deduplicates repeated or overlapping findings within the same hunk or file
STEP 8   Agent ranks findings by severity and confidence score
STEP 9   Agent sets needs_deep_analysis flag on findings that require security, architecture, or impact agent review
STEP 10  Agent writes list of RawFinding objects to session state for downstream agents to consume
STEP 11  ORC Agent routes flagged findings to security, standards, architecture, and impact agents in parallel

TITLE Code Review Agent - Decision Logic...
Rule                        | Description
----------------------------|------
Must run first              | This agent runs before all downstream analysis agents as the primary review entry point
Must accept structured input| It should accept standardized PR diff payloads, not raw unprocessed webhook events
Must be language agnostic   | It should rely on metadata and detected language context, not hardcoded language-specific logic
Must be line precise        | Every finding must map to an exact file path and line number or range
Must be concise             | Findings should be short, actionable, and clearly categorized
Must avoid duplication      | Merge or suppress repeated issues appearing in the same hunk or file
Must flag for deep analysis | Findings with security, architecture, or blast-radius implications must set needs_deep_analysis true
Must preserve traceability  | Each finding must reference its source file, line, symbol, and evidence snippet

TITLE Code Review Agent - Severity Guide...
Severity | When to use
---------|------
CRITICAL | Issue is dangerous, incorrect, or blocking and must be fixed before merge
HIGH     | Issue is likely to cause failure, regression, or a significant design problem
MEDIUM   | Issue is important but not immediately blocking, should be addressed before merge
LOW      | Issue is minor, a style suggestion, or a readability improvement

TITLE Code Review Agent - Category Guide...
Category      | When to use
--------------|------
bug           | Definite or likely incorrect behavior, null reference, off-by-one, wrong condition
smell         | Design weakness, overly complex logic, or structural anti-pattern
readability   | Hard to understand code, poor naming, missing documentation
missing_test  | Changed or added logic with no corresponding test coverage
logic         | Suspicious control flow, unreachable code, or incorrect branching
performance   | Inefficient loop, repeated computation, or unnecessary allocation
style         | Formatting, naming convention, or linting policy violation

TITLE Code Review Agent - What This Agent Does NOT Do...
- Does not perform deep security vulnerability analysis
- Does not compute blast radius or downstream service impact
- Does not evaluate architectural layering or boundary violations
- Does not fetch Git data or webhook events directly
- Does not maintain long-term memory across PRs
- Does not invent findings without code evidence from the diff hunk
- Does not post comments to the PR itself, ORC Agent handles posting

TITLE Code Review Agent - Summary Agent at a Glance...
AGENT           | codereviewagent
----------------|------
ADK             | LlmAgent
LLM             | gemini-flash-latest
MEMORY          | none, session state only
INPUTS          | repo id, pr id, diff hunks, file list, language context, PR description
OUTPUTS         | raw findings with file, line, category, severity, evidence, and suggested fix
TOOLS           | prschemachecker, difflinemapper, languagecontextdetector, codeanalyzerfinder
ROLE            | primary review layer before all downstream analysis agents
LANGUAGE SUPPORT| multi-language through structured metadata and language detection
OUTPUT TARGET   | session state raw findings consumed by security, standards, architecture, and impact agents
