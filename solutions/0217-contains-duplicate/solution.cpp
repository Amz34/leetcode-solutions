#include <vector>
#include <unordered_set>

class Solution {
public:
    bool containsDuplicate(std::vector<int>& nums) {
        std::unordered_set<int> seen;
        for (int num : nums) {
            if (seen.count(num)) { // Check if element exists
                return true;
            }
            seen.insert(num); // Add element
        }
        return false;
    }
};
