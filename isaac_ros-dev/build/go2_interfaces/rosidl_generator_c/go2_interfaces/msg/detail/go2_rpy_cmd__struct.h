// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from go2_interfaces:msg/Go2RpyCmd.idl
// generated code does not contain a copyright notice

#ifndef GO2_INTERFACES__MSG__DETAIL__GO2_RPY_CMD__STRUCT_H_
#define GO2_INTERFACES__MSG__DETAIL__GO2_RPY_CMD__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/Go2RpyCmd in the package go2_interfaces.
typedef struct go2_interfaces__msg__Go2RpyCmd
{
  float roll;
  float pitch;
  float yaw;
} go2_interfaces__msg__Go2RpyCmd;

// Struct for a sequence of go2_interfaces__msg__Go2RpyCmd.
typedef struct go2_interfaces__msg__Go2RpyCmd__Sequence
{
  go2_interfaces__msg__Go2RpyCmd * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} go2_interfaces__msg__Go2RpyCmd__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // GO2_INTERFACES__MSG__DETAIL__GO2_RPY_CMD__STRUCT_H_
