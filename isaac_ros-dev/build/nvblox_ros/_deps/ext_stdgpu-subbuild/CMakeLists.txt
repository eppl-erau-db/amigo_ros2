# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.22.1)

# We name the project and the target for the ExternalProject_Add() call
# to something that will highlight to the user what we are working on if
# something goes wrong and an error message is produced.

project(ext_stdgpu-populate NONE)


# Pass through things we've already detected in the main project to avoid
# paying the cost of redetecting them again in ExternalProject_Add()
set(GIT_EXECUTABLE [==[/usr/bin/git]==])
set(GIT_VERSION_STRING [==[2.34.1]==])
set_property(GLOBAL PROPERTY _CMAKE_FindGit_GIT_EXECUTABLE_VERSION
  [==[/usr/bin/git;2.34.1]==]
)


include(ExternalProject)
ExternalProject_Add(ext_stdgpu-populate
                     "UPDATE_DISCONNECTED" "False" "SYSTEM" "PREFIX" "stdgpu" "GIT_REPOSITORY" "https://github.com/stotko/stdgpu.git" "GIT_TAG" "e10f6f3ccc9902d693af4380c3bcd188ec34a2e6" "UPDATE_COMMAND" ""
                    SOURCE_DIR          "/workspaces/isaac_ros-dev/build/nvblox_ros/_deps/ext_stdgpu-src"
                    BINARY_DIR          "/workspaces/isaac_ros-dev/build/nvblox_ros/_deps/ext_stdgpu-build"
                    CONFIGURE_COMMAND   ""
                    BUILD_COMMAND       ""
                    INSTALL_COMMAND     ""
                    TEST_COMMAND        ""
                    USES_TERMINAL_DOWNLOAD  YES
                    USES_TERMINAL_UPDATE    YES
)


