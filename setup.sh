#!/bin/bash
echo "Setup unitree ros2 environment"
source /opt/ros/jazzy/setup.bash
source $HOME/workspaces/amigo_ros2_relasense/install/setup.bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export CYCLONEDDS_URI='<CycloneDDS><Domain><General><Interfaces>
                            <NetworkInterface name="enP2p1s0" priority="default" multicast="default" />
                        </Interfaces></General><Discovery><ParticipantIndex>none</ParticipantIndex></Discovery></Domain></CycloneDDS>'
