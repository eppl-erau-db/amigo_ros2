// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from unitree_go:msg/TimeSpec.idl
// generated code does not contain a copyright notice

#ifndef UNITREE_GO__MSG__DETAIL__TIME_SPEC__STRUCT_H_
#define UNITREE_GO__MSG__DETAIL__TIME_SPEC__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/TimeSpec in the package unitree_go.
/**
  * Time indicates a specific point in time, relative to a clock's 0 point.
  * The seconds component, valid over all int32 values.
 */
typedef struct unitree_go__msg__TimeSpec
{
  int32_t sec;
  /// The nanoseconds component, valid in the range [0, 10e9).
  uint32_t nanosec;
} unitree_go__msg__TimeSpec;

// Struct for a sequence of unitree_go__msg__TimeSpec.
typedef struct unitree_go__msg__TimeSpec__Sequence
{
  unitree_go__msg__TimeSpec * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} unitree_go__msg__TimeSpec__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // UNITREE_GO__MSG__DETAIL__TIME_SPEC__STRUCT_H_
