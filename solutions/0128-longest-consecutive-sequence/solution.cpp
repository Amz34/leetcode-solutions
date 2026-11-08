#include <vector>
#include <unordered_set>
#include <algorithm> // For std::max

class Solution {
public:
    int longestConsecutive(std::vector<int>& nums) {
        if (nums.empty()) {
            return 0;
        }

        std::unordered_set<int> num_set(nums.begin(), nums.end());
        int longest_streak = 0;

        for (int num : num_set) {
            // Check if the current number is the start of a sequence
            // (i.e., num - 1 is not in the set)
            if (num_set.find(num - 1) == num_set.end()) {
                int current_num = num;
                int current_streak = 1;

                // Extend the sequence upwards
                while (num_set.count(current_num + 1)) {
                    current_num++;
                    current_streak++;
                }
                
                longest_streak = std::max(longest_streak, current_streak);
            }
        }
        
        return longest_streak;
    }
};
