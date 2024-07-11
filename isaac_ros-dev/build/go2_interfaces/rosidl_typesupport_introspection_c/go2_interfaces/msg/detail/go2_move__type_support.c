// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from go2_interfaces:msg/Go2Move.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "go2_interfaces/msg/detail/go2_move__rosidl_typesupport_introspection_c.h"
#include "go2_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "go2_interfaces/msg/detail/go2_move__functions.h"
#include "go2_interfaces/msg/detail/go2_move__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void go2_interfaces__msg__Go2Move__rosidl_typesupport_introspection_c__Go2Move_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  go2_interfaces__msg__Go2Move__init(message_memory);
}

void go2_interfaces__msg__Go2Move__rosidl_typesupport_introspection_c__Go2Move_fini_function(void * message_memory)
{
  go2_interfaces__msg__Go2Move__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember go2_interfaces__msg__Go2Move__rosidl_typesupport_introspection_c__Go2Move_message_member_array[3] = {
  {
    "x",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(go2_interfaces__msg__Go2Move, x),  // bytes offset in struct
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
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(go2_interfaces__msg__Go2Move, y),  // bytes offset in struct
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
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(go2_interfaces__msg__Go2Move, z),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers go2_interfaces__msg__Go2Move__rosidl_typesupport_introspection_c__Go2Move_message_members = {
  "go2_interfaces__msg",  // message namespace
  "Go2Move",  // message name
  3,  // number of fields
  sizeof(go2_interfaces__msg__Go2Move),
  go2_interfaces__msg__Go2Move__rosidl_typesupport_introspection_c__Go2Move_message_member_array,  // message members
  go2_interfaces__msg__Go2Move__rosidl_typesupport_introspection_c__Go2Move_init_function,  // function to initialize message memory (memory has to be allocated)
  go2_interfaces__msg__Go2Move__rosidl_typesupport_introspection_c__Go2Move_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t go2_interfaces__msg__Go2Move__rosidl_typesupport_introspection_c__Go2Move_message_type_support_handle = {
  0,
  &go2_interfaces__msg__Go2Move__rosidl_typesupport_introspection_c__Go2Move_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_go2_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, go2_interfaces, msg, Go2Move)() {
  if (!go2_interfaces__msg__Go2Move__rosidl_typesupport_introspection_c__Go2Move_message_type_support_handle.typesupport_identifier) {
    go2_interfaces__msg__Go2Move__rosidl_typesupport_introspection_c__Go2Move_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &go2_interfaces__msg__Go2Move__rosidl_typesupport_introspection_c__Go2Move_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
