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
find_package(go2_interfaces REQUIRED)
find_package(std_msgs REQUIRED)
find_package(unitree_go REQUIRED)
find_package(unitree_api REQUIRED)
find_package(Threads REQUIRED)

# NEW deps for z-band filter
find_package(sensor_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2_eigen REQUIRED)

set(UNITREE_SDK_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/../../sdk/unitree_sdk2")
set(UNITREE_SDK_THIRDPARTY_ROOT "${UNITREE_SDK_ROOT}/thirdparty")
find_library(
  UNITREE_SDK2_LIB
  unitree_sdk2
  PATHS "${UNITREE_SDK_ROOT}/lib/${CMAKE_SYSTEM_PROCESSOR}"
  REQUIRED
  NO_DEFAULT_PATH
)
find_library(
  UNITREE_DDSC_LIB
  ddsc
  PATHS "${UNITREE_SDK_THIRDPARTY_ROOT}/lib/${CMAKE_SYSTEM_PROCESSOR}"
  REQUIRED
  NO_DEFAULT_PATH
)
find_library(
  UNITREE_DDSCXX_LIB
  ddscxx
  PATHS "${UNITREE_SDK_THIRDPARTY_ROOT}/lib/${CMAKE_SYSTEM_PROCESSOR}"
  REQUIRED
  NO_DEFAULT_PATH
)

# go2 driver
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

add_executable(person_follow_motion_bridge_node src/person_follow_motion_bridge_node.cpp)
target_include_directories(person_follow_motion_bridge_node PRIVATE
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
  "${UNITREE_SDK_ROOT}/include"
  "${UNITREE_SDK_THIRDPARTY_ROOT}/include"
  "${UNITREE_SDK_THIRDPARTY_ROOT}/include/ddscxx")
ament_target_dependencies(person_follow_motion_bridge_node
  rclcpp
  geometry_msgs
  go2_interfaces
  std_msgs
)
target_link_libraries(person_follow_motion_bridge_node
  ${UNITREE_SDK2_LIB}
  ${UNITREE_DDSC_LIB}
  ${UNITREE_DDSCXX_LIB}
  Threads::Threads
)

add_executable(voice_attention_motion_bridge_node src/voice_attention_motion_bridge_node.cpp)
target_include_directories(voice_attention_motion_bridge_node PRIVATE
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
  "${UNITREE_SDK_ROOT}/include"
  "${UNITREE_SDK_THIRDPARTY_ROOT}/include"
  "${UNITREE_SDK_THIRDPARTY_ROOT}/include/ddscxx")
ament_target_dependencies(voice_attention_motion_bridge_node
  rclcpp
  geometry_msgs
  std_msgs
)
target_link_libraries(voice_attention_motion_bridge_node
  ${UNITREE_SDK2_LIB}
  ${UNITREE_DDSC_LIB}
  ${UNITREE_DDSCXX_LIB}
  Threads::Threads
)

add_executable(go2_motion_mode_switcher src/go2_motion_mode_switcher.cpp)
target_include_directories(go2_motion_mode_switcher PRIVATE
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
  "${UNITREE_SDK_ROOT}/include"
  "${UNITREE_SDK_THIRDPARTY_ROOT}/include"
  "${UNITREE_SDK_THIRDPARTY_ROOT}/include/ddscxx")
target_link_libraries(go2_motion_mode_switcher
  ${UNITREE_SDK2_LIB}
  ${UNITREE_DDSC_LIB}
  ${UNITREE_DDSCXX_LIB}
  Threads::Threads
)

# z-band filter
add_executable(z_band_filter_node src/z_band_filter_node.cpp)
ament_target_dependencies(z_band_filter_node
  rclcpp
  sensor_msgs
  tf2
  tf2_ros
  tf2_eigen
)

install(TARGETS
  go2_driver_node
  person_follow_motion_bridge_node
  voice_attention_motion_bridge_node
  go2_motion_mode_switcher
  z_band_filter_node
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
