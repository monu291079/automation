#!/usr/bin/env bash
# Timelapse + reframing of the reference footage and the creator clip -> remotion/public/clips (1080x1920, 30 fps, no audio).
# Only machine/arch shots are used (no on-camera presenter, no burned-in text).
set -euo pipefail
cd "$(dirname "$0")/.."
R=assets/ref/ref2.mp4; O=remotion/public/clips
seg() { # name start dur speed
  local n=$1 s=$2 d=$3 sp=$4 blend; blend=$(python3 -c "print(max(1,min(10,round(2*$sp))))")
  ffmpeg -loglevel error -y -ss $s -t $d -i $R -an -vf "scale=1080:1920:flags=lanczos,unsharp=5:5:0.6,eq=contrast=1.07:saturation=1.18,tmix=frames=$blend,setpts=PTS/$sp,fps=30,format=yuv420p" -c:v libx264 -crf 17 -preset veryfast $O/$n.mp4
}
# hook timelapse (0-6.5 s) : arch building, orange arch, hands loading, big finished arches
seg b_fast   4.0 10.0 4.8 &
seg e_fast  18.0  3.4 2.1 &
seg d_fast  22.0  6.0 3.3 &
seg c_fast  29.3  4.2 3.2 &
wait
# explanation shots at (nearly) normal speed
seg a_slow   0.0  3.6 0.7 &
seg b_slow   4.0 10.0 1.95 &
seg c_slow  29.3  4.2 1.6 &
wait
ffmpeg -loglevel error -y -i assets/source/creator.mp4 -an -vf "fps=30,format=yuv420p" -c:v libx264 -crf 15 -preset veryfast $O/creator.mp4
for f in $O/*.mp4; do echo "$(basename $f) $(ffprobe -v error -show_entries format=duration -of csv=p=0 $f)"; done
