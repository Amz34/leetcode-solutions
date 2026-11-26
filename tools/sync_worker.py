#!/usr/bin/env python3
"""
Production Autonomous LeetCode Sync Engine (GitHub Actions + Local CLI)
Syncs accepted LeetCode submissions (code + metadata + README) via GraphQL,
validates authentication, preserves POTD problem descriptions, and updates
the repository dashboard.
"""

import os
import sys
import json
import subprocess
import requests
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOLUTIONS_DIR = REPO_ROOT / "solutions"
USERNAME = os.getenv("LEETCODE_USERNAME", "amz34")
CSRF_TOKEN = os.getenv("LEETCODE_CSRF_TOKEN", "")
SESSION_TOKEN = os.getenv("LEETCODE_SESSION", "")

LANG_EXT_MAP = {
    "python3": "py",
    "python": "py",
    "javascript": "js",
    "typescript": "ts",
    "cpp": "cpp",
    "golang": "go",
    "rust": "rs",
    "java": "java",
    "csharp": "cs",
    "c": "c",
    "ruby": "rb",
    "swift": "swift",
    "kotlin": "kt",
    "scala": "scala",
    "php": "php",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Referer": "https://leetcode.com",
    "Origin": "https://leetcode.com",
    "Content-Type": "application/json",
}

if CSRF_TOKEN and SESSION_TOKEN:
    HEADERS["x-csrftoken"] = CSRF_TOKEN
    HEADERS["Cookie"] = f"LEETCODE_SESSION={SESSION_TOKEN}; csrftoken={CSRF_TOKEN}"

RECENT_QUERY = """
query recentAcSubmissions($username: String!, $limit: Int!) {
  userStatus {
    isSignedIn
    username
  }
  recentAcSubmissionList(username: $username, limit: $limit) {
    id
    title
    titleSlug
    timestamp
  }
}
"""

SUBMISSION_DETAIL_QUERY = """
query submissionDetails($submissionId: Int!) {
  submissionDetails(submissionId: $submissionId) {
    runtimeDisplay
    memoryDisplay
    code
    timestamp
    lang {
      name
      verboseName
    }
    question {
      questionFrontendId
      title
      titleSlug
      difficulty
      topicTags {
        name
      }
    }
  }
}
"""


def gql(query: str, variables: dict):
    resp = requests.post(
        "https://leetcode.com/graphql",
        json={"query": query, "variables": variables},
        headers=HEADERS,
        timeout=20,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"LeetCode HTTP {resp.status_code}: {resp.text[:200]}")
    return resp.json().get("data") or {}


def sync() -> int:
    print(f"[*] Querying LeetCode GraphQL endpoint for @{USERNAME}...")
    try:
        data = gql(RECENT_QUERY, {"username": USERNAME, "limit": 30})
    except Exception as e:
        print(f"[!] Error contacting LeetCode (may be Cloudflare-gated from GH runner IP): {e}")
        return 0

    user_status = data.get("userStatus") or {}
    if SESSION_TOKEN and not user_status.get("isSignedIn"):
        print("[!] WARNING: LEETCODE_SESSION appears expired or unauthenticated (isSignedIn=False).")
        return 1

    submissions = data.get("recentAcSubmissionList") or []
    print(f"[✓] Retrieved {len(submissions)} accepted recent submissions.")
    if not submissions:
        return 0

    SOLUTIONS_DIR.mkdir(parents=True, exist_ok=True)
    synced_count = 0

    for sub in submissions:
        sub_id = int(sub["id"])
        title_slug = sub["titleSlug"]
        try:
            detail = gql(SUBMISSION_DETAIL_QUERY, {"submissionId": sub_id}).get("submissionDetails")
        except Exception as e:
            print(f"[!] Error fetching submissionDetails for {sub_id}: {e}")
            continue

        if not detail:
            continue

        q = detail.get("question") or {}
        qid = str(q.get("questionFrontendId", "0")).zfill(4)
        title = q.get("title", sub.get("title", title_slug))
        diff = q.get("difficulty", "Medium")
        tags = [t["name"] for t in q.get("topicTags", [])]
        lang_name = (detail.get("lang") or {}).get("name", "python3")
        verbose_lang = (detail.get("lang") or {}).get("verboseName", lang_name)
        code = detail.get("code", "")
        runtime_str = detail.get("runtimeDisplay", "")
        memory_str = detail.get("memoryDisplay", "")

        ext = LANG_EXT_MAP.get(lang_name, "txt")
        folder_name = f"{qid}-{title_slug}"
        target_dir = SOLUTIONS_DIR / folder_name
        target_dir.mkdir(parents=True, exist_ok=True)

        sol_file = target_dir / f"solution.{ext}"
        readme_file = target_dir / "README.md"
        meta_file = target_dir / ".meta.json"

        is_new = not sol_file.exists() or sol_file.read_text(encoding="utf-8").strip() != code.strip()
        if not is_new:
            continue

        sol_file.write_text(code, encoding="utf-8")

        if not readme_file.exists() or "## Problem Description" not in readme_file.read_text(encoding="utf-8"):
            readme_content = (
                f"# {int(qid)}. {title}\n\n"
                f"**Difficulty:** {diff}  \n"
                f"**Tags:** {', '.join(tags)}  \n"
                f"**LeetCode Link:** [https://leetcode.com/problems/{title_slug}/](https://leetcode.com/problems/{title_slug}/)\n\n"
                f"---\n\n"
                f"## Performance\n"
                f"- **Runtime:** {runtime_str}\n"
                f"- **Memory:** {memory_str}\n\n"
                f"## Solution ({verbose_lang})\n"
                f"```{lang_name}\n{code}\n```\n"
            )
            readme_file.write_text(readme_content, encoding="utf-8")

        meta = {
            "question_id": qid,
            "submission_id": sub_id,
            "slug": title_slug,
            "title": title,
            "difficulty": diff,
            "tags": tags,
            "lang": lang_name,
            "runtime": runtime_str,
            "memory": memory_str,
        }
        meta_file.write_text(json.dumps(meta, indent=2), encoding="utf-8")
        print(f"[+] Synced [{qid}] {title} ({runtime_str}, {memory_str})")
        synced_count += 1

    if synced_count > 0:
        subprocess.run([sys.executable, str(REPO_ROOT / "tools" / "leetcode_cli.py"), "dashboard"], check=False)

    print(f"[✓] Synchronization cycle complete. {synced_count} new entries synchronized.")
    return 0


if __name__ == "__main__":
    sys.exit(sync())
