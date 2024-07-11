// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from nvblox_msgs:msg/DistanceMapSlice.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "nvblox_msgs/msg/detail/distance_map_slice__rosidl_typesupport_introspection_c.h"
#include "nvblox_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "nvblox_msgs/msg/detail/distance_map_slice__functions.h"
#include "nvblox_msgs/msg/detail/distance_map_slice__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `origin`
#include "geometry_msgs/msg/point.h"
// Member `origin`
#include "geometry_msgs/msg/detail/point__rosidl_typesupport_introspection_c.h"
// Member `data`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void nvblox_msgs__msg__DistanceMapSlice__rosidl_typesupport_introspection_c__DistanceMapSlice_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  nvblox_msgs__msg__DistanceMapSlice__init(message_memory);
}

void nvblox_msgs__msg__DistanceMapSlice__rosidl_typesupport_introspection_c__DistanceMapSlice_fini_function(void * message_memory)
{
  nvblox_msgs__msg__DistanceMapSlice__fini(message_memory);
}

size_t nvblox_msgs__msg__DistanceMapSlice__rosidl_typesupport_introspection_c__size_function__DistanceMapSlice__data(
  const void * untyped_member)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return member->size;
}

const void * nvblox_msgs__msg__DistanceMapSlice__rosidl_typesupport_introspection_c__get_const_function__DistanceMapSlice__data(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void * nvblox_msgs__msg__DistanceMapSlice__rosidl_typesupport_introspection_c__get_function__DistanceMapSlice__data(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void nvblox_msgs__msg__DistanceMapSlice__rosidl_typesupport_introspection_c__fetch_function__DistanceMapSlice__data(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    nvblox_msgs__msg__DistanceMapSlice__rosidl_typesupport_introspection_c__get_const_function__DistanceMapSlice__data(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void nvblox_msgs__msg__DistanceMapSlice__rosidl_typesupport_introspection_c__assign_function__DistanceMapSlice__data(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    nvblox_msgs__msg__DistanceMapSlice__rosidl_typesupport_introspection_c__get_function__DistanceMapSlice__data(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

bool nvblox_msgs__msg__DistanceMapSlice__rosidl_typesupport_introspection_c__resize_function__DistanceMapSlice__data(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  rosidl_runtime_c__float__Sequence__fini(member);
  return rosidl_runtime_c__float__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember nvblox_msgs__msg__DistanceMapSlice__rosidl_typesupport_introspection_c__DistanceMapSlice_message_member_array[7] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(nvblox_msgs__msg__DistanceMapSlice, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "resolution",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(nvblox_msgs__msg__DistanceMapSlice, resolution),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "width",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(nvblox_msgs__msg__DistanceMapSlice, width),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "height",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(nvblox_msgs__msg__DistanceMapSlice, height),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "origin",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(nvblox_msgs__msg__DistanceMapSlice, origin),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "unknown_value",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(nvblox_msgs__msg__DistanceMapSlice, unknown_value),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "data",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(nvblox_msgs__msg__DistanceMapSlice, data),  // bytes offset in struct
    NULL,  // default value
    nvblox_msgs__msg__DistanceMapSlice__rosidl_typesupport_introspection_c__size_function__DistanceMapSlice__data,  // size() function pointer
    nvblox_msgs__msg__DistanceMapSlice__rosidl_typesupport_introspection_c__get_const_function__DistanceMapSlice__data,  // get_const(index) function pointer
    nvblox_msgs__msg__DistanceMapSlice__rosidl_typesupport_introspection_c__get_function__DistanceMapSlice__data,  // get(index) function pointer
    nvblox_msgs__msg__DistanceMapSlice__rosidl_typesupport_introspection_c__fetch_function__DistanceMapSlice__data,  // fetch(index, &value) function pointer
    nvblox_msgs__msg__DistanceMapSlice__rosidl_typesupport_introspection_c__assign_function__DistanceMapSlice__data,  // assign(index, value) function pointer
    nvblox_msgs__msg__DistanceMapSlice__rosidl_typesupport_introspection_c__resize_function__DistanceMapSlice__data  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers nvblox_msgs__msg__DistanceMapSlice__rosidl_typesupport_introspection_c__DistanceMapSlice_message_members = {
  "nvblox_msgs__msg",  // message namespace
  "DistanceMapSlice",  // message name
  7,  // number of fields
  sizeof(nvblox_msgs__msg__DistanceMapSlice),
  nvblox_msgs__msg__DistanceMapSlice__rosidl_typesupport_introspection_c__DistanceMapSlice_message_member_array,  // message members
  nvblox_msgs__msg__DistanceMapSlice__rosidl_typesupport_introspection_c__DistanceMapSlice_init_function,  // function to initialize message memory (memory has to be allocated)
  nvblox_msgs__msg__DistanceMapSlice__rosidl_typesupport_introspection_c__DistanceMapSlice_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t nvblox_msgs__msg__DistanceMapSlice__rosidl_typesupport_introspection_c__DistanceMapSlice_message_type_support_handle = {
  0,
  &nvblox_msgs__msg__DistanceMapSlice__rosidl_typesupport_introspection_c__DistanceMapSlice_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_nvblox_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, nvblox_msgs, msg, DistanceMapSlice)() {
  nvblox_msgs__msg__DistanceMapSlice__rosidl_typesupport_introspection_c__DistanceMapSlice_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  nvblox_msgs__msg__DistanceMapSlice__rosidl_typesupport_introspection_c__DistanceMapSlice_message_member_array[4].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Point)();
  if (!nvblox_msgs__msg__DistanceMapSlice__rosidl_typesupport_introspection_c__DistanceMapSlice_message_type_support_handle.typesupport_identifier) {
    nvblox_msgs__msg__DistanceMapSlice__rosidl_typesupport_introspection_c__DistanceMapSlice_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &nvblox_msgs__msg__DistanceMapSlice__rosidl_typesupport_introspection_c__DistanceMapSlice_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
