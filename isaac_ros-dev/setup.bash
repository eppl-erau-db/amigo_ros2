#!/bin/bash

# Update package list and install dependencies
echo "Updating package list and installing required packages..."
sudo apt update && \
sudo apt install -y \
  ros-humble-rmw-cyclonedds-cpp \
  ros-humble-rosidl-generator-dds-idl \
  ros-humble-nmea-navsat-driver \
  ros-humble-point-cloud-transport \
  libgeographic-dev \
  ros-humble-geographic-msgs \
  libyaml-cpp-dev \
  python3-smbus \
  i2c-tools \
  python3-tk \
  ros-humble-robot-localization \
  imagemagick && \
echo "Installing Python packages..."
pip install transforms3d pyserial smbus

# Update rosdep and install dependencies
echo "Updating rosdep and installing package dependencies..."
rosdep update
rosdep install -i -r --from-paths /workspaces/isaac_ros-dev/src/isaac_ros_nvblox/ --rosdistro humble -y


# Set permissions for devices
echo "Setting permissions for devices..."
# Camera devices
for cam_device in /dev/video{0..5}; do
  if [ -e "$cam_device" ]; then
    sudo chmod 666 "$cam_device"
    echo "Set permissions for $cam_device"
  else
    echo "Warning: $cam_device not found"
  fi
done

# LiDAR device
if [ -e "/dev/ttyUSB0" ]; then
  sudo chmod 777 /dev/ttyUSB0
  echo "Set permissions for /dev/ttyUSB0"
else
  echo "Warning: /dev/ttyUSB0 not found"
fi

# Other devices
if [ -e "/dev/ttyTHS1" ]; then
  sudo chmod 666 /dev/ttyTHS1
  echo "Set permissions for /dev/ttyTHS1"
else
  echo "Warning: /dev/ttyTHS1 not found"
fi

if [ -e "/dev/i2c-7" ]; then
  sudo chmod 666 /dev/i2c-7
  echo "Set permissions for /dev/i2c-7"
else
  echo "Warning: /dev/i2c-7 not found"
fi

sudo chmod +x ${ISAAC_ROS_WS}/src/isaac_ros_common/docker/scripts/install-zed-aarch64.sh && \
${ISAAC_ROS_WS}/src/isaac_ros_common/docker/scripts/install-zed-aarch64.sh

cd ${ISAAC_ROS_WS} && \
sudo apt update && \
rosdep update && rosdep install --from-paths src/zed-ros2-wrapper --ignore-src -r -y && \
colcon build --symlink-install --packages-up-to zed_wrapper

# Build the workspaces
echo "Building ROS workspaces..."

# Build Unitree ROS2 workspace
cd ${ISAAC_ROS_WS}/src/unitree_ros2/cyclonedds_ws && \
colcon build --packages-select cyclonedds && \
source /opt/ros/humble/setup.bash && \
colcon build && \

cd /workspaces/isaac_ros-dev && \
colcon build --symlink-install --packages-up-to realsense_splitter && \

# Building the ISAAC ROS workspace
cd ${ISAAC_ROS_WS} && \
colcon build --symlink-install && \

# Source ROS setup files
echo "Sourcing ROS setup files..."
source ${ISAAC_ROS_WS}/src/unitree_ros2/setup.sh && \
source ${ISAAC_ROS_WS}/install/setup.bash

echo "Setup completed successfully!"
