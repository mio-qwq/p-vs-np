#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <vector>
#include "polynomials.hpp"
using I=long long;
using Tuple=std::array<I,4>;
const std::set<std::string> remaining={"bcdea","bdeca","dabce","dbaec","dbeac","debca"};
struct Counts { I c3=0,l0=0,a0=0,k0=0,low=0,m0=0,z0=0,rm4=0,mod101=0,mod103=0,p7=0,p8=0; };
std::map<std::string,Counts> counts;
I total=0,selected=0,factor_pairs=0,bc_pairs=0;
int H; bool dump=false,allorders=false;
std::ofstream allfile, survivorfile, flagfile;
std::vector<signed char> cache101(101*101*101,-1),cache103(103*103*103,-1);
int residue(I n,int p) { int a=n%p;return a<0?a+p:a; }
bool modular_zero(I L,I A,I t,int p,std::vector<signed char>&cache) {
 int lr=residue(L,p),ar=residue(A,p),tr=residue(t,p);
 size_t key=(lr*p+ar)*p+tr;
 if(cache[key]>=0) return cache[key];
 I lp[10],ap[10],tp[10];lp[0]=ap[0]=tp[0]=1;
 for(int j=1;j<10;j++){lp[j]=lp[j-1]*lr%p;ap[j]=ap[j-1]*ar%p;tp[j]=tp[j-1]*tr%p;}
 I value=0;for(auto m:P7)value+=residue(m.c,p)*lp[m.l]*ap[m.a]*tp[m.t];
 cache[key]=(value%p==0);return cache[key];
}
void accept(I B,I C,I D,I E){
 std::array<std::pair<I,char>,5> ex={{{0,'a'},{B,'b'},{C,'c'},{D,'d'},{E,'e'}}};
 std::sort(ex.begin(),ex.end());
 if(ex[4].first-ex[0].first>H)return;
 for(int j=1;j<5;j++)if(ex[j].first==ex[j-1].first)return;
 if(D>=E || B>=C || D*E!=(D+E)*(B+C)-B*B-C*C){std::cerr<<"C3 invariant failure\n";std::exit(2);}
 std::string order;for(auto a:ex)order+=a.second;
 Counts &cnt=counts[order];cnt.c3++;total++;
 if(dump)allfile<<B<<'\t'<<C<<'\t'<<D<<'\t'<<E<<'\t'<<order<<'\n';
 if(!allorders && !remaining.count(order))return;
 selected++;
 I u=D+E,x=u-B,y=u-C,L=x+y,A=x*y,t=u-L,K=A+2*L;
 I M=-18*A*L+A*t-15*A+2*L*L*L-5*L*L*t+2*L*t*t-20*L;
 if(L==0 || A==0 || K==0 || M==0 || L*(t+1)+2*A==0 || A+4*L==0)
  flagfile<<B<<'\t'<<C<<'\t'<<D<<'\t'<<E<<'\t'<<order<<'\t'<<L<<'\t'<<A<<'\t'<<t<<'\t'<<M<<'\n';
 if(L==0){cnt.l0++;return;}if(A==0){cnt.a0++;return;}if(K==0){cnt.k0++;return;}
 cnt.low++;
 if(M==0)cnt.m0++;
 if(L*(t+1)+2*A==0)cnt.z0++;
 if(A+4*L==0)cnt.rm4++;
 if(!modular_zero(L,A,t,101,cache101))return;
 cnt.mod101++;
 if(!modular_zero(L,A,t,103,cache103))return;
 cnt.mod103++;
 survivorfile<<B<<'\t'<<C<<'\t'<<D<<'\t'<<E<<'\t'<<order<<'\t'<<L<<'\t'<<A<<'\t'<<t<<'\t'<<M<<'\n';
}
int main(int argc,char**argv){
 H=argc>1?std::stoi(argv[1]):1632;if(H<=0 || H>1632)return 2;
 dump=argc>2 && std::string(argv[2])=="dump";
 allorders=argc>2 && std::string(argv[2])=="all";
 if(dump)allfile.open("all-"+std::to_string(H)+".tsv");
 survivorfile.open(std::string(allorders?"allorders-":"")+"survivors-"+std::to_string(H)+".tsv");
 flagfile.open(std::string(allorders?"allorders-":"")+"flags-"+std::to_string(H)+".tsv");
 auto start=std::chrono::steady_clock::now();
 int maxn=2*H*H;std::vector<int> spf(maxn+1);
 for(int p=2;p<=maxn;p++)if(!spf[p]){spf[p]=p;if((I)p*p<=maxn)for(I j=(I)p*p;j<=maxn;j+=p)if(!spf[j])spf[j]=p;}
 std::vector<int> divisors;divisors.reserve(2048);
 for(I B=-H;B<=H;B++){
  if(B==0)continue;
  for(I C=B+1;C<=H && C-B<=H;C++){
   if(C==0)continue;
   bc_pairs++;
   I n=2*B*C;int m=std::abs(n);divisors.clear();divisors.push_back(1);
   while(m>1){int p=spf[m],power=1;size_t old=divisors.size();do{m/=p;power*=p;for(size_t j=0;j<old;j++)divisors.push_back(divisors[j]*power);}while(m%p==0);}
   for(I v:divisors)for(int sign:{-1,1}){I h=sign*v,k=n/h;if(h>=k)continue;factor_pairs++;accept(B,C,B+C+h,B+C+k);}
  }
  if(B%200==0)std::cerr<<"B="<<B<<" c3="<<total<<" selected="<<selected<<" seconds="<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<'\n';
 }
 std::cout<<"H "<<H<<"\nbc_pairs "<<bc_pairs<<"\nfactor_pairs "<<factor_pairs<<"\nall_c3 "<<total<<"\nselected_c3 "<<selected<<"\n";
 std::cout<<"order c3 L0 A0 K0 afterlow M0 Z0 Rm4 mod101 mod103\n";
 for(auto entry:counts){auto &c=entry.second;std::cout<<entry.first<<' '<<c.c3<<' '<<c.l0<<' '<<c.a0<<' '<<c.k0<<' '<<c.low<<' '<<c.m0<<' '<<c.z0<<' '<<c.rm4<<' '<<c.mod101<<' '<<c.mod103<<'\n';}
 std::cout<<"seconds "<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<'\n';
}
