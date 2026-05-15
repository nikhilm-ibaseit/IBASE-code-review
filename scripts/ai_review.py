"""
AI Code Review Script
Fetches PR diff from GitHub, sends it to Claude for review,
and posts the result back as a formal GitHub PR review.
"""

import json
import os
import sys

import anthropic
import requests

GITHUB_API = "https://api.github.com"
MAX_DIFF_CHARS = 80000  # Stay within Claude's context safely


# ── GitHub helpers ────────────────────────────────────────────────────────────

def github_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def get_pr_details() -> dict:
    event_path = os.environ["GITHUB_EVENT_PATH"]
    with open(event_path) as f:
        event = json.load(f)

    pr = event["pull_request"]
    return {
        "number":        pr["number"],
        "title":         pr["title"],
        "body":          pr.get("body") or "(no description provided)",
        "author":        pr["user"]["login"],
        "base_branch":   pr["base"]["ref"],
        "head_branch":   pr["head"]["ref"],
        "base_sha":      pr["base"]["sha"],
        "head_sha":      pr["head"]["sha"],
        "additions":     pr["additions"],
        "deletions":     pr["deletions"],
        "changed_files": pr["changed_files"],
    }


def fetch_pr_files(repo: str, pr_number: int, token: str) -> list:
    url = f"{GITHUB_API}/repos/{repo}/pulls/{pr_number}/files"
    resp = requests.get(url, headers=github_headers(token))
    resp.raise_for_status()
    return resp.json()


def build_diff(files: list) -> str:
    """Compile per-file patches into a single readable diff block."""
    sections = []
    total = 0

    for f in files:
        name    = f["filename"]
        status  = f["status"]          # added / modified / removed / renamed
        adds    = f.get("additions", 0)
        dels    = f.get("deletions", 0)
        patch   = f.get("patch", "")   # absent for binary files

        header = f"\n### {name}  [{status}]  +{adds} / -{dels}\n"
        body   = f"```diff\n{patch}\n```\n" if patch else "_Binary or empty file — no diff available_\n"
        block  = header + body

        if total + len(block) > MAX_DIFF_CHARS:
            sections.append(
                "\n---\n⚠️  Diff truncated — remaining files omitted to stay within context limit.\n"
            )
            break

        sections.append(block)
        total += len(block)

    return "\n".join(sections)


def post_pr_review(repo: str, pr_number: int, token: str, body: str, event: str) -> dict:
    """
    Post a formal GitHub PR review.
    event must be one of: APPROVE | REQUEST_CHANGES | COMMENT
    """
    url = f"{GITHUB_API}/repos/{repo}/pulls/{pr_number}/reviews"
    payload = {"body": body, "event": event}
    resp = requests.post(url, headers=github_headers(token), json=payload)
    resp.raise_for_status()
    return resp.json()


# ── AI review ─────────────────────────────────────────────────────────────────

def build_prompt(pr: dict, diff: str) -> str:
    return f"""You are a senior software engineer performing a thorough code review.
Analyse the pull request below and provide structured, actionable feedback.

## Pull Request
- **Title:** {pr["title"]}
- **Author:** `{pr["author"]}`
- **Branch:** `{pr["head_branch"]}` → `{pr["base_branch"]}`
- **Stats:** +{pr["additions"]} additions, -{pr["deletions"]} deletions, {pr["changed_files"]} file(s) changed
- **Description:**
{pr["body"]}

## Changed Files & Diff
{diff}

---

## Review Format (use exactly these headings)

### Summary
One short paragraph describing what this PR does.

### Strengths
Bullet list of what is done well.

### Issues
List every problem found. Tag each one:
- 🔴 **Critical** — bugs, security holes, data loss risk
- 🟡 **Warning** — logic errors, bad practices, missing validation
- 🔵 **Suggestion** — style, readability, minor improvements

For each issue include: file name, approximate line reference, explanation, and a suggested fix.

### Security
Any authentication, authorisation, injection, or data-exposure concerns.

### Performance
Any inefficiency, N+1 queries, memory leaks, or blocking calls.

### Final Verdict
State exactly one of: **APPROVE** | **REQUEST CHANGES** | **COMMENT**
Then one or two sentences justifying the verdict.
"""


def parse_verdict(review_text: str) -> str:
    """
    Extract the GitHub review event from the AI's Final Verdict section.
    Defaults to COMMENT if nothing clear is found.
    """
    text = review_text.upper()
    # Look inside the Final Verdict section only to avoid false positives
    verdict_start = text.find("FINAL VERDICT")
    section = text[verdict_start:] if verdict_start != -1 else text

    if "APPROVE" in section and "REQUEST CHANGES" not in section:
        return "APPROVE"
    if "REQUEST CHANGES" in section:
        return "REQUEST_CHANGES"
    return "COMMENT"


def run_ai_review(pr: dict, diff: str) -> tuple[str, str]:
    """Returns (review_markdown, github_event)."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    print("  Calling Claude API...")
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": build_prompt(pr, diff)}],
    )

    review_text = message.content[0].text
    event       = parse_verdict(review_text)
    return review_text, event


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    repo  = os.environ["GITHUB_REPOSITORY"]
    token = os.environ["GITHUB_TOKEN"]

    print("=== AI Code Review Agent ===")

    print("\n[1/4] Reading PR details from event payload...")
    pr = get_pr_details()
    print(f"      PR #{pr['number']}: {pr['title']}  by @{pr['author']}")

    print("\n[2/4] Fetching changed files from GitHub API...")
    files = fetch_pr_files(repo, pr["number"], token)
    print(f"      {len(files)} file(s) found")

    print("\n[3/4] Building diff and sending to Claude for review...")
    diff         = build_diff(files)
    review, event = run_ai_review(pr, diff)
    print(f"      Review generated — verdict: {event}")

    print("\n[4/4] Posting review to PR...")
    formatted_body = (
        "## 🤖 AI Code Review\n\n"
        + review
        + "\n\n---\n*Automated review powered by [Claude](https://claude.ai) · "
        + f"[View run](https://github.com/{repo}/actions/runs/{os.environ['GITHUB_RUN_ID']})*"
    )
    result = post_pr_review(repo, pr["number"], token, formatted_body, event)
    print(f"      Review posted successfully — Review ID: {result.get('id')}")
    print("\n=== Done ===")


if __name__ == "__main__":
    try:
        main()
    except requests.HTTPError as e:
        print(f"\n❌ GitHub API error: {e.response.status_code} — {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
