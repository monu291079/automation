#!/usr/bin/env bash
# 30fps 1080x1920 JPEG frames for the creator clip (synced to voiceover.mp3 from 0s) and the b-roll.
set -euo pipefail
cd "$(dirname "$0")/.."
ex() { mkdir -p build/$2; ffmpeg -loglevel error -y -i assets/source/$1 -vf "fps=30,scale=1080:1920:flags=lanczos,$3setsar=1,format=yuvj420p" -q:v 3 -start_number 0 build/$2/%05d.jpg; }
ex creator_main.mp4 creatorMain ""
for c in c1_vendor c2_sanding c3_polish c4_products c5_packing; do ex broll_$c.mp4 ${c%%_*} "eq=contrast=1.05:saturation=1.08,"; done
for d in build/*/; do echo "$d $(ls $d | wc -l)"; done
