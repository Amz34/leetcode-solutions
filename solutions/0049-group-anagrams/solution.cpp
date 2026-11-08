#include <vector>
#include <string>
#include <unordered_map>
#include <array> // For std::array
#include <numeric> // Not strictly needed, but often useful.

using namespace std; // Required by the prompt

// Custom hash function for std::array<int, 26> because it's not hashable by default
struct ArrayHasher {
    std::size_t operator()(const std::array<int, 26>& a) const {
        std::size_t h = 0;
        // A common hash combining strategy, similar to Boost's hash_combine.
        // It combines the hash of each element into a single hash value.
        for (int i : a) {
            h ^= std::hash<int>{}(i) + 0x9e3779b9 + (h << 6) + (h >> 2);
        }
        return h;
    }
};

class Solution {
public:
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        // Use an unordered_map with std::array<int, 26> as key and a custom hasher.
        // The value is a vector of strings that are anagrams.
        unordered_map<array<int, 26>, vector<string>, ArrayHasher> anagram_groups;

        for (const string& s : strs) {
            array<int, 26> count{}; // Initialize all elements to 0 for 'a' through 'z'

            for (char c : s) {
                count[c - 'a']++; // Increment count for the character (e.g., 'a' - 'a' = 0)
            }
            
            // Add the string to the vector associated with its count array key.
            // If the key doesn't exist, it's default-constructed (an empty vector) and then push_back is called.
            anagram_groups[count].push_back(s);
        }
        
        // Collect all the values (vectors of strings) from the map into the result vector.
        vector<vector<string>> result;
        for (auto const& pair : anagram_groups) {
            result.push_back(pair.second);
        }
        return result;
    }
};
