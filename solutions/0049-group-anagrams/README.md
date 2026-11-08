# 49. Group Anagrams

**Difficulty:** Medium  
**Tags:** Array, Hash Table, String, Sorting  
**LeetCode Link:** [https://leetcode.com/problems/group-anagrams/](https://leetcode.com/problems/group-anagrams/)

---

## Problem Description

Given an array of strings `strs`, group the anagrams together. You can return the answer in **any order**.



 


Example 1:




**Input:** strs = ["eat","tea","tan","ate","nat","bat"]



**Output:** [["bat"],["nat","tan"],["ate","eat","tea"]]



**Explanation:**


	
- There is no string in strs that can be rearranged to form `"bat"`.
	
- The strings `"nat"` and `"tan"` are anagrams as they can be rearranged to form each other.
	
- The strings `"ate"`, `"eat"`, and `"tea"` are anagrams as they can be rearranged to form each other.





Example 2:




**Input:** strs = [""]



**Output:** [[""]]




Example 3:




**Input:** strs = ["a"]



**Output:** [["a"]]




 


**Constraints:**


	
- `1 4`
	
- `0


---

## Algorithmic Complexity & Proof

- **Technique:** Hash Map with Character Count Array/Tuple as Key
- **Time Complexity:** $O(N * L)$
- **Space Complexity:** $O(N * L)$

### Proof & Mathematical Analysis
Let N be the number of strings in the input array `strs`, and L be the maximum length of a string in `strs`. Let K be the size of the alphabet (26 for lowercase English letters). The algorithm iterates through each of the N strings. For each string `s` of length `L_i`:
1. A character count array (of size K) is initialized and populated. This involves iterating through each character of `s`, taking O(L_i) time. Each character lookup and increment is O(1).
2. The character count array is used as a key for a hash map. Creating this key (e.g., converting to a tuple in Python, or using `std::array` in C++ / `[i32; 26]` in Rust) takes O(K) time. Hashing this key for map insertion/lookup also takes O(K) time on average.
3. The string `s` is then appended to the list associated with this key in the hash map. This is an O(1) operation on average.
Summing over all N strings, the total time complexity is O(Sum(L_i) + N*K). Since Sum(L_i) is at most N*L, and K is a constant (26), this simplifies to O(N*L). This is theoretically optimal because every character of every string must be examined at least once to determine anagram relationships.

The space complexity is determined by the storage required for the hash map. In the worst case, all N strings are distinct and not anagrams of each other, meaning the hash map will store N entries. Each entry consists of a key (the character count array, taking O(K) space) and a value (a list containing one string, taking O(L) space for the string itself). Thus, the total space for the hash map's values is O(Sum(L_i)), which is O(N*L) in the worst case. The space for the keys is O(N*K). Since K is a constant, the dominant factor is O(N*L). This is also optimal because the output itself (a list of lists of strings) must store all the input strings, requiring O(N*L) space.
