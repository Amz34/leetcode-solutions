# 125. Valid Palindrome

**Difficulty:** Easy  
**Tags:** Two Pointers, String  
**LeetCode Link:** [https://leetcode.com/problems/valid-palindrome/](https://leetcode.com/problems/valid-palindrome/)

---

## Problem Description

A phrase is a **palindrome** if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.



Given a string `s`, return `true`* if it is a **palindrome**, or *`false`* otherwise*.



 


Example 1:

```

**Input:** s = "A man, a plan, a canal: Panama"
**Output:** true
**Explanation:** "amanaplanacanalpanama" is a palindrome.

```



Example 2:

```

**Input:** s = "race a car"
**Output:** false
**Explanation:** "raceacar" is not a palindrome.

```



Example 3:

```

**Input:** s = " "
**Output:** true
**Explanation:** s is an empty string "" after removing non-alphanumeric characters.
Since an empty string reads the same forward and backward, it is a palindrome.

```



 


**Constraints:**


	
- `1 5`
	
- `s` consists only of printable ASCII characters.


---

## Algorithmic Complexity & Proof

- **Technique:** Two Pointers
- **Time Complexity:** $O(N)$
- **Space Complexity:** $O(1)$

### Proof & Mathematical Analysis
Time Complexity: The algorithm uses two pointers, 'left' and 'right', initialized at the beginning and end of the string, respectively. In each iteration of the main loop, at least one of the pointers moves towards the center. The inner loops for advancing 'left' and 'right' pointers also ensure that each character in the string is visited at most a constant number of times (once by 'left' and once by 'right'). Character checks (isalnum) and conversions (tolower) are O(1) operations. Therefore, the total time taken is directly proportional to the length of the string, N. Hence, the time complexity is O(N).

Space Complexity: The algorithm uses a fixed number of variables (two integer pointers, temporary character storage for comparison) regardless of the input string's length. No auxiliary data structures that grow with the input size are created. Thus, the space complexity is O(1). For the Rust solution, the use of iterators (`filter`, `map`) is lazy and does not create intermediate collections, maintaining O(1) auxiliary space.
