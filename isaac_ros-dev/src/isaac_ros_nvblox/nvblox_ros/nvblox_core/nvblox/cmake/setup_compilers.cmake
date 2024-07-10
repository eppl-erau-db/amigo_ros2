# ##############################################################################
# Handle user options
# ##############################################################################

# If GPU architectures are not explicitly set, cmake will detect the architecture of the build
# computer and compiles for that architecture only. This can be overridden by setting the
# CMAKE_CUDA_ARCHITECTURES variable to a semicolon-separated list of architectures to support, example
# cmake .. '-DCMAKE_CUDA_ARCHITECTURES=75;72'
include("${CMAKE_CURRENT_LIST_DIR}/cuda/setup_compute_capability.cmake")

# This option avoids any implementations using std::string in their signature in
# header files Useful for Nvblox PyTorch wrapper, which requires the old
# Pre-CXX11 ABI
option(PRE_CXX11_ABI_LINKABLE "Better support pre-C++11 ABI library users" OFF)

# Treat warnings as errors on an opt-in basis. This flag should be enabled in CI
# and is also recommended for developers. Reason for opt-in is to avoid
# nuisances for users with compilers different from the one the lib was tested
# on.
option(WARNING_AS_ERROR "Treat compiler warnings as errors")

option(USE_SANITIZER "Enable gcc sanitizer")


# Set default build type if not provided by user
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE
      "RelWithDebInfo"
      CACHE
        STRING
        "Choose the type of build, options are: None Debug Release RelWithDebInfo"
        FORCE)
endif(NOT CMAKE_BUILD_TYPE)

# ##############################################################################
# Specify the C++ standard and general options
# ##############################################################################
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# This link flag replaces "runpath" with "rpath" in executables and shared
# objects. This is important because it means the search paths are passed down
# the shared object tree.
# https://stackoverflow.com/questions/58997230/cmake-project-fails-to-find-shared-library
set(nvblox_link_options "-Wl,--disable-new-dtags")

# Cmake -fPIC flag.
# NOTE(alexmillane): I needed to add this when I changed to linking against a
# static version of stdgpu. Without is we get an error from thrust/cub linking.
set(CMAKE_POSITION_INDEPENDENT_CODE TRUE)

# ##############################################################################
# Setup compiler definitions
# ##############################################################################
add_compile_definitions(
  "$<$<BOOL:${PRE_CXX11_ABI_LINKABLE}>:PRE_CXX11_ABI_LINKABLE>")

# Change namespace cub:: into nvblox::cub. This is to avoid conflicts when other modules calls non
# thread safe functions in the cub namespace. Appending nvblox:: ensures an unique symbol that is
# only accesed by this library.
add_compile_definitions(CUB_WRAPPED_NAMESPACE=nvblox)

# ##############################################################################
# Setup c++ compiler flags
# ##############################################################################

# The common flags are used for both g++ and nvcc when compiling host code
set(CXX_FLAGS_COMMON
   # Enable more warnings
   "-Wall"
   "-Wextra"
   "-Wshadow"
   # Facilitate stack-trace debugging
   "-fno-omit-frame-pointer")

if (USE_SANITIZER)
  set(CXX_FLAGS_COMMON "${CXX_FLAGS_COMMON}" "-fsanitize=address")
  set(nvblox_link_options "${nvblox_link_options}" "-fsanitize=address")
endif(USE_SANITIZER)

set(CXX_FLAGS_DEBUG "${CXX_FLAGS_COMMON}" "-O0")
set(CXX_FLAGS_RELWITHDEBINFO "${CXX_FLAGS_COMMON}" "-O2" "-g")
set(CXX_FLAGS_RELEASE "${CXX_FLAGS_COMMON}" "-O3" "-DNDEBUG")

add_compile_options(
  "$<$<AND:$<COMPILE_LANGUAGE:CXX>,$<BOOL:${WARNING_AS_ERROR}>>:-Werror>")
add_compile_options(
  "$<$<AND:$<COMPILE_LANGUAGE:CXX>,$<CONFIG:Debug>>:${CXX_FLAGS_DEBUG}>")
add_compile_options(
  "$<$<AND:$<COMPILE_LANGUAGE:CXX>,$<CONFIG:RelWithDebInfo>>:${CXX_FLAGS_RELWITHDEBINFO}>"
)
add_compile_options(
  "$<$<AND:$<COMPILE_LANGUAGE:CXX>,$<CONFIG:Release>>:${CXX_FLAGS_RELEASE}>")

# When nvcc passes args to the native c++ compiler, it requires a comma
# separated list.
string(REPLACE ";" "," CXX_FLAGS_COMMON_COMMA_SEPARATED "${CXX_FLAGS_COMMON}")

set(CUDA_FLAGS_COMMON
    "${CMAKE_CUDA_FLAGS}"
    # Allow __host__, __device__ annotations in lambda declarations
    "--extended-lambda"
    # Allows sharing constexpr between host and device code
    "--expt-relaxed-constexpr"
    # Display warning numbers
    "-Xcudafe=--display_error_number"
    # Increased visibility of symbols
    "-Xcompiler=${CXX_FLAGS_COMMON_COMMA_SEPARATED}"
    # Suppress "dynamic initialization is not supported for a function-scope static __shared__
    # variable within a __device__/__global__ function". We cannot call the constructor in these
    # cases due to race condition. To my understanding, the variables are left un-constructed which
    # is still OK for our use case.
    "--diag-suppress=20054"
    # Suppress "a __constant__ variable cannot be directly read in a host function". We share
    # __constant__ between host and device in the marching cubes implementation.
    "--diag-suppress=20091"
  )

set(CUDA_FLAGS_DEBUG "--debug" "--device-debug" "-O0")
set(CUDA_FLAGS_RELWITHDEBINFO "-O2" "--debug" "--generate-line-info")
set(CUDA_FLAGS_RELEASE "-O3" "-DNDEBUG")

# Flags added for all builds
add_compile_options(
  "$<$<COMPILE_LANGUAGE:CUDA>:${CUDA_FLAGS_COMMON}>")

# Flags appended for special build types
add_compile_options(
  "$<$<AND:$<COMPILE_LANGUAGE:CUDA>,$<BOOL:${WARNING_AS_ERROR}>>:-Xcompiler=-Werror>")
add_compile_options(
  "$<$<AND:$<COMPILE_LANGUAGE:CUDA>,$<CONFIG:Debug>>:${CUDA_FLAGS_DEBUG}>")
add_compile_options(
  "$<$<AND:$<COMPILE_LANGUAGE:CUDA>,$<CONFIG:RelWithDebInfo>>:${CUDA_FLAGS_RELWITHDEBINFO}>")
add_compile_options(
  "$<$<AND:$<COMPILE_LANGUAGE:CUDA>,$<CONFIG:Release>>:${CUDA_FLAGS_RELEASE}>")
