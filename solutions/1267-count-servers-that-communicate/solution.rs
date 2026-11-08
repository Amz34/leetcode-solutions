impl Solution {
    pub fn count_servers(grid: Vec<Vec<i32>>) -> i32 {
        let m = grid.len();
        let n = grid[0].len();
        let mut row_counts = vec![0; m];
        let mut col_counts = vec![0; n];

        for r in 0..m {
            for c in 0..n {
                if grid[r][c] == 1 {
                    row_counts[r] += 1;
                    col_counts[c] += 1;
                }
            }
        }

        let mut servers = 0;
        for r in 0..m {
            for c in 0..n {
                if grid[r][c] == 1 && (row_counts[r] > 1 || col_counts[c] > 1) {
                    servers += 1;
                }
            }
        }

        servers
    }
}
