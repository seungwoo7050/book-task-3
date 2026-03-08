#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n,m; cin >> n >> m;
    struct Edge{ int u,v,w; };
    vector<Edge> edges(m);
    for(auto &e:edges) cin >> e.u >> e.v >> e.w;
    const long long INF = 1e18;
    vector<long long> dist(n+1, INF);
    dist[1]=0;
    for(int i=0;i<n;i++){
        for(auto &[u,v,w]:edges){
            if(dist[u]!=INF && dist[u]+w < dist[v]){
                if(i==n-1){ cout << -1 << '\n'; return 0; }
                dist[v]=dist[u]+w;
            }
        }
    }
    for(int i=2;i<=n;i++){
        if(dist[i]==INF) cout << -1 << '\n';
        else cout << dist[i] << '\n';
    }
    return 0;
}
