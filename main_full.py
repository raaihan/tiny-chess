import json,os,sys,urllib.request,urllib.error
U=os.environ.get("MAKEFUN_ENV_URL") or sys.exit("no env")
V=[0,100,320,330,500,900,0]
KN=[-33,-31,-18,-14,14,18,31,33]
KG=[-17,-16,-15,-1,1,15,16,17]
BD=[-17,-15,15,17]
RD=[-16,-1,1,16]
QD=BD+RD
B=[0]*128
S=1
C=0
E=-1
KW=4
KB=116
NODES=0
BUDGET=200000
TT={}
KIL=[[0,0] for _ in range(128)]
HIS=[[0]*128 for _ in range(13)]
class AB(Exception): pass
def pst():
 T=[[0]*128 for _ in range(7)]
 for r in range(8):
  for f in range(8):
   s=r*16+f
   c=min(f,7-f)+min(r,7-r)
   T[1][s]=100+[0,0,5,10,15,25,40,0][r]+(12 if f in(3,4) and r>=3 else 0)
   T[2][s]=320+6*c-20
   T[3][s]=330+4*c-8
   T[4][s]=500+(15 if r==6 else 0)+(5 if r==0 and f in(3,4) else 0)
   T[5][s]=900+2*c-6
   T[6][s]=[20,25,10,0,0,10,25,20][f] if r==0 else max(-50,-15*r)
 return T
PST=pst()
PKE=[[0]*128 for _ in range(7)]
for r in range(8):
 for f in range(8):
  s=r*16+f
  c=min(f,7-f)+min(r,7-r)
  PKE[6][s]=8*c-24
def parse(fen):
 global B,S,C,E,KW,KB
 p=fen.split()
 B=[0]*128
 for i,row in enumerate(p[0].split("/")):
  r=7-i;f=0
  for ch in row:
   if ch.isdigit(): f+=int(ch)
   else:
    t="pnbrqk".index(ch.lower())+1
    B[r*16+f]=t if ch.isupper() else -t
    f+=1
 S=1 if p[1]=="w" else -1
 C=0
 if "K" in p[2]: C|=1
 if "Q" in p[2]: C|=2
 if "k" in p[2]: C|=4
 if "q" in p[2]: C|=8
 E=-1
 if p[3]!="-": E=(int(p[3][1])-1)*16+ord(p[3][0])-97
 KW=4;KB=116
 for s in range(128):
  if B[s]==6: KW=s
  elif B[s]==-6: KB=s
def att(sq,by):
 for d in(-15,-17) if by>0 else(15,17):
  t=sq+d
  if not t&0x88 and B[t]==by: return 1
 for d in KN:
  t=sq+d
  if not t&0x88 and B[t]==by*2: return 1
 for d in KG:
  t=sq+d
  if not t&0x88 and B[t]==by*6: return 1
 for d in BD:
  t=sq+d
  while not t&0x88:
   q=B[t]
   if q:
    if q==by*3 or q==by*5: return 1
    break
   t+=d
 for d in RD:
  t=sq+d
  while not t&0x88:
   q=B[t]
   if q:
    if q==by*4 or q==by*5: return 1
    break
   t+=d
 return 0
def gen(caponly=False):
 ms=[]
 for sq in range(128):
  if sq&0x88: continue
  p=B[sq]
  if not p or(p>0)!=(S>0): continue
  t=abs(p)
  if t==1:
   d=16 if S>0 else -16
   sr=1 if S>0 else 6
   pr=7 if S>0 else 0
   to=sq+d
   if not caponly and B[to]==0:
    if to>>4==pr:
     for q in(5,4,3,2): ms.append(sq|to<<7|q<<14)
    else:
     ms.append(sq|to<<7)
     if sq>>4==sr and B[sq+2*d]==0: ms.append(sq|(sq+2*d)<<7)
   for dd in(d-1,d+1):
    to=sq+dd
    if to&0x88: continue
    q=B[to]
    if q and(q>0)!=(S>0):
     if to>>4==pr:
      for qq in(5,4,3,2): ms.append(sq|to<<7|qq<<14)
     else: ms.append(sq|to<<7)
    elif to==E: ms.append(sq|to<<7)
  elif t==2 or t==6:
   for d in(KN if t==2 else KG):
    to=sq+d
    if to&0x88: continue
    q=B[to]
    if not caponly and q==0: ms.append(sq|to<<7)
    elif q and(q>0)!=(S>0): ms.append(sq|to<<7)
   if t==6 and not caponly:
    if S>0:
     if C&1 and B[5]==0 and B[6]==0 and B[7]==4 and not att(4,-1) and not att(5,-1) and not att(6,-1): ms.append(4|6<<7)
     if C&2 and B[3]==0 and B[2]==0 and B[1]==0 and B[0]==4 and not att(4,-1) and not att(3,-1) and not att(2,-1): ms.append(4|2<<7)
    else:
     if C&4 and B[117]==0 and B[118]==0 and B[119]==-4 and not att(116,1) and not att(117,1) and not att(118,1): ms.append(116|118<<7)
     if C&8 and B[115]==0 and B[114]==0 and B[113]==0 and B[112]==-4 and not att(116,1) and not att(115,1) and not att(114,1): ms.append(116|114<<7)
  else:
   for d in(BD if t==3 else RD if t==4 else QD):
    to=sq+d
    while not to&0x88:
     q=B[to]
     if q==0:
      if not caponly: ms.append(sq|to<<7)
     else:
      if(q>0)!=(S>0): ms.append(sq|to<<7)
      break
     to+=d
 return ms
def make(m):
 global S,C,E,KW,KB
 f=m&127;t=(m>>7)&127;pr=(m>>14)&7
 p=B[f];cap=B[t];eq=-1
 if abs(p)==1 and t==E and cap==0:
  eq=t-16 if S>0 else t+16
  cap=B[eq];B[eq]=0
 u=(m,cap,eq,C,E)
 B[t]=pr*S if pr else p
 B[f]=0
 if abs(p)==6:
  if S>0: KW=t
  else: KB=t
  if abs(t-f)==2:
   if t>f: B[t-1]=B[t+1];B[t+1]=0
   else: B[t+1]=B[t-2];B[t-2]=0
 if f==4: C&=~3
 if f==116: C&=~12
 if f==0 or t==0: C&=~2
 if f==7 or t==7: C&=~1
 if f==112 or t==112: C&=~8
 if f==119 or t==119: C&=~4
 if abs(p)==1 and abs(t-f)==32: E=f+(16 if S>0 else -16)
 else: E=-1
 S=-S
 return u
def unmake(u):
 global S,C,E,KW,KB
 m,cap,eq,c0,e0=u
 f=m&127;t=(m>>7)&127;pr=(m>>14)&7
 S=-S
 C=c0;E=e0
 p=B[t]
 if abs(p)==6:
  if S>0: KW=f
  else: KB=f
  if abs(t-f)==2:
   if t>f: B[t+1]=B[t-1];B[t-1]=0
   else: B[t-2]=B[t+1];B[t+1]=0
 B[f]=S if pr else p
 if eq>=0: B[eq]=cap;B[t]=0
 else: B[t]=cap
def legal():
 ms=[]
 k=KW if S>0 else KB
 ck=att(k,-S)
 kr=k>>4;kf=k&7
 for m in gen():
  f=m&127;t=(m>>7)&127;p=B[f]
  if abs(p)==1 and t==E and B[t]==0:
   u=make(m)
   kk=KW if S<0 else KB
   if not att(kk,S): ms.append(m)
   unmake(u);continue
  if not ck and abs(p)!=6 and(f>>4)!=kr and(f&7)!=kf and abs((f>>4)-kr)!=abs((f&7)-kf):
   ms.append(m);continue
  u=make(m)
  kk=KW if S<0 else KB
  if not att(kk,S): ms.append(m)
  unmake(u)
 return ms
def ev():
 sc=0;np=0;bw=0;bb=0
 for r in range(8):
  b0=r*16
  for f in range(8):
   s=b0+f;p=B[s]
   if not p: continue
   t=abs(p)
   if t==6: continue
   v=PST[t][s if p>0 else s^0x70]
   sc+=v if p>0 else -v
   if t!=1: np+=V[t]
   if t==3:
    if p>0: bw+=1
    else: bb+=1
 if np>1500: sc+=PST[6][KW]-PST[6][KB^0x70]
 else: sc+=PKE[6][KW]-PKE[6][KB^0x70]
 if bw>=2: sc+=30
 if bb>=2: sc-=30
 return sc if S>0 else -sc
def order(ms,ttm,ply):
 def sc(m):
  if m==ttm: return 1000000
  f=m&127;t=(m>>7)&127
  q=B[t]
  if q or(t==E and abs(B[f])==1):
   v=abs(q) if q else 1
   return 10000+10*V[v]-V[abs(B[f])]
  if m==KIL[ply][0]: return 9000
  if m==KIL[ply][1]: return 8000
  p=B[f];ty=abs(p)
  if p>0: return HIS[p+6][t]+PST[ty][t]-PST[ty][f]
  return HIS[p+6][t]+PST[ty][t^0x70]-PST[ty][f^0x70]
 ms.sort(key=sc,reverse=True)
 return ms
def qs(a,b,ply):
 global NODES
 NODES+=1
 if NODES>BUDGET: raise AB
 st=ev()
 if st>=b: return b
 if st>a: a=st
 if ply>20: return a
 inck=att(KW if S>0 else KB,-S)
 ms=gen(False) if inck else gen(True)
 if inck:
  lm=[]
  for m in ms:
   u=make(m)
   k=KW if S<0 else KB
   if not att(k,S): lm.append(m)
   unmake(u)
  ms=lm
  if not ms: return -100000+ply
 order(ms,0,ply)
 for m in ms:
  if not inck and not((m>>14)&7):
   t=(m>>7)&127;v=abs(B[t]) if B[t] else 1
   if st+V[v]+100<a: continue
  u=make(m)
  s=-qs(-b,-a,ply+1)
  unmake(u)
  if s>=b: return b
  if s>a: a=s
 return a
def srch(d,a,b,ply):
 global NODES
 NODES+=1
 if NODES>BUDGET: raise AB
 if d<=0: return qs(a,b,ply)
 key=(tuple(B),S,C,E)
 e=TT.get(key)
 ttm=0;ao=a
 if e and e[0]>=d:
  _,s,fl,mv=e
  if fl==1: return s
  if fl==2 and s>a: a=s
  if fl==3 and s<b: b=s
  if a>=b: return s
  ttm=mv
 ms=legal()
 if not ms:
  return -100000+ply if att(KW if S>0 else KB,-S) else 0
 order(ms,ttm,ply)
 best=-1000000
 bm=ms[0]
 for i,m in enumerate(ms):
  u=make(m)
  if i==0: s=-srch(d-1,-b,-a,ply+1)
  else:
   s=-srch(d-1,-a-1,-a,ply+1)
   if a<s<b: s=-srch(d-1,-b,-a,ply+1)
  unmake(u)
  if s>best: best=s;bm=m
  if s>a: a=s
  if a>=b:
   if not B[m>>7&127] and not((m>>14)&7):
    if KIL[ply][0]!=m: KIL[ply][1]=KIL[ply][0];KIL[ply][0]=m
    HIS[B[m&127]+6][m>>7&127]+=d*d
   break
 fl=1 if best>ao and best<b else 2 if best>=b else 3
 TT[key]=(d,best,fl,bm)
 return best
def root(fen,legal_uci):
 global NODES
 parse(fen)
 ms=legal()
 if not ms: return None
 uci={mv:("abcdefgh"[ (mv&127)&7]+str(((mv&127)>>4)+1)+"abcdefgh"[((mv>>7)&127)&7]+str((((mv>>7)&127)>>4)+1)+("pnbrqk"[((mv>>14)&7)-1] if((mv>>14)&7) else "")) for mv in ms}
 best=ms[0]
 NODES=0
 dep=0
 for d in range(1,9):
  try:
   order(ms,0,0)
   bs=-1000000;bm=ms[0]
   for i,m in enumerate(ms):
    u=make(m)
    if i==0: s=-srch(d-1,-1000000,1000000,1)
    else:
     s=-srch(d-1,-bs-1,-bs,1)
     if s>bs: s=-srch(d-1,-1000000,1000000,1)
    unmake(u)
    if s>bs: bs=s;bm=m
   best=bm;dep=d
  except AB:
   break
  if len(TT)>400000: TT.clear()
 mv=uci[best]
 if mv not in legal_uci: return legal_uci[0]
 return mv
def post(path,body):
 req=urllib.request.Request(U+path,data=json.dumps(body).encode(),headers={"content-type":"application/json"})
 try:
  with urllib.request.urlopen(req) as r: return json.load(r)
 except urllib.error.HTTPError as e:
  sys.exit(f"{path}: HTTP {e.code}")
def main():
 while True:
  g=post("/game",{})
  if g["status"]=="done": break
  while g["status"]=="your_move":
   mv=root(g["fen"],g["legal_moves"])
   if mv is None: g=post("/resign",{"game":g["game"]});break
   try: g=post("/move",{"game":g["game"],"move":mv})
   except SystemExit:
    g=post("/move",{"game":g["game"],"move":g["legal_moves"][0]})
  print(f"game {g.get('game')}: {g.get('outcome')} by {g.get('reason')}",file=sys.stderr)
 print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost",file=sys.stderr)
if __name__=="__main__": main()
