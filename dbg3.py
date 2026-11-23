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
for mv in ["d2d4","d7d5","c2c4","c7c6","b1c3","g8f6","e2e3","e7e6","c4d5","c7d5" if False else "c6d5","c3d5"]:
    b.push_uci(mv)
print("FEN after cxd5 cxd5 Nxd5:", b.fen())
fen = b.fen()
M.parse(fen)
print("ev (black to move):", M.ev())
print("black captures:", [uci(m) for m in M.gen(True)])
M.BUDGET = 1000000
M.NODES = 0
print("qs (black to move):", M.qs(-1000000, 1000000, 0), "nodes:", M.NODES)
# full depth-3 score for cxd5 from the opening
b2 = chess.Board()
for mv in ["d2d4","d7d5","c2c4","c7c6","b1c3","g8f6","e2e3","e7e6"]:
    b2.push_uci(mv)
fen2 = b2.fen()
M.parse(fen2)
ms = M.legal()
M.NODES = 0
for m in ms:
    if uci(m) in ("c4d5","e2e4","e2e3","g1f3","c4c5"):
        u = M.make(m)
        s = -M.srch(2, -1000000, 1000000, 1)
        M.unmake(u)
        print(f"  {uci(m)}: depth3 score {s}")
print("nodes:", M.NODES)
