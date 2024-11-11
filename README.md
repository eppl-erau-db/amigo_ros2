# AMIGO ROS2 Humble 

AMIGO (Autonomous Machine for Inspecting Gas and Operations) is a ROS2 Humble-based robotic system developed by the Engineering Physics Propulsion Lab (EPPL) at Embry-Riddle Aeronautical University. Leavereging Unitree's Go2 quadruped robot, AMIGO facilitates autonomous navigation and inspection tasks in complex industrial environments.

## Requirements and Background

This repository contains all of the necessary software for running AMIGO, developed by EPPL. It is build off of ROS2 Humble, and uses various packages, cited at the end of this ReadMe.

To use this repository as is, you will need a Jetson device (preferably the AGX Orin) **flashed with JetPack 6.0**, a RealSense D435i or D455, an RPLiDAR A3, Internet connection, and accompanying mounting assembly. The CAD for the assembly can be downloaded [here](https://drive.google.com/file/d/1BN40XFT44lI892btThJ22HuvqJPCsLoT/view?usp=sharing). This repo works completely off of a container (isaac_ros_dev-aarch64-container), and anything under the isaac ros workspace will be volumized, such that any data saved in the workspace will not be lost when the container is shut down. 

For future work, we are looking to integrate Unitree's LiDAR for localization, and deployment in 3D navigation.

## Hardware Setup

- This is the current setup of our prototype:
- 
  **NOTE:** If you want to change the position of any of the sensors, the robot URDF file (found here: ${ISAAC_ROS_WS}/src/go2_description/urdf/go2_nav2_nvblox.urdf) must be updated to match the position of the sensor in reference to base_link

![setup](https://github.com/eppl-erau-db/amigo_ros2/blob/main/images/setup.jpg)

- If you are using a **Jetson AGX Orin** you will need to step down the voltage to ~20V with a DC-to-DC Buck Converter that can provide atleast 5 amps as pictured below:

![power](https://github.com/eppl-erau-db/amigo_ros2/blob/main/images/powerSystem.jpg)

- Our current CAD also includes some room for a capture card to use the ZED X series camera **this camera will soon be be integrated to add capabilities.**

![camera](https://github.com/eppl-erau-db/amigo_ros2/blob/main/images/sideView.jpg) 

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

```bash
cd ${ISAAC_ROS_WS} && \
chmod +x setup.bash && \
source ./setup.bash
```

Now, all ROS packages have been built and the container should be running correctly. You can move on to the next steps. If you would like to ensure the realsense is working (as it can sometimes be an issue), you can use the following command:

```bash
realsense-viewer
```

## Post-Startup/Post-Reboot Procedure 

### Launch a Terminal
To open a terminal in the container:

```bash
cd ${ISAAC_ROS_WS}/src/isaac_ros_common && \
./scripts/run_dev.sh -d ${ISAAC_ROS_WS}
```
### Post-Reboot

**If you have rebooted your device or closed down all container instances** you will have to run the setup.bash again to install dependencies and give permissions for the devices and the navstack to work porperly.

```bash
cd ${ISAAC_ROS_WS} && \
chmod +x setup.bash && \
source ./setup.bash
```
- NOTE: you only have to run this setup.bash on the first terminal you open after rebooting, any other terminals you only need to [source](#source-ros2-and-your-workspace) ROS2 and your workspace.


### Source ROS2 and your workspace
You also need to source ROS2 and your workspace for **every terminal**

```bash
source src/unitree_ros2/setup.sh && \
source install/setup.bash
```

- NOTE: If you need more terminals attached to the container, Launch a [container terminal](#launch-a-terminal) in each new Bash window as needed. 



## Navigation Deployment: Pose-Oriented Navigation

This navigation process involves two main phases: Mapping and Pose Logging and Autonomous Navigation. You start by creating a 2D map and logging poses, then use these for the robot's autonomous navigation.

### Phase 1: Constructing a 2D Map and Logging Poses

#### Mapping: 
Launch a [container terminal](#launch-a-terminal) in a new Bash window and [source](#source-ros2-and-your-workspace) ROS. Begin by manually driving the robot to create a 2D map of the area using a tool like Slam Toolbox(used here). This map serves as the foundation for the robot's navigation.

```bash
ros2 launch go2_bringup mapping.launch.py | tee mappingOutput.log
```
NOTE: While you are actively mapping, use the [log action pose call](#pose-logging) to create a file with defined poses on the current map at locations where you want the robot to navigate or perform certain tasks. These poses act as waypoints or goals for the robot.

#### Pose Logging: 
Launch a [container terminal](#launch-a-terminal) in a new Bash window [source](#source-ros2-and-your-workspace) your workspace and call the following actions as needed:

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
ros2 run nav2_map_server map_saver_cli -f src/go2_description/maps/<MAP_NAME> --free 0.25 --occ 0.65 --fmt png
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
Open a [container terminal](#launch-a-terminal) in a new Bash window, [source](#source-ros2-and-your-workspace) your workspace and launch the nav2 stack launch file. In this example, I am starting the navigation stack with RViz and using RealVNC to stream the desktop to my laptop via an HDMI dummy plug to follow robot around and use RViz for debugging. Set-up steps for RealVNC for jetson seen [here](https://developer.nvidia.com/embedded/learn/tutorials/vnc-setup). Or you can set visualization:=true and use Foxglove Studio to send and view all ROS topics (similar to RViz) over wifi to your laptop, additional information can be found [here](https://nvidia-isaac-ros.github.io/concepts/visualization/index.html).

```bash
ros2 launch go2_bringup go2_deploy.launch.py map_file:=src/go2_description/maps/<MAP_NAME>.yaml rviz:=true visualization:=false initial_pose:=false | tee navOutput.log
```

##### Important NOTES:
- Make sure to change <MAP_NAME> to the actual name of your map.
- If you did not use "initial_pose:=true" you will not see the robot and there will be error messages in the Bash window, this is normal becuase Nav2 requires an initial position to work, which will be done in the next step.
- **You CANNOT** set "initial_pose:=true" if you are planning to use the [navigation script](#start-navigation-script) becuase this will interfere with the nav2 system and it will not work properly.

#### Start Navigation Script
The following script, located in ${ISAAC_ROS_WS}/src/go2_control/go2_control/, sets the initial pose to the starting point of the map where you began mapping when you launched the [mapper](#mapping), and begins to navigate to the previously logged set of poses located in the pose_log.json file.

Open a [container terminal](#launch-a-terminal) in a new Bash window and [source](#source-ros2-and-your-workspace) your workspace to launch the script:

```bash
ros2 run go2_control task_nav_to_pose_test | tee taskOutput.log
```

**Note** you can edit this script to add functionality while its navigating or at the task pose itself. for more info on how to do this check out [Nav2_Simple_commander](https://github.com/ros-navigation/navigation2/tree/main/nav2_simple_commander/nav2_simple_commander) for example code.



## References and Citations

### Nav2:

**S. Macenski, F. Martín, R. White, J. Clavero. The Marathon 2: A Navigation System. IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2020.**

- @InProceedings{macenski2020marathon2,
  title = {The Marathon 2: A Navigation System},
  author = {Macenski, Steve and Martín, Francisco and White, Ruffin and Ginés Clavero, Jonatan},
  year = {2020},
  booktitle = {2020 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)},
  url = {https://github.com/ros-planning/navigation2},
  pdf = {https://arxiv.org/abs/2003.00368}
  }

**S. Macenski, T. Moore, DV Lu, A. Merzlyakov, M. Ferguson, From the desks of ROS maintainers: A survey of modern & capable mobile robotics algorithms in the robot operating system 2, Robotics and Autonomous Systems, 2023.**

  - @article{macenski2023survey,
    title={From the desks of ROS maintainers: A survey of modern & capable mobile robotics algorithms in the robot operating system 2}, 
    author={S. Macenski, T. Moore, DV Lu, A. Merzlyakov, M. Ferguson},
    year={2023},
    journal = {Robotics and Autonomous Systems}
    }

**S. Macenski, M. Booker, J. Wallace, Open-Source, Cost-Aware Kinematically Feasible Planning for Mobile and Surface Robotics. 2024.**

- @article{macenski2024smac,
  title={Open-Source, Cost-Aware Kinematically Feasible Planning for Mobile and Surface Robotics}, 
  author={Steve Macenski and Matthew Booker and Josh Wallace},
  year={2024},
  journal = {Arxiv}
  }

### NVIDIA Corporation. (2024). ISAAC ROS Packages. Retrieved from:

- isaac_ros_nvblox: https://nvidia-isaac-ros.github.io/repositories_and_packages/isaac_ros_nvblox/index.html
- isaac_ros_visual_slam: https://nvidia-isaac-ros.github.io/repositories_and_packages/isaac_ros_visual_slam/index.html
- isaac_ros_map_localization: https://nvidia-isaac-ros.github.io/repositories_and_packages/isaac_ros_map_localization/index.html
  
© 2024 NVIDIA Corporation. All rights reserved. NVIDIA and the NVIDIA logo are trademarks and/or registered trademarks of NVIDIA Corporation in the U.S. and other countries.

## Contributors

We are a team of researchers from the [Engineering Physics Propulsion Lab (EPPL)](https://daytonabeach.erau.edu/about/labs/engineering-physics-propulsion-lab) at Embry-Riddle Aeronautical University. You can find more about our work and connect with us on [LinkedIn](https://www.linkedin.com/company/eppl-erau-db/posts/?feedView=all).

## Thanks

Special thanks to:

- @brimokz, his repository helped me understand how to integrate the Go2 software.
Check out his [repository](https://github.com/abizovnuralem/go2_ros2_sdk)

- Check out **The RoboVerse** Discord channel where you will find everything Go2 related.
