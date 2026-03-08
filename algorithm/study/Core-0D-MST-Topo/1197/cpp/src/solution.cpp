#include <bits/stdc++.h>
using namespace std;
int par[10001], rnk[10001];
int find(int x){ return par[x]==x? x : par[x]=find(par[x]); }
bool unite(int a,int b){
    a=find(a); b=find(b);
    if(a==b) return false;
    if(rnk[a]<rnk[b]) swap(a,b);
    par[b]=a;
    if(rnk[a]==rnk[b]) rnk[a]++;
    return true;
}
int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int V,E; cin >> V >> E;
    vector<tuple<int,int,int>> edges(E);
    for(auto &[w,u,v]:edges) cin >> u >> v >> w;
    sort(edges.begin(), edges.end());
    for(int i=1;i<=V;i++) par[i]=i;
    long long total=0; int cnt=0;
    for(auto &[w,u,v]:edges){
        if(unite(u,v)){
            total+=w;
            if(++cnt==V-1) break;
        }
    }
    cout << total << '\n';
    return 0;
}
