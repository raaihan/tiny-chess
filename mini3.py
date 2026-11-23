import json,os,sys,urllib.request as u
U=os.environ.get("MAKEFUN_ENV_URL")or sys.exit()
V=[0,100,320,330,500,900,0]
K=[-33,-31,-18,-14,14,18,31,33];G=[-17,-16,-15,-1,1,15,16,17];B=[-17,-15,15,17];J=[-16,-1,1,16]
D=[0,0,K,B,J,B+J,G]
P=[[0]*128 for _ in range(7)]
for s in range(128):
 if s&0x88:continue
 r=s>>4;f=s&7;c=min(f,7-f)+min(r,7-r)
 P[1][s]=100+[0,0,5,10,15,25,40,0][r];P[2][s]=320+6*c-20;P[3][s]=330+4*c-8;P[4][s]=500+(15 if r==6 else 0);P[5][s]=900+2*c-6;P[6][s]=[20,25,10,0,0,10,25,20][f]if r==0 else-15*r
T=[0]*128;S=1;C=0;E=-1;W=4;X=116;N=0;Q=200000
class A(Exception):pass
def F(f):
 global T,S,C,E,W,X
 p=f.split();T=[0]*128
 for i,w in enumerate(p[0].split("/")):
  r=7-i;f=0
  for ch in w:
   if ch.isdigit():f+=int(ch)
   else:
    t="pnbrqk".index(ch.lower())+1;T[r*16+f]=t if ch.isupper()else-t
    if t==6:W=r*16+f if ch.isupper()else X
    f+=1
 S=1 if p[1]=="w"else-1;C=("K"in p[2])+2*("Q"in p[2])+4*("k"in p[2])+8*("q"in p[2])
 E=-1
 if p[3]!="-":E=(int(p[3][1])-1)*16+ord(p[3][0])-97
def a(s,b):
 for o,t in(((-15,-17)if b>0 else(15,17),1),(K,2),(G,6)):
  for d in o:
   x=s+d
   if not x&0x88 and T[x]==b*t:return 1
 for d in B+J:
  t=s+d
  while not t&0x88:
   q=T[t]
   if q:
    if q==b*3 and abs(d)in(15,17)or q==b*4 and abs(d)in(1,16)or q==b*5:return 1
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
   d=16 if S>0 else-16;w=7 if S>0 else 0
   for k,to in enumerate((s+d,s+d-1,s+d+1)):
    if to&0x88:continue
    y=T[to]
    if k==0:
     if o or y:continue
    elif not(y and(y>0)!=(S>0)or to==E):continue
    if to>>4==w:
     for x in(5,4,3,2):m.append(s|to<<7|x<<14)
    else:
     m.append(s|to<<7)
     if k==0 and(s>>4==(1 if S>0 else 6))and T[s+2*d]==0:m.append(s|(s+2*d)<<7)
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
     if t<3 or t>5:break
     v+=d
   if t==6 and not o:
    for d,b in((2,1),(-2,2))if S>0 else((2,4),(-2,8)):
     if C&b and T[s+d]==0 and T[s+d//2]==0 and(d>0 or T[s-3]==0)and T[s+3 if d>0 else s-4]==(4 if S>0 else-4)and not a(s,-S)and not a(s+d//2,-S)and not a(s+d,-S):m.append(s|(s+d)<<7)
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
 for s,b in((4,3),(116,12),(0,2),(7,1),(112,8),(119,4)):
  if f==s or t==s:C&=~b
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
 s=0
 for q in range(128):
  if q&0x88:continue
  p=T[q]
  if not p or abs(p)==6:continue
  t=abs(p);v=P[t][q if p>0 else q^0x70];s+=v if p>0 else-v
 s+=P[6][W]-P[6][X^0x70]
 return s if S>0 else-s
def o(v):
 t=(v>>7)&127;q=T[t]
 return(10000+10*V[abs(q)]-V[abs(T[v&127])])if q or t==E else 0
def q(x,y,l):
 global N
 N+=1
 if N>Q:raise A
 s=e()
 if s>=y:return y
 if s>x:x=s
 if l>20:return x
 k=a(W if S>0 else X,-S);m=g(0)if k else g(1)
 if k:
  d=[]
  for v in m:
   z=M(v);j=W if S<0 else X
   if not a(j,S):d.append(v)
   n(z)
  m=d
  if not m:return-100000+l
 m.sort(key=o,reverse=True)
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
 m.sort(key=o,reverse=True);b=-1000000
 for i,v in enumerate(m):
  z=M(v)
  if i==0:r=-R(d-1,-y,-x,l+1)
  else:
   r=-R(d-1,-x-1,-x,l+1)
   if x<r<y:r=-R(d-1,-y,-x,l+1)
  n(z)
  if r>b:b=r
  if r>x:x=r
  if x>=y:break
 return b
def H(f,l):
 global N
 F(f);m=L()
 if not m:return None
 b=m[0];N=0
 for d in range(1,9):
  try:
   s=-1000000;j=m[0]
   for i,v in enumerate(m):
    y=M(v)
    if i==0:r=-R(d-1,-1000000,1000000,1)
    else:
     r=-R(d-1,-s-1,-s,1)
     if r>s:r=-R(d-1,-1000000,1000000,1)
    n(y)
    if r>s:s=r;j=v
   b=j
  except A:break
 f=b&127;t=(b>>7)&127;r=(b>>14)&7
 v="abcdefgh"[f&7]+str((f>>4)+1)+"abcdefgh"[t&7]+str(((t>>4)+1))+("pnbrqk"[r-1]if r else"")
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
   v=H(g["fen"],g["legal_moves"])
   if v is None:g=p("/resign",{"game":g["game"]});break
   try:g=p("/move",{"game":g["game"],"move":v})
   except SystemExit:g=p("/move",{"game":g["game"],"move":g["legal_moves"][0]})
main()
