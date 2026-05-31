cmake_minimum_required(VERSION 3.8)
project(go2_person_follow)

find_package(ament_cmake REQUIRED)

if(BUILD_TESTING)
  find_package(ament_cmake_pytest QUIET)
  if(ament_cmake_pytest_FOUND)
    ament_add_pytest_test(person_follow_vision test/test_person_follow_vision.py)
  endif()
endif()

install(PROGRAMS
  scripts/person_follow_vision_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME person_follow_vision_node
)

ament_package()
