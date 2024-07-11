// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from isaac_ros_nova_interfaces:msg/EncoderTicks.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_NOVA_INTERFACES__MSG__DETAIL__ENCODER_TICKS__STRUCT_H_
#define ISAAC_ROS_NOVA_INTERFACES__MSG__DETAIL__ENCODER_TICKS__STRUCT_H_

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

/// Struct defined in msg/EncoderTicks in the package isaac_ros_nova_interfaces.
/**
  * Encoder Ticks
 */
typedef struct isaac_ros_nova_interfaces__msg__EncoderTicks
{
  std_msgs__msg__Header header;
  /// Ticks from the left wheel
  uint32_t left_ticks;
  /// Ticks from the right wheel
  uint32_t right_ticks;
  /// Timestamp from the encoder
  uint64_t encoder_timestamp;
} isaac_ros_nova_interfaces__msg__EncoderTicks;

// Struct for a sequence of isaac_ros_nova_interfaces__msg__EncoderTicks.
typedef struct isaac_ros_nova_interfaces__msg__EncoderTicks__Sequence
{
  isaac_ros_nova_interfaces__msg__EncoderTicks * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} isaac_ros_nova_interfaces__msg__EncoderTicks__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ISAAC_ROS_NOVA_INTERFACES__MSG__DETAIL__ENCODER_TICKS__STRUCT_H_
