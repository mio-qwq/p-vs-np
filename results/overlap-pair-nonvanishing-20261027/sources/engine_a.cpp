
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <stdexcept>
struct Term {int l,a,t,c;};
static const Term terms[]={{8,1,2,24},
{8,1,1,48},
{8,1,0,24},
{8,0,3,40},
{8,0,2,240},
{8,0,1,440},
{8,0,0,240},
{7,2,2,6},
{7,2,1,108},
{7,2,0,102},
{7,1,3,-140},
{7,1,2,280},
{7,1,1,1460},
{7,1,0,1120},
{7,0,4,-100},
{7,0,3,-600},
{7,0,2,-1100},
{7,0,1,-600},
{6,3,1,24},
{6,3,0,120},
{6,2,3,-35},
{6,2,2,-962},
{6,2,1,541},
{6,2,0,1828},
{6,1,4,248},
{6,1,3,-1464},
{6,1,2,-7352},
{6,1,1,-9320},
{6,1,0,-3480},
{6,0,5,40},
{6,0,4,240},
{6,0,3,40},
{6,0,2,-2160},
{6,0,1,-4400},
{6,0,0,-2400},
{5,4,0,24},
{5,3,2,-248},
{5,3,1,-2194},
{5,3,0,234},
{5,2,4,62},
{5,2,3,2160},
{5,2,2,-9118},
{5,2,1,-27626},
{5,2,0,-16430},
{5,1,5,-140},
{5,1,4,860},
{5,1,3,5860},
{5,1,2,2660},
{5,1,1,-14480},
{5,1,0,-13000},
{4,4,1,-562},
{4,4,0,-1660},
{4,3,3,591},
{4,3,2,6541},
{4,3,1,-23453},
{4,3,0,-30581},
{4,2,5,-35},
{4,2,4,-1042},
{4,2,3,10336},
{4,2,2,40658},
{4,2,1,17515},
{4,2,0,-16720},
{4,1,6,24},
{4,1,5,-192},
{4,1,4,-1536},
{4,1,3,-240},
{4,1,2,11880},
{4,1,1,21600},
{4,1,0,10800},
{3,5,0,-412},
{3,4,2,2101},
{3,4,1,7896},
{3,4,0,-20408},
{3,3,4,-328},
{3,3,3,-1590},
{3,3,2,54092},
{3,3,1,112314},
{3,3,0,29900},
{3,2,6,6},
{3,2,5,132},
{3,2,4,-2880},
{3,2,3,-10296},
{3,2,2,23490},
{3,2,1,90540},
{3,2,0,61200},
{2,5,1,3216},
{2,5,0,2940},
{2,4,3,-1209},
{2,4,2,6672},
{2,4,1,120819},
{2,4,0,105540},
{2,3,5,57},
{2,3,4,-237},
{2,3,3,-11454},
{2,3,2,-11604},
{2,3,1,119565},
{2,3,0,138825},
{1,6,0,1764},
{1,5,2,-2115},
{1,5,1,24543},
{1,5,0,95310},
{1,4,4,171},
{1,4,3,-1863},
{1,4,2,-16821},
{1,4,1,28215},
{1,4,0,140850},
{0,6,1,-1458},
{0,6,0,21870},
{0,5,3,162},
{0,5,2,-2106},
{0,5,1,-7830},
{0,5,0,44550}};
int mod(int64_t x,int p){int r=x%p;return r<0?r+p:r;}
std::vector<uint8_t> make_table(int p){
 std::vector<uint8_t> tab(p*p*p);
 for(int l=0;l<p;l++)for(int a=0;a<p;a++){
  int lp[10]={1},ap[8]={1},c[8]={0};
  for(int i=1;i<10;i++)lp[i]=lp[i-1]*l%p;
  for(int i=1;i<8;i++)ap[i]=ap[i-1]*a%p;
  for(auto v:terms)c[v.t]=(c[v.t]+mod(v.c,p)*lp[v.l]%p*ap[v.a])%p;
  for(int t=0;t<p;t++){int z=0;for(int i=7;i>=0;i--)z=(z*t+c[i])%p;tab[(l*p+a)*p+t]=(z==0);}
 }
 return tab;
}
int main(int argc,char**argv){
 int H=argc>1?std::stoi(argv[1]):1632;
 if(H<1||H>1632)throw std::runtime_error("height outside certified domain");
 std::string out=argc>2?argv[2]:"survivors.tsv";
 auto tab101=make_table(101),tab103=make_table(103);
 std::vector<std::vector<std::pair<int,int>>> fac(H+1);
 for(int n=1;n<=H;n++){int v=n;for(int p=2;p*p<=v;p++)if(v%p==0){int e=0;do{v/=p;e++;}while(v%p==0);fac[n].push_back({p,e});}if(v>1)fac[n].push_back({v,1});}
 const std::array<std::string,30> wanted={"abcde","abdce","abdec","adbce","adbec","adebc","bacde","badce","badec","bcade","bcdae","bcdea","bdace","bdaec","bdcae","bdcea","bdeac","bdeca","dabce","dabec","daebc","dbace","dbaec","dbcae","dbcea","dbeac","dbeca","deabc","debac","debca"};
 uint64_t pairs=0,shape=0,regular=0,lzero=0,azero=0,kzero=0,n101=0,n103=0;
 std::array<uint64_t,30> ords={};std::ofstream f(out);
 if(!f)throw std::runtime_error("output");
 std::vector<std::pair<int,int>> fs;std::vector<int> ds;ds.reserve(512);
 for(int B=-H;B<=H;B++){
  if(!B)continue;
  for(int C=B+1;C<=H;C++){
   if(!C||std::max(0,C)-std::min(0,B)>H)continue;
   pairs++;int S=B+C;int64_t N=2LL*B*C;
   fs=fac[std::abs(B)];
   auto add=[&](int p,int e){for(auto &v:fs)if(v.first==p){v.second+=e;return;}fs.push_back({p,e});};
   for(auto v:fac[std::abs(C)])add(v.first,v.second);add(2,1);
   ds.clear();ds.push_back(1);
   for(auto pe:fs){int sz=ds.size(),pwr=1;for(int e=1;e<=pe.second;e++){pwr*=pe.first;for(int i=0;i<sz;i++)ds.push_back(ds[i]*pwr);}}
   int lo=std::max(0,C)-H,hi=std::min(0,B)+H;
   for(int hp:ds)for(int sg:{-1,1}){
    int h=sg*hp;int k=N/h;if(h>=k)continue;
    int D=S+h,E=S+k;
    if(D<lo||D>hi||E<lo||E>hi||D==0||E==0||D==B||D==C||E==B||E==C)continue;
    if(std::max({0,B,C,D,E})-std::min({0,B,C,D,E})>H)continue;
    std::array<std::pair<int,int>,5> vals={{{0,0},{B,1},{C,2},{D,3},{E,4}}};std::sort(vals.begin(),vals.end());
    std::string order;for(auto v:vals)order.push_back('a'+v.second);
    int oi=-1;for(int i=0;i<30;i++)if(order==wanted[i])oi=i;if(oi<0)continue;
    shape++;ords[oi]++;
    int u=D+E,x=u-B,y=u-C,l=x+y,tt=u-l;int64_t aa=1LL*x*y;
    if(1LL*D*E!=1LL*u*(B+C)-1LL*B*B-1LL*C*C)throw std::runtime_error("C3 identity");
    if(!l){lzero++;continue;}if(!aa){azero++;continue;}if(aa+2*l==0){kzero++;continue;}
    regular++;
    if(!tab101[(mod(l,101)*101+mod(aa,101))*101+mod(tt,101)])continue;n101++;
    if(!tab103[(mod(l,103)*103+mod(aa,103))*103+mod(tt,103)])continue;n103++;
    f<<B<<'\t'<<C<<'\t'<<D<<'\t'<<E<<'\t'<<x<<'\t'<<y<<'\t'<<tt<<'\n';
   }
  }
 }
 std::cout<<"{\"height\":"<<H<<",\"BC_pairs\":"<<pairs<<",\"shapes\":"<<shape<<",\"L_zero\":"<<lzero<<",\"A_zero\":"<<azero<<",\"K_zero\":"<<kzero<<",\"regular\":"<<regular<<",\"mod101\":"<<n101<<",\"mod103\":"<<n103<<",\"orders\":[";
 for(int i=0;i<30;i++){if(i)std::cout<<',';std::cout<<ords[i];}std::cout<<"]}\n";
}
