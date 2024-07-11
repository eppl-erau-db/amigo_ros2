// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from nvblox_msgs:msg/Index3D.idl
// generated code does not contain a copyright notice

#ifndef NVBLOX_MSGS__MSG__DETAIL__INDEX3_D__STRUCT_H_
#define NVBLOX_MSGS__MSG__DETAIL__INDEX3_D__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/Index3D in the package nvblox_msgs.
typedef struct nvblox_msgs__msg__Index3D
{
  int32_t x;
  int32_t y;
  int32_t z;
} nvblox_msgs__msg__Index3D;

// Struct for a sequence of nvblox_msgs__msg__Index3D.
typedef struct nvblox_msgs__msg__Index3D__Sequence
{
  nvblox_msgs__msg__Index3D * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} nvblox_msgs__msg__Index3D__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // NVBLOX_MSGS__MSG__DETAIL__INDEX3_D__STRUCT_H_
