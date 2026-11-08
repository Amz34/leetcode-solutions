class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        n = len(nums)
        
        # Initialize the answer array with 1s. 
        # This array will first store prefix products.
        answer = [1] * n

        # Calculate prefix products and store them in the answer array.
        # answer[i] will contain the product of nums[0]...nums[i-1].
        # For i=0, the prefix product is 1 (empty prefix), which is already set.
        for i in range(1, n):
            answer[i] = answer[i-1] * nums[i-1]

        # Calculate suffix products and combine them with prefix products.
        # 'right_product' will store the product of elements to the right of the current index.
        right_product = 1
        for i in range(n - 1, -1, -1):
            # For each element, multiply its current prefix product (answer[i])
            # by the accumulated product of elements to its right (right_product).
            answer[i] = answer[i] * right_product
            
            # Update right_product for the next iteration (element to the left).
            right_product *= nums[i]
        
        return answer
