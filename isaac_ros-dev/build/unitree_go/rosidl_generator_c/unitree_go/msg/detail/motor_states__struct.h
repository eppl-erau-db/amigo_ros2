// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from unitree_go:msg/MotorStates.idl
// generated code does not contain a copyright notice

#ifndef UNITREE_GO__MSG__DETAIL__MOTOR_STATES__STRUCT_H_
#define UNITREE_GO__MSG__DETAIL__MOTOR_STATES__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'states'
#include "unitree_go/msg/detail/motor_state__struct.h"

/// Struct defined in msg/MotorStates in the package unitree_go.
typedef struct unitree_go__msg__MotorStates
{
  unitree_go__msg__MotorState__Sequence states;
} unitree_go__msg__MotorStates;

// Struct for a sequence of unitree_go__msg__MotorStates.
typedef struct unitree_go__msg__MotorStates__Sequence
{
  unitree_go__msg__MotorStates * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} unitree_go__msg__MotorStates__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // UNITREE_GO__MSG__DETAIL__MOTOR_STATES__STRUCT_H_
