class Solution:
    def isValidSudoku(self, board: list[list[str]]) -> bool:
        # Initialize 9 boolean arrays for rows, columns, and 3x3 sub-boxes
        # Each inner array tracks digits 1-9 (mapped to 0-8 index)
        rows = [[False] * 9 for _ in range(9)]
        cols = [[False] * 9 for _ in range(9)]
        boxes = [[False] * 9 for _ in range(9)]

        for r in range(9):
            for c in range(9):
                char = board[r][c]
                
                # Skip empty cells
                if char == '.':
                    continue
                
                # Convert character digit to 0-8 index
                digit_idx = int(char) - 1  

                # Calculate the index of the 3x3 sub-box
                # The 9 boxes are indexed from 0 to 8:
                # 0 1 2
                # 3 4 5
                # 6 7 8
                box_idx = (r // 3) * 3 + (c // 3)

                # Check for repetition in the current row
                if rows[r][digit_idx]:
                    return False
                rows[r][digit_idx] = True

                # Check for repetition in the current column
                if cols[c][digit_idx]:
                    return False
                cols[c][digit_idx] = True

                # Check for repetition in the current 3x3 sub-box
                if boxes[box_idx][digit_idx]:
                    return False
                boxes[box_idx][digit_idx] = True
        
        # If no repetitions were found, the board is valid
        return True
