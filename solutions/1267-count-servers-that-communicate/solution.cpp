#include <vector>

class Solution {
public:
    int countServers(std::vector<std::vector<int>>& grid) {
        int m = grid.size();
        int n = grid[0].size();
        std::vector<int> row_counts(m, 0);
        std::vector<int> col_counts(n, 0);

        for (int r = 0; r < m; ++r) {
            for (int c = 0; c < n; ++c) {
                if (grid[r][c] == 1) {
                    row_counts[r]++;
                    col_counts[c]++;
                }
            }
        }

        int servers = 0;
        for (int r = 0; r < m; ++r) {
            for (int c = 0; c < n; ++c) {
                if (grid[r][c] == 1 && (row_counts[r] > 1 || col_counts[c] > 1)) {
                    servers++;
                }
            }
        }

        return servers;
    }
};
