#!/usr/bin/env /home/ubuntu/.venvs/antigravity/bin/python
"""
AI Algorithmic Co-Pilot & Polyglot Synthesizer
===============================================
Synthesizes optimal asymptotic solutions (Python, Rust, C++),
extracts test cases, and proves complexity proofs using Gemini 2.5 Flash.

Author: Amz34 / Antigravity
"""

import os
import sys
import json
import re
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent.parent
SOLUTIONS_DIR = REPO_DIR / "solutions"

def solve_problem_ai(slug: str):
    from google import genai
    from google.genai import types

    client = genai.Client()

    # Find problem folder
    matched = list(SOLUTIONS_DIR.glob(f"*-{slug}"))
    if not matched:
        print(f"❌ Problem directory for '{slug}' not found under solutions/.")
        return False
    target_dir = matched[0]
    readme_path = target_dir / "README.md"
    if not readme_path.exists():
        print(f"❌ Problem README not found at {readme_path}")
        return False

    with open(readme_path, "r", encoding="utf-8") as f:
        problem_desc = f.read()

    meta_path = target_dir / ".meta.json"
    title = slug
    if meta_path.exists():
        with open(meta_path, "r", encoding="utf-8") as f:
            title = json.load(f).get("title", slug)

    print(f"\n🧠 Synthesizing optimal algorithmic solution for: {title} via Gemini 2.5 Flash...")

    prompt = f"""You are a World-Class Competitive Programmer & Senior Systems Engineer.
Solve the following LeetCode problem with the absolute lowest theoretical time & space complexity.

Problem Description:
{problem_desc}

Provide your response in strictly valid JSON with the following structure:
{{
  "approach": "Brief description of the optimal algorithmic technique used (e.g., Hash Set, Two Pointers, Dynamic Programming, Monotonic Stack)",
  "time_complexity": "O(...)",
  "space_complexity": "O(...)",
  "proof": "Concise mathematical proof of time and space complexity",
  "python3_code": "Complete Python 3 code starting with class Solution: ...",
  "rust_code": "Complete Rust code starting with pub struct Solution; impl Solution { ... }",
  "cpp_code": "Complete C++ code starting with #include <vector> ... class Solution { ... };",
  "test_cases": [
    {{
      "input": [param1, param2],
      "expected": expected_result
    }}
  ]
}}

Requirements:
1. Python code MUST use standard LeetCode class/method signatures.
2. Rust code MUST include 'pub struct Solution;' before 'impl Solution'.
3. C++ code MUST include standard headers and 'using namespace std;'.
4. Test cases MUST match the example inputs/outputs from the problem description. Each input list must be the arguments to the function in order.
5. Return ONLY the JSON object. Do not include markdown code block wrapper."""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.1,
            response_mime_type="application/json"
        )
    )

    try:
        data = json.loads(response.text)
    except Exception as e:
        # Fallback sanitize raw text in case of unescaped quotes/backslashes
        import re
        clean_text = response.text.strip()
        if clean_text.startswith("```"):
            clean_text = re.sub(r"^```[a-zA-Z]*\n", "", clean_text)
            clean_text = re.sub(r"\n```$", "", clean_text)
        try:
            data = json.loads(clean_text, strict=False)
        except Exception:
            # Retry with explicit json schema or repair
            print(f"⚠️ JSON parse issue ({e}), attempting resilient repair...")
            repair_prompt = f"Fix this broken JSON string and return ONLY valid RFC 8259 JSON:\n{response.text}"
            repaired = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=repair_prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )
            try:
                data = json.loads(repaired.text)
            except Exception as e2:
                print(f"❌ Failed to parse AI response JSON after repair: {e2}")
                return False

    py_code = data.get("python3_code", "").strip()
    rs_code = data.get("rust_code", "").strip()
    cpp_code = data.get("cpp_code", "").strip()
    tests = data.get("test_cases", [])
    approach = data.get("approach", "")
    time_comp = data.get("time_complexity", "")
    space_comp = data.get("space_complexity", "")
    proof = data.get("proof", "")

    # Write Python solution
    if py_code:
        with open(target_dir / "solution.py", "w", encoding="utf-8") as f:
            f.write(py_code + "\n")
        print(f"  ✅ Synthesized Python3 solution")

    # Write Rust solution
    if rs_code:
        with open(target_dir / "solution.rs", "w", encoding="utf-8") as f:
            f.write(rs_code + "\n")
        print(f"  ✅ Synthesized Rust solution")

    # Write C++ solution
    if cpp_code:
        with open(target_dir / "solution.cpp", "w", encoding="utf-8") as f:
            f.write(cpp_code + "\n")
        print(f"  ✅ Synthesized C++ solution")

    # Write tests.json
    if tests:
        with open(target_dir / "tests.json", "w", encoding="utf-8") as f:
            json.dump(tests, f, indent=2)
        print(f"  ✅ Extracted {len(tests)} unit test cases into tests.json")

    # Append complexity proof to README.md
    with open(readme_path, "r", encoding="utf-8") as f:
        existing = f.read()

    if "## Algorithmic Complexity & Proof" not in existing:
        addition = f"""

---

## Algorithmic Complexity & Proof

- **Technique:** {approach}
- **Time Complexity:** ${time_comp}$
- **Space Complexity:** ${space_comp}$

### Proof & Mathematical Analysis
{proof}
"""
        with open(readme_path, "a", encoding="utf-8") as f:
            f.write(addition)
        print(f"  ✅ Appended complexity proof to README.md")

    print(f"\n🎉 Polyglot solutions and unit tests successfully synthesized for {slug}!")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ai_solver.py <problem-slug>")
        sys.exit(1)
    success = solve_problem_ai(sys.argv[1])
    sys.exit(0 if success else 1)
