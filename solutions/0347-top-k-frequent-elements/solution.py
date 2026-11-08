import collections

class Solution:
    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        # Step 1: Count frequencies
        freq_map = collections.Counter(nums)

        # Step 2: Create buckets
        # buckets[i] will store numbers that appear i times
        # Max frequency can be len(nums)
        buckets = [[] for _ in range(len(nums) + 1)]

        # Step 3: Populate buckets
        for num, freq in freq_map.items():
            buckets[freq].append(num)

        # Step 4: Collect top k elements
        result = []
        # Iterate from highest possible frequency down to 1
        for i in range(len(nums), 0, -1):
            for num in buckets[i]:
                result.append(num)
                if len(result) == k:
                    return result
        return result # Should not be reached given constraints
