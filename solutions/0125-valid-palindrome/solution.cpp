#include <string>
#include <algorithm> // For std::tolower
#include <cctype>    // For std::isalnum

class Solution {
public:
    bool isPalindrome(std::string s) {
        int left = 0;
        int right = s.length() - 1;

        while (left < right) {
            // Move left pointer past non-alphanumeric characters
            while (left < right && !std::isalnum(s[left])) {
                left++;
            }
            // Move right pointer past non-alphanumeric characters
            while (left < right && !std::isalnum(s[right])) {
                right--;
            }

            // If pointers haven't crossed, compare characters
            if (left < right) {
                // Compare lowercase versions of characters
                if (std::tolower(s[left]) != std::tolower(s[right])) {
                    return false;
                }
                left++;
                right--;
            }
        }
        return true;
    }
};
