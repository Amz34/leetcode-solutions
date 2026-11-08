#include <vector>
#include <unordered_map>
#include <algorithm>

class Solution {
public:
    std::vector<int> topKFrequent(std::vector<int>& nums, int k) {
        // Step 1: Count frequencies
        std::unordered_map<int, int> freq_map;
        for (int num : nums) {
            freq_map[num]++;
        }

        // Step 2: Create buckets
        // buckets[i] will store numbers that appear i times
        // Max frequency can be nums.size()
        std::vector<std::vector<int>> buckets(nums.size() + 1);

        // Step 3: Populate buckets
        for (auto const& [num, freq] : freq_map) {
            buckets[freq].push_back(num);
        }

        // Step 4: Collect top k elements
        std::vector<int> result;
        result.reserve(k); // Pre-allocate capacity for efficiency

        // Iterate from highest possible frequency down to 1
        for (int i = nums.size(); i >= 1; --i) {
            for (int num : buckets[i]) {
                result.push_back(num);
                if (result.size() == k) {
                    return result;
                }
            }
        }
        return result; // Should not be reached given constraints
    }
};
