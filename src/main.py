"""Run the PR review agent."""

from __future__ import annotations

import argparse
import asyncio
import uuid

from google.adk.runners import InMemoryRunner
from google.genai import types

from .agent import pr_review_agent


async def run_review(event_path: str) -> str:
    if event_path:
        import os

        os.environ["GITHUB_EVENT_PATH"] = event_path

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
        parts=[types.Part.from_text(text="Review this pull request.")],
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
    args = parser.parse_args()
    review = asyncio.run(run_review(args.event))
    print(review)
    if args.output:
        from pathlib import Path

        Path(args.output).write_text(review + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
