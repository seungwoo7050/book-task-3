#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int V,E; cin >> V >> E;
    int K; cin >> K;
    vector<vector<pair<int,int>>> adj(V+1);
    for(int i=0;i<E;i++){
        int u,v,w; cin >> u >> v >> w;
        adj[u].push_back({v,w});
    }
    const long long INF = 1e18;
    vector<long long> dist(V+1, INF);
    dist[K]=0;
    priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<>> pq;
    pq.push({0,K});
    while(!pq.empty()){
        auto [d,u]=pq.top(); pq.pop();
        if(d>dist[u]) continue;
        for(auto [v,w]:adj[u]){
            if(dist[u]+w < dist[v]){
                dist[v]=dist[u]+w;
                pq.push({dist[v],v});
            }
        }
    }
    for(int i=1;i<=V;i++){
        if(dist[i]==INF) cout << "INF\n";
        else cout << dist[i] << '\n';
    }
    return 0;
}
