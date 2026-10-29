#!/usr/bin/env bash
# Joins the two creator clips at the voiceover sync point and writes 30fps JPEG frames.
# Clip 1 audio == voiceover from 0.000s. Clip 2 audio == voiceover from 22.172s.
# We cut inside the natural pause at 23.50s.
set -euo pipefail
cd "$(dirname "$0")/.."
CUT=23.50; B_OFF=22.172
mkdir -p build/creator
ffmpeg -loglevel error -y \
  -i assets/source/creator_part1.mov -i assets/source/creator_part2.mov \
  -filter_complex "[0:v]trim=0:${CUT},setpts=PTS-STARTPTS,fps=30,scale=1080:1920,setsar=1[a];\
[1:v]trim=start=$(python3 -c "print(${CUT}-${B_OFF})"),setpts=PTS-STARTPTS,fps=30,scale=1080:1920,setsar=1[b];\
[a][b]concat=n=2:v=1:a=0,format=yuvj420p[v]" \
  -map "[v]" -q:v 3 -start_number 0 build/creator/%05d.jpg
ls build/creator | wc -l

# Real printer demo footage -> 30fps 1080x1920 frames (upscaled from 720p, light sharpen + grade)
mkdir -p build/demo
ffmpeg -loglevel error -y -i assets/source/demo_resin_printing.mp4 \
  -vf "fps=30,scale=1080:1920:flags=lanczos,unsharp=5:5:0.6,eq=contrast=1.06:saturation=1.12,setsar=1,format=yuvj420p" \
  -q:v 3 -start_number 0 build/demo/%05d.jpg
ls build/demo | wc -l
