#!/usr/bin/env bash
# Splits the 1080p master into two <95 MB parts (GitHub's file limit is 100 MB) at the chapter-6 card.
set -euo pipefail
cd "$(dirname "$0")/.."
M=out/ideaspulse_flower_incense_glass.mp4; CUT=${1:-378}
enc() { ffmpeg -loglevel error -y "$@" -c:v libx264 -preset medium -crf 22 -maxrate 1500k -bufsize 3000k -profile:v high -pix_fmt yuv420p -c:a aac -b:a 112k -movflags +faststart; }
enc -i $M -t $CUT out/ideaspulse_flower_incense_1080p_part1.mp4 &
enc -ss $CUT -i $M out/ideaspulse_flower_incense_1080p_part2.mp4 &
wait
ls -la out/*1080p_part*.mp4 | awk '{print $5/1048576 " MB", $9}'
