import sys, time
sys.path.insert(0, '.')
import main as M

# instrument: count srch nodes vs qs nodes, TT hits
orig_srch = M.srch
orig_qs = M.qs
stats = {"srch": 0, "qs": 0, "tt_hit": 0, "tt_probe": 0}
def srch(d, a, b, ply):
    stats["srch"] += 1
    key = (tuple(M.B), M.S, M.C, M.E)
    stats["tt_probe"] += 1
    if key in M.TT: stats["tt_hit"] += 1
    return orig_srch(d, a, b, ply)
def qs(a, b, ply):
    stats["qs"] += 1
    return orig_qs(a, b, ply)
M.srch = srch
M.qs = qs

fen = "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1"
M.parse(fen)
M.BUDGET = 100000
ms = M.legal()
t0 = time.time()
M.NODES = 0
try:
    for m in ms:
        u = M.make(m)
        s = -M.srch(3, -1000000, 1000000, 1)
        M.unmake(u)
    print(f"depth 4: nodes={M.NODES} srch={stats['srch']} qs={stats['qs']} tt_hit={stats['tt_hit']}/{stats['tt_probe']} time={time.time()-t0:.2f}s")
except M.AB:
    print(f"ABORTED depth 4: nodes={M.NODES} srch={stats['srch']} qs={stats['qs']} tt_hit={stats['tt_hit']}/{stats['tt_probe']} time={time.time()-t0:.2f}s")
