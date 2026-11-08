class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        result = []
        n = len(nums)

        for i in range(n - 2):
            # Skip duplicate for the first element
            if i > 0 and nums[i] == nums[i-1]:
                continue

            # Optimization: if nums[i] is positive, sum cannot be 0 with other non-negative numbers
            # (since array is sorted, nums[left] and nums[right] will be >= nums[i])
            if nums[i] > 0:
                break

            left, right = i + 1, n - 1
            while left < right:
                current_sum = nums[i] + nums[left] + nums[right]
                if current_sum == 0:
                    result.append([nums[i], nums[left], nums[right]])
                    # Skip duplicates for the second element
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    # Skip duplicates for the third element
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1
                elif current_sum < 0:
                    left += 1
                else: # current_sum > 0
                    right -= 1
        return result
