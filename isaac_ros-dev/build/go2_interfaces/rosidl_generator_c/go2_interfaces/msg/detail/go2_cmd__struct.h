// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from go2_interfaces:msg/Go2Cmd.idl
// generated code does not contain a copyright notice

#ifndef GO2_INTERFACES__MSG__DETAIL__GO2_CMD__STRUCT_H_
#define GO2_INTERFACES__MSG__DETAIL__GO2_CMD__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/Go2Cmd in the package go2_interfaces.
typedef struct go2_interfaces__msg__Go2Cmd
{
  uint16_t cmd;
} go2_interfaces__msg__Go2Cmd;

// Struct for a sequence of go2_interfaces__msg__Go2Cmd.
typedef struct go2_interfaces__msg__Go2Cmd__Sequence
{
  go2_interfaces__msg__Go2Cmd * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} go2_interfaces__msg__Go2Cmd__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // GO2_INTERFACES__MSG__DETAIL__GO2_CMD__STRUCT_H_
