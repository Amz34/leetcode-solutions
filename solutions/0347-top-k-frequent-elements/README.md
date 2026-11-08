# 347. Top K Frequent Elements

**Difficulty:** Medium  
**Tags:** Array, Hash Table, Divide and Conquer, Sorting, Heap (Priority Queue), Bucket Sort, Counting, Quickselect  
**LeetCode Link:** [https://leetcode.com/problems/top-k-frequent-elements/](https://leetcode.com/problems/top-k-frequent-elements/)

---

## Problem Description

Given an integer array `nums` and an integer `k`, return *the* `k` *most frequent elements*. You may return the answer in **any order**.



 


Example 1:




**Input:** nums = [1,1,1,2,2,3], k = 2



**Output:** [1,2]




Example 2:




**Input:** nums = [1], k = 1



**Output:** [1]




Example 3:




**Input:** nums = [1,2,1,2,1,2,3,1,3,2], k = 2



**Output:** [1,2]




 


**Constraints:**


	
- `1 5`
	
- `-104 4`
	
- `k` is in the range `[1, the number of unique elements in the array]`.
	
- It is **guaranteed** that the answer is **unique**.




 


**Follow up:** Your algorithm&#39;s time complexity must be better than `O(n log n)`, where n is the array&#39;s size.


---

## Algorithmic Complexity & Proof

- **Technique:** Bucket Sort (Frequency Array)
- **Time Complexity:** $O(N)$
- **Space Complexity:** $O(N)$

### Proof & Mathematical Analysis
1. Frequency Counting: Using a hash map (e.g., Python's collections.Counter, C++'s unordered_map, Rust's HashMap) to count occurrences of each number takes O(N) time, where N is the number of elements in 'nums'. In the worst case, all elements are unique, so the hash map stores N entries. This requires O(U) space, where U is the number of unique elements (U <= N), thus O(N) space.
2. Bucket Creation and Population: An array of lists (buckets) is created, where the index represents a frequency and the list at that index stores numbers with that frequency. The maximum possible frequency is N, so the bucket array has size N+1. Initializing this array takes O(N) time and O(N) space. Populating the buckets by iterating through the hash map takes O(U) time, as each unique number is placed into its corresponding frequency bucket.
3. Collecting Top K Elements: The algorithm iterates through the buckets from the highest possible frequency (N) down to 1. For each frequency, it adds all numbers in that bucket to the result list until k elements are collected. In the worst case, this iteration might traverse all N+1 buckets. The total number of elements processed from the buckets is at most U. This step takes O(N) time.
Combining these steps, the total time complexity is O(N) + O(N) + O(U) + O(N) = O(N). The total space complexity is O(N) for the hash map and O(N) for the buckets array, resulting in O(N) space.
