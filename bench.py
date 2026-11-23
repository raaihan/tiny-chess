import sys, time
sys.path.insert(0, '.')
import main as M

def bench(fen, label, budget=100000):
    M.parse(fen)
    M.BUDGET = budget
    ms = M.legal()
    print(f"{label}: {len(ms)} legal moves")
    for d in range(1, 7):
        M.NODES = 0
        t0 = time.time()
        try:
            best = None; bs = -1000000
            for m in ms:
                u = M.make(m)
                s = -M.srch(d-1, -1000000, 1000000, 1)
                M.unmake(u)
                if s > bs: bs = s; best = m
            dt = time.time() - t0
            print(f"  depth {d}: nodes={M.NODES} time={dt:.2f}s nps={M.NODES/max(dt,0.01):.0f} score={bs}")
        except M.AB:
            dt = time.time() - t0
            print(f"  depth {d}: ABORTED at nodes={M.NODES} time={dt:.2f}s")
            break

bench("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "startpos")
bench("r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1", "italian-ish")
bench("rnbqkbnr/pp1ppppp/2p5/3p4/2PP4/2N5/PP2PPPP/R1BQKBNR w KQkq - 0 4", "semi-slav (game1)")
