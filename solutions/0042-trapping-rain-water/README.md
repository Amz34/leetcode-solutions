# 42. Trapping Rain Water

**Difficulty:** Hard  
**Tags:** Array, Two Pointers, Dynamic Programming, Stack, Monotonic Stack  
**LeetCode Link:** [https://leetcode.com/problems/trapping-rain-water/](https://leetcode.com/problems/trapping-rain-water/)

---

## Problem Description

Given `n` non-negative integers representing an elevation map where the width of each bar is `1`, compute how much water it can trap after raining.



 


Example 1:

```

**Input:** height = [0,1,0,2,1,0,1,3,2,1,2,1]
**Output:** 6
**Explanation:** The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped.

```



Example 2:

```

**Input:** height = [4,2,0,3,2,5]
**Output:** 9

```



 


**Constraints:**


	
- `n == height.length`
	
- `1 4`
	
- `0 5`


---

## Algorithmic Complexity & Proof

- **Technique:** Two Pointers
- **Time Complexity:** $O(N)$
- **Space Complexity:** $O(1)$

### Proof & Mathematical Analysis
Time Complexity: The algorithm uses two pointers, `left` and `right`, initialized at the beginning and end of the `height` array, respectively. In each iteration of the `while` loop, either `left` is incremented or `right` is decremented. Since `left` starts at 0 and `right` starts at `n-1`, and they move towards each other, the loop will run at most `n` times (until `left > right`). Each operation inside the loop (comparisons, assignments, additions) takes constant time. Therefore, the total time complexity is O(N).

Space Complexity: The algorithm uses a fixed number of variables (`left`, `right`, `left_max`, `right_max`, `total_water`) regardless of the input array size `n`. These variables consume a constant amount of memory. Therefore, the space complexity is O(1).
