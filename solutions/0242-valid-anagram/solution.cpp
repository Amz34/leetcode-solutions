#include <string>
#include <vector>
#include <numeric> // Not strictly needed for this specific implementation, but often useful

class Solution {
public:
    bool isAnagram(std::string s, std::string t) {
        if (s.length() != t.length()) {
            return false;
        }
        
        // Initialize a frequency vector for 26 lowercase English letters
        std::vector<int> char_counts(26, 0);
        
        // Increment counts for characters in string s
        for (char c : s) {
            char_counts[c - 'a']++;
        }
        
        // Decrement counts for characters in string t
        for (char c : t) {
            char_counts[c - 'a']--;
        }
        
        // Check if all counts are zero. If they are, t is an anagram of s.
        for (int count : char_counts) {
            if (count != 0) {
                return false;
            }
        }
        
        return true;
    }
};
