// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from isaac_ros_apriltag_interfaces:msg/AprilTagDetection.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "isaac_ros_apriltag_interfaces/msg/detail/april_tag_detection__rosidl_typesupport_introspection_c.h"
#include "isaac_ros_apriltag_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "isaac_ros_apriltag_interfaces/msg/detail/april_tag_detection__functions.h"
#include "isaac_ros_apriltag_interfaces/msg/detail/april_tag_detection__struct.h"


// Include directives for member types
// Member `family`
#include "rosidl_runtime_c/string_functions.h"
// Member `center`
// Member `corners`
#include "geometry_msgs/msg/point.h"
// Member `center`
// Member `corners`
#include "geometry_msgs/msg/detail/point__rosidl_typesupport_introspection_c.h"
// Member `pose`
#include "geometry_msgs/msg/pose_with_covariance_stamped.h"
// Member `pose`
#include "geometry_msgs/msg/detail/pose_with_covariance_stamped__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void isaac_ros_apriltag_interfaces__msg__AprilTagDetection__rosidl_typesupport_introspection_c__AprilTagDetection_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  isaac_ros_apriltag_interfaces__msg__AprilTagDetection__init(message_memory);
}

void isaac_ros_apriltag_interfaces__msg__AprilTagDetection__rosidl_typesupport_introspection_c__AprilTagDetection_fini_function(void * message_memory)
{
  isaac_ros_apriltag_interfaces__msg__AprilTagDetection__fini(message_memory);
}

size_t isaac_ros_apriltag_interfaces__msg__AprilTagDetection__rosidl_typesupport_introspection_c__size_function__AprilTagDetection__corners(
  const void * untyped_member)
{
  (void)untyped_member;
  return 4;
}

const void * isaac_ros_apriltag_interfaces__msg__AprilTagDetection__rosidl_typesupport_introspection_c__get_const_function__AprilTagDetection__corners(
  const void * untyped_member, size_t index)
{
  const geometry_msgs__msg__Point * member =
    (const geometry_msgs__msg__Point *)(untyped_member);
  return &member[index];
}

void * isaac_ros_apriltag_interfaces__msg__AprilTagDetection__rosidl_typesupport_introspection_c__get_function__AprilTagDetection__corners(
  void * untyped_member, size_t index)
{
  geometry_msgs__msg__Point * member =
    (geometry_msgs__msg__Point *)(untyped_member);
  return &member[index];
}

void isaac_ros_apriltag_interfaces__msg__AprilTagDetection__rosidl_typesupport_introspection_c__fetch_function__AprilTagDetection__corners(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const geometry_msgs__msg__Point * item =
    ((const geometry_msgs__msg__Point *)
    isaac_ros_apriltag_interfaces__msg__AprilTagDetection__rosidl_typesupport_introspection_c__get_const_function__AprilTagDetection__corners(untyped_member, index));
  geometry_msgs__msg__Point * value =
    (geometry_msgs__msg__Point *)(untyped_value);
  *value = *item;
}

void isaac_ros_apriltag_interfaces__msg__AprilTagDetection__rosidl_typesupport_introspection_c__assign_function__AprilTagDetection__corners(
  void * untyped_member, size_t index, const void * untyped_value)
{
  geometry_msgs__msg__Point * item =
    ((geometry_msgs__msg__Point *)
    isaac_ros_apriltag_interfaces__msg__AprilTagDetection__rosidl_typesupport_introspection_c__get_function__AprilTagDetection__corners(untyped_member, index));
  const geometry_msgs__msg__Point * value =
    (const geometry_msgs__msg__Point *)(untyped_value);
  *item = *value;
}

static rosidl_typesupport_introspection_c__MessageMember isaac_ros_apriltag_interfaces__msg__AprilTagDetection__rosidl_typesupport_introspection_c__AprilTagDetection_message_member_array[5] = {
  {
    "family",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(isaac_ros_apriltag_interfaces__msg__AprilTagDetection, family),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(isaac_ros_apriltag_interfaces__msg__AprilTagDetection, id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "center",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(isaac_ros_apriltag_interfaces__msg__AprilTagDetection, center),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "corners",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    4,  // array size
    false,  // is upper bound
    offsetof(isaac_ros_apriltag_interfaces__msg__AprilTagDetection, corners),  // bytes offset in struct
    NULL,  // default value
    isaac_ros_apriltag_interfaces__msg__AprilTagDetection__rosidl_typesupport_introspection_c__size_function__AprilTagDetection__corners,  // size() function pointer
    isaac_ros_apriltag_interfaces__msg__AprilTagDetection__rosidl_typesupport_introspection_c__get_const_function__AprilTagDetection__corners,  // get_const(index) function pointer
    isaac_ros_apriltag_interfaces__msg__AprilTagDetection__rosidl_typesupport_introspection_c__get_function__AprilTagDetection__corners,  // get(index) function pointer
    isaac_ros_apriltag_interfaces__msg__AprilTagDetection__rosidl_typesupport_introspection_c__fetch_function__AprilTagDetection__corners,  // fetch(index, &value) function pointer
    isaac_ros_apriltag_interfaces__msg__AprilTagDetection__rosidl_typesupport_introspection_c__assign_function__AprilTagDetection__corners,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "pose",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(isaac_ros_apriltag_interfaces__msg__AprilTagDetection, pose),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers isaac_ros_apriltag_interfaces__msg__AprilTagDetection__rosidl_typesupport_introspection_c__AprilTagDetection_message_members = {
  "isaac_ros_apriltag_interfaces__msg",  // message namespace
  "AprilTagDetection",  // message name
  5,  // number of fields
  sizeof(isaac_ros_apriltag_interfaces__msg__AprilTagDetection),
  isaac_ros_apriltag_interfaces__msg__AprilTagDetection__rosidl_typesupport_introspection_c__AprilTagDetection_message_member_array,  // message members
  isaac_ros_apriltag_interfaces__msg__AprilTagDetection__rosidl_typesupport_introspection_c__AprilTagDetection_init_function,  // function to initialize message memory (memory has to be allocated)
  isaac_ros_apriltag_interfaces__msg__AprilTagDetection__rosidl_typesupport_introspection_c__AprilTagDetection_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t isaac_ros_apriltag_interfaces__msg__AprilTagDetection__rosidl_typesupport_introspection_c__AprilTagDetection_message_type_support_handle = {
  0,
  &isaac_ros_apriltag_interfaces__msg__AprilTagDetection__rosidl_typesupport_introspection_c__AprilTagDetection_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_isaac_ros_apriltag_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, isaac_ros_apriltag_interfaces, msg, AprilTagDetection)() {
  isaac_ros_apriltag_interfaces__msg__AprilTagDetection__rosidl_typesupport_introspection_c__AprilTagDetection_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Point)();
  isaac_ros_apriltag_interfaces__msg__AprilTagDetection__rosidl_typesupport_introspection_c__AprilTagDetection_message_member_array[3].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Point)();
  isaac_ros_apriltag_interfaces__msg__AprilTagDetection__rosidl_typesupport_introspection_c__AprilTagDetection_message_member_array[4].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, PoseWithCovarianceStamped)();
  if (!isaac_ros_apriltag_interfaces__msg__AprilTagDetection__rosidl_typesupport_introspection_c__AprilTagDetection_message_type_support_handle.typesupport_identifier) {
    isaac_ros_apriltag_interfaces__msg__AprilTagDetection__rosidl_typesupport_introspection_c__AprilTagDetection_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &isaac_ros_apriltag_interfaces__msg__AprilTagDetection__rosidl_typesupport_introspection_c__AprilTagDetection_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
