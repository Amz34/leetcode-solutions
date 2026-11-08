use std::collections::HashMap;

pub struct Solution;

impl Solution {
    pub fn group_anagrams(strs: Vec<String>) -> Vec<Vec<String>> {
        // HashMap to store groups of anagrams.
        // Key: an array of 26 integers representing character counts (e.g., [1,0,0,...,0] for 'a').
        // Value: a vector of strings that are anagrams sharing that count array.
        let mut anagram_groups: HashMap<[i32; 26], Vec<String>> = HashMap::new();

        for s in strs {
            let mut count = [0; 26]; // Initialize an array of 26 zeros for 'a' through 'z'

            for c in s.chars() {
                // Increment the count for the corresponding character.
                // (c as u8 - b'a') converts 'a' to 0, 'b' to 1, etc.
                count[(c as u8 - b'a') as usize] += 1;
            }
            
            // Insert the string into the vector associated with its count array key.
            // entry().or_insert_with() gets a mutable reference to the value if the key exists,
            // or inserts a new empty Vec and returns a reference to it if the key is new.
            anagram_groups.entry(count).or_insert_with(Vec::new).push(s);
        }
        
        // Collect all the values (Vec<String>) from the HashMap into a new Vec<Vec<String>>.
        anagram_groups.into_values().collect()
    }
}
