#!/usr/bin/env bash
# Auto-start entry point for the Amigo Go2 mission stack at boot.
#
# Installed as the ExecStart of the systemd unit /etc/systemd/system/amigo.service
# (see that file). Runs as user 'castej'.
#
# Mirrors the interactive command:
#     source setup_robot.sh
#     amigo_launch deliver_use_arm:=false swag_debug:=true
#
# but with launch_profile:=mission_base so the FULL robot stack (base, nav,
# audio/voice, behaviors/swag) comes up WITHOUT RViz or the operator tools --
# at boot there is no graphical desktop for RViz to open on.
#
# NOTE: deliberately no `set -e`/`set -u` -- the ROS 2 and colcon setup scripts
# sourced below are not "strict mode" safe (they reference unbound vars and can
# return non-zero benignly).

# Source ROS 2 Jazzy + this workspace overlay + Unitree/CycloneDDS env.
source /home/castej/workspaces/amigo_ros2/setup_robot.sh

# Hand the process tree over to ros2 launch (so systemd manages it as the unit).
exec ros2 launch go2_bringup mapping.launch.py \
  launch_profile:=mission_base \
  deliver_use_arm:=false \
  swag_debug:=true
