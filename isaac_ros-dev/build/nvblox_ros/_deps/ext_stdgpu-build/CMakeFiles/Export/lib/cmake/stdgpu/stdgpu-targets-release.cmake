#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "stdgpu::stdgpu" for configuration "Release"
set_property(TARGET stdgpu::stdgpu APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(stdgpu::stdgpu PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libstdgpu.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS stdgpu::stdgpu )
list(APPEND _IMPORT_CHECK_FILES_FOR_stdgpu::stdgpu "${_IMPORT_PREFIX}/lib/libstdgpu.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
