# 167. Two Sum II - Input Array Is Sorted

**Difficulty:** Medium  
**Tags:** Array, Two Pointers, Binary Search  
**LeetCode Link:** [https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)

---

## Problem Description

You are given a **1-indexed** array of integers `numbers` that is already **sorted in non-decreasing order**.



Find **two** numbers such that they add up to a specific `target` number. Let these two numbers be `numbers[index1]` and `numbers[index2]` where `1 1 2 1` and `index2` as an integer array `[index1, index2]` of length 2.



The tests are generated such that there is **exactly one solution**. You **may not** use the same element twice.



Your solution must use only constant extra space.



 


Example 1:

```

**Input:** numbers = [2,7,11,15], target = 9
**Output:** [1,2]
**Explanation:** The sum of 2 and 7 is 9. Therefore, index1 = 1, index2 = 2. We return [1, 2].

```



Example 2:

```

**Input:** numbers = [2,3,4], target = 6
**Output:** [1,3]
**Explanation:** The sum of 2 and 4 is 6. Therefore index1 = 1, index2 = 3. We return [1, 3].

```



Example 3:

```

**Input:** numbers = [-1,0], target = -1
**Output:** [1,2]
**Explanation:** The sum of -1 and 0 is -1. Therefore index1 = 1, index2 = 2. We return [1, 2].

```



 


**Constraints:**


	
- `2 4`
	
- `-1000


---

## Algorithmic Complexity & Proof

- **Technique:** Two Pointers
- **Time Complexity:** $O(N)$
- **Space Complexity:** $O(1)$

### Proof & Mathematical Analysis
The array 'numbers' is sorted. We initialize two pointers, 'left' at the beginning (index 0) and 'right' at the end (index N-1). In each iteration of the loop, we calculate the sum of elements at 'left' and 'right'.
1. If the sum equals the target, we have found our pair and return their 1-indexed positions.
2. If the sum is less than the target, we need a larger sum. Since the array is sorted in non-decreasing order, moving the 'left' pointer to the right (left++) will increase or keep the same the value of numbers[left], thus increasing or keeping the same the total sum. We choose to increase it to get closer to the target.
3. If the sum is greater than the target, we need a smaller sum. Moving the 'right' pointer to the left (right--) will decrease or keep the same the value of numbers[right], thus decreasing or keeping the same the total sum. We choose to decrease it to get closer to the target.

In every step, either the 'left' pointer increments or the 'right' pointer decrements. This means the pointers move towards each other, and the loop terminates when 'left' >= 'right'. Since the pointers traverse the array at most once, the time complexity is linear, O(N), where N is the number of elements in 'numbers'.

For space complexity, we only use a few variables ('left', 'right', 'current_sum') to store indices and the sum, which consume a constant amount of memory regardless of the input array size. Therefore, the space complexity is O(1).
