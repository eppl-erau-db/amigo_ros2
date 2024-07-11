include(CMakeFindDependencyMacro)

set(STDGPU_BACKEND_DIRECTORY "cuda")

# Backend-specific modules have higher priority than generic modules
list(PREPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}")
list(PREPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/${STDGPU_BACKEND_DIRECTORY}")


find_dependency(thrust 1.9.2 REQUIRED MODULE)


find_dependency(CUDAToolkit 10.0 REQUIRED MODULE)


list(POP_FRONT CMAKE_MODULE_PATH)
list(POP_FRONT CMAKE_MODULE_PATH)
