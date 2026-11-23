import sys, random
sys.path.insert(0, '.')
import chess
src = open('mini4.py').read()
# strip the trailing main() call so importing doesn't run the game loop
src = src.rsplit('\nmain()', 1)[0]
M = type(sys)('mini4')
exec(compile(src, 'mini4.py', 'exec'), M.__dict__)

def uci_of(m):
    f=m&127; t=(m>>7)&127; pr=(m>>14)&7
    s="abcdefgh"[f&7]+str((f>>4)+1)+"abcdefgh"[t&7]+str((t>>4)+1)
    if pr: s+="pnbrqk"[pr-1]
    return s

def test_fen(fen, label):
    M.F(fen)
    mine = sorted(uci_of(m) for m in M.L())
    b = chess.Board(fen)
    ref = sorted(m.uci() for m in b.legal_moves)
    if mine != ref:
        print(f"MISMATCH {label}: {fen}")
        print("  mine only:", sorted(set(mine)-set(ref))[:10])
        print("  ref only:", sorted(set(ref)-set(mine))[:10])
        return False
    return True

ok = True
ok &= test_fen(chess.STARTING_FEN, "start")
random.seed(42)
tested = 0
for g in range(30):
    b = chess.Board()
    for ply in range(random.randint(5, 60)):
        if b.is_game_over(): break
        mv = random.choice(list(b.legal_moves))
        b.push(mv)
        if ply % 3 == 0:
            ok &= test_fen(b.fen(), f"rand g{g} ply{ply}")
            tested += 1
print("random positions tested:", tested)
tricky = [
 "r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1",
 "r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R b KQkq - 0 1",
 "8/8/8/3pP3/8/8/8/4K2k w - d6 0 1",
 "8/8/8/8/8/8/3pP3/4K2k b - e3 0 1",
 "8/P7/8/8/8/8/k6K/8 w - - 0 1",
 "8/8/8/8/8/8/7p/K6k b - - 0 1",
 "r1bqkbnr/pppp1ppp/2n5/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 0 1",
 "4k3/8/8/8/8/8/8/4K2R w K - 0 1",
]
for i, fen in enumerate(tricky):
    ok &= test_fen(fen, f"tricky{i}")
print("ALL OK" if ok else "FAILURES ABOVE")
M.F(chess.STARTING_FEN)
b0 = list(M.T); s0, c0 = M.S, M.C
for trial in range(200):
    ms = M.L()
    if not ms: break
    m = random.choice(ms)
    u = M.M(m)
    M.n(u)
    if M.T != b0 or M.S != s0 or M.C != c0:
        print("MAKE/UNMAKE MISMATCH at trial", trial, "move", uci_of(m))
        ok = False
        break
    M.M(m)
    b0 = list(M.T); s0, c0 = M.S, M.C
print("make/unmake roundtrip:", "OK" if ok else "FAIL")
