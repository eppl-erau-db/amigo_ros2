// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from isaac_ros_nitros_bridge_interfaces:msg/NitrosBridgeImage.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_NITROS_BRIDGE_INTERFACES__MSG__DETAIL__NITROS_BRIDGE_IMAGE__STRUCT_H_
#define ISAAC_ROS_NITROS_BRIDGE_INTERFACES__MSG__DETAIL__NITROS_BRIDGE_IMAGE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'encoding'
#include "rosidl_runtime_c/string.h"
// Member 'data'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/NitrosBridgeImage in the package isaac_ros_nitros_bridge_interfaces.
typedef struct isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage
{
  std_msgs__msg__Header header;
  uint32_t height;
  uint32_t width;
  rosidl_runtime_c__String encoding;
  uint8_t is_bigendian;
  uint32_t step;
  /// Filled with PID and file descriptor(exported from GPU memory)
  rosidl_runtime_c__int32__Sequence data;
} isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage;

// Struct for a sequence of isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage.
typedef struct isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__Sequence
{
  isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ISAAC_ROS_NITROS_BRIDGE_INTERFACES__MSG__DETAIL__NITROS_BRIDGE_IMAGE__STRUCT_H_
