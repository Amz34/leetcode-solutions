# 217. Contains Duplicate

**Difficulty:** Easy  
**Tags:** Array, Hash Table, Sorting  
**LeetCode Link:** [https://leetcode.com/problems/contains-duplicate/](https://leetcode.com/problems/contains-duplicate/)

---

## Problem Description

Given an integer array `nums`, return `true` if any value appears **at least twice** in the array, and return `false` if every element is distinct.



 


Example 1:




**Input:** nums = [1,2,3,1]



**Output:** true



**Explanation:**



The element 1 occurs at the indices 0 and 3.




Example 2:




**Input:** nums = [1,2,3,4]



**Output:** false



**Explanation:**



All elements are distinct.




Example 3:




**Input:** nums = [1,1,1,3,3,4,3,2,4,2]



**Output:** true




 


**Constraints:**


	
- `1 5`
	
- `-109 9`


---

## Algorithmic Complexity & Proof

- **Technique:** Hash Set
- **Time Complexity:** $O(N)$
- **Space Complexity:** $O(N)$

### Proof & Mathematical Analysis
Time Complexity: We iterate through the input array `nums` exactly once. For each element, we perform a lookup and potentially an insertion into a hash set. On average, hash set operations (insertion and lookup) take O(1) time. Therefore, the total time complexity is O(N * 1) = O(N), where N is the number of elements in `nums`.

Space Complexity: In the worst-case scenario, all elements in `nums` are distinct. In this situation, we would add all N elements to the hash set. Each element requires a constant amount of space. Thus, the space complexity is O(N).
