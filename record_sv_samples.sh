#!/usr/bin/env bash
set -euo pipefail

shopt -s nullglob

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"
CREATE_REFERENCE_SCRIPT="$REPO_ROOT/src/go2_control/go2_control/create_speaker_reference.py"

DEVICE="plughw:2,0"
OUT_DIR="$REPO_ROOT/models/enroll"
REFERENCE_PATH="$REPO_ROOT/models/speaker_ref.npy"
COUNT=""
PREFIX="enroll"
ACTIVE_PID=""

cleanup_active_recording() {
  if [[ -n "$ACTIVE_PID" ]] && kill -0 "$ACTIVE_PID" 2>/dev/null; then
    kill -INT "$ACTIVE_PID" 2>/dev/null || true
    wait "$ACTIVE_PID" 2>/dev/null || true
  fi
}

trap cleanup_active_recording EXIT INT TERM

phrases=(
  "hey amigo"
  "amigo"
  "hello amigo"
  "hey amigo stand up"
  "amigo stand up"
  "hey amigo lay down"
  "amigo lay down"
  "hey amigo can you stand up"
  "amigo can you stand up"
  "hey amigo can you get up"
  "amigo can you get up"
  "hey amigo can you lay down"
  "amigo can you lay down"
  "hey amigo can you lie down"
  "amigo can you lie down"
  "hey amigo can you look for a leak"
  "amigo can you look for a leak"
  "hey amigo follow me"
  "amigo follow me"
  "hey amigo can you follow me"
  "amigo can you follow me"
  "hey amigo track me"
  "amigo track me"
  "hey amigo stop following"
  "amigo stop following"
  "hey amigo stop follow me"
  "amigo stop follow me"
  "stand up"
  "lay down"
  "lie down"
  "follow me"
  "track me"
  "stop following"
  "stop follow me"
  "look for a leak"
  "get up"
  "down"
  "come with me"
  "cancel follow"
  "stop tracking me"
  "hey amigo are you ready"
  "hey amigo listen to me"
  "hey amigo start mapping"
  "hey amigo stop and wait"
  "hey amigo check the system"
  "the robot is ready"
  "mapping mission is active"
  "autonomy system ready"
  "please listen to my voice"
  "this is jose speaking"
)

prompt_enter_or_quit() {
  local prompt="$1"
  local response=""
  read -r -p "$prompt" response
  [[ "${response,,}" != "q" ]]
}

usage() {
  cat <<EOF
Usage: $(basename "$0") [-n count] [-d device] [-o out_dir] [-p prefix] [-r reference_path]

Defaults:
  device:         $DEVICE
  output dir:     $OUT_DIR
  reference path: $REFERENCE_PATH
  clip count:     all remaining phrases
  file prefix:    $PREFIX

Examples:
  ./record_sv_samples.sh
  ./record_sv_samples.sh -n 12
  ./record_sv_samples.sh -p other_speaker -o "$REPO_ROOT/models/test_other"
EOF
}

while getopts ":n:d:o:p:r:h" opt; do
  case "$opt" in
    n) COUNT="$OPTARG" ;;
    d) DEVICE="$OPTARG" ;;
    o) OUT_DIR="$OPTARG" ;;
    p) PREFIX="$OPTARG" ;;
    r) REFERENCE_PATH="$OPTARG" ;;
    h)
      usage
      exit 0
      ;;
    :)
      echo "Missing value for -$OPTARG" >&2
      usage >&2
      exit 1
      ;;
    \?)
      echo "Unknown option: -$OPTARG" >&2
      usage >&2
      exit 1
      ;;
  esac
done

mkdir -p "$OUT_DIR"

max_index=0
for path in "$OUT_DIR"/"${PREFIX}"_*.wav; do
  base_name="$(basename "$path")"
  suffix="${base_name#${PREFIX}_}"
  suffix="${suffix%.wav}"
  if [[ "$suffix" =~ ^[0-9]+$ ]] && (( 10#$suffix > max_index )); then
    max_index=$((10#$suffix))
  fi
done

phrase_count=${#phrases[@]}
start_index=$((max_index + 1))
remaining_count=$((phrase_count - max_index))

if [[ -z "$COUNT" ]]; then
  COUNT="$remaining_count"
fi

if (( remaining_count <= 0 )); then
  echo "All ${phrase_count} phrase slots already exist in $OUT_DIR for prefix $PREFIX."
  echo "Use a different prefix or remove old files if you want to re-record them."
  COUNT=0
fi

if (( COUNT > 0 )) && { ! [[ "$COUNT" =~ ^[0-9]+$ ]] || (( COUNT < 1 )); }; then
  echo "Clip count must be an integer >= 1." >&2
  exit 1
fi

if (( COUNT > remaining_count )); then
  echo "Requested $COUNT clips, but only $remaining_count phrase slots remain for prefix $PREFIX." >&2
  exit 1
fi

new_files=()

echo "Recording with device: $DEVICE"
echo "Saving clips to: $OUT_DIR"
echo "Reference output path: $REFERENCE_PATH"
echo "Clips to record: $COUNT"
echo "Phrases available total: $phrase_count"
echo "Clip timing: manual start/stop"
echo
echo "Enrollment tips:"
echo "- Aim for 8 to 15 short clips."
echo "- Keep each clip around 2 to 5 seconds."
echo "- Use natural command-style phrases."
echo "- Vary distance and room noise a little across takes."
echo "- Stop ODAS or other mic users first if the device is busy."
echo "- Type q then Enter at a prompt to stop the script."
echo

for ((i = 0; i < COUNT; i++)); do
  clip_index=$((start_index + i))
  phrase_index=$((clip_index - 1))
  phrase="${phrases[phrase_index]}"
  printf -v clip_name "%s_%02d.wav" "$PREFIX" "$clip_index"
  clip_path="$OUT_DIR/$clip_name"

  printf "Next clip: %s\n" "$clip_name"
  printf "Phrase %02d/%02d: %s\n" "$clip_index" "$phrase_count" "$phrase"
  if ! prompt_enter_or_quit "Press Enter to start recording, or q to quit: "; then
    echo "Stopping before recording $clip_name."
    echo
    break
  fi
  arecord -D "$DEVICE" -f S16_LE -r 16000 -c 1 "$clip_path" &
  ACTIVE_PID=$!
  sleep 0.2
  if ! kill -0 "$ACTIVE_PID" 2>/dev/null; then
    wait "$ACTIVE_PID" || true
    ACTIVE_PID=""
    echo "Recording failed to start. The device may be busy or unavailable." >&2
    exit 1
  fi
  quit_after_clip=0
  if ! prompt_enter_or_quit "Recording... press Enter to stop, or q to stop and quit: "; then
    quit_after_clip=1
  fi
  kill -INT "$ACTIVE_PID" 2>/dev/null || true
  wait "$ACTIVE_PID" 2>/dev/null || true
  ACTIVE_PID=""
  if [ ! -s "$clip_path" ]; then
    rm -f "$clip_path"
    echo "No audio was captured for $clip_name. Please run the script again for that clip." >&2
    exit 1
  fi
  new_files+=("$clip_path")
  echo "Saved $clip_path"
  echo
  if (( quit_after_clip )); then
    echo "Stopping after saving $clip_name."
    echo
    break
  fi
done

all_files=( "$OUT_DIR"/"${PREFIX}"_*.wav )

if (( ${#new_files[@]} > 0 )); then
  echo "Newly recorded files:"
  for path in "${new_files[@]}"; do
    echo "$path"
  done
else
  echo "No new files were recorded."
fi
echo

if [ ! -f "$CREATE_REFERENCE_SCRIPT" ]; then
  echo "Could not find $CREATE_REFERENCE_SCRIPT" >&2
  exit 1
fi

if (( ${#all_files[@]} < 3 )); then
  echo "You currently have ${#all_files[@]} WAV file(s) matching ${PREFIX}_*.wav in $OUT_DIR."
  echo "Record at least 3 clips before building a speaker reference."
else
  echo "Reference build command:"
  cmd=(python3 "$CREATE_REFERENCE_SCRIPT" --output "$REFERENCE_PATH")
  cmd+=( "${all_files[@]}" )
  printf '%q ' "${cmd[@]}"
  echo
  echo
  echo "This will use ${#all_files[@]} total WAV files matching ${PREFIX}_*.wav in $OUT_DIR."
fi
