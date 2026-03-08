#include <bits/stdc++.h>
using namespace std;
int V;
vector<pair<int,int>> adj[100001];
pair<int,long long> bfs(int s){
    vector<long long> dist(V+1, -1);
    queue<int> q;
    dist[s]=0; q.push(s);
    int far_node=s; long long far_dist=0;
    while(!q.empty()){
        int u=q.front(); q.pop();
        for(auto [v,w]:adj[u]){
            if(dist[v]==-1){
                dist[v]=dist[u]+w;
                q.push(v);
                if(dist[v]>far_dist){ far_dist=dist[v]; far_node=v; }
            }
        }
    }
    return {far_node, far_dist};
}
int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> V;
    for(int i=0;i<V;i++){
        int node; cin >> node;
        int x;
        while(cin >> x && x != -1){
            int w; cin >> w;
            adj[node].push_back({x,w});
        }
    }
    auto [u,_] = bfs(1);
    auto [__, diameter] = bfs(u);
    cout << diameter << '\n';
    return 0;
}
