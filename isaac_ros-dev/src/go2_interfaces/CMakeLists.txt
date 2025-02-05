cmake_minimum_required(VERSION 3.8)
project(go2_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Required packages for building interfaces
find_package(ament_cmake REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# Generate interfaces from .action and .srv files
# (Make sure you actually have 'srv/RegionMap.srv' in the 'go2_interfaces/srv/' directory)
rosidl_generate_interfaces(${PROJECT_NAME}
  "action/LogPose.action"
  "srv/RegionMap.srv"
  "action/Search.action"
  DEPENDENCIES geometry_msgs nav_msgs # or any other interface package needed
)

# Export dependencies so other packages that depend on go2_interfaces
# know about the generated code
ament_export_dependencies(rosidl_default_runtime)
ament_export_dependencies(nav_msgs)

ament_package()
