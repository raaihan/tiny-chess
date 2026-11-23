import sys
sys.path.insert(0, '.')
import main as M

def ev_of(fen):
    M.parse(fen)
    return M.ev()

print("startpos ev (white to move, expect ~0):", ev_of("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"))
print("startpos black to move:", ev_of("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1"))
print("white up a knight (expect ~+320):", ev_of("rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 0 1"))
print("white down a knight (expect ~-320):", ev_of("rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1"))
print("white up a queen (expect ~+900):", ev_of("rnb1kbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1"))

# game 1 position after opening: semi-slav, white to move
fen1 = "rnbqkbnr/pp1ppppp/2p5/3p4/2PP4/2N5/PP2PPPP/R1BQKBNR w KQkq - 0 4"
M.parse(fen1)
print("game1 ev:", M.ev())
# what does root choose?
M.BUDGET = 60000
mv = M.root(fen1, [m for m in ["c4d5","c3d5","e2e3","g1f3","c1d2","d1c2"]])
print("game1 root choice:", mv)
# score each root move at depth 3
M.parse(fen1)
ms = M.legal()
def uci(m):
    f=m&127; t=(m>>7)&127; pr=(m>>14)&7
    s="abcdefgh"[f&7]+str((f>>4)+1)+"abcdefgh"[t&7]+str((t>>4)+1)
    if pr: s+="pnbrqk"[pr-1]
    return s
M.NODES=0
for m in ms:
    u=M.make(m)
    s=-M.srch(2,-1000000,1000000,1)
    M.unmake(u)
    print(f"  {uci(m)}: depth3 score {s}")
print("nodes:", M.NODES)
