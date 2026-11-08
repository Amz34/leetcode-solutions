pub struct Solution;

impl Solution {
    pub fn product_except_self(nums: Vec<i32>) -> Vec<i32> {
        let n = nums.len();
        
        // Initialize the answer vector with 1s.
        // This vector will first store prefix products.
        let mut answer = vec![1; n];

        // Calculate prefix products and store them in the answer vector.
        // answer[i] will contain the product of nums[0]...nums[i-1].
        // For i=0, the prefix product is 1 (empty prefix), which is already set.
        for i in 1..n {
            answer[i] = answer[i-1] * nums[i-1];
        }

        // Calculate suffix products and combine them with prefix products.
        // 'right_product' will store the product of elements to the right of the current index.
        let mut right_product = 1;
        for i in (0..n).rev() { // Iterate from n-1 down to 0
            // For each element, multiply its current prefix product (answer[i])
            // by the accumulated product of elements to its right (right_product).
            answer[i] = answer[i] * right_product;
            
            // Update right_product for the next iteration (element to the left).
            right_product *= nums[i];
        }
        
        answer
    }
}
