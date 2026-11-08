pub struct Solution;

impl Solution {
    pub fn trap(height: Vec<i32>) -> i32 {
        if height.is_empty() {
            return 0;
        }

        let n = height.len();
        let mut left = 0;
        let mut right = n - 1;
        let mut left_max = 0;
        let mut right_max = 0;
        let mut total_water = 0;

        while left <= right {
            if height[left] < height[right] {
                if height[left] >= left_max {
                    left_max = height[left];
                } else {
                    total_water += left_max - height[left];
                }
                left += 1;
            } else {
                if height[right] >= right_max {
                    right_max = height[right];
                } else {
                    total_water += right_max - height[right];
                }
                right -= 1;
            }
        }
        
        total_water
    }
}
