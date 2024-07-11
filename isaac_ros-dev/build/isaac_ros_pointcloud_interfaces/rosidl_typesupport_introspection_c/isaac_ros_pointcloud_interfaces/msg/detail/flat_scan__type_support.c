// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from isaac_ros_pointcloud_interfaces:msg/FlatScan.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "isaac_ros_pointcloud_interfaces/msg/detail/flat_scan__rosidl_typesupport_introspection_c.h"
#include "isaac_ros_pointcloud_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "isaac_ros_pointcloud_interfaces/msg/detail/flat_scan__functions.h"
#include "isaac_ros_pointcloud_interfaces/msg/detail/flat_scan__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `angles`
// Member `ranges`
// Member `intensities`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__FlatScan_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  isaac_ros_pointcloud_interfaces__msg__FlatScan__init(message_memory);
}

void isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__FlatScan_fini_function(void * message_memory)
{
  isaac_ros_pointcloud_interfaces__msg__FlatScan__fini(message_memory);
}

size_t isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__size_function__FlatScan__angles(
  const void * untyped_member)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return member->size;
}

const void * isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__get_const_function__FlatScan__angles(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void * isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__get_function__FlatScan__angles(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__fetch_function__FlatScan__angles(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__get_const_function__FlatScan__angles(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__assign_function__FlatScan__angles(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__get_function__FlatScan__angles(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

bool isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__resize_function__FlatScan__angles(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  rosidl_runtime_c__float__Sequence__fini(member);
  return rosidl_runtime_c__float__Sequence__init(member, size);
}

size_t isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__size_function__FlatScan__ranges(
  const void * untyped_member)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return member->size;
}

const void * isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__get_const_function__FlatScan__ranges(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void * isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__get_function__FlatScan__ranges(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__fetch_function__FlatScan__ranges(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__get_const_function__FlatScan__ranges(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__assign_function__FlatScan__ranges(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__get_function__FlatScan__ranges(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

bool isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__resize_function__FlatScan__ranges(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  rosidl_runtime_c__float__Sequence__fini(member);
  return rosidl_runtime_c__float__Sequence__init(member, size);
}

size_t isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__size_function__FlatScan__intensities(
  const void * untyped_member)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return member->size;
}

const void * isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__get_const_function__FlatScan__intensities(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void * isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__get_function__FlatScan__intensities(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__fetch_function__FlatScan__intensities(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__get_const_function__FlatScan__intensities(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__assign_function__FlatScan__intensities(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__get_function__FlatScan__intensities(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

bool isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__resize_function__FlatScan__intensities(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  rosidl_runtime_c__float__Sequence__fini(member);
  return rosidl_runtime_c__float__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__FlatScan_message_member_array[6] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(isaac_ros_pointcloud_interfaces__msg__FlatScan, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "range_min",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(isaac_ros_pointcloud_interfaces__msg__FlatScan, range_min),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "range_max",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(isaac_ros_pointcloud_interfaces__msg__FlatScan, range_max),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "angles",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(isaac_ros_pointcloud_interfaces__msg__FlatScan, angles),  // bytes offset in struct
    NULL,  // default value
    isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__size_function__FlatScan__angles,  // size() function pointer
    isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__get_const_function__FlatScan__angles,  // get_const(index) function pointer
    isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__get_function__FlatScan__angles,  // get(index) function pointer
    isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__fetch_function__FlatScan__angles,  // fetch(index, &value) function pointer
    isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__assign_function__FlatScan__angles,  // assign(index, value) function pointer
    isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__resize_function__FlatScan__angles  // resize(index) function pointer
  },
  {
    "ranges",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(isaac_ros_pointcloud_interfaces__msg__FlatScan, ranges),  // bytes offset in struct
    NULL,  // default value
    isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__size_function__FlatScan__ranges,  // size() function pointer
    isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__get_const_function__FlatScan__ranges,  // get_const(index) function pointer
    isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__get_function__FlatScan__ranges,  // get(index) function pointer
    isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__fetch_function__FlatScan__ranges,  // fetch(index, &value) function pointer
    isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__assign_function__FlatScan__ranges,  // assign(index, value) function pointer
    isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__resize_function__FlatScan__ranges  // resize(index) function pointer
  },
  {
    "intensities",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(isaac_ros_pointcloud_interfaces__msg__FlatScan, intensities),  // bytes offset in struct
    NULL,  // default value
    isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__size_function__FlatScan__intensities,  // size() function pointer
    isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__get_const_function__FlatScan__intensities,  // get_const(index) function pointer
    isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__get_function__FlatScan__intensities,  // get(index) function pointer
    isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__fetch_function__FlatScan__intensities,  // fetch(index, &value) function pointer
    isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__assign_function__FlatScan__intensities,  // assign(index, value) function pointer
    isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__resize_function__FlatScan__intensities  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__FlatScan_message_members = {
  "isaac_ros_pointcloud_interfaces__msg",  // message namespace
  "FlatScan",  // message name
  6,  // number of fields
  sizeof(isaac_ros_pointcloud_interfaces__msg__FlatScan),
  isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__FlatScan_message_member_array,  // message members
  isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__FlatScan_init_function,  // function to initialize message memory (memory has to be allocated)
  isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__FlatScan_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__FlatScan_message_type_support_handle = {
  0,
  &isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__FlatScan_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_isaac_ros_pointcloud_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, isaac_ros_pointcloud_interfaces, msg, FlatScan)() {
  isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__FlatScan_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  if (!isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__FlatScan_message_type_support_handle.typesupport_identifier) {
    isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__FlatScan_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &isaac_ros_pointcloud_interfaces__msg__FlatScan__rosidl_typesupport_introspection_c__FlatScan_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
