import json,os,urllib.request as u
U=os.environ.get("MAKEFUN_ENV_URL")or exit()
K=[-33,-31,-18,-14,14,18,31,33];B=[-17,-15,15,17];J=[-16,-1,1,16];Y=B+J;Z=136
D=[0,0,K,B,J,Y,Y]
P=[[0]*128 for _ in range(7)]
for s in range(128):
 if s&Z:continue
 r=s>>4;f=s&7;c=min(f,7-f)+min(r,7-r)
 P[1][s]=100+r*5;P[2][s]=320+6*c-20;P[4][s]=500;P[5][s]=900
P[3]=P[2]
T=[0]*128;S=1;C=0;W=4;X=116;N=0;I=1e5;G={};J=0
A=Exception
def F(f):
 global T,S,C,W,X
 p=f.split();T=[0]*128
 for i,w in enumerate(p[0].split("/")):
  r=7-i;f=0
  for ch in w:
   if ch.isdigit():f+=int(ch)
   else:
    t="pnbrqk".index(ch.lower())+1;T[r*16+f]=t*(2*ch.isupper()-1)
    if t==6:W,X=(r*16+f,X)if ch.isupper()else(W,r*16+f)
    f+=1
 S=(p[1]=="w")*2-1;C=sum(1<<i for i in range(4)if"KQkq"[i]in p[2])
def a(s,b):
 for o,t in(((-15*b,-17*b),1),(K,2),(Y,6)):
  for d in o:
   x=s+d
   if not x&Z and T[x]==b*t:return 1
 for d in Y:
  t=s+d
  while not t&Z:
   q=T[t]
   if q:
    if q==b*3 and abs(d)in(15,17)or q==b*4 and abs(d)in(1,16)or q==b*5:return 1
    break
   t+=d
 return 0
def g(o=0):
 m=[]
 for s,p in enumerate(T):
  if s&Z or not p or p*S<0:continue
  t=abs(p)
  if t==1:
   d=16*S
   for k,to in enumerate((s+d,s+d-1,s+d+1)):
    if to&Z:continue
    y=T[to]
    if k==0:
     if o or y:continue
    elif not(y and y*S<0):continue
    m.append(s|to<<7|(to>>4==7*(S>0))*5<<14)
    if k==0 and(s>>4==(1+5*(S<0)))and not T[s+2*d]:m.append(s|(s+2*d)<<7)
  else:
   for d in D[t]:
    v=s+d
    while not v&Z:
     y=T[v]
     if y and y*S<0:m.append(s|v<<7)
     if y:break
     if not o:m.append(s|v<<7)
     if t%4==2:break
     v+=d
   if t==6 and not o:
    for d,b in((2,1),(-2,2))if S>0 else((2,4),(-2,8)):
     if C&b and not(T[s+d]or T[s+d//2])and(d>0 or not T[s-3])and T[s+3 if d>0 else s-4]==4*S and not a(s,-S)and not a(s+d//2,-S)and not a(s+d,-S):m.append(s|(s+d)<<7)
 return m
def M(m):
 global S,C,W,X
 f=m&127;t=(m>>7)&127;r=(m>>14)&7;p=T[f]
 z=(list(T),C,W,X);T[t]=r*S if r else p;T[f]=0
 if abs(p)==6:
  if S>0:W=t
  else:X=t
  if abs(t-f)==2:
   u=t+1-3*(t<f);v=t-1+2*(t<f);T[v]=T[u];T[u]=0
 for s,b in((4,3),(116,12),(0,2),(7,1),(112,8),(119,4)):
  if f==s or t==s:C&=~b
 S=-S;return z
def n(z):
 global S,C,W,X
 T[:],C,W,X=z;S=-S
def L():
 m=[]
 for x in g():
  z=M(x);j=(W,X)[S>0]
  if not a(j,S):m.append(x)
  n(z)
 return m
def e():
 s=0;d=0
 for q,p in enumerate(T):
  if q&Z or not p:continue
  t=abs(p);s+=P[t][q^(p<0)*112]*p//t
  d+=(t==3)*p//t
 return(s+30*((d>1)-(d<-1)))*S
def o(v):
 t=(v>>7)&127;f=v&127;q=T[t];p=T[f]
 if v==J:return 1e5
 if q:return 10000+10*P[abs(q)][0]-P[abs(p)][0]
 h=abs(p);x=(p<0)*112;return P[h][t^x]-P[h][f^x]
def q(x,y,l):
 global N
 N+=1
 if N>2*I:raise A
 s=e()
 if s>=y:return y
 x=max(x,s)
 k=a((W,X)[S<0],-S);m=L()if k else g(1)
 if k and not m:return-I+l
 m.sort(key=o,reverse=True)
 for v in m:
  z=M(v);r=-q(-y,-x,l+1);n(z)
  if r>=y:return y
  x=max(x,r)
 return x
def R(d,x,y,l):
 global N,J
 N+=1
 if N>2*I:raise A
 if d<=0:return q(x,y,l)
 k=(tuple(T),S,C);e=G.get(k);w=x
 if e and e[0]>=d:
  s=e[1];f=e[2]
  if f==1:return s
  if f==2:x=max(x,s)
  else:y=min(y,s)
  if x>=y:return s
 J=e[3]if e else 0
 m=L()
 if not m:return-I+l if a((W,X)[S<0],-S)else 0
 m.sort(key=o,reverse=True);b=-I*10;j=m[0]
 for i,v in enumerate(m):
  z=M(v)
  if i==0:r=-R(d-1,-y,-x,l+1)
  else:
   r=-R(d-1,-x-1,-x,l+1)
   if x<r<y:r=-R(d-1,-y,-x,l+1)
  n(z)
  if r>b:b=r;j=v
  x=max(x,r)
  if x>=y:break
 G[k]=(d,b,1+(b>=y)+2*(b<=w),j)
 return b
def H(f,l):
 global N
 F(f);m=L()
 if len(G)>1e5:G.clear()
 N=0;b=m[0]
 for d in range(1,9):
  try:
   s=-I*10
   for v in m:
    y=M(v);r=-R(d-1,-I*10,-s,1);n(y)
    if r>s:s=r;j=v
   b=j;m.remove(j);m.insert(0,j)
  except A:break
 f=b&127;t=(b>>7)&127;r=(b>>14)&7
 v=""
 for s in(f,t):v+="abcdefgh"[s&7]+str((s>>4)+1)
 v+="q"*(r>0)
 return l[0] if v not in l else v
def p(h,b):
 return json.load(u.urlopen(U+h,json.dumps(b).encode()))
def main():
 while 1:
  g=p("/game",{})
  if g["status"]=="done":break
  if g["status"]=="your_move":
   v=H(g["fen"],g["legal_moves"])
   g=p("/move",{"game":g["game"],"move":v})
main()
