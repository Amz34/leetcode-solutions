class Solution:
    def climbStairs(self, n: int) -> int:
        if n == 1:
            return 1
        
        # dp_i_minus_2 represents ways to reach step i-2
        # dp_i_minus_1 represents ways to reach step i-1
        # Base cases:
        # Ways to reach step 1: 1 (1 step)
        dp_i_minus_2 = 1 
        # Ways to reach step 2: 2 (1+1, 2)
        dp_i_minus_1 = 2

        # Iterate from step 3 up to n
        for _ in range(3, n + 1):
            current_dp = dp_i_minus_1 + dp_i_minus_2
            dp_i_minus_2 = dp_i_minus_1
            dp_i_minus_1 = current_dp
            
        return dp_i_minus_1
