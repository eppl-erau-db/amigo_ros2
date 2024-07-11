#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "nvblox_rviz_plugin::nvblox_rviz_plugin" for configuration "Release"
set_property(TARGET nvblox_rviz_plugin::nvblox_rviz_plugin APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(nvblox_rviz_plugin::nvblox_rviz_plugin PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libnvblox_rviz_plugin.so"
  IMPORTED_SONAME_RELEASE "libnvblox_rviz_plugin.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS nvblox_rviz_plugin::nvblox_rviz_plugin )
list(APPEND _IMPORT_CHECK_FILES_FOR_nvblox_rviz_plugin::nvblox_rviz_plugin "${_IMPORT_PREFIX}/lib/libnvblox_rviz_plugin.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
