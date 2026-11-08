# 36. Valid Sudoku

**Difficulty:** Medium  
**Tags:** Array, Hash Table, Matrix  
**LeetCode Link:** [https://leetcode.com/problems/valid-sudoku/](https://leetcode.com/problems/valid-sudoku/)

---

## Problem Description

Determine if a `9 x 9` Sudoku board is valid. Only the filled cells need to be validated **according to the following rules**:


	
- Each row must contain the digits `1-9` without repetition.
	
- Each column must contain the digits `1-9` without repetition.
	
- Each of the nine `3 x 3` sub-boxes of the grid must contain the digits `1-9` without repetition.




**Note:**


	
- A Sudoku board (partially filled) could be valid but is not necessarily solvable.
	
- Only the filled cells need to be validated according to the mentioned rules.




 


Example 1:

```

**Input:** board = 
[["5","3",".",".","7",".",".",".","."]
,["6",".",".","1","9","5",".",".","."]
,[".","9","8",".",".",".",".","6","."]
,["8",".",".",".","6",".",".",".","3"]
,["4",".",".","8",".","3",".",".","1"]
,["7",".",".",".","2",".",".",".","6"]
,[".","6",".",".",".",".","2","8","."]
,[".",".",".","4","1","9",".",".","5"]
,[".",".",".",".","8",".",".","7","9"]]
**Output:** true

```



Example 2:

```

**Input:** board = 
[["8","3",".",".","7",".",".",".","."]
,["6",".",".","1","9","5",".",".","."]
,[".","9","8",".",".",".",".","6","."]
,["8",".",".",".","6",".",".",".","3"]
,["4",".",".","8",".","3",".",".","1"]
,["7",".",".",".","2",".",".",".","6"]
,[".","6",".",".",".",".","2","8","."]
,[".",".",".","4","1","9",".",".","5"]
,[".",".",".",".","8",".",".","7","9"]]
**Output:** false
**Explanation:** Same as Example 1, except with the **5** in the top left corner being modified to **8**. Since there are two 8&#39;s in the top left 3x3 sub-box, it is invalid.

```



 


**Constraints:**


	
- `board.length == 9`
	
- `board[i].length == 9`
	
- `board[i][j]` is a digit `1-9` or `&#39;.&#39;`.


---

## Algorithmic Complexity & Proof

- **Technique:** Single pass iteration over the 9x9 board. For each cell containing a digit, the algorithm checks its presence in the corresponding row, column, and 3x3 sub-box using three sets of boolean arrays. If a digit is found to be a duplicate in any of these structures, the board is immediately deemed invalid. Otherwise, the digit is marked as seen in all three structures. If all cells are processed without finding any duplicates, the board is considered valid.
- **Time Complexity:** $O(N^2)$
- **Space Complexity:** $O(N^2)$

### Proof & Mathematical Analysis
Let N be the side length of the Sudoku board. In this problem, N is fixed at 9. The algorithm iterates through each of the N*N cells exactly once. For each cell, it performs a constant number of operations: a character comparison, type conversion, integer arithmetic for calculating the box index, and three array lookups/assignments. Each of these operations takes O(1) time. Therefore, the total time complexity is O(N^2). Given N=9, this is O(9^2) = O(81), which is constant time.

The algorithm uses three 2D boolean arrays to keep track of seen digits: `rows`, `cols`, and `boxes`. Each array is of size N x N (specifically, N rows/columns/boxes, each tracking N possible digits). For example, `rows` has N sub-arrays, and each sub-array has N boolean flags (one for each digit 1-9). Thus, each structure requires O(N*N) space. Since there are three such structures, the total space complexity is O(3*N*N) = O(N^2). Given N=9, this is O(9^2) = O(81), which is constant space.

This approach achieves the lowest theoretical time and space complexity because, to validate the board, every filled cell must be visited at least once (requiring O(N^2) time), and information about seen numbers must be stored for each row, column, and block (requiring O(N^2) space).
