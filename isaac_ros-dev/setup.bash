sudo apt update && \
sudo apt install -y ros-humble-rmw-cyclonedds-cpp ros-humble-rosidl-generator-dds-idl ros-humble-isaac-ros-nvblox ros-humble-nmea-navsat-driver libgeographic-dev ros-humble-geographic-msgs libyaml-cpp-dev python3-smbus i2c-tools ros-humble-isaac-ros-occupancy-grid-localizer python3-tk && \
sudo apt install ros-humble-robot-localization &&
sudo apt-get install -y ros-humble-isaac-ros-peoplesemseg-models-install && \
pip install transforms3d pyserial smbus && \
rosdep update && \
rosdep install isaac_ros_nvblox && \
rosdep install --from-paths ${ISAAC_ROS_WS}/src/isaac_ros_map_localization --ignore-src -y && \

## TODO: Make it so that it tries to give the correct permissions to the camera and the lidar, if there isn't a device detected, print a warning and keep going with the rest of the setup.bash 

## NOTE: This is for the camera
sudo chmod 666 /dev/video0 && \
sudo chmod 666 /dev/video1 && \
sudo chmod 666 /dev/video2 && \

## NOTE: This is for the lidar
sudo chmod 777 /dev/ttyUSB0 && \


## NOTE: These are permissions for other devices
sudo chmod 666 /dev/ttyTHS1 && \
sudo chmod 666 /dev/i2c-7 && \

# realsense ros set up
cd ${ISAAC_ROS_WS} && \
colcon build --symlink-install --packages-up-to-regex realsense* && \

# unitree ros set up (building unitree workspaces)
cd ${ISAAC_ROS_WS}/src/unitree_ros2/cyclonedds_ws && \
colcon build --packages-select cyclonedds && \
source /opt/ros/humble/setup.bash && \
colcon build && \

# building the isaac ros ws
cd ${ISAAC_ROS_WS} && \
colcon build --symlink-install && \

# sourcing ros 
source src/unitree_ros2/setup.sh && \
source install/setup.bash 

