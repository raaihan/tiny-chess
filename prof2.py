import sys, cProfile, pstats, io
sys.path.insert(0, '.')
import main as M

M.parse("r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1")
M.BUDGET = 1000000
ms = M.legal()
pr = cProfile.Profile()
pr.enable()
M.NODES = 0
try:
    for m in ms:
        u = M.make(m)
        s = -M.srch(3, -1000000, 1000000, 1)
        M.unmake(u)
except M.AB:
    pass
pr.disable()
print(f"nodes={M.NODES}")
s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
ps.print_stats(18)
print(s.getvalue()[:3000])
