#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;
int main(){
 const int n=5; vector<array<int,5>> ps; vector<int> signs; vector<long long> weights; vector<array<long long,11>> polys; vector<vector<int>> edgeps(25); array<int,5> p={0,1,2,3,4};
 do{int s=1;for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)if(p[i]>p[j])s=-s; int id=ps.size();ps.push_back(p);signs.push_back(s);long long w=s;array<long long,11> a{};a[0]=s;int deg=0;for(int i=0;i<n;i++){edgeps[i*5+p[i]].push_back(id);for(int k=0;k<p[i];k++){w*=i+1;for(int j=deg+1;j>=0;j--)a[j]=(j<=deg ? i*a[j]:0)+(j>0?a[j-1]:0);deg++;}}weights.push_back(w);polys.push_back(a);}while(next_permutation(p.begin(),p.end()));
 array<int,120> tc{}; array<long long,6> sum{};array<int,6> cnt{};for(int id=0;id<120;id++){sum[0]+=weights[id];cnt[0]++;}
 uint64_t candidates=0,checked=0;int oldmask=0;const int stop=1<<24;
 for(int step=0;step<stop;step++){
  if(step){int b=__builtin_ctz((unsigned)step),mask=step^(step>>1),delta=(mask&(1<<b))?1:-1;for(int id:edgeps[b]){int t=tc[id];sum[t]-=weights[id];cnt[t]--;t+=delta;tc[id]=t;sum[t]+=weights[id];cnt[t]++;}oldmask=mask;}
  for(int t=0;t<=5;t++)if(cnt[t]&&sum[t]==0){candidates++;array<long long,11> z{};for(int id=0;id<120;id++)if(tc[id]==t)for(int d=0;d<=10;d++)z[d]+=polys[id][d];bool zero=all_of(z.begin(),z.end(),[](auto v){return v==0;});if(zero){cout<<"ZERO mask="<<oldmask<<" t="<<t<<" count="<<cnt[t]<<endl;return 0;}}
  checked++;if(step%2097152==0)cerr<<step<<" candidates="<<candidates<<endl;
 }
 cout<<"PASS complete n5 standard; complement representatives="<<checked<<" evaluation-zero candidates="<<candidates<<endl;
}
