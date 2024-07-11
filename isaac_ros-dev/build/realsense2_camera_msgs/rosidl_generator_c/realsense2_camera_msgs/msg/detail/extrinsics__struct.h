// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from realsense2_camera_msgs:msg/Extrinsics.idl
// generated code does not contain a copyright notice

#ifndef REALSENSE2_CAMERA_MSGS__MSG__DETAIL__EXTRINSICS__STRUCT_H_
#define REALSENSE2_CAMERA_MSGS__MSG__DETAIL__EXTRINSICS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/Extrinsics in the package realsense2_camera_msgs.
typedef struct realsense2_camera_msgs__msg__Extrinsics
{
  double rotation[9];
  double translation[3];
} realsense2_camera_msgs__msg__Extrinsics;

// Struct for a sequence of realsense2_camera_msgs__msg__Extrinsics.
typedef struct realsense2_camera_msgs__msg__Extrinsics__Sequence
{
  realsense2_camera_msgs__msg__Extrinsics * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} realsense2_camera_msgs__msg__Extrinsics__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // REALSENSE2_CAMERA_MSGS__MSG__DETAIL__EXTRINSICS__STRUCT_H_
