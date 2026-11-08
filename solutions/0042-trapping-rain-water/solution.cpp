#include <vector>
#include <algorithm> // Required for std::max, though not explicitly used in this specific implementation as if/else handles it.

using namespace std;

class Solution {
public:
    int trap(vector<int>& height) {
        if (height.empty()) {
            return 0;
        }

        int n = height.size();
        int left = 0;
        int right = n - 1;
        int left_max = 0;
        int right_max = 0;
        int total_water = 0;

        while (left <= right) {
            if (height[left] < height[right]) {
                if (height[left] >= left_max) {
                    left_max = height[left];
                } else {
                    total_water += left_max - height[left];
                }
                left++;
            } else {
                if (height[right] >= right_max) {
                    right_max = height[right];
                } else {
                    total_water += right_max - height[right];
                }
                right--;
            }
        }
        
        return total_water;
    }
};
