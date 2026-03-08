#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n,m; cin >> n >> m;
    vector<vector<int>> adj(n+1);
    vector<int> indeg(n+1,0);
    for(int i=0;i<m;i++){
        int a,b; cin >> a >> b;
        adj[a].push_back(b);
        indeg[b]++;
    }
    queue<int> q;
    for(int i=1;i<=n;i++) if(indeg[i]==0) q.push(i);
    bool first=true;
    while(!q.empty()){
        int u=q.front(); q.pop();
        if(!first) cout << ' ';
        cout << u; first=false;
        for(int v:adj[u]){
            if(--indeg[v]==0) q.push(v);
        }
    }
    cout << '\n';
    return 0;
}
