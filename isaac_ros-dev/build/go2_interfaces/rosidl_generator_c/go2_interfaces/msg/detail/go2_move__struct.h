// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from go2_interfaces:msg/Go2Move.idl
// generated code does not contain a copyright notice

#ifndef GO2_INTERFACES__MSG__DETAIL__GO2_MOVE__STRUCT_H_
#define GO2_INTERFACES__MSG__DETAIL__GO2_MOVE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/Go2Move in the package go2_interfaces.
typedef struct go2_interfaces__msg__Go2Move
{
  float x;
  float y;
  float z;
} go2_interfaces__msg__Go2Move;

// Struct for a sequence of go2_interfaces__msg__Go2Move.
typedef struct go2_interfaces__msg__Go2Move__Sequence
{
  go2_interfaces__msg__Go2Move * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} go2_interfaces__msg__Go2Move__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // GO2_INTERFACES__MSG__DETAIL__GO2_MOVE__STRUCT_H_
