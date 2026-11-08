# 242. Valid Anagram

**Difficulty:** Easy  
**Tags:** Hash Table, String, Sorting  
**LeetCode Link:** [https://leetcode.com/problems/valid-anagram/](https://leetcode.com/problems/valid-anagram/)

---

## Problem Description

Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, and `false` otherwise.



 


Example 1:




**Input:** s = "anagram", t = "nagaram"



**Output:** true




Example 2:




**Input:** s = "rat", t = "car"



**Output:** false




 


**Constraints:**


	
- `1 4`
	
- `s` and `t` consist of lowercase English letters.




 


**Follow up:** What if the inputs contain Unicode characters? How would you adapt your solution to such a case?


---

## Algorithmic Complexity & Proof

- **Technique:** Frequency Counter (Array)
- **Time Complexity:** $O(N)$
- **Space Complexity:** $O(1)$

### Proof & Mathematical Analysis
Time Complexity: The solution first checks if the lengths of strings `s` and `t` are equal, which is an O(1) operation. It then iterates through string `s` once to increment character counts (O(N)), and then iterates through string `t` once to decrement character counts (O(N)). Finally, it iterates through a fixed-size array of 26 integers to check if all counts are zero (O(26), which simplifies to O(1)). Therefore, the total time complexity is O(N) + O(N) + O(1) = O(N), where N is the length of the strings.
Space Complexity: A fixed-size array of 26 integers is used to store the frequency of lowercase English letters. This array's size is constant and does not depend on the input string lengths. Hence, the space complexity is O(26), which simplifies to O(1).
