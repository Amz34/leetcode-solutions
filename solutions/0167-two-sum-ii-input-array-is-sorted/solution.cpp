#include <vector>

class Solution {
public:
    std::vector<int> twoSum(std::vector<int>& numbers, int target) {
        int left = 0;
        int right = numbers.size() - 1;

        while (left < right) {
            int current_sum = numbers[left] + numbers[right];
            if (current_sum == target) {
                // Problem asks for 1-indexed result
                return {left + 1, right + 1};
            } else if (current_sum < target) {
                // Sum is too small, need a larger number. Move left pointer right.
                left++;
            } else { // current_sum > target
                // Sum is too large, need a smaller number. Move right pointer left.
                right--;
            }
        }
        
        // According to problem constraints, there is exactly one solution,
        // so this line should theoretically not be reached.
        return {};
    }
};
