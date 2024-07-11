# Install script for directory: /workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen/unsupported/Eigen

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
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

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/eigen3/unsupported/Eigen" TYPE FILE FILES
    "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen/unsupported/Eigen/AdolcForward"
    "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen/unsupported/Eigen/AlignedVector3"
    "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen/unsupported/Eigen/ArpackSupport"
    "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen/unsupported/Eigen/AutoDiff"
    "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen/unsupported/Eigen/BVH"
    "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen/unsupported/Eigen/EulerAngles"
    "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen/unsupported/Eigen/FFT"
    "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen/unsupported/Eigen/IterativeSolvers"
    "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen/unsupported/Eigen/KroneckerProduct"
    "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen/unsupported/Eigen/LevenbergMarquardt"
    "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen/unsupported/Eigen/MatrixFunctions"
    "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen/unsupported/Eigen/MoreVectorization"
    "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen/unsupported/Eigen/MPRealSupport"
    "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen/unsupported/Eigen/NonLinearOptimization"
    "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen/unsupported/Eigen/NumericalDiff"
    "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen/unsupported/Eigen/OpenGLSupport"
    "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen/unsupported/Eigen/Polynomials"
    "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen/unsupported/Eigen/Skyline"
    "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen/unsupported/Eigen/SparseExtra"
    "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen/unsupported/Eigen/SpecialFunctions"
    "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen/unsupported/Eigen/Splines"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/eigen3/unsupported/Eigen" TYPE DIRECTORY FILES "/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen/unsupported/Eigen/src" FILES_MATCHING REGEX "/[^/]*\\.h$")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/eigen/src/ext_eigen-build/unsupported/Eigen/CXX11/cmake_install.cmake")

endif()

