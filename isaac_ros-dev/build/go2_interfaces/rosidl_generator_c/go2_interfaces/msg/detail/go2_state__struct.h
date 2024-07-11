// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from go2_interfaces:msg/Go2State.idl
// generated code does not contain a copyright notice

#ifndef GO2_INTERFACES__MSG__DETAIL__GO2_STATE__STRUCT_H_
#define GO2_INTERFACES__MSG__DETAIL__GO2_STATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/Go2State in the package go2_interfaces.
typedef struct go2_interfaces__msg__Go2State
{
  uint8_t mode;
  int32_t progress;
  uint8_t gait_type;
  float foot_raise_height;
  float position[3];
  float body_height;
  float velocity[3];
  float range_obstacle[4];
  int16_t foot_force[4];
  float foot_position_body[12];
  float foot_speed_body[12];
} go2_interfaces__msg__Go2State;

// Struct for a sequence of go2_interfaces__msg__Go2State.
typedef struct go2_interfaces__msg__Go2State__Sequence
{
  go2_interfaces__msg__Go2State * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} go2_interfaces__msg__Go2State__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // GO2_INTERFACES__MSG__DETAIL__GO2_STATE__STRUCT_H_
