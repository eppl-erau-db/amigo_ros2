// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from realsense2_camera_msgs:msg/Metadata.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "realsense2_camera_msgs/msg/detail/metadata__rosidl_typesupport_introspection_c.h"
#include "realsense2_camera_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "realsense2_camera_msgs/msg/detail/metadata__functions.h"
#include "realsense2_camera_msgs/msg/detail/metadata__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `json_data`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void realsense2_camera_msgs__msg__Metadata__rosidl_typesupport_introspection_c__Metadata_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  realsense2_camera_msgs__msg__Metadata__init(message_memory);
}

void realsense2_camera_msgs__msg__Metadata__rosidl_typesupport_introspection_c__Metadata_fini_function(void * message_memory)
{
  realsense2_camera_msgs__msg__Metadata__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember realsense2_camera_msgs__msg__Metadata__rosidl_typesupport_introspection_c__Metadata_message_member_array[2] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(realsense2_camera_msgs__msg__Metadata, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "json_data",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(realsense2_camera_msgs__msg__Metadata, json_data),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers realsense2_camera_msgs__msg__Metadata__rosidl_typesupport_introspection_c__Metadata_message_members = {
  "realsense2_camera_msgs__msg",  // message namespace
  "Metadata",  // message name
  2,  // number of fields
  sizeof(realsense2_camera_msgs__msg__Metadata),
  realsense2_camera_msgs__msg__Metadata__rosidl_typesupport_introspection_c__Metadata_message_member_array,  // message members
  realsense2_camera_msgs__msg__Metadata__rosidl_typesupport_introspection_c__Metadata_init_function,  // function to initialize message memory (memory has to be allocated)
  realsense2_camera_msgs__msg__Metadata__rosidl_typesupport_introspection_c__Metadata_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t realsense2_camera_msgs__msg__Metadata__rosidl_typesupport_introspection_c__Metadata_message_type_support_handle = {
  0,
  &realsense2_camera_msgs__msg__Metadata__rosidl_typesupport_introspection_c__Metadata_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_realsense2_camera_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, realsense2_camera_msgs, msg, Metadata)() {
  realsense2_camera_msgs__msg__Metadata__rosidl_typesupport_introspection_c__Metadata_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  if (!realsense2_camera_msgs__msg__Metadata__rosidl_typesupport_introspection_c__Metadata_message_type_support_handle.typesupport_identifier) {
    realsense2_camera_msgs__msg__Metadata__rosidl_typesupport_introspection_c__Metadata_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &realsense2_camera_msgs__msg__Metadata__rosidl_typesupport_introspection_c__Metadata_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
