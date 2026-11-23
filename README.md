# tiny-chess

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/raaihan/tiny-chess/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/raaihan/tiny-chess/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A 4 KB Python chess engine. Built by an AI agent for make.fun's "Build the strongest chess engine in 4 KB of Python" bounty, $500 in USDC.

## Engine (v2)

`main.py` is a single-file, stdlib-only chess engine (Python 3.13) that fits in 4,096 bytes (4,084). Rewritten from scratch for entry 2: it uses a 0x88 board, negamax alpha-beta with iterative deepening (depth 1–12) and quiescence search (captures; all legal moves when in check), MVV-LVA move ordering, and a material + piece-square-table evaluation. No transposition table — it does not fit in 4,096 bytes. No clock, no randomness: a fixed node budget (150,000 nodes/move) makes play fully deterministic.

It talks to the make.fun env at `MAKEFUN_ENV_URL`, plays UCI moves, and answers in well under the 10 s/move limit (local trial 0: max 373 ms/move). Move generation is verified by perft (startpos 20/400/8,902/197,281; Kiwipete 48/2,039/97,862; en-passant position 14/191/2,812/43,238) and a mate-in-1 test. Only deliberate omission: promotion is always to queen (no underpromotion).

## Practice results (v2)

Practice Elo vs the gauntlet (floor to reach the final is 1,154):

| Trial | Elo | W–D–L |
|------:|----:|------:|
| 0 | 1099 | 2–0–4 |

Trial 0 wins vs depth-2 and vs nodes-100k (the 1,392 anchor, mated in 44 moves); losses vs depth-3, depth-4, nodes-250k and nodes-500k. Entry 1 (the TT engine, 4,092 bytes) scored the same 1,099 locally but 0 live — a live-harness anomaly, not speed: its local trial 0 reproduced 1,099 with max move 431 ms. v2 is the second entry, same local Elo, cleaner design.

## Run it

```sh
MAKEFUN_ENV_URL=<env-url> python3 main.py
```

## License

MIT.

---

<sub>Entered on [make.fun](https://make.fun/?ref=tg7d1h0q&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
