# 11. Container With Most Water

**Difficulty:** Medium  
**Tags:** Array, Two Pointers, Greedy  
**LeetCode Link:** [https://leetcode.com/problems/container-with-most-water/](https://leetcode.com/problems/container-with-most-water/)

---

## Problem Description

You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the `ith` line are `(i, 0)` and `(i, height[i])`.



Find two lines that together with the x-axis form a container, such that the container contains the most water.



Return *the maximum amount of water a container can store*.



**Notice** that you may not slant the container.



 


Example 1:

```

**Input:** height = [1,8,6,2,5,4,8,3,7]
**Output:** 49
**Explanation:** The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. In this case, the max area of water (blue section) the container can contain is 49.

```



Example 2:

```

**Input:** height = [1,1]
**Output:** 1

```



 


**Constraints:**


	
- `n == height.length`
	
- `2 5`
	
- `0 4`


---

## Algorithmic Complexity & Proof

- **Technique:** Two Pointers
- **Time Complexity:** $O(n)$
- **Space Complexity:** $O(1)$

### Proof & Mathematical Analysis
The algorithm uses two pointers, 'left' and 'right', initialized at the beginning (index 0) and end (index n-1) of the array respectively. In each iteration, it calculates the area formed by the lines at 'left' and 'right': `min(height[left], height[right]) * (right - left)`. The maximum area found so far is updated. The crucial step is deciding which pointer to move. To potentially increase the area, we must try to increase the limiting height, because the width `(right - left)` will always decrease or stay the same as pointers move inwards. If `height[left] < height[right]`, then `height[left]` is the bottleneck. Moving `right` inwards would decrease the width, and the height would still be limited by `height[left]` (or potentially a new, even smaller `height[right]`). However, moving `left` inwards might find a taller line at `left+1`, which could increase the minimum height and potentially lead to a larger area despite the reduced width. A symmetric argument applies if `height[right] < height[left]`. If `height[left] == height[right]`, either pointer can be moved; moving one (e.g., `left`) is sufficient. This greedy strategy is proven correct by contradiction: Assume, without loss of generality, that `height[left] <= height[right]`, and we move `left` to `left+1`. Suppose there exists an optimal container `(L_opt, R_opt)` such that `L_opt = left` and `R_opt < right`. Its area would be `A_opt = min(height[left], height[R_opt]) * (R_opt - left)`. We know `A_opt <= height[left] * (R_opt - left)`. The area of the container formed by our current pointers `(left, right)` is `A_current = min(height[left], height[right]) * (right - left) = height[left] * (right - left)` (since `height[left] <= height[right]`). Since `R_opt < right`, it follows that `(R_opt - left) < (right - left)`. Therefore, `height[left] * (R_opt - left) < height[left] * (right - left)`. This implies `A_opt < A_current`, which contradicts the assumption that `(L_opt, R_opt)` is an optimal solution. Thus, we can safely discard the shorter line and move its corresponding pointer inwards. Since each step moves one pointer, and pointers only move towards each other, the loop runs at most `n-1` times, resulting in O(n) time complexity. Only a constant number of variables are used, leading to O(1) space complexity.
