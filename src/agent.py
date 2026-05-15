"""Google ADK PR review agent using local LiteLLM."""

from google.adk import Agent
from google.adk.tools import FunctionTool

from .config import get_local_llm
from .pr_tools import load_pull_request

pr_review_agent = Agent(
    name="pr_review_agent",
    model=get_local_llm(),
    description="Reviews pull request changes and returns actionable feedback.",
    instruction="""You are a pull request code review agent.

Steps:
1. Call load_pull_request once to get the PR metadata and diff.
2. Review only the changed code in the diff.
3. Write a clear PR review with:
   - **Summary** (2-3 sentences)
   - **Issues** (file:line — problem — suggested fix)
   - **Verdict** (approve / request changes)

Be specific. Do not invent files or lines not present in the diff.""",
    tools=[FunctionTool(load_pull_request)],
)
