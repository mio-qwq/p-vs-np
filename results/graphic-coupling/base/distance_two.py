"""Force arbitrary disjoint forbidden pairs to line-graph distance <=2."""
from graphic import valid,brute_join

def localize(n,edges,pairs,target,pad_all=True):
    out=[];halves=[];nextv=n+len(edges);newtarget=target
    for i,(u,v) in enumerate(edges):
        mid=n+i;halves.append((len(out),len(out)+1));out.extend([(u,mid),(mid,v)])
    newpairs=[];forced_one=[];forced_zero=[]
    for i,j in pairs:
        newpairs.append((halves[i][0],halves[j][0]))
        c=len(out);out.append((n+i,n+j))
        d=len(out);out.append((n+i,nextv));newtarget^=(1<<(n+i))|(1<<nextv);nextv+=1
        newpairs.append((c,d));forced_one.append(d);forced_zero.append(c)
    if pad_all:
        used={e for pair in newpairs for e in pair}
        for i in range(len(out)):
            if i not in used:
                zero=len(out);out.append((out[i][0],nextv));nextv+=1;newpairs.append((i,zero));forced_zero.append(zero)
    return nextv,out,newpairs,newtarget,halves,forced_one,forced_zero

def lift(mask,halves,ones):
    ans=sum(1<<e for i,pair in enumerate(halves) if mask>>i&1 for e in pair)
    return ans|sum(1<<e for e in ones)

def pair_distance_at_most_two(edges,pair):
    i,j=pair
    if set(edges[i])&set(edges[j]):return True
    return any(set(e)&set(edges[i]) and set(e)&set(edges[j]) for e in edges)
