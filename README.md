# AMIGO ROS2

## Requirements and Background

This repository contains all of the necessary software for running the AMIGO (Autonomous Machine for Inspecting Gas and Operations), developed by EPPL. It is build off of ROS2 Humble, and uses various packages, cited at the end of this ReadMe.

To use this repository as is, you will need a Jetson device (preferably the AGX Orin), a RealSense D435i, an RPLiDAR A3, Internet connection, and accompanying mounting assembly. The CAD for the assembly will soon be published. This repo works completely off of a container (isaac_ros_dev-aarch64-container), and anything under the isaac ros workspace will be volumized, such that any data saved in the workspace will not be lost when the container is shut down. 

For future work, we are looking to integrate Unitree's LiDAR for localization, and deployment in 3D navigation. 

## Initial Startup Procedure

Make sure that your jetson is flashed with JetPack 6.0 on SSD. Then follow setup instructions for jetson [here](https://nvidia-isaac-ros.github.io/getting_started/hardware_setup/compute/index.html#jetson-platforms), and the isaac-ros setup page instructions, stopping AFTER step 3 [here](https://nvidia-isaac-ros.github.io/getting_started/dev_env_setup.html).

Then, ensure that you have workspaces directory at the correct location and clone this repo: 

```bash
mkdir -p ~/workspaces &&
cd ~/workspaces &&
git clone --recurse-submodules https://github.com/eppl-erau-db/amigo_ros2.git
```

Next, you need to add the shortcut of your workspace to the .bashrc for later usage:

```bash
mkdir -p  ~/workspaces/isaac_ros-dev/src
echo "export ISAAC_ROS_WS=~/workspaces/isaac_ros-dev/" >> ~/.bashrc
source ~/.bashrc
```

Now, configuring the container to use realsense-ros:

```bash
cd ${ISAAC_ROS_WS}/src/isaac_ros_common/scripts && \
touch .isaac_ros_common-config && \
echo CONFIG_IMAGE_KEY=ros2_humble.realsense > .isaac_ros_common-config
```

After ensuring your realsense if plugged in to your Jetson device, you can build the image and start the container. This will take a long time.

```bash
cd ${ISAAC_ROS_WS}/src/isaac_ros_common && \
./scripts/run_dev.sh -d ${ISAAC_ROS_WS}
```

Once in the container, source the setup script to install all required dependencies and packages.

```bash
cd ${ISAAC_ROS_WS} && \
chmod +x setup.bash && \
source ./setup.bash
```

Now, all ROS packages have been built and the container should be running correctly. You can move on to the next steps. If you would like to ensure the realsense is working (as it can sometimes be an issue), you can use the following command:

```bash
realsense-viewer
```

## Post_Reboot and/or Post_Startup Procedure 

We have made it such that the container continues to run, so that the dependencies do not need to be re-installed every time you run the container. Keep in mind that you still need an internet connection however. To open the container again:

```bash
docker exec -it isaac_ros_dev-aarch64-container /bin/bash
```

If you need more terminals in the container, run the same command in each terminal. 

## Navigation Deployment: Pose-oriented Navigation

### Mapping Launch: Construct a 2D Map and Log Poses

Launch a [terminal](#Post_Reboot-and/or-Post_Startup-Procedure) in the container and source ROS: First you must begin by creating a 2D map of the area using a tool like Slam Toolbox(used here). This map serves as the foundation for the robot's navigation.

```bash
source src/unitree_ros2/setup.sh && \
source install/setup.bash && \
ros2 launch go2_bringup mapping.launch.py | tee output.log
```
* While mapping use the log pose action call to define specific poses on this map at locations where you want the robot to navigate or perform certain tasks. These poses act as waypoints or goals for the robot.

Launch a [terminal](#Post_Reboot-and/or-Post_Startup-Procedure):

task_type 'normal': A pose defined as 'normal' is treated as a standard navigation task. This is useful if you want to constrain the global path planning algorithm to follow a specific path, avoiding high-traffic or hard-to-navigate areas.

```bash
ros2 action send_goal /log_pose go2_interfaces/action/LogPose "{task_type: 'normal'}"
```
task_type 'task': A pose defined as 'task' makes the robot stop at that pose for 5 seconds, simulating a task being performed, before continuing to the next pose.
You can customize this behavior by editing the task_nav_to_pose_test.py script to add functionalities like object detection or other task-specific actions.

```bash
ros2 action send_goal /log_pose go2_interfaces/action/LogPose "{task_type: 'task'}"
```

Saving the map:

TODO: How to save this map in the same location (src/go2_description/maps) every time?

```bash
ros2 run nav2_map_server map_saver_cli -f <MAP_NAME>
```

close out...

### Navigation Launch

After mapping is completed ...

run navigation like this ...

parameters that you can use

TODO: explain each of launch parameters

```bash
launch arguments: 
-use_sim_time (boolean, default = false)
-map_file (full path to map file*, default first_floor_coas.yaml)
-rviz (boolean, default = false)
-visualization (boolean, default = true)
-intial_pose (boolean, default = false)
```

starting nav stack:

```bash
source src/unitree_ros2/setup.sh && \
source install/setup.bash && \
ros2 launch go2_bringup go2_deploy.launch.py map_file:=src/go2_description/maps/<MAP_NAME>.yaml rviz:=true visualization:=false initial_pose:=false | tee nav_output.log
```

starting navigation

```bash
ros2 run go2_control task_nav_to_pose_test | tee task_output.log
```

If you're having trouble localizing (if your LiDAR...), go here (link to the Map Localization section)

### Map Localization

To use map localization service, yuo need to do this...

```bash
sudo apt update
sudo apt install imagemagick
convert <MAP_NAME>.pgm <MAP_NAME>.png
```

To run, use this command ...

```bash
ros2 service call trigger_grid_search_localization std_srvs/srv/Empty {}
```

## References and Citations

TODO: Link repos that we copied and stuff

## Contributors

TODO: Link your LinkedIn and GitHub
