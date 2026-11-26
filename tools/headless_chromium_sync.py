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
TELEGRAM_CFG = Path("/home/ubuntu/.config/telegram/azgem_bot.json")
CHROME_PATH = "/usr/bin/google-chrome"

def send_telegram(html_text: str) -> bool:
    try:
        if not TELEGRAM_CFG.exists():
            return False
        with open(TELEGRAM_CFG, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        token = cfg.get("token")
        chat_id = cfg.get("chat_id")
        if not token or not chat_id:
            return False
        import urllib.request
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = json.dumps({
            "chat_id": chat_id,
            "text": html_text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            return resp.status == 200
    except Exception as e:
        print(f"⚠️ Telegram notification skipped: {e}")
        return False

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

def save_refreshed_cookies(config: dict, cookies: list[dict]) -> None:
    """Persist rotated LEETCODE_SESSION / csrftoken cookies and sync GH Actions secrets."""
    cookie_map = {c.get("name"): c.get("value", "") for c in cookies}
    new_session = cookie_map.get("LEETCODE_SESSION") or config["session"]
    new_csrf = cookie_map.get("csrftoken") or config["csrf_token"]
    if new_session == config["session"] and new_csrf == config["csrf_token"]:
        return

    updated = {**config, "session": new_session, "csrf_token": new_csrf}
    tmp_path = CONFIG_FILE.with_suffix(".tmp")
    tmp_path.write_text(json.dumps(updated, indent=2), encoding="utf-8")
    tmp_path.chmod(0o600)
    tmp_path.replace(CONFIG_FILE)
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 🔄 Persisted refreshed LeetCode cookies to {CONFIG_FILE}")

    for secret_name, secret_val in (("LEETCODE_SESSION", new_session), ("LEETCODE_CSRF_TOKEN", new_csrf)):
        try:
            subprocess.run(
                ["gh", "secret", "set", secret_name, "-R", "Amz34/leetcode-solutions"],
                input=secret_val,
                text=True,
                capture_output=True,
                timeout=15,
                check=False,
            )
        except Exception:
            pass


def run_headless_sync():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 🚀 Starting Headless Chromium Sync...")
    config = load_config()
    session = config["session"]
    csrf = config["csrf_token"]
    username = config.get("username", "amz34")

    from patchright.sync_api import sync_playwright

    new_syncs = 0
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
        context = None
        is_authenticated = False
        try:
            context = browser.new_context(
                viewport={"width": 1280, "height": 800}
            )
            context.add_cookies([
                {"name": "LEETCODE_SESSION", "value": session, "domain": ".leetcode.com", "path": "/"},
                {"name": "csrftoken", "value": csrf, "domain": ".leetcode.com", "path": "/"}
            ])

            page = context.new_page()
            page.goto("https://leetcode.com", wait_until="domcontentloaded", timeout=20000)

            # Persist any refreshed csrf/session cookies issued on initial navigation
            live_cookies = context.cookies("https://leetcode.com")
            live_csrf = next((c["value"] for c in live_cookies if c.get("name") == "csrftoken" and c.get("value")), csrf)

            # 1. Verify authentication + fetch recent accepted submission list
            list_query = """
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
            }""", {"query": list_query, "username": username, "csrf": live_csrf})

            data = raw_list.get("data") or {}
            user_status = data.get("userStatus") or {}
            if not user_status.get("isSignedIn"):
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ❌ LeetCode session expired or invalid (isSignedIn=False). Refresh {CONFIG_FILE}.")
                sys.exit(1)

            is_authenticated = True
            save_refreshed_cookies(config, context.cookies("https://leetcode.com"))
            config = load_config()

            submissions = data.get("recentAcSubmissionList") or []
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 📋 Retrieved {len(submissions)} recent submissions for @{username}.")

            if not submissions:
                print("No submissions to sync.")
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
                }""", {"query": detail_query, "subId": sub_id, "csrf": live_csrf})

                detail = (sub_detail_raw.get("data") or {}).get("submissionDetails")
                if not detail:
                    print(f"  ⚠️ Empty submissionDetails for {sub_id} ({title_slug}); skipping.")
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

                    # Generate clean Markdown description only if README doesn't already have a problem description
                    if not readme_file.exists() or "## Problem Description" not in readme_file.read_text(encoding="utf-8"):
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
        finally:
            if context is not None and is_authenticated:
                try:
                    save_refreshed_cookies(config, context.cookies("https://leetcode.com"))
                except Exception:
                    pass
            browser.close()

    if new_syncs > 0:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 💾 Committing & pushing {new_syncs} updates to GitHub...")
        os.chdir(REPO_DIR)
        subprocess.run(["python3", "tools/leetcode_cli.py", "dashboard"], check=False)
        subprocess.run(["git", "add", "."], check=False)
        msg = f"chore(sync): automated headless chromium sync ({new_syncs} problems)"
        subprocess.run(["git", "commit", "-m", msg], check=False)
        subprocess.run(["git", "pull", "--rebase", "--autostash", "origin", "main"], check=False)
        push_res = subprocess.run(["git", "push", "origin", "main"], check=False)
        if push_res.returncode != 0:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ❌ git push failed (rc={push_res.returncode}).")
            sys.exit(push_res.returncode)
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ✅ Synced and pushed successfully!")

        tele_alert = f"""🤖 <b>Stealth Chromium: Synced {new_syncs} Accepted Problem(s)</b>
<b>Account:</b> @amz34
<b>Vault:</b> <a href="https://github.com/Amz34/leetcode-solutions">Amz34/leetcode-solutions</a>
✅ <b>Dynamic Dashboard Updated & Pushed</b>"""
        send_telegram(tele_alert)
    else:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ☕ Everything up to date. No new submissions.")

if __name__ == "__main__":
    run_headless_sync()
