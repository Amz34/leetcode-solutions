class Solution:
    def longestConsecutive(self, nums: list[int]) -> int:
        if not nums:
            return 0

        num_set = set(nums)
        longest_streak = 0

        for num in num_set:
            # Check if the current number is the start of a sequence
            # (i.e., num - 1 is not in the set)
            if (num - 1) not in num_set:
                current_num = num
                current_streak = 1

                # Extend the sequence upwards
                while (current_num + 1) in num_set:
                    current_num += 1
                    current_streak += 1
                
                longest_streak = max(longest_streak, current_streak)
        
        return longest_streak
