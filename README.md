# AMIGO ROS2 Humble

AMIGO (Autonomous Machine for Inspecting Gas and Operations) is a ROS2 Humble-based robotic system developed by the Engineering Physics Propulsion Lab (EPPL) at Embry-Riddle Aeronautical University. Leveraging Unitree's Go2 quadruped robot, AMIGO provides autonomous navigation and inspection workflows for industrial environments.

## Requirements and Background

This repository contains the software stack for running AMIGO on ROS2 Humble. The current primary camera is a ZED X Mini, but the launch files and URDF can be adapted for Intel RealSense cameras if desired.

### Hardware (current reference build)

- Jetson AGX Orin (JetPack 6.1) or Ubuntu 22.04 x86_64
- Unitree Go2
- ZED X Mini (primary camera) or Intel RealSense D435i/D455 (alternate)
- RPLiDAR A3 (or compatible RPLiDAR)
- GPS receiver (u-blox ZED-F9R tested)
- Network access for package installs

### Workspace layout

- `src/go2_bringup`: launch files for mapping, navigation, GPS
- `src/go2_description`: URDF, RViz configs, navigation and localization configs
- `src/go2_control`: logging, navigation scripts, GPS helpers
- `src/zed-ros2-wrapper`: ZED ROS2 wrapper (requires ZED SDK)
- `qtquick_test/qtquick_test-main`: QtQuick monitoring UI

## Setup

### Install ROS2 Humble

Follow the official ROS2 Humble install guide for Ubuntu 22.04. For Jetson, ensure JetPack 6.1 is installed first.

### Clone the repository

```bash
mkdir -p ~/workspaces
cd ~/workspaces
git clone --recurse-submodules https://github.com/eppl-erau-db/amigo_ros2.git
cd amigo_ros2
git submodule update --init --recursive
```

### Install dependencies

```bash
sudo apt update
rosdep update
rosdep install --from-paths src --ignore-src -r -y
```

### ZED SDK (if using ZED)

Install the Stereolabs ZED SDK before building so `zed-ros2-wrapper` can compile. Follow the Stereolabs installation guide for your platform.

### Build the workspace

```bash
source /opt/ros/humble/setup.bash
colcon build --symlink-install
```

### Source the environment

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
```

## Camera selection

### ZED (default)

The default URDF and mapping launch files assume a ZED camera and include the ZED macro in `src/go2_description/urdf/go2.urdf.xacro`. Ensure the ZED SDK is installed and the `zed-ros2-wrapper` package builds successfully.

### RealSense (alternative)

To use RealSense cameras:

1. Install the Intel RealSense ROS2 wrapper (`realsense-ros`).
2. Update `src/go2_description/urdf/go2.urdf.xacro` to replace the ZED macro with the RealSense URDF macro.
3. Update the launch files in `src/go2_bringup/launch` to start the RealSense driver and remap any camera topics as needed.

## Mapping and pose logging

### Mapping

```bash
ros2 launch go2_bringup mapping.launch.py
```

### Pose logging

- Log a normal navigation pose:

```bash
ros2 action send_goal /log_pose go2_interfaces/action/LogPose "{task_type: 'normal'}"
```

- Log a task pose:

```bash
ros2 action send_goal /log_pose go2_interfaces/action/LogPose "{task_type: 'task'}"
```

### Save the map

```bash
ros2 run nav2_map_server map_saver_cli -f src/go2_description/maps/<MAP_NAME> --free 0.25 --occ 0.65 --fmt png
```

## Localization and navigation

1. Update the map in `src/go2_description/config/slam_toolbox_localization.yaml`:
   - `map_file_name`
   - `map_start_pose`
2. Launch localization and navigation:

```bash
ros2 launch go2_bringup go2_deploy.launch.py rviz:=true initial_pose:=false
```

3. Start the navigation script:

```bash
ros2 run go2_control task_nav_to_pose_test
```

## GPS navigation (optional)

```bash
ros2 launch go2_bringup gps.launch.py use_rviz:=true use_mapviz:=true
```

## QtQuick monitoring UI

```bash
pip3 install PySide6
sudo apt install libxcb-cursor0
python3 qtquick_test/qtquick_test-main/main.py
```

## References and Citations

### Nav2

**S. Macenski, F. Martin, R. White, J. Clavero. The Marathon 2: A Navigation System. IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2020.**

- @InProceedings{macenski2020marathon2,
  title = {The Marathon 2: A Navigation System},
  author = {Macenski, Steve and Martin, Francisco and White, Ruffin and Gines Clavero, Jonatan},
  year = {2020},
  booktitle = {2020 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)},
  url = {https://github.com/ros-planning/navigation2},
  pdf = {https://arxiv.org/abs/2003.00368}
  }

**S. Macenski, T. Moore, DV Lu, A. Merzlyakov, M. Ferguson, From the desks of ROS maintainers: A survey of modern and capable mobile robotics algorithms in the robot operating system 2, Robotics and Autonomous Systems, 2023.**

  - @article{macenski2023survey,
    title={From the desks of ROS maintainers: A survey of modern and capable mobile robotics algorithms in the robot operating system 2},
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

## Contributors

We are a team of researchers from the [Engineering Physics Propulsion Lab (EPPL)](https://daytonabeach.erau.edu/about/labs/engineering-physics-propulsion-lab) at Embry-Riddle Aeronautical University. You can find more about our work and connect with us on [LinkedIn](https://www.linkedin.com/company/eppl-erau-db/posts/?feedView=all).

## Thanks

Special thanks to:

- @brimokz, his repository helped us understand how to integrate the Go2 software.
  Check out his repository: https://github.com/abizovnuralem/go2_ros2_sdk

- Check out The RoboVerse Discord channel where you will find everything Go2 related.
