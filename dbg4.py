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
print("FEN after cxd5 cxd5:", fen)
M.parse(fen)
print("ev (white to move):", M.ev())
M.BUDGET = 60000
# score each root move at increasing depth (like root does)
ms = M.legal()
M.NODES = 0
print("depth-by-depth for Nxd5 and Nf3:")
for d in range(1, 6):
    M.NODES = 0
    try:
        scores = {}
        for m in ms:
            u = M.make(m)
            s = -M.srch(d-1, -1000000, 1000000, 1)
            M.unmake(u)
            scores[uci(m)] = s
        print(f" depth {d}: nodes={M.NODES} Nxd5={scores.get('c3d5')} Nf3={scores.get('g1f3')} e4={scores.get('e3e4')} best={max(scores, key=scores.get)}({max(scores.values())})")
    except M.AB:
        print(f" depth {d}: ABORTED nodes={M.NODES}")
        break
# what does root() choose?
M.BUDGET = 60000
print("root choice:", M.root(fen, [uci(m) for m in M.legal()]))
