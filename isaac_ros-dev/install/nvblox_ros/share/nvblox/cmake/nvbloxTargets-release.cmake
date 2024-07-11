#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "nvblox::nvblox_lib" for configuration "Release"
set_property(TARGET nvblox::nvblox_lib APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(nvblox::nvblox_lib PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libnvblox_lib.so"
  IMPORTED_SONAME_RELEASE "libnvblox_lib.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS nvblox::nvblox_lib )
list(APPEND _IMPORT_CHECK_FILES_FOR_nvblox::nvblox_lib "${_IMPORT_PREFIX}/lib/libnvblox_lib.so" )

# Import target "nvblox::nvblox_gpu_hash" for configuration "Release"
set_property(TARGET nvblox::nvblox_gpu_hash APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(nvblox::nvblox_gpu_hash PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CUDA;CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/nvblox/libnvblox_gpu_hash.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS nvblox::nvblox_gpu_hash )
list(APPEND _IMPORT_CHECK_FILES_FOR_nvblox::nvblox_gpu_hash "${_IMPORT_PREFIX}/lib/nvblox/libnvblox_gpu_hash.a" )

# Import target "nvblox::nvblox_datasets" for configuration "Release"
set_property(TARGET nvblox::nvblox_datasets APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(nvblox::nvblox_datasets PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libnvblox_datasets.so"
  IMPORTED_SONAME_RELEASE "libnvblox_datasets.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS nvblox::nvblox_datasets )
list(APPEND _IMPORT_CHECK_FILES_FOR_nvblox::nvblox_datasets "${_IMPORT_PREFIX}/lib/libnvblox_datasets.so" )

# Import target "nvblox::stdgpu" for configuration "Release"
set_property(TARGET nvblox::stdgpu APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(nvblox::stdgpu PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/nvblox/libstdgpu.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS nvblox::stdgpu )
list(APPEND _IMPORT_CHECK_FILES_FOR_nvblox::stdgpu "${_IMPORT_PREFIX}/lib/nvblox/libstdgpu.a" )

# Import target "nvblox::fuse_3dmatch" for configuration "Release"
set_property(TARGET nvblox::fuse_3dmatch APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(nvblox::fuse_3dmatch PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/nvblox/fuse_3dmatch"
  )

list(APPEND _IMPORT_CHECK_TARGETS nvblox::fuse_3dmatch )
list(APPEND _IMPORT_CHECK_FILES_FOR_nvblox::fuse_3dmatch "${_IMPORT_PREFIX}/bin/nvblox/fuse_3dmatch" )

# Import target "nvblox::fuse_replica" for configuration "Release"
set_property(TARGET nvblox::fuse_replica APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(nvblox::fuse_replica PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/nvblox/fuse_replica"
  )

list(APPEND _IMPORT_CHECK_TARGETS nvblox::fuse_replica )
list(APPEND _IMPORT_CHECK_FILES_FOR_nvblox::fuse_replica "${_IMPORT_PREFIX}/bin/nvblox/fuse_replica" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
