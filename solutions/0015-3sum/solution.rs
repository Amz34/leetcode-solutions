pub struct Solution;

impl Solution {
    pub fn three_sum(nums: Vec<i32>) -> Vec<Vec<i32>> {
        let mut nums = nums; // Make it mutable to sort
        nums.sort_unstable(); // Use unstable sort for potentially better performance, stable sort is also fine
        let n = nums.len();
        let mut result: Vec<Vec<i32>> = Vec::new();

        if n < 3 {
            return result;
        }

        for i in 0..n - 2 {
            // Skip duplicate for the first element
            if i > 0 && nums[i] == nums[i-1] {
                continue;
            }

            // Optimization: if nums[i] is positive, sum cannot be 0 with other non-negative numbers
            if nums[i] > 0 {
                break;
            }

            let mut left = i + 1;
            let mut right = n - 1;

            while left < right {
                let current_sum = nums[i] + nums[left] + nums[right];

                if current_sum == 0 {
                    result.push(vec![nums[i], nums[left], nums[right]]);
                    
                    // Skip duplicates for the second element
                    while left < right && nums[left] == nums[left + 1] {
                        left += 1;
                    }
                    // Skip duplicates for the third element
                    while left < right && nums[right] == nums[right - 1] {
                        right -= 1;
                    }
                    left += 1;
                    right -= 1;
                } else if current_sum < 0 {
                    left += 1;
                } else { // current_sum > 0
                    right -= 1;
                }
            }
        }
        result
    }
}
