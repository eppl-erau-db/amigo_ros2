# Install script for directory: /mnt/nvme_partition/workspaces/lse_go2_ws/src/unitree_ros2/cyclonedds_ws/src/rmw_cyclonedds/rmw_cyclonedds_cpp

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/mnt/nvme_partition/workspaces/lse_go2_ws/src/unitree_ros2/cyclonedds_ws/install/rmw_cyclonedds_cpp")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ament_index/resource_index/rmw_typesupport_c" TYPE FILE FILES "/mnt/nvme_partition/workspaces/lse_go2_ws/src/unitree_ros2/cyclonedds_ws/build/rmw_cyclonedds_cpp/ament_cmake_index/share/ament_index/resource_index/rmw_typesupport_c/rmw_cyclonedds_cpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ament_index/resource_index/rmw_typesupport_cpp" TYPE FILE FILES "/mnt/nvme_partition/workspaces/lse_go2_ws/src/unitree_ros2/cyclonedds_ws/build/rmw_cyclonedds_cpp/ament_cmake_index/share/ament_index/resource_index/rmw_typesupport_cpp/rmw_cyclonedds_cpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ament_index/resource_index/rmw_typesupport" TYPE FILE FILES "/mnt/nvme_partition/workspaces/lse_go2_ws/src/unitree_ros2/cyclonedds_ws/build/rmw_cyclonedds_cpp/ament_cmake_index/share/ament_index/resource_index/rmw_typesupport/rmw_cyclonedds_cpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ament_index/resource_index/package_run_dependencies" TYPE FILE FILES "/mnt/nvme_partition/workspaces/lse_go2_ws/src/unitree_ros2/cyclonedds_ws/build/rmw_cyclonedds_cpp/ament_cmake_index/share/ament_index/resource_index/package_run_dependencies/rmw_cyclonedds_cpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ament_index/resource_index/parent_prefix_path" TYPE FILE FILES "/mnt/nvme_partition/workspaces/lse_go2_ws/src/unitree_ros2/cyclonedds_ws/build/rmw_cyclonedds_cpp/ament_cmake_index/share/ament_index/resource_index/parent_prefix_path/rmw_cyclonedds_cpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rmw_cyclonedds_cpp/environment" TYPE FILE FILES "/opt/ros/humble/share/ament_cmake_core/cmake/environment_hooks/environment/ament_prefix_path.sh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rmw_cyclonedds_cpp/environment" TYPE FILE FILES "/mnt/nvme_partition/workspaces/lse_go2_ws/src/unitree_ros2/cyclonedds_ws/build/rmw_cyclonedds_cpp/ament_cmake_environment_hooks/ament_prefix_path.dsv")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rmw_cyclonedds_cpp/environment" TYPE FILE FILES "/opt/ros/humble/share/ament_cmake_core/cmake/environment_hooks/environment/path.sh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rmw_cyclonedds_cpp/environment" TYPE FILE FILES "/mnt/nvme_partition/workspaces/lse_go2_ws/src/unitree_ros2/cyclonedds_ws/build/rmw_cyclonedds_cpp/ament_cmake_environment_hooks/path.dsv")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rmw_cyclonedds_cpp" TYPE FILE FILES "/mnt/nvme_partition/workspaces/lse_go2_ws/src/unitree_ros2/cyclonedds_ws/build/rmw_cyclonedds_cpp/ament_cmake_environment_hooks/local_setup.bash")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rmw_cyclonedds_cpp" TYPE FILE FILES "/mnt/nvme_partition/workspaces/lse_go2_ws/src/unitree_ros2/cyclonedds_ws/build/rmw_cyclonedds_cpp/ament_cmake_environment_hooks/local_setup.sh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rmw_cyclonedds_cpp" TYPE FILE FILES "/mnt/nvme_partition/workspaces/lse_go2_ws/src/unitree_ros2/cyclonedds_ws/build/rmw_cyclonedds_cpp/ament_cmake_environment_hooks/local_setup.zsh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rmw_cyclonedds_cpp" TYPE FILE FILES "/mnt/nvme_partition/workspaces/lse_go2_ws/src/unitree_ros2/cyclonedds_ws/build/rmw_cyclonedds_cpp/ament_cmake_environment_hooks/local_setup.dsv")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rmw_cyclonedds_cpp" TYPE FILE FILES "/mnt/nvme_partition/workspaces/lse_go2_ws/src/unitree_ros2/cyclonedds_ws/build/rmw_cyclonedds_cpp/ament_cmake_environment_hooks/package.dsv")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ament_index/resource_index/packages" TYPE FILE FILES "/mnt/nvme_partition/workspaces/lse_go2_ws/src/unitree_ros2/cyclonedds_ws/build/rmw_cyclonedds_cpp/ament_cmake_index/share/ament_index/resource_index/packages/rmw_cyclonedds_cpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/share/rmw_cyclonedds_cpp/cmake/export_rmw_cyclonedds_cppExport.cmake")
    file(DIFFERENT EXPORT_FILE_CHANGED FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/share/rmw_cyclonedds_cpp/cmake/export_rmw_cyclonedds_cppExport.cmake"
         "/mnt/nvme_partition/workspaces/lse_go2_ws/src/unitree_ros2/cyclonedds_ws/build/rmw_cyclonedds_cpp/CMakeFiles/Export/share/rmw_cyclonedds_cpp/cmake/export_rmw_cyclonedds_cppExport.cmake")
    if(EXPORT_FILE_CHANGED)
      file(GLOB OLD_CONFIG_FILES "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/share/rmw_cyclonedds_cpp/cmake/export_rmw_cyclonedds_cppExport-*.cmake")
      if(OLD_CONFIG_FILES)
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/share/rmw_cyclonedds_cpp/cmake/export_rmw_cyclonedds_cppExport.cmake\" will be replaced.  Removing files [${OLD_CONFIG_FILES}].")
        file(REMOVE ${OLD_CONFIG_FILES})
      endif()
    endif()
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rmw_cyclonedds_cpp/cmake" TYPE FILE FILES "/mnt/nvme_partition/workspaces/lse_go2_ws/src/unitree_ros2/cyclonedds_ws/build/rmw_cyclonedds_cpp/CMakeFiles/Export/share/rmw_cyclonedds_cpp/cmake/export_rmw_cyclonedds_cppExport.cmake")
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^()$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rmw_cyclonedds_cpp/cmake" TYPE FILE FILES "/mnt/nvme_partition/workspaces/lse_go2_ws/src/unitree_ros2/cyclonedds_ws/build/rmw_cyclonedds_cpp/CMakeFiles/Export/share/rmw_cyclonedds_cpp/cmake/export_rmw_cyclonedds_cppExport-noconfig.cmake")
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rmw_cyclonedds_cpp/cmake" TYPE FILE FILES "/mnt/nvme_partition/workspaces/lse_go2_ws/src/unitree_ros2/cyclonedds_ws/build/rmw_cyclonedds_cpp/ament_cmake_export_dependencies/ament_cmake_export_dependencies-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rmw_cyclonedds_cpp/cmake" TYPE FILE FILES "/mnt/nvme_partition/workspaces/lse_go2_ws/src/unitree_ros2/cyclonedds_ws/build/rmw_cyclonedds_cpp/ament_cmake_export_targets/ament_cmake_export_targets-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rmw_cyclonedds_cpp/cmake" TYPE FILE FILES
    "/mnt/nvme_partition/workspaces/lse_go2_ws/src/unitree_ros2/cyclonedds_ws/build/rmw_cyclonedds_cpp/ament_cmake_core/rmw_cyclonedds_cppConfig.cmake"
    "/mnt/nvme_partition/workspaces/lse_go2_ws/src/unitree_ros2/cyclonedds_ws/build/rmw_cyclonedds_cpp/ament_cmake_core/rmw_cyclonedds_cppConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rmw_cyclonedds_cpp" TYPE FILE FILES "/mnt/nvme_partition/workspaces/lse_go2_ws/src/unitree_ros2/cyclonedds_ws/src/rmw_cyclonedds/rmw_cyclonedds_cpp/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/librmw_cyclonedds_cpp.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/librmw_cyclonedds_cpp.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/librmw_cyclonedds_cpp.so"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/mnt/nvme_partition/workspaces/lse_go2_ws/src/unitree_ros2/cyclonedds_ws/build/rmw_cyclonedds_cpp/librmw_cyclonedds_cpp.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/librmw_cyclonedds_cpp.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/librmw_cyclonedds_cpp.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/librmw_cyclonedds_cpp.so"
         OLD_RPATH "/mnt/nvme_partition/workspaces/lse_go2_ws/src/unitree_ros2/cyclonedds_ws/install/cyclonedds/lib:/opt/ros/humble/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/librmw_cyclonedds_cpp.so")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ament_index/resource_index/rmw_output_patterns" TYPE FILE FILES "/mnt/nvme_partition/workspaces/lse_go2_ws/src/unitree_ros2/cyclonedds_ws/build/rmw_cyclonedds_cpp/ament_cmake_index/share/ament_index/resource_index/rmw_output_patterns/rmw_cyclonedds_cpp")
endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/mnt/nvme_partition/workspaces/lse_go2_ws/src/unitree_ros2/cyclonedds_ws/build/rmw_cyclonedds_cpp/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
