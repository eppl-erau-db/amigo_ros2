// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from nvblox_msgs:msg/Index3D.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "nvblox_msgs/msg/detail/index3_d__rosidl_typesupport_introspection_c.h"
#include "nvblox_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "nvblox_msgs/msg/detail/index3_d__functions.h"
#include "nvblox_msgs/msg/detail/index3_d__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void nvblox_msgs__msg__Index3D__rosidl_typesupport_introspection_c__Index3D_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  nvblox_msgs__msg__Index3D__init(message_memory);
}

void nvblox_msgs__msg__Index3D__rosidl_typesupport_introspection_c__Index3D_fini_function(void * message_memory)
{
  nvblox_msgs__msg__Index3D__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember nvblox_msgs__msg__Index3D__rosidl_typesupport_introspection_c__Index3D_message_member_array[3] = {
  {
    "x",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(nvblox_msgs__msg__Index3D, x),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "y",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(nvblox_msgs__msg__Index3D, y),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "z",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(nvblox_msgs__msg__Index3D, z),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers nvblox_msgs__msg__Index3D__rosidl_typesupport_introspection_c__Index3D_message_members = {
  "nvblox_msgs__msg",  // message namespace
  "Index3D",  // message name
  3,  // number of fields
  sizeof(nvblox_msgs__msg__Index3D),
  nvblox_msgs__msg__Index3D__rosidl_typesupport_introspection_c__Index3D_message_member_array,  // message members
  nvblox_msgs__msg__Index3D__rosidl_typesupport_introspection_c__Index3D_init_function,  // function to initialize message memory (memory has to be allocated)
  nvblox_msgs__msg__Index3D__rosidl_typesupport_introspection_c__Index3D_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t nvblox_msgs__msg__Index3D__rosidl_typesupport_introspection_c__Index3D_message_type_support_handle = {
  0,
  &nvblox_msgs__msg__Index3D__rosidl_typesupport_introspection_c__Index3D_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_nvblox_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, nvblox_msgs, msg, Index3D)() {
  if (!nvblox_msgs__msg__Index3D__rosidl_typesupport_introspection_c__Index3D_message_type_support_handle.typesupport_identifier) {
    nvblox_msgs__msg__Index3D__rosidl_typesupport_introspection_c__Index3D_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &nvblox_msgs__msg__Index3D__rosidl_typesupport_introspection_c__Index3D_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
