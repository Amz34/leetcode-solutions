# 128. Longest Consecutive Sequence

**Difficulty:** Medium  
**Tags:** Array, Hash Table, Union-Find  
**LeetCode Link:** [https://leetcode.com/problems/longest-consecutive-sequence/](https://leetcode.com/problems/longest-consecutive-sequence/)

---

## Problem Description

Given an unsorted array of integers `nums`, return *the length of the longest consecutive elements sequence.*



You must write an algorithm that runs in `O(n)` time.



 


Example 1:

```

**Input:** nums = [100,4,200,1,3,2]
**Output:** 4
**Explanation:** The longest consecutive elements sequence is `[1, 2, 3, 4]`. Therefore its length is 4.

```



Example 2:

```

**Input:** nums = [0,3,7,2,5,8,4,6,0,1]
**Output:** 9

```



Example 3:

```

**Input:** nums = [1,0,1,2]
**Output:** 3

```



 


**Constraints:**


	
- `0 5`
	
- `-109 9`


---

## Algorithmic Complexity & Proof

- **Technique:** Hash Set
- **Time Complexity:** $O(n)$
- **Space Complexity:** $O(n)$

### Proof & Mathematical Analysis
The algorithm first inserts all 'n' numbers into a hash set. This operation takes O(n) time on average. Then, it iterates through each number in the hash set. For each number 'x', it checks if 'x-1' exists in the set. If 'x-1' does not exist, 'x' is considered the potential start of a consecutive sequence. The algorithm then extends this sequence by checking for 'x+1', 'x+2', and so on, until a number is not found. Each number in the input array is processed at most a constant number of times: once for insertion into the set, once as a potential starting point (checking 'x-1'), and at most once as part of extending a sequence (checking 'x+k'). Therefore, the total time complexity is O(n) on average. The space complexity is O(n) because, in the worst case, all 'n' unique numbers are stored in the hash set.
