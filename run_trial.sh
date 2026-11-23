#!/bin/bash
# Run one practice trial (0,1,2) against the local env server, then score it.
# usage: run_trial.sh <trial> <botdir> [port]
set -u
KIT=/home/hatch/workspace/makefun/tiny-chess-01-kit
T=${1:-0}
BOT=${2:-$KIT/starter}
PORT=${3:-8081}
STATE=/tmp/chess-state-$T
rm -rf $STATE; mkdir -p $STATE
MAKEFUN_ENV_DATA_DIR=$KIT/practice/trial-$T/input/env MAKEFUN_STATE_DIR=$STATE MAKEFUN_ENV_PORT=$PORT node $KIT/program/env/server.mjs > $STATE/env.log 2>&1 &
ENV_PID=$!
sleep 1
START=$(date +%s)
MAKEFUN_ENV_URL=http://127.0.0.1:$PORT python3 $BOT/main.py > $STATE/bot.log 2>&1
BOT_RC=$?
END=$(date +%s)
kill -TERM $ENV_PID 2>/dev/null
wait $ENV_PID 2>/dev/null
echo "bot rc=$BOT_RC wall=$((END-START))s"
tail -3 $STATE/bot.log
ls $STATE/export/ 2>/dev/null
MAKEFUN_OUTPUT_DIR=$STATE/export MAKEFUN_REFERENCE_DIR=$KIT/practice/trial-$T/reference MAKEFUN_SCORES_DIR=$STATE/scores node $KIT/program/scorer/score.mjs
cat $STATE/scores/scores.json 2>/dev/null
