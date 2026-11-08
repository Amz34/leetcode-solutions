#include <vector>
#include <numeric>
#include <algorithm>

class Solution {
public:
    int climbStairs(int n) {
        if (n == 1) {
            return 1;
        }

        // dp_i_minus_2 represents ways to reach step i-2
        // dp_i_minus_1 represents ways to reach step i-1
        // Base cases:
        // Ways to reach step 1: 1 (1 step)
        int dp_i_minus_2 = 1;
        // Ways to reach step 2: 2 (1+1, 2)
        int dp_i_minus_1 = 2;

        // Iterate from step 3 up to n
        for (int i = 3; i <= n; ++i) {
            int current_dp = dp_i_minus_1 + dp_i_minus_2;
            dp_i_minus_2 = dp_i_minus_1;
            dp_i_minus_1 = current_dp;
        }
        return dp_i_minus_1;
    }
};
