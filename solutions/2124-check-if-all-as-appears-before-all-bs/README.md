# 2124. Check if All A's Appears Before All B's

**Date:** 2026-11-22 (Daily Challenge)  
**Difficulty:** Easy  
**Tags:** String  
**LeetCode Link:** [https://leetcode.com/problems/check-if-all-as-appears-before-all-bs/](https://leetcode.com/problems/check-if-all-as-appears-before-all-bs/)

---

## Problem Description

Given a string `s` consisting of **only** the characters `&#39;a&#39;` and `&#39;b&#39;`, return `true` *if **every** *`&#39;a&#39;` *appears before **every** *`&#39;b&#39;`* in the string*. Otherwise, return `false`.



 


Example 1:

```

**Input:** s = "aaabbb"
**Output:** true
**Explanation:**
The &#39;a&#39;s are at indices 0, 1, and 2, while the &#39;b&#39;s are at indices 3, 4, and 5.
Hence, every &#39;a&#39; appears before every &#39;b&#39; and we return true.

```



Example 2:

```

**Input:** s = "abab"
**Output:** false
**Explanation:**
There is an &#39;a&#39; at index 2 and a &#39;b&#39; at index 1.
Hence, not every &#39;a&#39; appears before every &#39;b&#39; and we return false.

```



Example 3:

```

**Input:** s = "bbb"
**Output:** true
**Explanation:**
There are no &#39;a&#39;s, hence, every &#39;a&#39; appears before every &#39;b&#39; and we return true.

```



 


**Constraints:**


	
- `1
