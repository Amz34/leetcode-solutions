# 15. 3Sum

**Difficulty:** Medium  
**Tags:** Array, Two Pointers, Sorting  
**LeetCode Link:** [https://leetcode.com/problems/3sum/](https://leetcode.com/problems/3sum/)

---

## Problem Description

Given an integer array nums, return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.



Notice that the solution set must not contain duplicate triplets.



 


Example 1:

```

**Input:** nums = [-1,0,1,2,-1,-4]
**Output:** [[-1,-1,2],[-1,0,1]]
**Explanation:** 
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
The distinct triplets are [-1,0,1] and [-1,-1,2].
Notice that the order of the output and the order of the triplets does not matter.

```



Example 2:

```

**Input:** nums = [0,1,1]
**Output:** []
**Explanation:** The only possible triplet does not sum up to 0.

```



Example 3:

```

**Input:** nums = [0,0,0]
**Output:** [[0,0,0]]
**Explanation:** The only possible triplet sums up to 0.

```



 


**Constraints:**


	
- `3 5 5`


---

## Algorithmic Complexity & Proof

- **Technique:** Sorting and Two Pointers. The array is first sorted to enable efficient searching and duplicate handling. Then, a single pointer iterates through the array, and for each element, two additional pointers (left and right) are used to find the remaining two numbers that sum to zero. Duplicate triplets are avoided by skipping elements that are identical to their predecessors.
- **Time Complexity:** $O(N^2)$
- **Space Complexity:** $O(N)$

### Proof & Mathematical Analysis
Time Complexity:
1. Sorting the input array `nums` takes `O(N log N)` time, where `N` is the number of elements in `nums`.
2. The main loop iterates with pointer `i` from `0` to `N-3`. In the worst case, this loop runs `N` times.
3. Inside the main loop, the two-pointer approach (with `left` and `right` pointers) traverses the remaining part of the array. In each iteration of the inner `while` loop, either `left` is incremented or `right` is decremented, meaning the `left` and `right` pointers together make at most `N` steps for a fixed `i`.
4. Therefore, the nested loops contribute `O(N * N) = O(N^2)` time.
5. Combining sorting and the nested loops, the total time complexity is `O(N log N + N^2)`, which simplifies to `O(N^2)` as `N^2` dominates `N log N` for large `N`.

Space Complexity:
1. The auxiliary space required for sorting depends on the specific algorithm used. Python's `list.sort()` (Timsort) uses `O(N)` space in the worst case. C++ `std::sort` typically uses `O(log N)` auxiliary space (Introsort). If an in-place sort like Heapsort is used, it's `O(1)` auxiliary space. For a general analysis, `O(N)` is a safe upper bound for sorting auxiliary space.
2. The variables `i`, `left`, `right`, `current_sum`, etc., use `O(1)` auxiliary space.
3. The `result` list stores the triplets. In the worst case, the number of unique triplets can be `O(N^2)` (e.g., if `nums` contains many zeros and many positive/negative pairs that sum to zero). Each triplet has 3 integers. Thus, the space for the output list is `O(N^2)`.
4. When competitive programming problems ask for space complexity, they often refer to auxiliary space *excluding* the output. In that context, the space complexity is `O(N)` (due to sorting) or `O(1)` (if sorting is considered in-place). We state `O(N)` to account for typical sorting implementations, acknowledging that the output list itself can take `O(N^2)` space.
