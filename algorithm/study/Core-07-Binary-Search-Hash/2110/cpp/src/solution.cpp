#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, C; cin >> N >> C;
    vector<long long> h(N);
    for(int i = 0; i < N; i++) cin >> h[i];
    sort(h.begin(), h.end());

    auto feasible = [&](long long d) -> bool {
        int cnt = 1;
        long long last = h[0];
        for(int i = 1; i < N; i++){
            if(h[i] - last >= d){
                cnt++;
                last = h[i];
                if(cnt >= C) return true;
            }
        }
        return false;
    };

    long long lo = 1, hi = h[N-1] - h[0], ans = 0;
    while(lo <= hi){
        long long mid = (lo + hi) / 2;
        if(feasible(mid)){
            ans = mid;
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    cout << ans << "\n";
    return 0;
}
