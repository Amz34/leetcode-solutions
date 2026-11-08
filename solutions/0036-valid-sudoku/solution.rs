pub struct Solution;

impl Solution {
    pub fn is_valid_sudoku(board: Vec<Vec<char>>) -> bool {
        // Initialize 9 boolean arrays for rows, columns, and 3x3 sub-boxes
        // Each inner array tracks digits 1-9 (mapped to 0-8 index)
        let mut rows: Vec<Vec<bool>> = vec![vec![false; 9]; 9];
        let mut cols: Vec<Vec<bool>> = vec![vec![false; 9]; 9];
        let mut boxes: Vec<Vec<bool>> = vec![vec![false; 9]; 9];

        for r in 0..9 {
            for c in 0..9 {
                let char_val = board[r][c];
                
                // Skip empty cells
                if char_val == '.' {
                    continue;
                }

                // Convert character digit to 0-8 index
                // unwrap() is safe here because problem constraints guarantee '1'-'9'
                let digit_idx = char_val.to_digit(10).unwrap() as usize - 1;

                // Calculate the index of the 3x3 sub-box
                let box_row = r / 3;
                let box_col = c / 3;
                let box_idx = box_row * 3 + box_col;

                // Check for repetition in the current row
                if rows[r][digit_idx] {
                    return false;
                }
                rows[r][digit_idx] = true;

                // Check for repetition in the current column
                if cols[c][digit_idx] {
                    return false;
                }
                cols[c][digit_idx] = true;

                // Check for repetition in the current 3x3 sub-box
                if boxes[box_idx][digit_idx] {
                    return false;
                }
                boxes[box_idx][digit_idx] = true;
            }
        }

        // If no repetitions were found, the board is valid
        true
    }
}
