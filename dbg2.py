import sys
sys.path.insert(0, '.')
import main as M
import chess

def uci(m):
    f=m&127; t=(m>>7)&127; pr=(m>>14)&7
    s="abcdefgh"[f&7]+str((f>>4)+1)+"abcdefgh"[t&7]+str((t>>4)+1)
    if pr: s+="pnbrqk"[pr-1]
    return s

def find_move(uci_str):
    for m in M.legal():
        if uci(m)==uci_str: return m
    return None

# Position after 1.cxd5 cxd5 2.Nxd5, black to move
fen = "rnbqkbnr/pp2pppp/2p5/3N4/3P4/8/PP2PPPP/R1BQKBNR b KQkq - 0 3"
M.parse(fen)
print("ev (black to move, black up a knight soon? white just won 2 pawns, knight on d5):", M.ev())
print("black captures available:", [uci(m) for m in M.gen(True)])
# what does qs return here?
M.BUDGET = 1000000
M.NODES = 0
print("qs(black to move):", M.qs(-1000000, 1000000, 0), "nodes:", M.NODES)
# now exd5 then eval
m = find_move("e6d5")
print("exd5 move found:", m is not None)
if m:
    u = M.make(m)
    print("after exd5, ev (white to move):", M.ev())
    print("white legal moves:", len(M.legal()))
    M.unmake(u)

# Also check: what does srch(1) return from the position after cxd5 cxd5 (white to move, Nxd5 available)?
fen2 = "rnbqkbnr/pp2pppp/2p5/3p4/3P4/2N5/PP2PPPP/R1BQKBNR w KQkq - 0 3"
M.parse(fen2)
print("\nposition after cxd5 cxd5, white to move, ev:", M.ev())
M.NODES = 0
print("srch(1) white:", M.srch(1, -1000000, 1000000, 0), "nodes:", M.NODES)
# Nxd5 score at depth 1
m = find_move("c3d5")
u = M.make(m)
print("after Nxd5, ev (black to move):", M.ev())
M.NODES = 0
print("qs after Nxd5 (black to move):", M.qs(-1000000, 1000000, 1), "nodes:", M.NODES)
M.unmake(u)
