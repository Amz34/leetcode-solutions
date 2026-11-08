#!/usr/bin/env python3
"""
Autonomous Daily LeetCode POTD Dispatcher
=========================================
Runs automatically via cron at 06:00 UTC (09:00 AM Riyadh).
Pulls the Daily LeetCode Problem of the Day, scaffolds multi-language
templates (Python, Rust, C++), commits to GitHub, and delivers
an instant morning briefing to Telegram via @AzGem_Bot.

Author: Amz34 / Antigravity
"""

import os
import sys
import json
import time
import subprocess
import urllib.request
import urllib.error
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent.parent
SOLUTIONS_DIR = REPO_DIR / "solutions"
TELEGRAM_CFG = Path("/home/ubuntu/.config/telegram/azgem_bot.json")

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
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = json.dumps({
            "chat_id": chat_id,
            "text": html_text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            return resp.status == 200
    except Exception as e:
        print(f"⚠️ Telegram dispatch failed: {e}")
        return False

def clean_html(html_text):
    if not html_text:
        return ""
    import re
    text = re.sub(r'<pre>(.*?)</pre>', r'```\n\1\n```', html_text, flags=re.DOTALL)
    text = re.sub(r'<code>(.*?)</code>', r'`\1`', text)
    text = re.sub(r'<strong>(.*?)</strong>', r'**\1**', text)
    text = re.sub(r'<em>(.*?)</em>', r'*\1*', text)
    text = re.sub(r'<p>', r'\n\n', text)
    text = re.sub(r'</p>', r'', text)
    text = re.sub(r'<br\s*/?>', r'\n', text)
    text = re.sub(r'<li>', r'\n- ', text)
    text = re.sub(r'</li>', r'', text)
    text = re.sub(r'&nbsp;', r' ', text)
    text = re.sub(r'&lt;', r'<', text)
    text = re.sub(r'&gt;', r'>', text)
    text = re.sub(r'&amp;', r'&', text)
    text = re.sub(r'&quot;', r'"', text)
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()

def run_daily_dispatch():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ☀️ Querying Daily Problem of the Day (POTD)...")
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://leetcode.com"
    }

    # Query daily challenge
    query = """
    query questionOfToday {
        activeDailyCodingChallengeQuestion {
            date
            link
            question {
                questionId
                questionFrontendId
                title
                titleSlug
                difficulty
                content
                codeSnippets {
                    lang
                    langSlug
                    code
                }
                topicTags {
                    name
                }
            }
        }
    }
    """
    payload = json.dumps({"query": query}).encode("utf-8")
    req = urllib.request.Request("https://leetcode.com/graphql", data=payload, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"❌ Failed to fetch daily question: {e}")
        return 1

    daily = data.get("data", {}).get("activeDailyCodingChallengeQuestion")
    if not daily:
        print("❌ Could not parse daily question data.")
        return 1

    q = daily["question"]
    qid = str(q["questionFrontendId"]).zfill(4)
    slug = q["titleSlug"]
    title = q["title"]
    diff = q["difficulty"]
    date_str = daily["date"]
    tags = [t["name"] for t in q.get("topicTags", [])]

    folder_name = f"{qid}-{slug}"
    target_dir = SOLUTIONS_DIR / folder_name
    already_existed = target_dir.exists()
    target_dir.mkdir(parents=True, exist_ok=True)

    print(f"🎯 #{q['questionFrontendId']}: {title} ({diff}) [{date_str}]")

    # Write problem description
    readme_path = target_dir / "README.md"
    if not readme_path.exists():
        content_md = f"""# {int(qid)}. {title}

**Date:** {date_str} (Daily Challenge)  
**Difficulty:** {diff}  
**Tags:** {', '.join(tags)}  
**LeetCode Link:** [https://leetcode.com/problems/{slug}/](https://leetcode.com/problems/{slug}/)

---

## Problem Description

{clean_html(q.get('content', ''))}
"""
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content_md)

    # Scaffolding templates in Python, Rust, C++
    snippet_map = {s["langSlug"]: s["code"] for s in q.get("codeSnippets", [])}

    # Python3
    py_file = target_dir / "solution.py"
    if not py_file.exists() and "python3" in snippet_map:
        with open(py_file, "w", encoding="utf-8") as f:
            f.write(snippet_map["python3"])

    # Rust
    rs_file = target_dir / "solution.rs"
    if not rs_file.exists() and "rust" in snippet_map:
        with open(rs_file, "w", encoding="utf-8") as f:
            f.write(snippet_map["rust"])

    # C++
    cpp_file = target_dir / "solution.cpp"
    if not cpp_file.exists() and "cpp" in snippet_map:
        with open(cpp_file, "w", encoding="utf-8") as f:
            f.write(snippet_map["cpp"])

    # Metadata
    meta_path = target_dir / ".meta.json"
    if not meta_path.exists():
        meta = {
            "question_id": q["questionId"],
            "frontend_id": q["questionFrontendId"],
            "slug": slug,
            "title": title,
            "difficulty": diff,
            "tags": tags,
            "date": date_str
        }
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

    # Auto commit and push if new
    if not already_existed:
        print(f"📦 Committing new daily scaffold for {title}...")
        os.chdir(REPO_DIR)
        subprocess.run(["python3", "tools/leetcode_cli.py", "dashboard"], check=False)
        subprocess.run(["git", "add", "."], check=False)
        msg = f"chore(daily): scaffold POTD #{q['questionFrontendId']} - {title} ({diff})"
        subprocess.run(["git", "commit", "-m", msg], check=False)
        subprocess.run(["git", "push"], check=False)
        print("✅ Committed & pushed to GitHub!")

    # Telegram briefing
    tele_msg = f"""🎯 <b>Daily LeetCode Challenge: #{q['questionFrontendId']} {title}</b>
<b>Date:</b> {date_str}
<b>Difficulty:</b> {diff}
<b>Tags:</b> {', '.join(tags)}
<b>Problem Link:</b> <a href="https://leetcode.com/problems/{slug}/">Open on LeetCode</a>
📂 <b>Scaffolded:</b> <code>solutions/{folder_name}</code>
⚡ <i>Ready to solve in your IDE (Python, Rust, C++)!</i>"""
    send_telegram(tele_msg)
    print("📱 Telegram briefing dispatched to @AzGem_Bot!")
    return 0

if __name__ == "__main__":
    sys.exit(run_daily_dispatch())
