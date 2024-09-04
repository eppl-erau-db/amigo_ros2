# AMIGO ROS2
This repository contains all of the necessary software for running the AMIGO (Autonomous Machine for Inspecting Gas and Operations), developed by EPPL. 

## Requirements and Background

To use this repository as is, you will need a Jetson device (preferably the AGX Orin), a RealSense D435i, an RPLiDAR A3, and accompanying mounting assembly. The CAD for the assembly will soon be published. 

This repo works completely off of a container (isaac_ros_dev-aarch64-container), and anything under the isaac ros workspace will be volumized, such that you any data saved in the workspace will not be lost when the container is shut down. 

## Startup Procedure

Make sure that your jetson is flashed with JetPack 6.0 on SSD. Then follow setup instructions for jetson [here](https://nvidia-isaac-ros.github.io/getting_started/hardware_setup/compute/index.html#jetson-platforms), and the isaac-ros setup page instructions, stopping AFTER step 3 [here](https://nvidia-isaac-ros.github.io/getting_started/dev_env_setup.html).

Then, clone the repo.

```bash
git clone --recurse-submodules https://github.com/gabearod2/workspaces.git
```

Next, you need to add the shortcut of your workspace to the .bashrc. Assuming you clone this repo into your workspaces directory.

```bash
mkdir -p  ~/workspaces/isaac_ros-dev/src
echo "export ISAAC_ROS_WS=~/workspaces/isaac_ros-dev/" >> ~/.bashrc
source ~/.bashrc
```

Configuring to build the container to use realsense-ros.

```bash
cd ${ISAAC_ROS_WS}/src/isaac_ros_common/scripts && \
touch .isaac_ros_common-config && \
echo CONFIG_IMAGE_KEY=ros2_humble.realsense > .isaac_ros_common-config
```

First ensuring your realsense if plugged in, build the conatiner. This will take a long time.

```bash
cd ${ISAAC_ROS_WS}/src/isaac_ros_common && \
./scripts/run_dev.sh -d ${ISAAC_ROS_WS}
```

Once in the container, source the setup script.

```bash
cd ${ISAAC_ROS_WS} && \
chmod +x setup.bash &&
source ./setup.bash
```

To test the realsense, use the following command.

```bash
realsense-viewer
```

Source r

## Post-Reboot Setup Procedure 

For the run.sh of the container, we have removed the "-rm" such that the conatiner continues to run, so that the dependencies do not need to be re-installed every time you run the container. Keep in mind that you still need an internet connection however. To open the container again:

```bash
docker exec -it isaac_ros_dev-aarch64-container /bin/bash
```

If you need more terminals in the container, run the same line on each terminal. 

## Running XXX

Open a new 

```bash
source src/unitree_ros2/setup.sh && \
source install/setup.bash 
```





