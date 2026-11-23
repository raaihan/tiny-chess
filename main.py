import os,json,urllib.request as u
V=[0,100,320,330,500,900,0]
A1="MMMMMMMMNNOOOOPQPQRRQRSSSTUUMMMM"
A2="GIKKIKMMKMOOMOQQMOQQKMOOIKMMGIKK"
A3="MMMMMMNNMMNNMNNOMNNOMNOOOPPQMMMM"
A4="OPNMNOMLMMKJKJIIKJIIMMKJNOMLOPNM"
Y=['M'*32,A1,A2,A2,A3,A3,A4]
P=[[V[t]+(ord(c)-77)*5 for c in Y[t]] for t in range(7)]
B=[0]*128;CR=15;EP=-1;S=1;K=[4,116];U=[];N=0;L=15e4
CK={0:13,7:14,4:12,112:7,119:11,116:3}
KI=[1,-1,16,-16,15,17,-15,-17];RD=KI[:4];BD=KI[4:];KN=[14,18,31,33,-14,-18,-31,-33]
MT={2:(KN,0),3:(BD,1),4:(RD,1),5:(KI,1),6:(KI,0)}
def A(s,by):
 for O,t in (((-15,-17) if by>0 else (15,17),1),(KN,2),(KI,6)):
  for o in O:
   if not (s+o)&136 and B[s+o]==by*t:return 1
 for O,t in ((BD,3),(RD,4)):
  for o in O:
   w=s+o
   while not w&136:
    p=B[w]
    if p:
     if p in (by*t,by*5):return 1
     break
    w+=o
 return 0
def G():
 ms=[];L7=7*(S>0);SR=1+5*(S<0)
 for f in range(128):
  if f&136:continue
  p=B[f]
  if p*S<=0:continue
  t=abs(p);d=16*S
  if t==1:
   q=(5<<14) if (f+d)>>4==L7 else 0
   for w in (f+d,f+d-1,f+d+1):
    if w&136:continue
    if w==f+d:
     if B[w]:continue
     ms.append(f+(w<<7)+q)
     if (f>>4)==SR and not B[f+2*d]:ms.append(f+(f+2*d<<7))
    elif B[w]*S<0 or w==EP:
     ms.append(f+(w<<7)+q)
  else:
   O,sl=MT[t]
   for o in O:
    w=f+o
    while not w&136:
     if B[w]:
      if B[w]*S<0:ms.append(f+(w<<7))
      break
     ms.append(f+(w<<7))
     if not sl:break
     w+=o
 for r,kf,kt,rf in ((1,4,6,7),(2,4,2,0),(4,116,118,119),(8,116,114,112)):
  if (S>0)==(r<4) and CR&r and B[rf]==4*S and all(not B[s] for s in range(min(kf,rf)+1,max(kf,rf))) and not(A(kf,-S) or A((kf+kt)//2,-S) or A(kt,-S)):ms.append(kf+(kt<<7))
 return ms
def MK(m):
 global CR,EP,S
 f=m&127;t=(m>>7)&127;pr=(m>>14)&7
 p=B[f];c=B[t];e=-1
 if abs(p)==1 and t==EP and not c:
  e=t-16*S;c=B[e];B[e]=0
 U.append((c,e,CR,EP))
 B[t]=pr*S if pr else p;B[f]=0
 if abs(p)==6 and abs(t-f)==2:
  rt=(f+t)//2;rf=t+1 if t>f else t-2;B[rt]=B[rf];B[rf]=0
 CR&=CK.get(f,15);CR&=CK.get(t,15)
 EP=f+16*S if abs(p)==1 and abs(t-f)==32 else -1
 if abs(p)==6:K[0 if S>0 else 1]=t
 S=-S
def UM(m):
 global CR,EP,S
 f=m&127;t=(m>>7)&127;pr=(m>>14)&7
 c,e,CR,EP=U.pop()
 S=-S
 p=B[t]
 if abs(p)==6:
  K[0 if S>0 else 1]=f
  if abs(t-f)==2:rt=(f+t)//2;rf=t+1 if t>f else t-2;B[rf]=B[rt];B[rt]=0
 B[f]=S if pr else p
 B[t]=0
 if e>=0:B[e]=c
 elif c:B[t]=c
def E():
 s=0
 for i,p in enumerate(B):
  if p:
   t=abs(p);h=min(i&7,7-(i&7));r=i>>4
   j=(r if p>0 else 7-r)*4+h
   s+=P[t][j]*(p>0 or -1)
 return s*S
def W(d,a,b,pl):
 global N
 N+=1
 if N>L:raise ValueError
 kk=K[0 if S>0 else 1];c=A(kk,-S)
 if d<=0 and not c:
  s=E()
  if s>=b:return b
  if s>a:a=s
 ms=G() if d>0 or c else [m for m in G() if B[(m>>7)&127]*S<0 or (m>>7)&127==EP]
 ms.sort(key=lambda m:-(V[abs(B[(m>>7)&127])]*10-V[abs(B[m&127])]//10))
 best=-10**9;n=0
 for m in ms:
  MK(m)
  if A(K[0 if S<0 else 1],S):UM(m);continue
  n=1
  s=-W(d-1,-b,-a,pl+1)
  UM(m)
  if s>best:best=s
  if s>a:a=s
  if a>=b:break
 if d<=0:return -100000+pl if c and not n else a
 if best==-10**9:
  return -100000+pl if A(kk,-S) else 0
 return best
def RT(legal):
 global N
 N=0;bm=legal[0]
 for d in range(1,13):
  try:
   a=-10**9;bb=legal[0];best=-10**9
   for m in legal:
    MK(m)
    s=-W(d-1,-10**9,-a,1)
    UM(m)
    if s>best:best=s;bb=m
    if s>a:a=s
   bm=bb
  except ValueError:
   break
 return bm
def UMV(s):
 f=ord(s[0])+16*int(s[1])-113;t=ord(s[2])+16*int(s[3])-113
 pr='nbrq'.index(s[4])+2 if len(s)>4 else 0
 return f+(t<<7)+(pr<<14)
def MVU(m):
 f=m&127;t=(m>>7)&127;pr=(m>>14)&7
 s='%c%d%c%d'%(f%8+97,f//16+1,t%8+97,t//16+1)
 return s+('nbrq'[pr-2]if pr else'')
def post(p,o):
 return json.load(u.urlopen(os.getenv('MAKEFUN_ENV_URL')+p,json.dumps(o).encode()))
while 1:
 g=post('/game',{});st=g['status']
 if st=='done':break
 if st=='your_move':
  B=[0]*128;CR=15;EP=-1;S=1;K=[4,116];U=[]
  for i,c in enumerate('RNBQKBNR'):
   t='PNBRQK'.index(c)+1;B[i]=t;B[112+i]=-t;B[16+i]=1;B[96+i]=-1
  for mv in g['moves']:MK(UMV(mv))
  m=RT([UMV(s) for s in g['legal_moves']])
  post('/move',{'game':g['game'],'move':MVU(m)})
