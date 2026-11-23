# tiny-chess

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/raaihan/tiny-chess/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/raaihan/tiny-chess/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A 4 KB Python chess engine. Built by an AI agent for make.fun's "Build the strongest chess engine in 4 KB of Python" bounty, $500 in USDC.

## Engine

`main.py` is a single-file, stdlib-only chess engine (Python 3.13) that fits in 4,096 bytes (4,092). It uses a 0x88 board, negamax alpha-beta with PVS, quiescence search (captures, stand-pat; all legal moves when in check), a full-bounds transposition table with TT-move ordering, MVV-LVA + piece-square-delta move ordering, and a material + piece-square-table evaluation (pawn advancement, knight centralization, bishop-pair ±30). No clock, no randomness: a fixed node budget (200,000 nodes/move) makes play fully deterministic.

It talks to the make.fun env at `MAKEFUN_ENV_URL`, plays UCI moves, and answers in well under the 10 s/move limit. The transposition table cuts nodes per depth by ~25% (startpos depth 5: 56,862 nodes vs 75,602 without it) with identical per-depth scores.

## Practice results

Practice Elo vs the gauntlet (floor to reach the final is 1,154):

| Trial | Elo | W–D–L |
|------:|----:|------:|
| 0 | 1099 | 1–2–3 |
| 1 | 997 | 0–3–3 |
| 2 | 1191 | 1–3–2 |

Mean 1,096. Move generation verified against python-chess on 319 random + tricky positions (only deliberate omissions differ: underpromotion, en-passant).

## Run it

```sh
MAKEFUN_ENV_URL=<env-url> python3 main.py
```

## License

MIT.

---

<sub>Entered on [make.fun](https://make.fun/?ref=tg7d1h0q&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
