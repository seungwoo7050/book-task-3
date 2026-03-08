#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int M, N;
    cin >> M >> N;

    vector<vector<int>> grid(N, vector<int>(M));
    queue<tuple<int,int,int>> q;

    for (int i = 0; i < N; i++)
        for (int j = 0; j < M; j++) {
            cin >> grid[i][j];
            if (grid[i][j] == 1) q.push({i, j, 0});
        }

    int dx[] = {0, 0, 1, -1};
    int dy[] = {1, -1, 0, 0};
    int ans = 0;

    while (!q.empty()) {
        auto [x, y, day] = q.front(); q.pop();
        for (int k = 0; k < 4; k++) {
            int nx = x + dx[k], ny = y + dy[k];
            if (nx >= 0 && nx < N && ny >= 0 && ny < M && grid[nx][ny] == 0) {
                grid[nx][ny] = 1;
                q.push({nx, ny, day + 1});
                ans = max(ans, day + 1);
            }
        }
    }

    for (int i = 0; i < N; i++)
        for (int j = 0; j < M; j++)
            if (grid[i][j] == 0) { cout << -1 << '\n'; return 0; }

    cout << ans << '\n';
    return 0;
}
