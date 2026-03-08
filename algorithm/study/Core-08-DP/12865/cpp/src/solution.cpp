#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, K; cin >> N >> K;
    vector<int> dp(K + 1, 0);

    for(int i = 0; i < N; i++){
        int w, v; cin >> w >> v;
        for(int j = K; j >= w; j--)
            dp[j] = max(dp[j], dp[j - w] + v);
    }

    cout << dp[K] << "\n";
    return 0;
}
