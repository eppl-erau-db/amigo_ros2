cmake_minimum_required(VERSION 3.8)
project(go2_person_follow)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

find_package(ament_cmake REQUIRED)
find_package(image_transport REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(zed_msgs REQUIRED)
find_package(OpenCV REQUIRED)

add_executable(person_follow_vision_node
  src/person_follow_vision_node.cpp
)

target_include_directories(person_follow_vision_node PRIVATE
  ${OpenCV_INCLUDE_DIRS}
)

ament_target_dependencies(person_follow_vision_node
  image_transport
  rclcpp
  sensor_msgs
  geometry_msgs
  std_msgs
  zed_msgs
)

target_link_libraries(person_follow_vision_node
  ${OpenCV_LIBRARIES}
)

install(TARGETS
  person_follow_vision_node
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
