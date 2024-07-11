# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_nvblox_image_padding_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED nvblox_image_padding_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(nvblox_image_padding_FOUND FALSE)
  elseif(NOT nvblox_image_padding_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(nvblox_image_padding_FOUND FALSE)
  endif()
  return()
endif()
set(_nvblox_image_padding_CONFIG_INCLUDED TRUE)

# output package information
if(NOT nvblox_image_padding_FIND_QUIETLY)
  message(STATUS "Found nvblox_image_padding: 3.0.1 (${nvblox_image_padding_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'nvblox_image_padding' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${nvblox_image_padding_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(nvblox_image_padding_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "ament_cmake_export_include_directories-extras.cmake;ament_cmake_export_libraries-extras.cmake;ament_cmake_export_targets-extras.cmake;ament_cmake_export_dependencies-extras.cmake")
foreach(_extra ${_extras})
  include("${nvblox_image_padding_DIR}/${_extra}")
endforeach()
