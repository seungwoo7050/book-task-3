#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N; cin >> N;
    vector<pair<int,int>> seg(N);
    for(int i = 0; i < N; i++) cin >> seg[i].first >> seg[i].second;
    sort(seg.begin(), seg.end());

    long long total = 0;
    int curS = seg[0].first, curE = seg[0].second;

    for(int i = 1; i < N; i++){
        if(seg[i].first <= curE){
            curE = max(curE, seg[i].second);
        } else {
            total += curE - curS;
            curS = seg[i].first;
            curE = seg[i].second;
        }
    }
    total += curE - curS;
    cout << total << "\n";

    return 0;
}
