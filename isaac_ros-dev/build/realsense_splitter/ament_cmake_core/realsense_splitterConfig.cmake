# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_realsense_splitter_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED realsense_splitter_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(realsense_splitter_FOUND FALSE)
  elseif(NOT realsense_splitter_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(realsense_splitter_FOUND FALSE)
  endif()
  return()
endif()
set(_realsense_splitter_CONFIG_INCLUDED TRUE)

# output package information
if(NOT realsense_splitter_FIND_QUIETLY)
  message(STATUS "Found realsense_splitter: 3.0.1 (${realsense_splitter_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'realsense_splitter' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${realsense_splitter_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(realsense_splitter_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "ament_cmake_export_include_directories-extras.cmake;ament_cmake_export_libraries-extras.cmake;ament_cmake_export_targets-extras.cmake;ament_cmake_export_dependencies-extras.cmake")
foreach(_extra ${_extras})
  include("${realsense_splitter_DIR}/${_extra}")
endforeach()
