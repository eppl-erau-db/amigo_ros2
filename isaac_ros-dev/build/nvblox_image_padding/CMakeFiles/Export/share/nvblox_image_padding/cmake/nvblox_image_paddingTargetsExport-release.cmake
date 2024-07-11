#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "nvblox_image_padding::nvblox_image_padding_lib" for configuration "Release"
set_property(TARGET nvblox_image_padding::nvblox_image_padding_lib APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(nvblox_image_padding::nvblox_image_padding_lib PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libnvblox_image_padding_lib.so"
  IMPORTED_SONAME_RELEASE "libnvblox_image_padding_lib.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS nvblox_image_padding::nvblox_image_padding_lib )
list(APPEND _IMPORT_CHECK_FILES_FOR_nvblox_image_padding::nvblox_image_padding_lib "${_IMPORT_PREFIX}/lib/libnvblox_image_padding_lib.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
