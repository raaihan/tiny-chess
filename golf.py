import json,os,sys,urllib.request as u
U=os.environ.get("MAKEFUN_ENV_URL") or sys.exit("no env")
V=[0,100,320,330,500,900,0]
KN=[-33,-31,-18,-14,14,18,31,33]
KG=[-17,-16,-15,-1,1,15,16,17]
BD=[-17,-15,15,17]
RD=[-16,-1,1,16]
D=[0,0,KN,BD,RD,BD+RD,KG]
B=[0]*128
S=1;C=0;E=-1;KW=4;KB=116;N=0;BDG=200000
T={};KI=[[0,0] for _ in range(128)];HI=[[0]*128 for _ in range(13)]
class A(Exception):pass
P=[[0]*128 for _ in range(7)]
for r in range(8):
 for f in range(8):
  s=r*16+f;c=min(f,7-f)+min(r,7-r)
  P[1][s]=100+[0,0,5,10,15,25,40,0][r]+(12 if f in(3,4) and r>=3 else 0)
  P[2][s]=320+6*c-20
  P[3][s]=330+4*c-8
  P[4][s]=500+(15 if r==6 else 0)+(5 if r==0 and f in(3,4) else 0)
  P[5][s]=900+2*c-6
  P[6][s]=[20,25,10,0,0,10,25,20][f] if r==0 else max(-50,-15*r)
K=[[0]*128 for _ in range(7)]
for r in range(8):
 for f in range(8):
  s=r*16+f;c=min(f,7-f)+min(r,7-r)
  K[6][s]=8*c-24
def F(f):
 global B,S,C,E,KW,KB
 p=f.split();B=[0]*128
 for i,w in enumerate(p[0].split("/")):
  r=7-i;f=0
  for ch in w:
   if ch.isdigit():f+=int(ch)
   else:
    t="pnbrqk".index(ch.lower())+1;B[r*16+f]=t if ch.isupper() else -t;f+=1
 S=1 if p[1]=="w" else -1;C=0
 if "K" in p[2]:C|=1
 if "Q" in p[2]:C|=2
 if "k" in p[2]:C|=4
 if "q" in p[2]:C|=8
 E=-1
 if p[3]!="-":E=(int(p[3][1])-1)*16+ord(p[3][0])-97
 KW=4;KB=116
 for s in range(128):
  if B[s]==6:KW=s
  elif B[s]==-6:KB=s
def a(s,b):
 for d in(-15,-17) if b>0 else(15,17):
  t=s+d
  if not t&0x88 and B[t]==b:return 1
 for d in KN:
  t=s+d
  if not t&0x88 and B[t]==b*2:return 1
 for d in KG:
  t=s+d
  if not t&0x88 and B[t]==b*6:return 1
 for d in BD:
  t=s+d
  while not t&0x88:
   q=B[t]
   if q:
    if q==b*3 or q==b*5:return 1
    break
   t+=d
 for d in RD:
  t=s+d
  while not t&0x88:
   q=B[t]
   if q:
    if q==b*4 or q==b*5:return 1
    break
   t+=d
 return 0
def G(o=0):
 m=[]
 for s in range(128):
  if s&0x88:continue
  p=B[s]
  if not p or(p>0)!=(S>0):continue
  t=abs(p)
  if t==1:
   d=16 if S>0 else-16;q=1 if S>0 else 6;w=7 if S>0 else 0;v=s+d
   if not o and B[v]==0:
    if v>>4==w:
     for x in(5,4,3,2):m.append(s|v<<7|x<<14)
    else:
     m.append(s|v<<7)
     if s>>4==q and B[s+2*d]==0:m.append(s|(s+2*d)<<7)
   for dd in(d-1,d+1):
    v=s+dd
    if v&0x88:continue
    y=B[v]
    if y and(y>0)!=(S>0):
     if v>>4==w:
      for x in(5,4,3,2):m.append(s|v<<7|x<<14)
     else:m.append(s|v<<7)
    elif v==E:m.append(s|v<<7)
  else:
   for d in D[t]:
    v=s+d
    while not v&0x88:
     y=B[v]
     if y==0:
      if not o:m.append(s|v<<7)
     else:
      if(y>0)!=(S>0):m.append(s|v<<7)
      break
     if t not in(3,4,5):break
     v+=d
   if t==6 and not o:
    if S>0:
     if C&1 and B[5]==0 and B[6]==0 and B[7]==4 and not a(4,-1) and not a(5,-1) and not a(6,-1):m.append(4|6<<7)
     if C&2 and B[3]==0 and B[2]==0 and B[1]==0 and B[0]==4 and not a(4,-1) and not a(3,-1) and not a(2,-1):m.append(4|2<<7)
    else:
     if C&4 and B[117]==0 and B[118]==0 and B[119]==-4 and not a(116,1) and not a(117,1) and not a(118,1):m.append(116|118<<7)
     if C&8 and B[115]==0 and B[114]==0 and B[113]==0 and B[112]==-4 and not a(116,1) and not a(115,1) and not a(114,1):m.append(116|114<<7)
 return m
def M(m):
 global S,C,E,KW,KB
 f=m&127;t=(m>>7)&127;r=(m>>14)&7;p=B[f];c=B[t];e=-1
 if abs(p)==1 and t==E and c==0:
  e=t-16 if S>0 else t+16;c=B[e];B[e]=0
 u=(m,c,e,C,E);B[t]=r*S if r else p;B[f]=0
 if abs(p)==6:
  if S>0:KW=t
  else:KB=t
  if abs(t-f)==2:
   if t>f:B[t-1]=B[t+1];B[t+1]=0
   else:B[t+1]=B[t-2];B[t-2]=0
 if f==4:C&=~3
 if f==116:C&=~12
 if f==0 or t==0:C&=~2
 if f==7 or t==7:C&=~1
 if f==112 or t==112:C&=~8
 if f==119 or t==119:C&=~4
 E=f+(16 if S>0 else-16) if abs(p)==1 and abs(t-f)==32 else-1
 S=-S
 return u
def n(u):
 global S,C,E,KW,KB
 m,c,e,w,v=u;f=m&127;t=(m>>7)&127;r=(m>>14)&7;S=-S;C=w;E=v;p=B[t]
 if abs(p)==6:
  if S>0:KW=f
  else:KB=f
  if abs(t-f)==2:
   if t>f:B[t+1]=B[t-1];B[t-1]=0
   else:B[t-2]=B[t+1];B[t+1]=0
 B[f]=S if r else p
 if e>=0:B[e]=c;B[t]=0
 else:B[t]=c
def L():
 m=[];k=KW if S>0 else KB;z=a(k,-S);r=k>>4;g=k&7
 for x in G():
  f=x&127;t=(x>>7)&127;p=B[f]
  if abs(p)==1 and t==E and B[t]==0:
   u=M(x);j=KW if S<0 else KB
   if not a(j,S):m.append(x)
   n(u);continue
  if not z and abs(p)!=6 and(f>>4)!=r and(f&7)!=g and abs((f>>4)-r)!=abs((f&7)-g):m.append(x);continue
  u=M(x);j=KW if S<0 else KB
  if not a(j,S):m.append(x)
  n(u)
 return m
def e():
 s=0;y=0;w=0;b=0
 for r in range(8):
  o=r*16
  for f in range(8):
   q=o+f;p=B[q]
   if not p:continue
   t=abs(p)
   if t==6:continue
   v=P[t][q if p>0 else q^0x70];s+=v if p>0 else-v
   if t!=1:y+=V[t]
   if t==3:
    if p>0:w+=1
    else:b+=1
 s+=P[6][KW]-P[6][KB^0x70] if y>1500 else K[6][KW]-K[6][KB^0x70]
 if w>=2:s+=30
 if b>=2:s-=30
 return s if S>0 else-s
def O(m,v,y):
 def z(x):
  if x==v:return 1000000
  f=x&127;t=(x>>7)&127;q=B[t]
  if q or(t==E and abs(B[f])==1):
   w=abs(q) if q else 1;return 10000+10*V[w]-V[abs(B[f])]
  if x==KI[y][0]:return 9000
  if x==KI[y][1]:return 8000
  p=B[f];h=abs(p)
  return HI[p+6][t]+(P[h][t]-P[h][f] if p>0 else P[h][t^0x70]-P[h][f^0x70])
 m.sort(key=z,reverse=True);return m
def q(x,y,l):
 global N
 N+=1
 if N>BDG:raise A
 s=e()
 if s>=y:return y
 if s>x:x=s
 if l>20:return x
 k=a(KW if S>0 else KB,-S)
 m=G(0) if k else G(1)
 if k:
  d=[]
  for v in m:
   u=M(v);j=KW if S<0 else KB
   if not a(j,S):d.append(v)
   n(u)
  m=d
  if not m:return-100000+l
 O(m,0,l)
 for v in m:
  if not k and not((v>>14)&7):
   t=(v>>7)&127;w=abs(B[t]) if B[t] else 1
   if s+V[w]+100<x:continue
  u=M(v);r=-q(-y,-x,l+1);n(u)
  if r>=y:return y
  if r>x:x=r
 return x
def R(d,x,y,l):
 global N
 N+=1
 if N>BDG:raise A
 if d<=0:return q(x,y,l)
 k=(tuple(B),S,C,E);w=T.get(k);v=0;o=x
 if w and w[0]>=d:
  _,s,g,j=w
  if g==1:return s
  if g==2 and s>x:x=s
  if g==3 and s<y:y=s
  if x>=y:return s
  v=j
 m=L()
 if not m:return-100000+l if a(KW if S>0 else KB,-S) else 0
 O(m,v,l);b=-1000000;j=m[0]
 for i,v in enumerate(m):
  u=M(v)
  if i==0:r=-R(d-1,-y,-x,l+1)
  else:
   r=-R(d-1,-x-1,-x,l+1)
   if x<r<y:r=-R(d-1,-y,-x,l+1)
  n(u)
  if r>b:b=r;j=v
  if r>x:x=r
  if x>=y:
   if not B[v>>7&127] and not((v>>14)&7):
    if KI[l][0]!=v:KI[l][1]=KI[l][0];KI[l][0]=v
    HI[B[v&127]+6][v>>7&127]+=d*d
   break
 g=1 if b>o and b<y else 2 if b>=y else 3
 T[k]=(d,b,g,j)
 return b
def W(f,l):
 global N
 F(f);m=L()
 if not m:return None
 z={v:("abcdefgh"[(v&127)&7]+str(((v&127)>>4)+1)+"abcdefgh"[((v>>7)&127)&7]+str((((v>>7)&127)>>4)+1)+("pnbrqk"[((v>>14)&7)-1] if((v>>14)&7) else "")) for v in m}
 b=m[0];N=0
 for d in range(1,9):
  try:
   O(m,0,0);s=-1000000;j=m[0]
   for i,v in enumerate(m):
    u=M(v)
    if i==0:r=-R(d-1,-1000000,1000000,1)
    else:
     r=-R(d-1,-s-1,-s,1)
     if r>s:r=-R(d-1,-1000000,1000000,1)
    n(u)
    if r>s:s=r;j=v
   b=j
  except A:break
  if len(T)>400000:T.clear()
 v=z[b]
 return l[0] if v not in l else v
def p(h,b):
 q=u.Request(U+h,data=json.dumps(b).encode(),headers={"content-type":"application/json"})
 try:
  with u.urlopen(q) as r:return json.load(r)
 except Exception as z:sys.exit(str(z))
def main():
 while True:
  g=p("/game",{})
  if g["status"]=="done":break
  while g["status"]=="your_move":
   v=W(g["fen"],g["legal_moves"])
   if v is None:g=p("/resign",{"game":g["game"]});break
   try:g=p("/move",{"game":g["game"],"move":v})
   except SystemExit:g=p("/move",{"game":g["game"],"move":g["legal_moves"][0]})
  print(f"game {g.get('game')}: {g.get('outcome')} by {g.get('reason')}",file=sys.stderr)
 print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost",file=sys.stderr)
if __name__=="__main__":main()
