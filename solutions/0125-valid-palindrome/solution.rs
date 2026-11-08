pub struct Solution;

impl Solution {
    pub fn is_palindrome(s: String) -> bool {
        let mut chars = s.chars()
            .filter(|c| c.is_alphanumeric())
            .map(|c| c.to_ascii_lowercase());
        
        // Use two iterators, one from the front and one from the back
        // This effectively simulates two pointers without creating a new collection
        while let (Some(left_char), Some(right_char)) = (chars.next(), chars.next_back()) {
            if left_char != right_char {
                return false;
            }
        }
        true
    }
}
