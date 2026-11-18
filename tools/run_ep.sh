#!/bin/bash
# Take one episode from rendered beats to delivered files.
# usage: bash tools/run_ep.sh <EP> "<THUMB LINE 1>" "<THUMB LINE 2>" "<KICKER>"
set -e
R=/home/claude/upsc-ancient-india-videos
EP=$(printf %02d "$1")
D=$R/episodes/ep$EP
cd "$D"

N=$(python3 -c "from text import EN; print(len(EN))")
TITLE=$(python3 -c "
import re
s=open('ep.py',encoding='utf-8').read()
print(re.search(r\"^TITLE = '(.*)'\", s, re.M).group(1))")

# --- narration, if this episode's scratch has been cleared
# Delivery deletes vo/ and vo_hi/ (see the end of this script), so a re-render
# of an already-delivered episode has to speak its lines again first. The
# timeline reads vo/durs.json, so without this the render fails on beat 0.
if [ ! -f vo/durs.json ] || [ ! -f vo_hi/durs.json ]; then
  python3 ../../engine/cli.py tts    ../../voice/en-us-lessac-medium.onnx  > tts_en.log 2>&1
  python3 ../../engine/cli.py tts-hi ../../voice/hi_IN-pratham-medium.onnx > tts_hi.log 2>&1
fi

# --- render, two workers (the box has two cores)
rm -rf parts; mkdir -p parts
EVEN=$(python3 -c "print(','.join(str(i) for i in range(0,$N,2)))")
ODD=$(python3 -c "print(','.join(str(i) for i in range(1,$N,2)))")
python3 ../../engine/cli.py render "$EVEN" > r0.log 2>&1 &
P0=$!
python3 ../../engine/cli.py render "$ODD"  > r1.log 2>&1 &
P1=$!
wait $P0 $P1

DONE=$(ls parts/ | grep -c '^[0-9][0-9]\.mp4' || true)
if [ "$DONE" -ne "$N" ]; then
  echo "ep$EP RENDER INCOMPLETE: $DONE/$N parts" >&2
  tail -n 5 r0.log r1.log >&2
  exit 1
fi

# --- audio, both languages
python3 ../../engine/cli.py audio > audio.log 2>&1

# --- assemble: one video, English first, Hindi second
python3 -c "
print('\n'.join(f\"file 'parts/{i:02d}.mp4'\" for i in range($N)))" > concat.txt
ffmpeg -y -f concat -safe 0 -i concat.txt -c copy video.mp4 -loglevel error
ffmpeg -y -i mix_hi.wav -c:a aac -b:a 192k hi.m4a -loglevel error
ffmpeg -y -i video.mp4 -i mix_en.wav -i hi.m4a \
  -map 0:v -map 1:a -map 2:a -c:v copy -c:a aac -b:a 192k \
  -metadata:s:a:0 language=eng -metadata:s:a:1 language=hin \
  -movflags +faststart final.mp4 -loglevel error

# --- keep every file under GitHub's limit
SZ=$(stat -c%s final.mp4)
if [ "$SZ" -gt 99000000 ]; then
  ffmpeg -y -i video.mp4 -c:v libx264 -b:v 900k -preset slow -pass 1 -an -f mp4 /dev/null -loglevel error
  ffmpeg -y -i video.mp4 -i mix_en.wav -i hi.m4a -map 0:v -map 1:a -map 2:a \
    -c:v libx264 -b:v 900k -preset slow -pass 2 -pix_fmt yuv420p -c:a aac -b:a 128k \
    -metadata:s:a:0 language=eng -metadata:s:a:1 language=hin \
    -movflags +faststart small.mp4 -loglevel error
  OUT=small.mp4
else
  OUT=final.mp4
fi

# --- deliver
mkdir -p "$R/output/hindi" "$R/output/youtube"
cp "$OUT" "$R/output/Anc${EP}_${TITLE}.mp4"
cp "Anc${EP}.en.srt" "Anc${EP}.hi.srt" "$R/output/"
cp hi.m4a "$R/output/hindi/Anc${EP}.hi.m4a"
if [ -n "$2" ]; then
  cd "$R" && python3 tools/thumb.py "$1" "$2" "$3" "$4" "output/youtube/Anc${EP}_thumb.png" > /dev/null
fi
echo "ep$EP DELIVERED $(du -h "$R/output/Anc${EP}_${TITLE}.mp4" | cut -f1)"

# --- clear this episode's scratch
# The session's disk is a fixed allowance, and one episode leaves roughly a
# gigabyte of parts, narration and mixes behind. Episode 27 failed mid-queue
# once because 26 episodes' worth of scratch had filled the volume. Now that
# the deliverables are copied out, none of it is needed again: a re-render
# regenerates all of it.
rm -rf "$D/parts" "$D/vo" "$D/vo_hi"
rm -f "$D"/*.wav "$D"/*.m4a "$D"/*.mp4 "$D"/*.srt "$D"/*.log "$D"/*.png "$D"/concat.txt \
      "$D"/ffmpeg2pass-*.log* 2>/dev/null || true
