pub struct Solution;

impl Solution {
    pub fn climb_stairs(n: i32) -> i32 {
        if n == 1 {
            return 1;
        }

        // dp_i_minus_2 represents ways to reach step i-2
        // dp_i_minus_1 represents ways to reach step i-1
        // Base cases:
        // Ways to reach step 1: 1 (1 step)
        let mut dp_i_minus_2 = 1;
        // Ways to reach step 2: 2 (1+1, 2)
        let mut dp_i_minus_1 = 2;

        // Iterate from step 3 up to n
        for _i in 3..=n {
            let current_dp = dp_i_minus_1 + dp_i_minus_2;
            dp_i_minus_2 = dp_i_minus_1;
            dp_i_minus_1 = current_dp;
        }
        dp_i_minus_1
    }
}
