import json,os,sys,urllib.request as u
U=os.environ.get("MAKEFUN_ENV_URL") or sys.exit()
V=[0,100,320,330,500,900,0]
K=[-33,-31,-18,-14,14,18,31,33]
G=[-17,-16,-15,-1,1,15,16,17]
B=[-17,-15,15,17]
R=[-16,-1,1,16]
D=[0,0,K,B,R,B+R,G]
P=[[0]*128 for _ in range(7)]
for r in range(8):
 for f in range(8):
  s=r*16+f;c=min(f,7-f)+min(r,7-r)
  P[1][s]=100+[0,0,5,10,15,25,40,0][r]
  P[2][s]=320+6*c-20
  P[3][s]=330+4*c-8
  P[4][s]=500+(15 if r==6 else 0)
  P[5][s]=900+2*c-6
  P[6][s]=[20,25,10,0,0,10,25,20][f] if r==0 else-15*r
T=[0]*128;S=1;C=0;E=-1;W=4;X=116;N=0;Q=200000
class A(Exception):pass
def F(f):
 global T,S,C,E,W,X
 p=f.split();T=[0]*128
 for i,w in enumerate(p[0].split("/")):
  r=7-i;f=0
  for ch in w:
   if ch.isdigit():f+=int(ch)
   else:t="pnbrqk".index(ch.lower())+1;T[r*16+f]=t if ch.isupper() else-t;f+=1
 S=1 if p[1]=="w" else-1;C=0
 if"K"in p[2]:C|=1
 if"Q"in p[2]:C|=2
 if"k"in p[2]:C|=4
 if"q"in p[2]:C|=8
 E=-1
 if p[3]!="-":E=(int(p[3][1])-1)*16+ord(p[3][0])-97
 W=4;X=116
 for s in range(128):
  if T[s]==6:W=s
  elif T[s]==-6:X=s
def a(s,b):
 for d in(-15,-17)if b>0 else(15,17):
  t=s+d
  if not t&0x88 and T[t]==b:return 1
 for d in K:
  t=s+d
  if not t&0x88 and T[t]==b*2:return 1
 for d in G:
  t=s+d
  if not t&0x88 and T[t]==b*6:return 1
 for d in B:
  t=s+d
  while not t&0x88:
   q=T[t]
   if q:
    if q==b*3 or q==b*5:return 1
    break
   t+=d
 for d in R:
  t=s+d
  while not t&0x88:
   q=T[t]
   if q:
    if q==b*4 or q==b*5:return 1
    break
   t+=d
 return 0
def g(o=0):
 m=[]
 for s in range(128):
  if s&0x88:continue
  p=T[s]
  if not p or(p>0)!=(S>0):continue
  t=abs(p)
  if t==1:
   d=16 if S>0 else-16;w=7 if S>0 else 0;v=s+d
   if not o and T[v]==0:
    if v>>4==w:
     for x in(5,4,3,2):m.append(s|v<<7|x<<14)
    else:
     m.append(s|v<<7)
     if(s>>4==(1 if S>0 else 6))and T[s+2*d]==0:m.append(s|(s+2*d)<<7)
   for e in(d-1,d+1):
    v=s+e
    if v&0x88:continue
    y=T[v]
    if y and(y>0)!=(S>0):
     if v>>4==w:
      for x in(5,4,3,2):m.append(s|v<<7|x<<14)
     else:m.append(s|v<<7)
    elif v==E:m.append(s|v<<7)
  else:
   for d in D[t]:
    v=s+d
    while not v&0x88:
     y=T[v]
     if y==0:
      if not o:m.append(s|v<<7)
     else:
      if(y>0)!=(S>0):m.append(s|v<<7)
      break
     if t not in(3,4,5):break
     v+=d
   if t==6 and not o:
    if S>0:
     if C&1 and T[5]==0 and T[6]==0 and T[7]==4 and not a(4,-1)and not a(5,-1)and not a(6,-1):m.append(4|6<<7)
     if C&2 and T[3]==0 and T[2]==0 and T[1]==0 and T[0]==4 and not a(4,-1)and not a(3,-1)and not a(2,-1):m.append(4|2<<7)
    else:
     if C&4 and T[117]==0 and T[118]==0 and T[119]==-4 and not a(116,1)and not a(117,1)and not a(118,1):m.append(116|118<<7)
     if C&8 and T[115]==0 and T[114]==0 and T[113]==0 and T[112]==-4 and not a(116,1)and not a(115,1)and not a(114,1):m.append(116|114<<7)
 return m
def M(m):
 global S,C,E,W,X
 f=m&127;t=(m>>7)&127;r=(m>>14)&7;p=T[f];c=T[t];e=-1
 if abs(p)==1 and t==E and c==0:e=t-16 if S>0 else t+16;c=T[e];T[e]=0
 z=(m,c,e,C,E);T[t]=r*S if r else p;T[f]=0
 if abs(p)==6:
  if S>0:W=t
  else:X=t
  if abs(t-f)==2:
   if t>f:T[t-1]=T[t+1];T[t+1]=0
   else:T[t+1]=T[t-2];T[t-2]=0
 if f==4:C&=~3
 if f==116:C&=~12
 if f==0 or t==0:C&=~2
 if f==7 or t==7:C&=~1
 if f==112 or t==112:C&=~8
 if f==119 or t==119:C&=~4
 E=f+(16 if S>0 else-16)if abs(p)==1 and abs(t-f)==32 else-1
 S=-S;return z
def n(z):
 global S,C,E,W,X
 m,c,e,w,v=z;f=m&127;t=(m>>7)&127;r=(m>>14)&7;S=-S;C=w;E=v;p=T[t]
 if abs(p)==6:
  if S>0:W=f
  else:X=f
  if abs(t-f)==2:
   if t>f:T[t+1]=T[t-1];T[t-1]=0
   else:T[t-2]=T[t+1];T[t+1]=0
 T[f]=S if r else p
 if e>=0:T[e]=c;T[t]=0
 else:T[t]=c
def L():
 m=[];k=W if S>0 else X
 for x in g():
  z=M(x);j=W if S<0 else X
  if not a(j,S):m.append(x)
  n(z)
 return m
def e():
 s=0;y=0
 for q in range(128):
  if q&0x88:continue
  p=T[q]
  if not p or abs(p)==6:continue
  t=abs(p);v=P[t][q if p>0 else q^0x70];s+=v if p>0 else-v
  if t!=1:y+=V[t]
 s+=P[6][W]-P[6][X^0x70] if y>1500 else P[6][W]*2-P[6][X^0x70]*2
 return s if S>0 else-s
def q(x,y,l):
 global N
 N+=1
 if N>Q:raise A
 s=e()
 if s>=y:return y
 if s>x:x=s
 if l>20:return x
 k=a(W if S>0 else X,-S)
 m=g(0)if k else g(1)
 if k:
  d=[]
  for v in m:
   z=M(v);j=W if S<0 else X
   if not a(j,S):d.append(v)
   n(z)
  m=d
  if not m:return-100000+l
 m.sort(key=lambda v:(10000+10*V[abs(T[(v>>7)&127])]-V[abs(T[v&127])])if T[(v>>7)&127]or((v>>7)&127)==E else 0,reverse=True)
 for v in m:
  if not k and not((v>>14)&7):
   t=(v>>7)&127;w=abs(T[t])if T[t]else 1
   if s+V[w]+100<x:continue
  z=M(v);r=-q(-y,-x,l+1);n(z)
  if r>=y:return y
  if r>x:x=r
 return x
def R(d,x,y,l):
 global N
 N+=1
 if N>Q:raise A
 if d<=0:return q(x,y,l)
 m=L()
 if not m:return-100000+l if a(W if S>0 else X,-S)else 0
 m.sort(key=lambda v:(10000+10*V[abs(T[(v>>7)&127])]-V[abs(T[v&127])])if T[(v>>7)&127]or((v>>7)&127)==E else 0,reverse=True)
 b=-1000000
 for v in m:
  z=M(v);r=-R(d-1,-y,-x,l+1);n(z)
  if r>b:b=r
  if r>x:x=r
  if x>=y:break
 return b
def W(f,l):
 global N
 F(f);m=L()
 if not m:return None
 z={v:("abcdefgh"[(v&127)&7]+str(((v&127)>>4)+1)+"abcdefgh"[((v>>7)&127)&7]+str((((v>>7)&127)>>4)+1)+("pnbrqk"[((v>>14)&7)-1]if((v>>14)&7)else""))for v in m}
 b=m[0];N=0
 for d in range(1,9):
  try:
   s=-1000000;j=m[0]
   for v in m:
    z2=M(v);r=-R(d-1,-1000000,1000000,1);n(z2)
    if r>s:s=r;j=v
   b=j
  except A:break
 v=z[b]
 return l[0] if v not in l else v
def p(h,b):
 r=u.Request(U+h,data=json.dumps(b).encode(),headers={"content-type":"application/json"})
 try:
  with u.urlopen(r)as w:return json.load(w)
 except Exception as z:sys.exit(str(z))
def main():
 while 1:
  g=p("/game",{})
  if g["status"]=="done":break
  while g["status"]=="your_move":
   v=W(g["fen"],g["legal_moves"])
   if v is None:g=p("/resign",{"game":g["game"]});break
   try:g=p("/move",{"game":g["game"],"move":v})
   except SystemExit:g=p("/move",{"game":g["game"],"move":g["legal_moves"][0]})
  print(f"game {g.get('game')}: {g.get('outcome')} by {g.get('reason')}",file=sys.stderr)
 print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost",file=sys.stderr)
main()
