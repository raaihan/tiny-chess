import sys
sys.path.insert(0, '.')
import main as M
import chess

def uci(m):
    f=m&127; t=(m>>7)&127; pr=(m>>14)&7
    s="abcdefgh"[f&7]+str((f>>4)+1)+"abcdefgh"[t&7]+str((t>>4)+1)
    if pr: s+="pnbrqk"[pr-1]
    return s

b = chess.Board()
for mv in ["d2d4","d7d5","c2c4","c7c6","b1c3","g8f6","e2e3","e7e6","c4d5","c6d5"]:
    b.push_uci(mv)
fen = b.fen()
M.parse(fen)
ms = M.legal()
print("legal moves:", len(ms), "first few:", [uci(m) for m in ms[:5]])
M.BUDGET = 60000
M.NODES = 0
# replicate root() step by step
best = ms[0]
print("initial best:", uci(best))
for d in range(1, 6):
    try:
        M.order(ms, 0, 0)
        bs = -1000000; bm = ms[0]
        print(f"depth {d}: NODES before={M.NODES}, ms[0]={uci(ms[0])}")
        for m in ms:
            u = M.make(m)
            s = -M.srch(d-1, -1000000, 1000000, 1)
            M.unmake(u)
            if s > bs: bs = s; bm = m
        best = bm
        print(f" depth {d} done: NODES={M.NODES} best={uci(best)} score={bs}")
    except M.AB:
        print(f" depth {d}: ABORTED at NODES={M.NODES}, best stays {uci(best)}")
        break
print("final best:", uci(best))
