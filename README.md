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
mkdir -p  ~/workspaces/amigo_ros2/isaac_ros-dev/src
echo "export ISAAC_ROS_WS=~/workspaces/amigo_ros2/isaac_ros-dev/" >> ~/.bashrc
source ~/.bashrc
```

Now, configuring the container to use realsense-ros:

```bash
cd ${ISAAC_ROS_WS}/src/isaac_ros_common/scripts && \
touch .isaac_ros_common-config && \
echo CONFIG_IMAGE_KEY=ros2_humble.realsense > .isaac_ros_common-config
```

After **ensuring your realsense is plugged in** to your Jetson device, you can build the image and start the container. **This will take a long time.**

```bash
cd ${ISAAC_ROS_WS}/src/isaac_ros_common && \
./scripts/run_dev.sh -d ${ISAAC_ROS_WS}
```

Once in the container, source the setup script to install all required dependencies and packages.

TODO: SETUP THE SETUP.BASH

```bash
cd ${ISAAC_ROS_WS} && \
chmod +x setup.bash && \
source ./setup.bash
```

Now, all ROS packages have been built and the container should be running correctly. You can move on to the next steps. If you would like to ensure the realsense is working (as it can sometimes be an issue), you can use the following command:

```bash
realsense-viewer
```

## Post-Reboot and/or Post-Startup Procedure 

We have made it such that the container continues to run and automatically starts up on boot, so that the dependencies do not need to be re-installed every time you run the container. However, Keep in mind that you still need an internet connection. 

### Launch a Terminal
To open a terminal in the container:

```bash
docker exec -it isaac_ros_dev-aarch64-container /bin/bash
```

If you need more terminals attached to the container, run the same command in each new terminal as needed. 

## Navigation Deployment: Pose-Oriented Navigation

This navigation process involves two main phases: Mapping and Pose Logging and Autonomous Navigation. You start by creating a 2D map and logging poses, then use these for the robot's autonomous navigation.

### Phase 1: Constructing a 2D Map and Logging Poses

#### Mapping: 
Launch a [container terminal](#launch-a-terminal) in a new terminal window and source ROS. Begin by manually driving the robot to create a 2D map of the area using a tool like Slam Toolbox(used here). This map serves as the foundation for the robot's navigation.

```bash
source src/unitree_ros2/setup.sh && \
source install/setup.bash && \
ros2 launch go2_bringup mapping.launch.py | tee output.log
```
NOTE: While you are actively mapping, use the [log action pose call](#pose-logging) to create a file with defined poses on the current map at locations where you want the robot to navigate or perform certain tasks. These poses act as waypoints or goals for the robot.

#### Pose Logging: 
Launch a [container terminal](#launch-a-terminal) in a new terminal window and call the following actions as needed:

- task_type 'normal': A pose defined as 'normal' is treated as a standard navigation task. This is useful if you want to constrain the global path planning algorithm to follow a specific path, avoiding high-traffic or hard-to-navigate areas.

```bash
ros2 action send_goal /log_pose go2_interfaces/action/LogPose "{task_type: 'normal'}"
```
- task_type 'task': A pose defined as 'task' makes the robot stop at that pose for 5 seconds, simulating a task being performed, before continuing to the next pose.
You can customize this behavior by editing the task_nav_to_pose_test.py script located in ${ISAAC_ROS_WS}/src/go2_control/go2_control/task_nav_to_pose_test.py to add functionalities like object detection or other task-specific actions.

```bash
ros2 action send_goal /log_pose go2_interfaces/action/LogPose "{task_type: 'task'}"
```

#### Saving the map: 
Once done with mapping the area and creating poses for navigation, save the map. Make sure to replace <MAP_NAME> with the name of your map.

```bash
ros2 run nav2_map_server map_saver_cli -f src/go2_description/maps/<MAP_NAME>
```
You now have a map saved in the ${ISAAC_ROS_WS}/src/go2_description/maps/ directory, along with a JSON file in the current directory containing a set of poses for navigation.

### Phase 2: Autonomous Navigation

To navigate you need to launch 2 separate files:

#### launch arguments:

You can use various launch parameters for regular deployment, testing and debugging in both simulation and real-world scenarios, as well as for deployment with Foxglove Studio.

- use_sim_time (boolean, default = false) *Used for simulation in Gazebo etc.
- map_file (full path to map file, default = first_floor_coas.yaml) *useful for quick change of map without having to edit launch file
- rviz (boolean, default = false) *useful to turn off rviz as needed
- visualization (boolean, default = true) *useful to send navigation info over wifi to laptop using Foxglove Studio
- intial_pose (boolean, default = false) *useful to start the robot at the same spot where you started mapping without sending it on a navigation run. you can the use rviz to make sure all sensors are working properly

#### Launch the nav stack:
Open a [container terminal](#launch-a-terminal) in a new terminal window and launch the nav2 stack launch file. In this example, I am starting the navigation stack with RViz and using RealVNC to stream the desktop to my laptop via an HDMI dummy plug to follow robot around and use RViz for debugging. Set-up steps for RealVNC for jetson seen [here](https://developer.nvidia.com/embedded/learn/tutorials/vnc-setup).

```bash
source src/unitree_ros2/setup.sh && \
source install/setup.bash && \
ros2 launch go2_bringup go2_deploy.launch.py map_file:=src/go2_description/maps/<MAP_NAME>.yaml rviz:=true visualization:=false initial_pose:=false | tee nav_output.log
```

##### Important NOTES: 
- if you did not use "initial_pose:=true" you will not see the robot and there will be error messages in the Terminal window, this is normal becuase Nav2 requires an initial position to work.
- you CANNOT set "initial_pose:=true" if you are planning to use the [navigation script](#start-navigation-script) becuase this will interfere with the nav2 system.
- If you want to use Foxglove Studio additional information can be found [here](https://nvidia-isaac-ros.github.io/concepts/visualization/index.html).

#### Start Navigation Script
The following script, located in ${ISAAC_ROS_WS}/src/go2_control/go2_control/, sets the initial pose to the starting point of the map where you began mapping when you launched the [mapper](#mapping), and begins to navigate to the previously logged set of poses located in the pose_log.json file.

Open a [container terminal](#launch-a-terminal) in a new terminal window and launch the script:

```bash
ros2 run go2_control task_nav_to_pose_test | tee task_output.log
```

### Map Localization
This service is optional but useful in certain situations. I typically use it when the robot is not correctly positioned on the map or when the robot starts from a different location than the initial pose, requiring a recalculation of its position.

#### How to Use the Service:

##### Convert the Map Format:
 Before starting the navigation stack, convert the map from .pgm to .png format. Then, update the <MAP_NAME>.yaml file to match the new image format

```bash
convert ${ISAAC_ROS_WS}/src/go2_description/maps/<MAP_NAME>.pgm ${ISAAC_ROS_WS}/src/go2_description/maps/<MAP_NAME>.png && \
sed -i 's/image: <MAP_NAME>.pgm/image: <MAP_NAME>.png/' ${ISAAC_ROS_WS}/src/go2_description/maps/<MAP_NAME>.yaml
```
##### Use the Service to Re-Localize:
Once the map is in the correct format, you can use the service to re-localize the robot on the map. Run the following command in a container terminal while the Nav2 stack is active as many times as needed until you reach actual robot position.

```bash
ros2 service call trigger_grid_search_localization std_srvs/srv/Empty {}
```

## References and Citations

TODO: Link repos that we copied and stuff

## Contributors

TODO: Link your LinkedIn and GitHub
