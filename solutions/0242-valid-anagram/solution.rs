pub struct Solution;

impl Solution {
    pub fn is_anagram(s: String, t: String) -> bool {
        if s.len() != t.len() {
            return false;
        }

        // Initialize a frequency array for 26 lowercase English letters
        let mut char_counts = [0; 26];

        // Increment counts for characters in string s
        for c in s.chars() {
            // Convert char to its 0-25 index
            char_counts[(c as u8 - b'a') as usize] += 1;
        }

        // Decrement counts for characters in string t
        for c in t.chars() {
            // Convert char to its 0-25 index
            char_counts[(c as u8 - b'a') as usize] -= 1;
        }

        // Check if all counts are zero. If they are, t is an anagram of s.
        for &count in char_counts.iter() {
            if count != 0 {
                return false;
            }
        }

        true
    }
}
