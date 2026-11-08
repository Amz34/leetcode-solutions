#include <vector>
#include <algorithm> // For std::sort

class Solution {
public:
    std::vector<std::vector<int>> threeSum(std::vector<int>& nums) {
        std::sort(nums.begin(), nums.end());
        std::vector<std::vector<int>> result;
        int n = nums.size();

        if (n < 3) {
            return result;
        }

        for (int i = 0; i < n - 2; ++i) {
            // Skip duplicate for the first element
            if (i > 0 && nums[i] == nums[i-1]) {
                continue;
            }

            // Optimization: if nums[i] is positive, sum cannot be 0 with other non-negative numbers
            if (nums[i] > 0) {
                break;
            }

            int left = i + 1;
            int right = n - 1;

            while (left < right) {
                int current_sum = nums[i] + nums[left] + nums[right];

                if (current_sum == 0) {
                    result.push_back({nums[i], nums[left], nums[right]});
                    
                    // Skip duplicates for the second element
                    while (left < right && nums[left] == nums[left + 1]) {
                        left++;
                    }
                    // Skip duplicates for the third element
                    while (left < right && nums[right] == nums[right - 1]) {
                        right--;
                    }
                    left++;
                    right--;
                } else if (current_sum < 0) {
                    left++;
                } else { // current_sum > 0
                    right--;
                }
            }
        }
        return result;
    }
};
