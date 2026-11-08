# ⚡ LeetCode Solutions Vault & Algorithmic Excellence

<div align="center">
  <a href="https://leetcode.com/u/amz34/">
    <img src="https://leetcard.jacoblin.cool/amz34?theme=dark&font=Ubuntu" alt="LeetCode Stats" />
  </a>
</div>

---

### 📊 Real-Time Metrics & Breakdown

| Category | Metric | Status |
|:---|:---|:---|
| **Total Solved** | **2** | <img src="https://img.shields.io/badge/LeetCode-2%20Solved-blue?style=flat-square&logo=leetcode" /> |
| **Easy** | **1** | <img src="https://img.shields.io/badge/Easy-1-00B8A3?style=flat-square" /> |
| **Medium** | **1** | <img src="https://img.shields.io/badge/Medium-1-FFC01E?style=flat-square" /> |
| **Hard** | **0** | <img src="https://img.shields.io/badge/Hard-0-FF375F?style=flat-square" /> |
| **Sync Engine** | Stealth Chromium Daemon | `Operational` (2h Interval + GitHub Actions) |

---

## 🚀 Enterprise Architecture

1. **Stealth Headless Chromium Automation (`tools/headless_chromium_sync.py`)**:
   - Driven by **Patchright** (stealth Playwright fork) and real Google Chrome to bypass Cloudflare bot shields.
   - Runs locally on schedule (every 2 hours via cron) to extract full code, runtimes, and memory percentiles.
2. **Cloud-Native Auto-Sync (`.github/workflows/leetcode-sync.yml`)**:
   - Secondary cloud backup running on GitHub Actions every 6 hours using encrypted repository secrets.
3. **VM / IDE Bi-Directional CLI (`tools/leetcode_cli.py`)**:
   - Full CLI workflow for daily challenge fetching, solution scaffolding, and zero-browser submissions.

---

## 🛠️ CLI Commands (On VM / Dev Environment)

```bash
# Check LeetCode profile connection & stats
./tools/leetcode_cli.py status

# Fetch today's LeetCode Problem of the Day (POTD)
./tools/leetcode_cli.py daily

# Fetch any arbitrary problem by slug
./tools/leetcode_cli.py fetch count-servers-that-communicate --lang python3

# Submit solution directly to LeetCode with instant testcase run & auto-push
./tools/leetcode_cli.py submit solutions/0001-two-sum/solution.py --git

# Regenerate dynamic README dashboard & table
./tools/leetcode_cli.py dashboard
```

---

## 📂 Algorithmic Solutions Index

| # | Title | Difficulty | Solution | Performance |
|:---:|:---|:---:|:---:|:---:|
| 0001 | [Two Sum](https://leetcode.com/problems/two-sum/) | <img src="https://img.shields.io/badge/-Easy-00B8A3?style=flat-square" /> | [`python3`](./solutions/0001-two-sum/solution.py) | `1 ms` |
| 1267 | [Count Servers that Communicate](https://leetcode.com/problems/count-servers-that-communicate/) | <img src="https://img.shields.io/badge/-Medium-FFC01E?style=flat-square" /> | [`python3`](./solutions/1267-count-servers-that-communicate/solution.py) | `14 ms` |

---

*Architected and maintained autonomously by [Aamir Zameer (@Amz34)](https://github.com/Amz34) & Antigravity AI.*
