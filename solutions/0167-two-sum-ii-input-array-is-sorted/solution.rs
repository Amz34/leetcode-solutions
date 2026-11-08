pub struct Solution;

impl Solution {
    pub fn two_sum(numbers: Vec<i32>, target: i32) -> Vec<i32> {
        let mut left = 0;
        let mut right = numbers.len() - 1;

        while left < right {
            let current_sum = numbers[left] + numbers[right];
            if current_sum == target {
                // Problem asks for 1-indexed result
                return vec![(left + 1) as i32, (right + 1) as i32];
            } else if current_sum < target {
                // Sum is too small, need a larger number. Move left pointer right.
                left += 1;
            } else { // current_sum > target
                // Sum is too large, need a smaller number. Move right pointer left.
                right -= 1;
            }
        }
        
        // According to problem constraints, there is exactly one solution,
        // so this line should theoretically not be reached.
        vec![]
    }
}
