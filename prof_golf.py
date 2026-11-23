import sys, cProfile, pstats, io
sys.path.insert(0, '.')
import golf as M
M.F("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
M.BDG = 200000
ms = M.L()
pr = cProfile.Profile()
pr.enable()
for d in range(1, 6):
    M.N = 0
    try:
        for m in ms:
            u = M.M(m)
            s = -M.R(d-1, -1000000, 1000000, 1)
            M.n(u)
    except M.A:
        break
pr.disable()
s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
ps.print_stats(14)
print(s.getvalue()[:3000])
