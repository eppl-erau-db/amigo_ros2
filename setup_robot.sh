#!/usr/bin/env bash
# Source this before launching the Go2 mapping/voice workflow on the Jetson Thor.
#   source ~/workspaces/amigo_ros2/setup_robot.sh
#   ros2 launch go2_bringup mapping.launch.py
#
# Sets up ROS 2 Jazzy + this workspace and points the Unitree Go2 link at the
# correct network interface via CycloneDDS.

# --- ROS 2 distro + this workspace overlay ---
source /opt/ros/jazzy/setup.bash
WS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
if [ -f "$WS_DIR/install/setup.bash" ]; then
  source "$WS_DIR/install/setup.bash"
else
  echo "[setup_robot] WARNING: $WS_DIR/install/setup.bash not found -- build the workspace first (colcon build)."
fi

# --- Unitree Go2 link ---
# The Go2 is connected over the 'enP2p1s0' Ethernet interface on this Jetson Thor.
# go2_driver_node talks to the robot through the ROS 2 RMW, so the RMW must be
# CycloneDDS bound to that interface. (The SDK2 nodes get the same interface via
# the person_follow_unitree_network_interface launch arg, which now defaults to it.)
export UNITREE_NET_IFACE="${UNITREE_NET_IFACE:-enP2p1s0}"
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
# ParticipantIndex=none removes CycloneDDS's per-host participant-index cap. Without
# it, the ~36-node mapping launch plus the Go2's ~100 DDS endpoints exhaust the index
# space and nodes die with "Failed to find a free participant index for domain 0".
export CYCLONEDDS_URI="<CycloneDDS><Domain><General><Interfaces>
    <NetworkInterface name=\"${UNITREE_NET_IFACE}\" priority=\"default\" multicast=\"default\" />
  </Interfaces></General>
  <Discovery><ParticipantIndex>none</ParticipantIndex><MaxAutoParticipantIndex>120</MaxAutoParticipantIndex></Discovery>
  </Domain></CycloneDDS>"

# The Unitree SDK bundles CycloneDDS 0.10.2 (libddsc + libddscxx). ROS Jazzy ships
# libddsc 0.10.5 but NO libddscxx, so without this the SDK nodes load a MIXED pair
# (system 0.10.5 ddsc + Unitree 0.10.2 ddscxx) and crash with "free(): invalid pointer".
# Prepend Unitree's lib dir so the whole stack uses the matched 0.10.2 pair. Verified:
# ros-jazzy rmw_cyclonedds_cpp runs fine on 0.10.2.
export LD_LIBRARY_PATH="$WS_DIR/sdk/unitree_sdk2/thirdparty/lib/aarch64:${LD_LIBRARY_PATH}"

# --- Voice STT model (auto-discovered too, but make it explicit) ---
if [ -d "$WS_DIR/models/vosk-model-small-en-us-0.15" ]; then
  export VOSK_MODEL_PATH="$WS_DIR/models/vosk-model-small-en-us-0.15"
fi

# --- Quiet helpers ---
# The Go2 runs a Foxy-era DDS whose endpoints carry no ROS 2 type hash, so Jazzy's
# rmw_cyclonedds logs a harmless "Failed to parse type hash ... USER_DATA '(null)'"
# once per discovered topic, from EVERY node, at startup. Jazzy has no per-logger
# severity env var and rmw_cyclonedds emits it unconditionally, so the only complete
# fix is to filter the console. These wrappers drop only that noise and keep the rest.
_amigo_filter() { grep --line-buffered -vE "Failed to parse type hash|rmw_cyclonedds_cpp.*type hash"; }
amigo_launch() { ros2 launch go2_bringup mapping.launch.py "$@" 2>&1 | _amigo_filter; }
amigo_echo()   { ros2 topic echo "$@" 2>&1 | _amigo_filter; }
# Run AND save a clean log:  amigo_log [launch args...]   -> writes ./amigo_run.log
amigo_log()    { ros2 launch go2_bringup mapping.launch.py "$@" 2>&1 | _amigo_filter | tee amigo_run.log; }

echo "[setup_robot] ROS 2 Jazzy + amigo_ros2 sourced."
echo "[setup_robot] RMW=$RMW_IMPLEMENTATION  iface=$UNITREE_NET_IFACE"
echo "[setup_robot] launch (quiet): amigo_launch     clean log: amigo_log     echo: amigo_echo /topic"
echo "[setup_robot] NOTE: the raw 'ros2 launch ...' shows the harmless rmw type-hash spam; use amigo_launch/amigo_log to hide it."
