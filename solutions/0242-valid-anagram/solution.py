class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        
        # Initialize a frequency array for 26 lowercase English letters
        char_counts = [0] * 26
        
        # Increment counts for characters in string s
        for char_s in s:
            char_counts[ord(char_s) - ord('a')] += 1
            
        # Decrement counts for characters in string t
        for char_t in t:
            char_counts[ord(char_t) - ord('a')] -= 1
            
        # Check if all counts are zero. If they are, t is an anagram of s.
        for count in char_counts:
            if count != 0:
                return False
                
        return True
