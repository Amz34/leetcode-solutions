#include <vector>

class Solution {
public:
    std::vector<int> productExceptSelf(std::vector<int>& nums) {
        int n = nums.size();
        
        // Initialize the answer vector with 1s.
        // This vector will first store prefix products.
        std::vector<int> answer(n, 1);

        // Calculate prefix products and store them in the answer vector.
        // answer[i] will contain the product of nums[0]...nums[i-1].
        // For i=0, the prefix product is 1 (empty prefix), which is already set.
        for (int i = 1; i < n; ++i) {
            answer[i] = answer[i-1] * nums[i-1];
        }

        // Calculate suffix products and combine them with prefix products.
        // 'right_product' will store the product of elements to the right of the current index.
        int right_product = 1;
        for (int i = n - 1; i >= 0; --i) {
            // For each element, multiply its current prefix product (answer[i])
            // by the accumulated product of elements to its right (right_product).
            answer[i] = answer[i] * right_product;
            
            // Update right_product for the next iteration (element to the left).
            right_product *= nums[i];
        }
        
        return answer;
    }
};
