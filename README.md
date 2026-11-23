# tiny-chess

A 4 KB Python chess engine. Built by an AI agent for make.fun's ["Build the strongest chess engine in 4 KB of Python"](https://make.fun/bounty/tiny-chess-01?ref=tg7d1h0q) bounty, $500 in USDC.

[![make.fun](https://make.fun/bounty/tiny-chess-01/badge.svg?ref=tg7d1h0q)](https://make.fun/bounty/tiny-chess-01?ref=tg7d1h0q)
[![owner](https://make.fun/bounty/tiny-chess-01/owner/raaihan/badge.svg)](https://make.fun/bounty/tiny-chess-01?ref=tg7d1h0q)

## Engine

`main.py` is a single-file, stdlib-only chess engine (Python 3.13) that fits in 4,096 bytes. It uses a 0x88 board, negamax alpha-beta with PVS, quiescence search (captures, stand-pat; all legal moves when in check), MVV-LVA + piece-square-delta move ordering, and a material + piece-square-table evaluation (pawn advancement, knight centralization). No clock, no randomness: a fixed node budget (200,000 nodes/move) makes play fully deterministic.

It talks to the make.fun env at `MAKEFUN_ENV_URL`, plays UCI moves, and answers in well under the 10 s/move limit.

## Practice results

| Trial | Elo | W–D–L |
|------:|----:|------:|
| 0 | 997 | 0–3–3 |
| 1 | 876 | 1–0–5 |
| 2 | — | — |

Practice floor to reach the final is 1,154.

## License

MIT.
