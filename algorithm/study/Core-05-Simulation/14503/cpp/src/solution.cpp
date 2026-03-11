#include <iostream>
#include <vector>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, M; cin >> N >> M;
    int r, c, d; cin >> r >> c >> d;

    vector<vector<int>> grid(N, vector<int>(M));
    for(int i = 0; i < N; i++)
        for(int j = 0; j < M; j++)
            cin >> grid[i][j];

    int dr[] = {-1, 0, 1, 0};
    int dc[] = {0, 1, 0, -1};
    vector<vector<bool>> cleaned(N, vector<bool>(M, false));
    int count = 0;

    while(true){
        // 현재 칸을 청소
        if(!cleaned[r][c]){
            cleaned[r][c] = true;
            count++;
        }

        // 왼쪽으로 4번 회전해 본다
        bool found = false;
        for(int i = 0; i < 4; i++){
            d = (d + 3) % 4;
            int nr = r + dr[d], nc = c + dc[d];
            if(nr >= 0 && nr < N && nc >= 0 && nc < M
               && grid[nr][nc] == 0 && !cleaned[nr][nc]){
                r = nr; c = nc;
                found = true;
                break;
            }
        }
        if(found) continue;

        // 네 방향이 모두 막히면 뒤로 한 칸 시도한다.
        int bd = (d + 2) % 4;
        int br = r + dr[bd], bc = c + dc[bd];
        if(br >= 0 && br < N && bc >= 0 && bc < M && grid[br][bc] != 1){
            r = br; c = bc;
        } else {
            break;
        }
    }

    cout << count << "\n";
    return 0;
}
