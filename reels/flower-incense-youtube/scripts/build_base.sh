#!/usr/bin/env bash
# 30fps 1920x1080 JPEG frames for every clip. Vertical (9:16) clips get a blurred 16:9 background.
set -euo pipefail
cd "$(dirname "$0")/.."
for f in assets/clips/*.mp4; do
  n=$(basename "$f" .mp4); mkdir -p build/clips/$n
  if [[ $n == r_* ]]; then
    vf="split[a][b];[a]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=30:3,eq=brightness=-0.12[bg];[b]scale=-2:1080[fg];[bg][fg]overlay=(W-w)/2:0,fps=30,format=yuvj420p"
  else
    vf="crop=1560:878:120:0,fps=30,scale=1920:1080:flags=lanczos,eq=contrast=1.04:saturation=1.06,format=yuvj420p"   # reframe: slight zoom, keeps the corner out of frame
  fi
  ffmpeg -loglevel error -y -i "$f" -vf "$vf" -q:v 4 -start_number 0 build/clips/$n/%05d.jpg
  echo "$n $(ls build/clips/$n | wc -l)"
done
