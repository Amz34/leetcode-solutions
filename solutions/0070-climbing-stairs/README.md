# 70. Climbing Stairs

**Difficulty:** Easy  
**Tags:** Math, Dynamic Programming, Memoization  
**LeetCode Link:** [https://leetcode.com/problems/climbing-stairs/](https://leetcode.com/problems/climbing-stairs/)

---

## Problem Description

You are climbing a staircase. It takes `n` steps to reach the top.



Each time you can either climb `1` or `2` steps. In how many distinct ways can you climb to the top?



 


Example 1:

```

**Input:** n = 2
**Output:** 2
**Explanation:** There are two ways to climb to the top.
1. 1 step + 1 step
2. 2 steps

```



Example 2:

```

**Input:** n = 3
**Output:** 3
**Explanation:** There are three ways to climb to the top.
1. 1 step + 1 step + 1 step
2. 1 step + 2 steps
3. 2 steps + 1 step

```



 


**Constraints:**


	
- `1


---

## Algorithmic Complexity & Proof

- **Technique:** Dynamic Programming with space optimization. The problem can be modeled as finding the Nth Fibonacci number. To reach step 'i', one can either take 1 step from 'i-1' or 2 steps from 'i-2'. Thus, the number of ways to reach step 'i' is the sum of ways to reach 'i-1' and 'i-2'. This forms the Fibonacci recurrence relation: `dp[i] = dp[i-1] + dp[i-2]`. Base cases are `dp[1]=1` (one way to reach step 1: (1)) and `dp[2]=2` (two ways to reach step 2: (1,1), (2)). The solution iteratively calculates these values, only storing the two previous results to achieve O(1) space complexity.
- **Time Complexity:** $O(n)$
- **Space Complexity:** $O(1)$

### Proof & Mathematical Analysis
Time Complexity: The algorithm uses a single loop that iterates from `i = 3` up to `n`. In each iteration, a constant number of arithmetic operations (addition, assignments) are performed. Therefore, the total number of operations is directly proportional to `n`, resulting in a time complexity of O(n). While matrix exponentiation can achieve O(log n) for Fibonacci numbers, for the given constraint `n <= 45`, the O(n) iterative approach is simpler, often faster in practice due to smaller constant factors, and considered optimal for typical competitive programming scenarios.

Space Complexity: The algorithm maintains only three variables (`dp_i_minus_2`, `dp_i_minus_1`, `current_dp`) to store the necessary previous results. The amount of memory used does not grow with the input `n`. Hence, the space complexity is constant, O(1).
