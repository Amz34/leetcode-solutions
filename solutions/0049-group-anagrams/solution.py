import collections

class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        # Use a defaultdict to automatically create a list for a new key
        # The key will be a tuple of character counts, which is hashable.
        anagram_groups = collections.defaultdict(list)

        for s in strs:
            # Create a count array for the 26 lowercase English letters (a-z)
            count = [0] * 26 

            for char in s:
                # Increment the count for the corresponding character
                # ord('a') is used to get the 0-indexed position (0 for 'a', 1 for 'b', etc.)
                count[ord(char) - ord('a')] += 1
            
            # Use the tuple of counts as the key for the hash map.
            # Tuples are immutable and thus hashable in Python, unlike lists.
            anagram_groups[tuple(count)].append(s)
        
        # The values of the dictionary are the grouped anagrams.
        # Convert the dictionary values to a list of lists.
        return list(anagram_groups.values())
