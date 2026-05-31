#!/usr/bin/env bash
set -euo pipefail

AMIGO_ROS2_WS="${AMIGO_ROS2_WS:-/home/castej/workspaces/amigo_ros2_relasense}"
ISAAC_ROS_WS="${ISAAC_ROS_WS:-/home/castej/workspaces/isaac_ros-dev}"
ISAAC_ROS_VENV_PATH="${ISAAC_ROS_VENV_PATH:-/var/lib/isaac-ros-cli/isaac-ros}"
ROS_SETUP="${ROS_SETUP:-/opt/ros/jazzy/setup.bash}"
YOLO_ENGINE_FILE="${YOLO_ENGINE_FILE:-${ISAAC_ROS_WS}/isaac_ros_assets/models/yolov8/yolov8s.plan}"
YOLO_INPUT_IMAGE_WIDTH="${YOLO_INPUT_IMAGE_WIDTH:-640}"
YOLO_INPUT_IMAGE_HEIGHT="${YOLO_INPUT_IMAGE_HEIGHT:-360}"
YOLO_NETWORK_IMAGE_WIDTH="${YOLO_NETWORK_IMAGE_WIDTH:-640}"
YOLO_NETWORK_IMAGE_HEIGHT="${YOLO_NETWORK_IMAGE_HEIGHT:-640}"

default_launch_file() {
  local filename="$1"
  local source_path="${AMIGO_ROS2_WS}/src/go2_bringup/launch/${filename}"
  local install_path="${AMIGO_ROS2_WS}/install/go2_bringup/share/go2_bringup/launch/${filename}"
  if [[ -f "$source_path" ]]; then
    printf '%s\n' "$source_path"
    return
  fi
  printf '%s\n' "$install_path"
}

MAPPING_LAUNCH_FILE="${MAPPING_LAUNCH_FILE:-$(default_launch_file mapping.launch.py)}"
YOLO_LAUNCH_FILE="${YOLO_LAUNCH_FILE:-$(default_launch_file yolov8_person_detection.launch.py)}"

require_file() {
  local path="$1"
  local label="$2"
  if [[ ! -f "$path" ]]; then
    echo "Missing ${label}: ${path}" >&2
    exit 1
  fi
}

source_setup() {
  local setup_file="$1"
  set +u
  # shellcheck source=/dev/null
  source "$setup_file"
  set -u
}

require_file "$ROS_SETUP" "ROS setup file"
require_file "${AMIGO_ROS2_WS}/install/setup.bash" "Go2 workspace setup file"
require_file "${ISAAC_ROS_VENV_PATH}/bin/activate" "Isaac ROS venv activation file"
require_file "$MAPPING_LAUNCH_FILE" "Go2 mapping launch file"
require_file "$YOLO_LAUNCH_FILE" "YOLOv8 person detection launch file"
require_file "$YOLO_ENGINE_FILE" "YOLOv8 TensorRT engine"

pids=()
cleanup() {
  local status=$?
  trap - EXIT INT TERM
  for pid in "${pids[@]}"; do
    if kill -0 "$pid" 2>/dev/null; then
      kill -TERM "$pid" 2>/dev/null || true
    fi
  done
  for pid in "${pids[@]}"; do
    wait "$pid" 2>/dev/null || true
  done
  exit "$status"
}
trap cleanup EXIT INT TERM

(
  set -euo pipefail
  source_setup "$ROS_SETUP"
  source_setup "${AMIGO_ROS2_WS}/install/setup.bash"
  mapping_args=(
    ros2 launch "$MAPPING_LAUNCH_FILE"
    person_follow_enable:=true
    voice_control:=true
    "$@"
  )
  exec "${mapping_args[@]}"
) &
pids+=("$!")

(
  set -euo pipefail
  source_setup "${ISAAC_ROS_VENV_PATH}/bin/activate"
  export ISAAC_ROS_WS
  source_setup "$ROS_SETUP"
  if [[ -f "${ISAAC_ROS_WS}/install/setup.bash" ]]; then
    source_setup "${ISAAC_ROS_WS}/install/setup.bash"
  fi
  source_setup "${AMIGO_ROS2_WS}/install/setup.bash"
  yolo_args=(
    ros2 launch "$YOLO_LAUNCH_FILE"
    engine_file_path:="${YOLO_ENGINE_FILE}"
    input_image_width:="${YOLO_INPUT_IMAGE_WIDTH}"
    input_image_height:="${YOLO_INPUT_IMAGE_HEIGHT}"
    network_image_width:="${YOLO_NETWORK_IMAGE_WIDTH}"
    network_image_height:="${YOLO_NETWORK_IMAGE_HEIGHT}"
  )
  exec "${yolo_args[@]}"
) &
pids+=("$!")

wait -n "${pids[@]}"
