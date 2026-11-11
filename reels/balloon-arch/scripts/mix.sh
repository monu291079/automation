#!/bin/bash
# voice + side-chain ducked music + sfx -> loudnorm -14 LUFS, muxed onto the silent Remotion render
set -e; cd "$(dirname "$0")/.."
D=37.78
ffmpeg -v error -y -i build/silent.mp4 -i assets/source/voiceover.mp3 -i build/music.wav -i build/sfx.wav -filter_complex "
[1:a]aresample=48000,highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,apad=whole_dur=$D[v];
[v]asplit=2[v1][v2];
[2:a]aresample=48000,volume=-17dB,apad=whole_dur=$D[m];
[m][v2]sidechaincompress=threshold=0.03:ratio=8:attack=10:release=300[md];
[3:a]aresample=48000,volume=-9dB,apad=whole_dur=$D[s];
[v1][md][s]amix=inputs=3:normalize=0:duration=longest,atrim=0:$D,loudnorm=I=-14:TP=-1.5:LRA=9,afade=t=out:st=37.2:d=0.58[a]" -map 0:v -map "[a]" -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart -t $D out/ideaspulse_balloon_arch_reel.mp4
ffmpeg -v error -y -i out/ideaspulse_balloon_arch_reel.mp4 -vf scale=720:1280 -c:v libx264 -crf 25 -preset medium -c:a aac -b:a 128k -movflags +faststart out/ideaspulse_balloon_arch_reel_720p.mp4
