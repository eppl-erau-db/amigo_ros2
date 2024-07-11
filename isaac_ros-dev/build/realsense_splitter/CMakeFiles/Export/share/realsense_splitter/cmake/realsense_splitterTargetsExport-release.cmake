#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "realsense_splitter::realsense_splitter_component" for configuration "Release"
set_property(TARGET realsense_splitter::realsense_splitter_component APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(realsense_splitter::realsense_splitter_component PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/librealsense_splitter_component.so"
  IMPORTED_SONAME_RELEASE "librealsense_splitter_component.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS realsense_splitter::realsense_splitter_component )
list(APPEND _IMPORT_CHECK_FILES_FOR_realsense_splitter::realsense_splitter_component "${_IMPORT_PREFIX}/lib/librealsense_splitter_component.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
