# ⚡ LeetCode Solutions Vault

[![LeetCode Stats](https://leetcard.jacoblin.cool/amz34?theme=dark&font=Ubuntu)](https://leetcode.com/u/amz34/)

Automated, bidirectional LeetCode synchronization and problem-solving infrastructure for [@amz34](https://leetcode.com/u/amz34/).

---

## 🚀 Architecture

1. **Cloud-Native Auto-Sync (`.github/workflows/leetcode-sync.yml`)**:
   - Runs automatically on schedule (every 6 hours) or manual trigger (`workflow_dispatch`).
   - Syncs all accepted submissions directly from LeetCode into GitHub using GitHub Actions and encrypted repository secrets (`LEETCODE_SESSION`, `LEETCODE_CSRF_TOKEN`).

2. **VM / IDE CLI Suite (`tools/leetcode_cli.py`)**:
   - Integrated command-line interface running on the development VM / IDE.
   - Allows fetching problem statements, generating solution templates, and submitting code directly to LeetCode with instant test-case execution and optional auto-git commit/push.

---

## 🛠️ CLI Usage (On VM / Dev Environment)

### 1. Check Account & Problem Stats
```bash
./tools/leetcode_cli.py status
```

### 2. Fetch Problem Statement & Boilerplate
```bash
./tools/leetcode_cli.py fetch two-sum --lang python3
# or
./tools/leetcode_cli.py fetch longest-substring-without-repeating-characters --lang python3
```
This automatically creates:
- `solutions/<id>-<slug>/README.md` (clean Markdown problem description & tags)
- `solutions/<id>-<slug>/solution.py` (starter code template)
- `solutions/<id>-<slug>/.meta.json` (metadata for submissions)

### 3. Solve & Submit Directly to LeetCode
```bash
# Submit to LeetCode and inspect execution:
./tools/leetcode_cli.py submit solutions/0001-two-sum/solution.py

# Submit and automatically commit & push on ACCEPTED:
./tools/leetcode_cli.py submit solutions/0001-two-sum/solution.py --git
```

---

## 📂 Solutions Index

| # | Title | Difficulty | Solution | Status |
|---|---|---|---|---|
| 0001 | [Two Sum](https://leetcode.com/problems/two-sum/) | Easy | [Python3](./solutions/0001-two-sum/solution.py) | ✅ Solved |

---

*Powered by Antigravity Automation & GitHub Actions.*
