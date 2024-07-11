// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from go2_interfaces:msg/IMU.idl
// generated code does not contain a copyright notice

#ifndef GO2_INTERFACES__MSG__DETAIL__IMU__STRUCT_H_
#define GO2_INTERFACES__MSG__DETAIL__IMU__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/IMU in the package go2_interfaces.
typedef struct go2_interfaces__msg__IMU
{
  float quaternion[4];
  float gyroscope[3];
  float accelerometer[3];
  float rpy[3];
  int8_t temperature;
} go2_interfaces__msg__IMU;

// Struct for a sequence of go2_interfaces__msg__IMU.
typedef struct go2_interfaces__msg__IMU__Sequence
{
  go2_interfaces__msg__IMU * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} go2_interfaces__msg__IMU__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // GO2_INTERFACES__MSG__DETAIL__IMU__STRUCT_H_
