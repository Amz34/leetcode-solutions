#include <vector>
#include <string>

class Solution {
public:
    bool isValidSudoku(std::vector<std::vector<char>>& board) {
        // Initialize 9 boolean arrays for rows, columns, and 3x3 sub-boxes
        // Each inner array tracks digits 1-9 (mapped to 0-8 index)
        std::vector<std::vector<bool>> rows(9, std::vector<bool>(9, false));
        std::vector<std::vector<bool>> cols(9, std::vector<bool>(9, false));
        std::vector<std::vector<bool>> boxes(9, std::vector<bool>(9, false));

        for (int r = 0; r < 9; ++r) {
            for (int c = 0; c < 9; ++c) {
                char char_val = board[r][c];
                
                // Skip empty cells
                if (char_val == '.') {
                    continue;
                }

                // Convert character digit to 0-8 index
                int digit_idx = char_val - '1'; 

                // Calculate the index of the 3x3 sub-box
                int box_row = r / 3;
                int box_col = c / 3;
                int box_idx = box_row * 3 + box_col;

                // Check for repetition in the current row
                if (rows[r][digit_idx]) {
                    return false;
                }
                rows[r][digit_idx] = true;

                // Check for repetition in the current column
                if (cols[c][digit_idx]) {
                    return false;
                }
                cols[c][digit_idx] = true;

                // Check for repetition in the current 3x3 sub-box
                if (boxes[box_idx][digit_idx]) {
                    return false;
                }
                boxes[box_idx][digit_idx] = true;
            }
        }

        // If no repetitions were found, the board is valid
        return true;
    }
};
