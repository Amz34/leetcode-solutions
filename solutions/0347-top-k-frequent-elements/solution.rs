use std::collections::HashMap;

pub struct Solution;

impl Solution {
    pub fn top_k_frequent(nums: Vec<i32>, k: i32) -> Vec<i32> {
        // Step 1: Count frequencies
        let mut freq_map: HashMap<i32, i32> = HashMap::new();
        for num in nums.iter() {
            *freq_map.entry(*num).or_insert(0) += 1;
        }

        // Step 2: Create buckets
        // buckets[i] will store numbers that appear i times
        // Max frequency can be nums.len()
        let mut buckets: Vec<Vec<i32>> = vec![vec![]; nums.len() + 1];

        // Step 3: Populate buckets
        for (num, freq) in freq_map.into_iter() {
            buckets[freq as usize].push(num);
        }

        // Step 4: Collect top k elements
        let mut result: Vec<i32> = Vec::with_capacity(k as usize);
        // Iterate from highest possible frequency down to 1
        for i in (1..=nums.len()).rev() {
            for num in buckets[i].drain(..) {
                result.push(num);
                if result.len() == k as usize {
                    return result;
                }
            }
        }
        result // Should not be reached given constraints
    }
}
