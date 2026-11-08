class Solution:
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        left = 0
        right = len(numbers) - 1

        while left < right:
            current_sum = numbers[left] + numbers[right]
            if current_sum == target:
                # Problem asks for 1-indexed result
                return [left + 1, right + 1]
            elif current_sum < target:
                # Sum is too small, need a larger number. Move left pointer right.
                left += 1
            else: # current_sum > target
                # Sum is too large, need a smaller number. Move right pointer left.
                right -= 1
        
        # According to problem constraints, there is exactly one solution,
        # so this line should theoretically not be reached.
        return []
