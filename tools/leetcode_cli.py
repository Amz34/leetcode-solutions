#!/usr/bin/env python3
"""
LeetCode CLI & Automation Suite
=================================
Automated bidirectional integration for LeetCode <-> GitHub / VM.
Author: Amz34 / Antigravity
"""

import os
import sys
import json
import time
import re
import argparse
import urllib.request
import urllib.error
import subprocess
from pathlib import Path

CONFIG_PATHS = [
    Path("/home/ubuntu/.config/leetcode/config.json"),
    Path.home() / ".config" / "leetcode" / "config.json",
    Path(__file__).resolve().parent.parent / ".leetcode_config.json"
]

def load_credentials():
    session = os.environ.get("LEETCODE_SESSION")
    csrf = os.environ.get("LEETCODE_CSRF_TOKEN") or os.environ.get("LEETCODE_CSRF")
    username = os.environ.get("LEETCODE_USERNAME")

    if not session or not csrf:
        for p in CONFIG_PATHS:
            if p.exists():
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        session = session or data.get("session")
                        csrf = csrf or data.get("csrf_token")
                        username = username or data.get("username")
                        break
                except Exception:
                    pass

    return {
        "session": session,
        "csrf": csrf,
        "username": username or "amz34"
    }

def get_headers(creds, slug=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "*/*",
    }
    cookie_parts = []
    if creds.get("session"):
        cookie_parts.append(f"LEETCODE_SESSION={creds['session']}")
    if creds.get("csrf"):
        cookie_parts.append(f"csrftoken={creds['csrf']}")
        headers["x-csrftoken"] = creds["csrf"]

    if cookie_parts:
        headers["Cookie"] = "; ".join(cookie_parts)

    if slug:
        headers["Referer"] = f"https://leetcode.com/problems/{slug}/"
        headers["Origin"] = "https://leetcode.com"
    else:
        headers["Referer"] = "https://leetcode.com"
        headers["Origin"] = "https://leetcode.com"

    return headers

def graphql_query(creds, query, variables=None):
    url = "https://leetcode.com/graphql"
    payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    headers = get_headers(creds)
    req = urllib.request.Request(url, data=payload, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GraphQL HTTP {e.code}: {body}")

def cmd_status(creds, args):
    print("🔍 Checking LeetCode Account Connection...")
    status_query = "query { userStatus { isSignedIn username isPremium } }"
    res = graphql_query(creds, status_query)
    user_status = res.get("data", {}).get("userStatus", {})
    if not user_status.get("isSignedIn"):
        print("❌ Not signed in! Please check your LEETCODE_SESSION.")
        return 1

    username = user_status.get("username", creds["username"])
    print(f"✅ Authenticated as: @{username} (Premium: {user_status.get('isPremium')})")

    stats_query = """
    query userProfile($username: String!) {
        matchedUser(username: $username) {
            submitStatsGlobal {
                acSubmissionNum {
                    difficulty
                    count
                }
            }
        }
        recentAcSubmissionList(username: $username, limit: 10) {
            id
            title
            titleSlug
            timestamp
        }
    }
    """
    stats_res = graphql_query(creds, stats_query, {"username": username})
    user_data = stats_res.get("data", {}).get("matchedUser")
    if user_data:
        counts = {x["difficulty"]: x["count"] for x in user_data["submitStatsGlobal"]["acSubmissionNum"]}
        print(f"\n📊 Solved Problems: Total {counts.get('All', 0)} | Easy: {counts.get('Easy', 0)} | Med: {counts.get('Medium', 0)} | Hard: {counts.get('Hard', 0)}")

    recents = stats_res.get("data", {}).get("recentAcSubmissionList", [])
    print(f"\n🕒 Recent Accepted Submissions ({len(recents)}):")
    if not recents:
        print("   (No recent accepted submissions found)")
    for item in recents:
        ts = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(item['timestamp'])))
        print(f"   - [{item['id']}] {item['title']} ({ts})")

    return 0

def clean_html(html_text):
    if not html_text:
        return ""
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

LANG_EXTENSIONS = {
    "python3": "py",
    "python": "py",
    "javascript": "js",
    "typescript": "ts",
    "cpp": "cpp",
    "golang": "go",
    "rust": "rs",
    "java": "java",
    "csharp": "cs",
    "c": "c"
}

def cmd_fetch(creds, args):
    slug = args.slug.strip().lower()
    lang = args.lang.strip().lower()

    print(f"📥 Fetching problem: {slug}...")
    query = """
    query questionData($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
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
                slug
            }
        }
    }
    """
    res = graphql_query(creds, query, {"titleSlug": slug})
    q = res.get("data", {}).get("question")
    if not q:
        print(f"❌ Problem '{slug}' not found.")
        return 1

    qid = q["questionFrontendId"]
    title = q["title"]
    diff = q["difficulty"]
    tags = [t["name"] for t in q.get("topicTags", [])]

    # Find code snippet
    snippet = None
    for s in q.get("codeSnippets", []):
        if s["langSlug"] == lang:
            snippet = s["code"]
            break

    if not snippet:
        available = [s["langSlug"] for s in q.get("codeSnippets", [])]
        print(f"⚠️ Language '{lang}' not found. Available: {', '.join(available)}")
        return 1

    ext = LANG_EXTENSIONS.get(lang, lang)
    out_dir = Path("solutions") / f"{int(qid):04d}-{slug}"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Save problem description
    readme_path = out_dir / "README.md"
    readme_content = f"""# {qid}. {title}

**Difficulty:** {diff}  
**Tags:** {', '.join(tags)}  
**LeetCode Link:** [https://leetcode.com/problems/{slug}/](https://leetcode.com/problems/{slug}/)

---

## Problem Description

{clean_html(q.get('content', ''))}
"""
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)

    # Save solution template
    sol_file = out_dir / f"solution.{ext}"
    if not sol_file.exists():
        with open(sol_file, "w", encoding="utf-8") as f:
            f.write(snippet)
        print(f"✅ Created solution template: {sol_file}")
    else:
        print(f"ℹ️ Solution file already exists: {sol_file}")

    # Metadata for runner/submitter
    meta_path = out_dir / ".meta.json"
    meta = {
        "question_id": q["questionId"],
        "frontend_id": qid,
        "slug": slug,
        "title": title,
        "lang": lang
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    print(f"✅ Saved problem documentation: {readme_path}")
    print(f"🚀 Ready to solve in: {sol_file}")
    return 0

def cmd_submit(creds, args):
    file_path = Path(args.file).resolve()
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return 1

    # Locate .meta.json or deduce problem
    meta_file = file_path.parent / ".meta.json"
    slug = None
    qid = None
    lang = None

    if meta_file.exists():
        with open(meta_file, "r", encoding="utf-8") as f:
            meta = json.load(f)
            slug = meta.get("slug")
            qid = meta.get("question_id")
            lang = meta.get("lang")

    if not slug:
        # Deduce from folder name (e.g. 0001-two-sum)
        folder = file_path.parent.name
        m = re.match(r'^\d+-(.+)$', folder)
        if m:
            slug = m.group(1)

    if not slug:
        print("❌ Could not determine LeetCode problem slug. Specify using --slug <slug>.")
        return 1

    if not lang:
        ext = file_path.suffix.lstrip(".")
        rev_ext = {v: k for k, v in LANG_EXTENSIONS.items()}
        lang = rev_ext.get(ext, "python3")

    if not qid:
        print(f"🔍 Fetching problem metadata for {slug}...")
        query = "query questionData($titleSlug: String!) { question(titleSlug: $titleSlug) { questionId } }"
        res = graphql_query(creds, query, {"titleSlug": slug})
        qid = res.get("data", {}).get("question", {}).get("questionId")

    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    print(f"🚀 Submitting solution for '{slug}' (ID: {qid}, Lang: {lang})...")
    submit_url = f"https://leetcode.com/problems/{slug}/submit/"
    headers = get_headers(creds, slug=slug)
    payload = json.dumps({
        "question_id": str(qid),
        "lang": lang,
        "typed_code": code
    }).encode("utf-8")

    req = urllib.request.Request(submit_url, data=payload, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            submit_data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"❌ Submission failed (HTTP {e.code}): {body}")
        return 1

    submission_id = submit_data.get("submission_id")
    if not submission_id:
        print("❌ No submission_id returned:", submit_data)
        return 1

    print(f"⏳ Submission queued (ID: {submission_id}). Checking status...")
    check_url = f"https://leetcode.com/submissions/detail/{submission_id}/check/"
    
    for _ in range(20):
        time.sleep(1.5)
        req = urllib.request.Request(check_url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            check_data = json.loads(resp.read().decode("utf-8"))
        
        state = check_data.get("state")
        if state == "SUCCESS":
            status = check_data.get("status_msg") or check_data.get("status_display")
            if status == "Accepted" or check_data.get("status_code") == 10:
                runtime = check_data.get("status_runtime", "N/A")
                memory = check_data.get("status_memory", "N/A")
                run_p = check_data.get("runtime_percentile")
                mem_p = check_data.get("memory_percentile")
                print(f"\n🎉 ACCEPTED!")
                print(f"⏱️  Runtime: {runtime}" + (f" (beats {run_p:.1f}%)" if run_p is not None else ""))
                print(f"💾 Memory:  {memory}" + (f" (beats {mem_p:.1f}%)" if mem_p is not None else ""))

                if args.git:
                    print("\n📦 Auto-committing to git...")
                    subprocess.run(["git", "add", str(file_path.parent)], check=False)
                    msg = f"Solved: {slug} [Accepted] ({runtime}, {memory})"
                    subprocess.run(["git", "commit", "-m", msg], check=False)
                    subprocess.run(["git", "push"], check=False)
                    print("✅ Pushed to GitHub!")
                return 0
            else:
                print(f"\n❌ Result: {status}")
                if "compile_error" in check_data:
                    print(f"Compile Error:\n{check_data.get('full_compile_error')}")
                if "total_correct" in check_data and "total_testcases" in check_data:
                    print(f"Passed: {check_data.get('total_correct')}/{check_data.get('total_testcases')} test cases")
                if "input_formatted" in check_data:
                    print(f"Last Input: {check_data.get('input_formatted')}")
                    print(f"Output:     {check_data.get('code_output')}")
                    print(f"Expected:   {check_data.get('expected_output')}")
                return 1

    print("⚠️ Submission check timed out.")
    return 1

def main():
    parser = argparse.ArgumentParser(description="LeetCode CLI & GitHub Sync Suite")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_status = subparsers.add_parser("status", help="Check LeetCode account & problem stats")
    
    p_fetch = subparsers.add_parser("fetch", help="Fetch a LeetCode problem description and code template")
    p_fetch.add_argument("slug", help="LeetCode problem title slug (e.g. 'two-sum')")
    p_fetch.add_argument("--lang", default="python3", help="Target programming language (default: python3)")

    p_submit = subparsers.add_parser("submit", help="Submit a solution to LeetCode from VM/IDE")
    p_submit.add_argument("file", help="Path to solution file to submit")
    p_submit.add_argument("--slug", help="Optional override for problem slug")
    p_submit.add_argument("--git", action="store_true", help="Auto git commit and push on ACCEPTED")

    args = parser.parse_args()
    creds = load_credentials()

    if args.command == "status":
        sys.exit(cmd_status(creds, args))
    elif args.command == "fetch":
        sys.exit(cmd_fetch(creds, args))
    elif args.command == "submit":
        sys.exit(cmd_submit(creds, args))

if __name__ == "__main__":
    main()
