cmake_minimum_required(VERSION 3.8)
project(go2_driver)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Set CMAKE_PREFIX_PATH
set(CMAKE_PREFIX_PATH "/workspaces/isaac_ros-dev/src/unitree_ros2/cyclonedds_ws/src/unitree" ${CMAKE_PREFIX_PATH})

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(unitree_go REQUIRED)
find_package(unitree_api REQUIRED)

add_executable(go2_driver_node src/go2_driver_node.cpp src/common/ros2_sport_client.cpp)
target_include_directories(go2_driver_node PRIVATE
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
ament_target_dependencies(go2_driver_node
  rclcpp
  geometry_msgs
  unitree_go
  unitree_api
)

install(TARGETS
  go2_driver_node
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()

