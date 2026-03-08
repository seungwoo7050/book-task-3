#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N; cin >> N;
    vector<int> pos, neg;
    int ones = 0, zeros = 0;

    for(int i = 0; i < N; i++){
        int x; cin >> x;
        if(x > 1) pos.push_back(x);
        else if(x == 1) ones++;
        else if(x == 0) zeros++;
        else neg.push_back(x);
    }

    long long total = ones;

    sort(pos.rbegin(), pos.rend());
    for(int i = 0; i + 1 < (int)pos.size(); i += 2)
        total += (long long)pos[i] * pos[i+1];
    if(pos.size() % 2 == 1) total += pos.back();

    sort(neg.begin(), neg.end());
    for(int i = 0; i + 1 < (int)neg.size(); i += 2)
        total += (long long)neg[i] * neg[i+1];
    if(neg.size() % 2 == 1 && zeros == 0)
        total += neg.back();

    cout << total << "\n";
    return 0;
}
