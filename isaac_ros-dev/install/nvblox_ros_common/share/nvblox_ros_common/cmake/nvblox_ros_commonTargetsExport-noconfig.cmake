#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "nvblox_ros_common::nvblox_ros_common_lib" for configuration ""
set_property(TARGET nvblox_ros_common::nvblox_ros_common_lib APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(nvblox_ros_common::nvblox_ros_common_lib PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libnvblox_ros_common_lib.so"
  IMPORTED_SONAME_NOCONFIG "libnvblox_ros_common_lib.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS nvblox_ros_common::nvblox_ros_common_lib )
list(APPEND _IMPORT_CHECK_FILES_FOR_nvblox_ros_common::nvblox_ros_common_lib "${_IMPORT_PREFIX}/lib/libnvblox_ros_common_lib.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
