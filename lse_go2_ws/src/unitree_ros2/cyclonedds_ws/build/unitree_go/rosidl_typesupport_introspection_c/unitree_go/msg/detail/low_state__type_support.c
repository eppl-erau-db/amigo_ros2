// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from unitree_go:msg/LowState.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "unitree_go/msg/detail/low_state__rosidl_typesupport_introspection_c.h"
#include "unitree_go/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "unitree_go/msg/detail/low_state__functions.h"
#include "unitree_go/msg/detail/low_state__struct.h"


// Include directives for member types
// Member `imu_state`
#include "unitree_go/msg/imu_state.h"
// Member `imu_state`
#include "unitree_go/msg/detail/imu_state__rosidl_typesupport_introspection_c.h"
// Member `motor_state`
#include "unitree_go/msg/motor_state.h"
// Member `motor_state`
#include "unitree_go/msg/detail/motor_state__rosidl_typesupport_introspection_c.h"
// Member `bms_state`
#include "unitree_go/msg/bms_state.h"
// Member `bms_state`
#include "unitree_go/msg/detail/bms_state__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void unitree_go__msg__LowState__rosidl_typesupport_introspection_c__LowState_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  unitree_go__msg__LowState__init(message_memory);
}

void unitree_go__msg__LowState__rosidl_typesupport_introspection_c__LowState_fini_function(void * message_memory)
{
  unitree_go__msg__LowState__fini(message_memory);
}

size_t unitree_go__msg__LowState__rosidl_typesupport_introspection_c__size_function__LowState__head(
  const void * untyped_member)
{
  (void)untyped_member;
  return 2;
}

const void * unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_const_function__LowState__head(
  const void * untyped_member, size_t index)
{
  const uint8_t * member =
    (const uint8_t *)(untyped_member);
  return &member[index];
}

void * unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_function__LowState__head(
  void * untyped_member, size_t index)
{
  uint8_t * member =
    (uint8_t *)(untyped_member);
  return &member[index];
}

void unitree_go__msg__LowState__rosidl_typesupport_introspection_c__fetch_function__LowState__head(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint8_t * item =
    ((const uint8_t *)
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_const_function__LowState__head(untyped_member, index));
  uint8_t * value =
    (uint8_t *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__LowState__rosidl_typesupport_introspection_c__assign_function__LowState__head(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint8_t * item =
    ((uint8_t *)
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_function__LowState__head(untyped_member, index));
  const uint8_t * value =
    (const uint8_t *)(untyped_value);
  *item = *value;
}

size_t unitree_go__msg__LowState__rosidl_typesupport_introspection_c__size_function__LowState__sn(
  const void * untyped_member)
{
  (void)untyped_member;
  return 2;
}

const void * unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_const_function__LowState__sn(
  const void * untyped_member, size_t index)
{
  const uint32_t * member =
    (const uint32_t *)(untyped_member);
  return &member[index];
}

void * unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_function__LowState__sn(
  void * untyped_member, size_t index)
{
  uint32_t * member =
    (uint32_t *)(untyped_member);
  return &member[index];
}

void unitree_go__msg__LowState__rosidl_typesupport_introspection_c__fetch_function__LowState__sn(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint32_t * item =
    ((const uint32_t *)
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_const_function__LowState__sn(untyped_member, index));
  uint32_t * value =
    (uint32_t *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__LowState__rosidl_typesupport_introspection_c__assign_function__LowState__sn(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint32_t * item =
    ((uint32_t *)
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_function__LowState__sn(untyped_member, index));
  const uint32_t * value =
    (const uint32_t *)(untyped_value);
  *item = *value;
}

size_t unitree_go__msg__LowState__rosidl_typesupport_introspection_c__size_function__LowState__version(
  const void * untyped_member)
{
  (void)untyped_member;
  return 2;
}

const void * unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_const_function__LowState__version(
  const void * untyped_member, size_t index)
{
  const uint32_t * member =
    (const uint32_t *)(untyped_member);
  return &member[index];
}

void * unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_function__LowState__version(
  void * untyped_member, size_t index)
{
  uint32_t * member =
    (uint32_t *)(untyped_member);
  return &member[index];
}

void unitree_go__msg__LowState__rosidl_typesupport_introspection_c__fetch_function__LowState__version(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint32_t * item =
    ((const uint32_t *)
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_const_function__LowState__version(untyped_member, index));
  uint32_t * value =
    (uint32_t *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__LowState__rosidl_typesupport_introspection_c__assign_function__LowState__version(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint32_t * item =
    ((uint32_t *)
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_function__LowState__version(untyped_member, index));
  const uint32_t * value =
    (const uint32_t *)(untyped_value);
  *item = *value;
}

size_t unitree_go__msg__LowState__rosidl_typesupport_introspection_c__size_function__LowState__motor_state(
  const void * untyped_member)
{
  (void)untyped_member;
  return 20;
}

const void * unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_const_function__LowState__motor_state(
  const void * untyped_member, size_t index)
{
  const unitree_go__msg__MotorState * member =
    (const unitree_go__msg__MotorState *)(untyped_member);
  return &member[index];
}

void * unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_function__LowState__motor_state(
  void * untyped_member, size_t index)
{
  unitree_go__msg__MotorState * member =
    (unitree_go__msg__MotorState *)(untyped_member);
  return &member[index];
}

void unitree_go__msg__LowState__rosidl_typesupport_introspection_c__fetch_function__LowState__motor_state(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const unitree_go__msg__MotorState * item =
    ((const unitree_go__msg__MotorState *)
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_const_function__LowState__motor_state(untyped_member, index));
  unitree_go__msg__MotorState * value =
    (unitree_go__msg__MotorState *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__LowState__rosidl_typesupport_introspection_c__assign_function__LowState__motor_state(
  void * untyped_member, size_t index, const void * untyped_value)
{
  unitree_go__msg__MotorState * item =
    ((unitree_go__msg__MotorState *)
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_function__LowState__motor_state(untyped_member, index));
  const unitree_go__msg__MotorState * value =
    (const unitree_go__msg__MotorState *)(untyped_value);
  *item = *value;
}

size_t unitree_go__msg__LowState__rosidl_typesupport_introspection_c__size_function__LowState__foot_force(
  const void * untyped_member)
{
  (void)untyped_member;
  return 4;
}

const void * unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_const_function__LowState__foot_force(
  const void * untyped_member, size_t index)
{
  const int16_t * member =
    (const int16_t *)(untyped_member);
  return &member[index];
}

void * unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_function__LowState__foot_force(
  void * untyped_member, size_t index)
{
  int16_t * member =
    (int16_t *)(untyped_member);
  return &member[index];
}

void unitree_go__msg__LowState__rosidl_typesupport_introspection_c__fetch_function__LowState__foot_force(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const int16_t * item =
    ((const int16_t *)
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_const_function__LowState__foot_force(untyped_member, index));
  int16_t * value =
    (int16_t *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__LowState__rosidl_typesupport_introspection_c__assign_function__LowState__foot_force(
  void * untyped_member, size_t index, const void * untyped_value)
{
  int16_t * item =
    ((int16_t *)
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_function__LowState__foot_force(untyped_member, index));
  const int16_t * value =
    (const int16_t *)(untyped_value);
  *item = *value;
}

size_t unitree_go__msg__LowState__rosidl_typesupport_introspection_c__size_function__LowState__foot_force_est(
  const void * untyped_member)
{
  (void)untyped_member;
  return 4;
}

const void * unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_const_function__LowState__foot_force_est(
  const void * untyped_member, size_t index)
{
  const int16_t * member =
    (const int16_t *)(untyped_member);
  return &member[index];
}

void * unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_function__LowState__foot_force_est(
  void * untyped_member, size_t index)
{
  int16_t * member =
    (int16_t *)(untyped_member);
  return &member[index];
}

void unitree_go__msg__LowState__rosidl_typesupport_introspection_c__fetch_function__LowState__foot_force_est(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const int16_t * item =
    ((const int16_t *)
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_const_function__LowState__foot_force_est(untyped_member, index));
  int16_t * value =
    (int16_t *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__LowState__rosidl_typesupport_introspection_c__assign_function__LowState__foot_force_est(
  void * untyped_member, size_t index, const void * untyped_value)
{
  int16_t * item =
    ((int16_t *)
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_function__LowState__foot_force_est(untyped_member, index));
  const int16_t * value =
    (const int16_t *)(untyped_value);
  *item = *value;
}

size_t unitree_go__msg__LowState__rosidl_typesupport_introspection_c__size_function__LowState__wireless_remote(
  const void * untyped_member)
{
  (void)untyped_member;
  return 40;
}

const void * unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_const_function__LowState__wireless_remote(
  const void * untyped_member, size_t index)
{
  const uint8_t * member =
    (const uint8_t *)(untyped_member);
  return &member[index];
}

void * unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_function__LowState__wireless_remote(
  void * untyped_member, size_t index)
{
  uint8_t * member =
    (uint8_t *)(untyped_member);
  return &member[index];
}

void unitree_go__msg__LowState__rosidl_typesupport_introspection_c__fetch_function__LowState__wireless_remote(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint8_t * item =
    ((const uint8_t *)
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_const_function__LowState__wireless_remote(untyped_member, index));
  uint8_t * value =
    (uint8_t *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__LowState__rosidl_typesupport_introspection_c__assign_function__LowState__wireless_remote(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint8_t * item =
    ((uint8_t *)
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_function__LowState__wireless_remote(untyped_member, index));
  const uint8_t * value =
    (const uint8_t *)(untyped_value);
  *item = *value;
}

size_t unitree_go__msg__LowState__rosidl_typesupport_introspection_c__size_function__LowState__fan_frequency(
  const void * untyped_member)
{
  (void)untyped_member;
  return 4;
}

const void * unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_const_function__LowState__fan_frequency(
  const void * untyped_member, size_t index)
{
  const uint16_t * member =
    (const uint16_t *)(untyped_member);
  return &member[index];
}

void * unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_function__LowState__fan_frequency(
  void * untyped_member, size_t index)
{
  uint16_t * member =
    (uint16_t *)(untyped_member);
  return &member[index];
}

void unitree_go__msg__LowState__rosidl_typesupport_introspection_c__fetch_function__LowState__fan_frequency(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint16_t * item =
    ((const uint16_t *)
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_const_function__LowState__fan_frequency(untyped_member, index));
  uint16_t * value =
    (uint16_t *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__LowState__rosidl_typesupport_introspection_c__assign_function__LowState__fan_frequency(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint16_t * item =
    ((uint16_t *)
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_function__LowState__fan_frequency(untyped_member, index));
  const uint16_t * value =
    (const uint16_t *)(untyped_value);
  *item = *value;
}

static rosidl_typesupport_introspection_c__MessageMember unitree_go__msg__LowState__rosidl_typesupport_introspection_c__LowState_message_member_array[22] = {
  {
    "head",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    2,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__LowState, head),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__size_function__LowState__head,  // size() function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_const_function__LowState__head,  // get_const(index) function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_function__LowState__head,  // get(index) function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__fetch_function__LowState__head,  // fetch(index, &value) function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__assign_function__LowState__head,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "level_flag",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__LowState, level_flag),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "frame_reserve",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__LowState, frame_reserve),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "sn",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    2,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__LowState, sn),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__size_function__LowState__sn,  // size() function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_const_function__LowState__sn,  // get_const(index) function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_function__LowState__sn,  // get(index) function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__fetch_function__LowState__sn,  // fetch(index, &value) function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__assign_function__LowState__sn,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "version",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    2,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__LowState, version),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__size_function__LowState__version,  // size() function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_const_function__LowState__version,  // get_const(index) function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_function__LowState__version,  // get(index) function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__fetch_function__LowState__version,  // fetch(index, &value) function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__assign_function__LowState__version,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "bandwidth",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT16,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__LowState, bandwidth),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "imu_state",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__LowState, imu_state),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "motor_state",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    20,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__LowState, motor_state),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__size_function__LowState__motor_state,  // size() function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_const_function__LowState__motor_state,  // get_const(index) function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_function__LowState__motor_state,  // get(index) function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__fetch_function__LowState__motor_state,  // fetch(index, &value) function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__assign_function__LowState__motor_state,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "bms_state",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__LowState, bms_state),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "foot_force",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT16,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    4,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__LowState, foot_force),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__size_function__LowState__foot_force,  // size() function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_const_function__LowState__foot_force,  // get_const(index) function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_function__LowState__foot_force,  // get(index) function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__fetch_function__LowState__foot_force,  // fetch(index, &value) function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__assign_function__LowState__foot_force,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "foot_force_est",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT16,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    4,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__LowState, foot_force_est),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__size_function__LowState__foot_force_est,  // size() function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_const_function__LowState__foot_force_est,  // get_const(index) function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_function__LowState__foot_force_est,  // get(index) function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__fetch_function__LowState__foot_force_est,  // fetch(index, &value) function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__assign_function__LowState__foot_force_est,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "tick",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__LowState, tick),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "wireless_remote",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    40,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__LowState, wireless_remote),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__size_function__LowState__wireless_remote,  // size() function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_const_function__LowState__wireless_remote,  // get_const(index) function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_function__LowState__wireless_remote,  // get(index) function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__fetch_function__LowState__wireless_remote,  // fetch(index, &value) function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__assign_function__LowState__wireless_remote,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "bit_flag",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__LowState, bit_flag),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "adc_reel",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__LowState, adc_reel),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "temperature_ntc1",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__LowState, temperature_ntc1),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "temperature_ntc2",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__LowState, temperature_ntc2),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "power_v",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__LowState, power_v),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "power_a",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__LowState, power_a),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "fan_frequency",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT16,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    4,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__LowState, fan_frequency),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__size_function__LowState__fan_frequency,  // size() function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_const_function__LowState__fan_frequency,  // get_const(index) function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__get_function__LowState__fan_frequency,  // get(index) function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__fetch_function__LowState__fan_frequency,  // fetch(index, &value) function pointer
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__assign_function__LowState__fan_frequency,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "reserve",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__LowState, reserve),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "crc",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__LowState, crc),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers unitree_go__msg__LowState__rosidl_typesupport_introspection_c__LowState_message_members = {
  "unitree_go__msg",  // message namespace
  "LowState",  // message name
  22,  // number of fields
  sizeof(unitree_go__msg__LowState),
  unitree_go__msg__LowState__rosidl_typesupport_introspection_c__LowState_message_member_array,  // message members
  unitree_go__msg__LowState__rosidl_typesupport_introspection_c__LowState_init_function,  // function to initialize message memory (memory has to be allocated)
  unitree_go__msg__LowState__rosidl_typesupport_introspection_c__LowState_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t unitree_go__msg__LowState__rosidl_typesupport_introspection_c__LowState_message_type_support_handle = {
  0,
  &unitree_go__msg__LowState__rosidl_typesupport_introspection_c__LowState_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_unitree_go
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unitree_go, msg, LowState)() {
  unitree_go__msg__LowState__rosidl_typesupport_introspection_c__LowState_message_member_array[6].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unitree_go, msg, IMUState)();
  unitree_go__msg__LowState__rosidl_typesupport_introspection_c__LowState_message_member_array[7].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unitree_go, msg, MotorState)();
  unitree_go__msg__LowState__rosidl_typesupport_introspection_c__LowState_message_member_array[8].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unitree_go, msg, BmsState)();
  if (!unitree_go__msg__LowState__rosidl_typesupport_introspection_c__LowState_message_type_support_handle.typesupport_identifier) {
    unitree_go__msg__LowState__rosidl_typesupport_introspection_c__LowState_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &unitree_go__msg__LowState__rosidl_typesupport_introspection_c__LowState_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
