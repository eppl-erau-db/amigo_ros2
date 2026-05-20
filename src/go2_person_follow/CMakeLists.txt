cmake_minimum_required(VERSION 3.8)
project(go2_person_follow)

find_package(ament_cmake REQUIRED)

install(PROGRAMS
  scripts/person_follow_vision_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME person_follow_vision_node
)

ament_package()
