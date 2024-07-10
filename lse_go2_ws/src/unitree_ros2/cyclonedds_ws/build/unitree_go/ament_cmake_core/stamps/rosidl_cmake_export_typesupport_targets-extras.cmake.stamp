# generated from
# rosidl_cmake/cmake/template/rosidl_cmake_export_typesupport_targets.cmake.in

set(_exported_typesupport_targets
  "__rosidl_generator_c:unitree_go__rosidl_generator_c;__rosidl_typesupport_fastrtps_c:unitree_go__rosidl_typesupport_fastrtps_c;__rosidl_generator_cpp:unitree_go__rosidl_generator_cpp;__rosidl_typesupport_fastrtps_cpp:unitree_go__rosidl_typesupport_fastrtps_cpp;__rosidl_typesupport_introspection_c:unitree_go__rosidl_typesupport_introspection_c;__rosidl_typesupport_c:unitree_go__rosidl_typesupport_c;__rosidl_typesupport_introspection_cpp:unitree_go__rosidl_typesupport_introspection_cpp;__rosidl_typesupport_cpp:unitree_go__rosidl_typesupport_cpp;__rosidl_generator_py:unitree_go__rosidl_generator_py")

# populate unitree_go_TARGETS_<suffix>
if(NOT _exported_typesupport_targets STREQUAL "")
  # loop over typesupport targets
  foreach(_tuple ${_exported_typesupport_targets})
    string(REPLACE ":" ";" _tuple "${_tuple}")
    list(GET _tuple 0 _suffix)
    list(GET _tuple 1 _target)

    set(_target "unitree_go::${_target}")
    if(NOT TARGET "${_target}")
      # the exported target must exist
      message(WARNING "Package 'unitree_go' exports the typesupport target '${_target}' which doesn't exist")
    else()
      list(APPEND unitree_go_TARGETS${_suffix} "${_target}")
    endif()
  endforeach()
endif()
