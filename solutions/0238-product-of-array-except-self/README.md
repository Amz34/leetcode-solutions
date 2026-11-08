# 238. Product of Array Except Self

**Difficulty:** Medium  
**Tags:** Array, Prefix Sum  
**LeetCode Link:** [https://leetcode.com/problems/product-of-array-except-self/](https://leetcode.com/problems/product-of-array-except-self/)

---

## Problem Description

Given an integer array `nums`, return *an array* `answer` *such that* `answer[i]` *is equal to the product of all the elements of* `nums` *except* `nums[i]`.



The product of any prefix or suffix of `nums` is **guaranteed** to fit in a **32-bit** integer.



You must write an algorithm that runs in `O(n)` time and without using the division operation.



 


Example 1:
```
**Input:** nums = [1,2,3,4]
**Output:** [24,12,8,6]

```

Example 2:
```
**Input:** nums = [-1,1,0,-3,3]
**Output:** [0,0,9,0,0]

```


 


**Constraints:**


	
- `2 5`
	
- `-30 



 


**Follow up:** Can you solve the problem in `O(1)` extra space complexity? (The output array **does not** count as extra space for space complexity analysis.)


---

## Algorithmic Complexity & Proof

- **Technique:** Prefix and Suffix Products (Optimized Space)
- **Time Complexity:** $O(n)$
- **Space Complexity:** $O(1)$

### Proof & Mathematical Analysis
Time Complexity: The algorithm involves two main passes over the input array `nums`. The first pass iterates from the second element to the end (n-1 iterations) to compute prefix products and store them in the `answer` array. The second pass iterates from the last element down to the first (n iterations) to compute suffix products and combine them with the already stored prefix products. Each iteration involves a constant number of arithmetic operations and assignments. Therefore, the total number of operations is proportional to (n-1) + n, which simplifies to O(n).

Space Complexity: We initialize an `answer` array of size `n` to store the results. As per the problem statement, the output array does not count towards extra space complexity. We use a single additional variable, `right_product`, to keep track of the product of elements to the right of the current index during the second pass. This variable consumes a constant amount of memory, i.e., O(1) space. Thus, the overall extra space complexity is O(1).
