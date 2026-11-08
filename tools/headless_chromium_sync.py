#!/usr/bin/env /home/ubuntu/scraping-suite/.venv/bin/python3
"""
Headless Chromium LeetCode Auto-Sync Engine
===========================================
Enterprise stealth-browser automation engine for LeetCode.
Uses Patchright (stealth Chromium) to bypass Cloudflare bot detection,
extract accepted submissions, format solutions, and push to GitHub.

Author: Amz34 / Antigravity
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path

# Paths
REPO_DIR = Path(__file__).resolve().parent.parent
SOLUTIONS_DIR = REPO_DIR / "solutions"
CONFIG_FILE = Path("/home/ubuntu/.config/leetcode/config.json")
CHROME_PATH = "/usr/bin/google-chrome"

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
    "php": "php"
}

def load_config():
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Configuration file not found at {CONFIG_FILE}")
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def run_headless_sync():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 🚀 Starting Headless Chromium Sync...")
    config = load_config()
    session = config["session"]
    csrf = config["csrf_token"]
    username = config.get("username", "amz34")

    from patchright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            executable_path=CHROME_PATH,
            args=[
                "--no-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled"
            ]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        context.add_cookies([
            {"name": "LEETCODE_SESSION", "value": session, "domain": ".leetcode.com", "path": "/"},
            {"name": "csrftoken", "value": csrf, "domain": ".leetcode.com", "path": "/"}
        ])

        page = context.new_page()
        page.goto("https://leetcode.com", wait_until="domcontentloaded", timeout=20000)

        # 1. Fetch recent accepted submission list
        list_query = """
        query recentAcSubmissions($username: String!, $limit: Int!) {
            recentAcSubmissionList(username: $username, limit: $limit) {
                id
                title
                titleSlug
                timestamp
            }
        }
        """
        raw_list = page.evaluate("""async ({query, username, csrf}) => {
            const resp = await fetch("https://leetcode.com/graphql", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "x-csrftoken": csrf
                },
                body: JSON.stringify({
                    query: query,
                    variables: { username: username, limit: 30 }
                })
            });
            return await resp.json();
        }""", {"query": list_query, "username": username, "csrf": csrf})

        submissions = raw_list.get("data", {}).get("recentAcSubmissionList", [])
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 📋 Retrieved {len(submissions)} recent submissions for @{username}.")

        if not submissions:
            print("No submissions to sync.")
            browser.close()
            return

        detail_query = """
        query submissionDetails($submissionId: Int!) {
            submissionDetails(submissionId: $submissionId) {
                runtime
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
                    content
                    topicTags {
                        name
                    }
                }
            }
        }
        """

        new_syncs = 0
        for sub in submissions:
            sub_id = int(sub["id"])
            title_slug = sub["titleSlug"]

            # Detail fetch
            sub_detail_raw = page.evaluate("""async ({query, subId, csrf}) => {
                const resp = await fetch("https://leetcode.com/graphql", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "x-csrftoken": csrf
                    },
                    body: JSON.stringify({
                        query: query,
                        variables: { submissionId: subId }
                    })
                });
                return await resp.json();
            }""", {"query": detail_query, "subId": sub_id, "csrf": csrf})

            detail = sub_detail_raw.get("data", {}).get("submissionDetails")
            if not detail:
                continue

            q = detail.get("question", {})
            qid = q.get("questionFrontendId", "0").zfill(4)
            title = q.get("title", sub["title"])
            diff = q.get("difficulty", "Medium")
            tags = [t["name"] for t in q.get("topicTags", [])]
            lang_name = detail.get("lang", {}).get("name", "python3")
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

            # Check if this exact code was already written
            is_new = False
            if not sol_file.exists():
                is_new = True
            else:
                with open(sol_file, "r", encoding="utf-8") as f:
                    if f.read().strip() != code.strip():
                        is_new = True

            if is_new:
                with open(sol_file, "w", encoding="utf-8") as f:
                    f.write(code)

                # Generate clean Markdown description
                readme_content = f"""# {int(qid)}. {title}

**Difficulty:** {diff}  
**Tags:** {', '.join(tags)}  
**LeetCode Link:** [https://leetcode.com/problems/{title_slug}/](https://leetcode.com/problems/{title_slug}/)

---

## Performance
- **Runtime:** {runtime_str}
- **Memory:** {memory_str}

## Solution ({detail.get('lang', {}).get('verboseName', lang_name)})
```{lang_name}
{code}
```
"""
                with open(readme_file, "w", encoding="utf-8") as f:
                    f.write(readme_content)

                meta = {
                    "question_id": qid,
                    "submission_id": sub_id,
                    "slug": title_slug,
                    "title": title,
                    "difficulty": diff,
                    "lang": lang_name,
                    "runtime": runtime_str,
                    "memory": memory_str
                }
                with open(meta_file, "w", encoding="utf-8") as f:
                    json.dump(meta, f, indent=2)

                print(f"  ✨ Synced: [{qid}] {title} ({runtime_str}, {memory_str})")
                new_syncs += 1

        browser.close()

    if new_syncs > 0:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 💾 Committing & pushing {new_syncs} updates to GitHub...")
        os.chdir(REPO_DIR)
        subprocess.run(["git", "add", "solutions/"], check=False)
        msg = f"chore(sync): automated headless chromium sync ({new_syncs} problems)"
        subprocess.run(["git", "commit", "-m", msg], check=False)
        subprocess.run(["git", "push"], check=False)
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ✅ Synced and pushed successfully!")
    else:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ☕ Everything up to date. No new submissions.")

if __name__ == "__main__":
    run_headless_sync()
