
if(NOT "/workspaces/isaac_ros-dev/build/nvblox_ros/_deps/ext_stdgpu-subbuild/stdgpu/src/ext_stdgpu-populate-stamp/ext_stdgpu-populate-gitinfo.txt" IS_NEWER_THAN "/workspaces/isaac_ros-dev/build/nvblox_ros/_deps/ext_stdgpu-subbuild/stdgpu/src/ext_stdgpu-populate-stamp/ext_stdgpu-populate-gitclone-lastrun.txt")
  message(STATUS "Avoiding repeated git clone, stamp file is up to date: '/workspaces/isaac_ros-dev/build/nvblox_ros/_deps/ext_stdgpu-subbuild/stdgpu/src/ext_stdgpu-populate-stamp/ext_stdgpu-populate-gitclone-lastrun.txt'")
  return()
endif()

execute_process(
  COMMAND ${CMAKE_COMMAND} -E rm -rf "/workspaces/isaac_ros-dev/build/nvblox_ros/_deps/ext_stdgpu-src"
  RESULT_VARIABLE error_code
  )
if(error_code)
  message(FATAL_ERROR "Failed to remove directory: '/workspaces/isaac_ros-dev/build/nvblox_ros/_deps/ext_stdgpu-src'")
endif()

# try the clone 3 times in case there is an odd git clone issue
set(error_code 1)
set(number_of_tries 0)
while(error_code AND number_of_tries LESS 3)
  execute_process(
    COMMAND "/usr/bin/git"  clone --no-checkout --config "advice.detachedHead=false" "https://github.com/stotko/stdgpu.git" "ext_stdgpu-src"
    WORKING_DIRECTORY "/workspaces/isaac_ros-dev/build/nvblox_ros/_deps"
    RESULT_VARIABLE error_code
    )
  math(EXPR number_of_tries "${number_of_tries} + 1")
endwhile()
if(number_of_tries GREATER 1)
  message(STATUS "Had to git clone more than once:
          ${number_of_tries} times.")
endif()
if(error_code)
  message(FATAL_ERROR "Failed to clone repository: 'https://github.com/stotko/stdgpu.git'")
endif()

execute_process(
  COMMAND "/usr/bin/git"  checkout e10f6f3ccc9902d693af4380c3bcd188ec34a2e6 --
  WORKING_DIRECTORY "/workspaces/isaac_ros-dev/build/nvblox_ros/_deps/ext_stdgpu-src"
  RESULT_VARIABLE error_code
  )
if(error_code)
  message(FATAL_ERROR "Failed to checkout tag: 'e10f6f3ccc9902d693af4380c3bcd188ec34a2e6'")
endif()

set(init_submodules TRUE)
if(init_submodules)
  execute_process(
    COMMAND "/usr/bin/git"  submodule update --recursive --init 
    WORKING_DIRECTORY "/workspaces/isaac_ros-dev/build/nvblox_ros/_deps/ext_stdgpu-src"
    RESULT_VARIABLE error_code
    )
endif()
if(error_code)
  message(FATAL_ERROR "Failed to update submodules in: '/workspaces/isaac_ros-dev/build/nvblox_ros/_deps/ext_stdgpu-src'")
endif()

# Complete success, update the script-last-run stamp file:
#
execute_process(
  COMMAND ${CMAKE_COMMAND} -E copy
    "/workspaces/isaac_ros-dev/build/nvblox_ros/_deps/ext_stdgpu-subbuild/stdgpu/src/ext_stdgpu-populate-stamp/ext_stdgpu-populate-gitinfo.txt"
    "/workspaces/isaac_ros-dev/build/nvblox_ros/_deps/ext_stdgpu-subbuild/stdgpu/src/ext_stdgpu-populate-stamp/ext_stdgpu-populate-gitclone-lastrun.txt"
  RESULT_VARIABLE error_code
  )
if(error_code)
  message(FATAL_ERROR "Failed to copy script-last-run stamp file: '/workspaces/isaac_ros-dev/build/nvblox_ros/_deps/ext_stdgpu-subbuild/stdgpu/src/ext_stdgpu-populate-stamp/ext_stdgpu-populate-gitclone-lastrun.txt'")
endif()

