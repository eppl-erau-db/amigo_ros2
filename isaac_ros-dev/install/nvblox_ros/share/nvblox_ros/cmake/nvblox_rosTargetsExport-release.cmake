#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "nvblox_ros::nvblox_ros_lib" for configuration "Release"
set_property(TARGET nvblox_ros::nvblox_ros_lib APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(nvblox_ros::nvblox_ros_lib PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libnvblox_ros_lib.so"
  IMPORTED_SONAME_RELEASE "libnvblox_ros_lib.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS nvblox_ros::nvblox_ros_lib )
list(APPEND _IMPORT_CHECK_FILES_FOR_nvblox_ros::nvblox_ros_lib "${_IMPORT_PREFIX}/lib/libnvblox_ros_lib.so" )

# Import target "nvblox_ros::nvblox_lib" for configuration "Release"
set_property(TARGET nvblox_ros::nvblox_lib APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(nvblox_ros::nvblox_lib PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libnvblox_lib.so"
  IMPORTED_SONAME_RELEASE "libnvblox_lib.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS nvblox_ros::nvblox_lib )
list(APPEND _IMPORT_CHECK_FILES_FOR_nvblox_ros::nvblox_lib "${_IMPORT_PREFIX}/lib/libnvblox_lib.so" )

# Import target "nvblox_ros::nvblox_gpu_hash" for configuration "Release"
set_property(TARGET nvblox_ros::nvblox_gpu_hash APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(nvblox_ros::nvblox_gpu_hash PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CUDA;CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libnvblox_gpu_hash.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS nvblox_ros::nvblox_gpu_hash )
list(APPEND _IMPORT_CHECK_FILES_FOR_nvblox_ros::nvblox_gpu_hash "${_IMPORT_PREFIX}/lib/libnvblox_gpu_hash.a" )

# Import target "nvblox_ros::stdgpu" for configuration "Release"
set_property(TARGET nvblox_ros::stdgpu APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(nvblox_ros::stdgpu PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libstdgpu.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS nvblox_ros::stdgpu )
list(APPEND _IMPORT_CHECK_FILES_FOR_nvblox_ros::stdgpu "${_IMPORT_PREFIX}/lib/libstdgpu.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
