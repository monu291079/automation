#!/usr/bin/env bash
# 30fps 1080x1920 JPEG frames for the creator clips and b-roll.
# creator_main.mp4 matches voiceover.mp3 from 0.000s; creator_part2.mp4 starts at 47.45s.
set -euo pipefail
cd "$(dirname "$0")/.."
ex() { mkdir -p build/$2; ffmpeg -loglevel error -y -i assets/source/$1 -vf "fps=30,scale=1080:1920:flags=lanczos,$3setsar=1,format=yuvj420p" -q:v 3 -start_number 0 build/$2/%05d.jpg; }
ex creator_main.mp4 creatorMain ""
ex creator_part2.mp4 creatorPart2 ""
for c in c1_temple_waste c2_handmade c3_collect c4_dry_grind c5_smoke c6_market; do ex broll_$c.mp4 ${c%%_*} "eq=contrast=1.05:saturation=1.08,"; done
for d in build/*/; do echo "$d $(ls $d | wc -l)"; done
