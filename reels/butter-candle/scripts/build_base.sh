#!/usr/bin/env bash
# Extracts 30fps 1080x1920 JPEG frames for the three creator takes and the b-roll clips.
# All three creator takes are lip-synced to voiceover.mp3 from 0.000s.
set -euo pipefail
cd "$(dirname "$0")/.."
for k in A B C; do
  mkdir -p build/creator$k
  ffmpeg -loglevel error -y -i assets/source/creator_take$k.mp4 \
    -vf "fps=30,scale=1080:1920,setsar=1,format=yuvj420p" -q:v 3 -start_number 0 build/creator$k/%05d.jpg
done
for k in b1 b2 b3; do
  mkdir -p build/$k
  ffmpeg -loglevel error -y -i assets/source/broll_$k.mp4 \
    -vf "fps=30,scale=1080:1920:flags=lanczos,unsharp=5:5:0.5,eq=contrast=1.05:saturation=1.10,setsar=1,format=yuvj420p" \
    -q:v 3 -start_number 0 build/$k/%05d.jpg
done
for d in build/*/; do echo "$d $(ls $d | wc -l)"; done
