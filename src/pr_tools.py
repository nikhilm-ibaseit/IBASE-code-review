"""Load PR metadata and diff for the review agent."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

MAX_DIFF_CHARS = 50_000

# Tiny diff for fast local testing (2 files, few lines)
SAMPLE_DIFF = """diff --git a/src/auth.py b/src/auth.py
index 1111111..2222222 100644
--- a/src/auth.py
+++ b/src/auth.py
@@ -12,6 +12,8 @@ def get_user_email(user_id: str) -> str:
     user = db.find_user(user_id)
+    if user is None:
+        raise ValueError("User not found")
     return user.email

diff --git a/tests/test_auth.py b/tests/test_auth.py
index 3333333..4444444 100644
--- a/tests/test_auth.py
+++ b/tests/test_auth.py
@@ -5,0 +6,4 @@
+def test_get_user_email_missing_user():
+    with pytest.raises(ValueError):
+        get_user_email("unknown-id")
"""


def _git_diff(repo_root: str, base: str, head: str) -> str:
    try:
        proc = subprocess.run(
            ["git", "diff", f"{base}...{head}"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if proc.returncode == 0 and proc.stdout.strip():
            return proc.stdout
        proc = subprocess.run(
            ["git", "diff", base, head],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=120,
        )
        return proc.stdout if proc.returncode == 0 else proc.stderr or ""
    except Exception as exc:
        return f"(could not load diff: {exc})"


def load_pull_request(event_path: str = "") -> dict:
    """Load PR title, description, and diff from a GitHub event file or local git."""
    path = event_path or os.environ.get("GITHUB_EVENT_PATH", "")
    repo_root = os.environ.get("GITHUB_WORKSPACE", os.getcwd())

    if path and Path(path).is_file():
        with open(path, encoding="utf-8") as f:
            event = json.load(f)
        if event.get("use_sample_diff"):
            pr = event.get("pull_request", {})
            return {
                "number": pr.get("number", 1),
                "title": pr.get("title", "Sample PR"),
                "body": pr.get("body") or "",
                "url": pr.get("html_url", ""),
                "author": pr.get("user", {}).get("login", ""),
                "base_branch": pr.get("base", {}).get("ref", "main"),
                "head_branch": pr.get("head", {}).get("ref", "sample"),
                "diff": SAMPLE_DIFF,
            }
        pr = event.get("pull_request", {})
        base_ref = pr.get("base", {}).get("ref", "main")
        base_sha = pr.get("base", {}).get("sha", "")
        head_sha = pr.get("head", {}).get("sha", "HEAD")
        if base_sha and head_sha:
            diff = _git_diff(repo_root, base_sha, head_sha)
        else:
            diff = _git_diff(repo_root, f"origin/{base_ref}", head_sha)
        return {
            "number": pr.get("number"),
            "title": pr.get("title", ""),
            "body": pr.get("body") or "",
            "url": pr.get("html_url", ""),
            "author": pr.get("user", {}).get("login", ""),
            "base_branch": base_ref,
            "head_branch": pr.get("head", {}).get("ref", ""),
            "diff": diff[:MAX_DIFF_CHARS],
        }

    diff = _git_diff(repo_root, "main", "HEAD")
    return {
        "number": 0,
        "title": "Local changes",
        "body": "",
        "url": "",
        "author": "",
        "base_branch": "main",
        "head_branch": "HEAD",
        "diff": diff[:MAX_DIFF_CHARS],
    }
