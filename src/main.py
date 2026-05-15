"""Run the PR review agent."""

from __future__ import annotations

import argparse
import asyncio
import uuid

from google.adk.runners import InMemoryRunner
from google.genai import types

from .agent import pr_review_agent


async def run_review(event_path: str) -> str:
    import os
    from pathlib import Path

    from .pr_tools import load_pull_request

    if event_path:
        event_path = str(Path(event_path).resolve())
        os.environ["GITHUB_EVENT_PATH"] = event_path

    pr = load_pull_request(event_path)
    prompt = (
        f"Review pull request #{pr.get('number', '?')}: {pr['title']}\n\n"
        f"Description: {pr.get('body') or '(none)'}\n\n"
        f"```diff\n{pr['diff']}\n```\n\n"
        "Write Summary, Issues (file:line — problem — fix), and Verdict (approve / request changes)."
    )

    runner = InMemoryRunner(agent=pr_review_agent, app_name="pr_review")
    user_id = "reviewer"
    session_id = str(uuid.uuid4())

    await runner.session_service.create_session(
        app_name="pr_review",
        user_id=user_id,
        session_id=session_id,
    )

    message = types.Content(
        role="user",
        parts=[types.Part.from_text(text=prompt)],
    )

    review_parts: list[str] = []
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=message,
    ):
        if not event.content or not event.content.parts:
            continue
        for part in event.content.parts:
            if part.text:
                review_parts.append(part.text)

    return "\n".join(review_parts).strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Review a PR with Google ADK + local LiteLLM")
    parser.add_argument(
        "--event",
        default="",
        help="Path to GitHub pull_request event JSON (defaults to GITHUB_EVENT_PATH)",
    )
    parser.add_argument(
        "--output",
        default="",
        help="Write review markdown to this file (used by GitHub Actions)",
    )
    parser.add_argument(
        "--sample",
        action="store_true",
        help="Use a small simulated PR diff for fast local testing",
    )
    args = parser.parse_args()
    event_path = args.event
    if args.sample and not event_path:
        from pathlib import Path

        event_path = str(Path(__file__).resolve().parent.parent / "test" / "sample-event.json")
    review = asyncio.run(run_review(event_path))
    print(review)
    if args.output:
        from pathlib import Path

        Path(args.output).write_text(review + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
