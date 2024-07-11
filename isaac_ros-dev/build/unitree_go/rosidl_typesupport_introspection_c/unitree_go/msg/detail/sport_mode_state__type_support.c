// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from unitree_go:msg/SportModeState.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "unitree_go/msg/detail/sport_mode_state__rosidl_typesupport_introspection_c.h"
#include "unitree_go/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "unitree_go/msg/detail/sport_mode_state__functions.h"
#include "unitree_go/msg/detail/sport_mode_state__struct.h"


// Include directives for member types
// Member `stamp`
#include "unitree_go/msg/time_spec.h"
// Member `stamp`
#include "unitree_go/msg/detail/time_spec__rosidl_typesupport_introspection_c.h"
// Member `imu_state`
#include "unitree_go/msg/imu_state.h"
// Member `imu_state`
#include "unitree_go/msg/detail/imu_state__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__SportModeState_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  unitree_go__msg__SportModeState__init(message_memory);
}

void unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__SportModeState_fini_function(void * message_memory)
{
  unitree_go__msg__SportModeState__fini(message_memory);
}

size_t unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__size_function__SportModeState__position(
  const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_const_function__SportModeState__position(
  const void * untyped_member, size_t index)
{
  const float * member =
    (const float *)(untyped_member);
  return &member[index];
}

void * unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_function__SportModeState__position(
  void * untyped_member, size_t index)
{
  float * member =
    (float *)(untyped_member);
  return &member[index];
}

void unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__fetch_function__SportModeState__position(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_const_function__SportModeState__position(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__assign_function__SportModeState__position(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_function__SportModeState__position(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

size_t unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__size_function__SportModeState__velocity(
  const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_const_function__SportModeState__velocity(
  const void * untyped_member, size_t index)
{
  const float * member =
    (const float *)(untyped_member);
  return &member[index];
}

void * unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_function__SportModeState__velocity(
  void * untyped_member, size_t index)
{
  float * member =
    (float *)(untyped_member);
  return &member[index];
}

void unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__fetch_function__SportModeState__velocity(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_const_function__SportModeState__velocity(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__assign_function__SportModeState__velocity(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_function__SportModeState__velocity(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

size_t unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__size_function__SportModeState__range_obstacle(
  const void * untyped_member)
{
  (void)untyped_member;
  return 4;
}

const void * unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_const_function__SportModeState__range_obstacle(
  const void * untyped_member, size_t index)
{
  const float * member =
    (const float *)(untyped_member);
  return &member[index];
}

void * unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_function__SportModeState__range_obstacle(
  void * untyped_member, size_t index)
{
  float * member =
    (float *)(untyped_member);
  return &member[index];
}

void unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__fetch_function__SportModeState__range_obstacle(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_const_function__SportModeState__range_obstacle(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__assign_function__SportModeState__range_obstacle(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_function__SportModeState__range_obstacle(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

size_t unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__size_function__SportModeState__foot_force(
  const void * untyped_member)
{
  (void)untyped_member;
  return 4;
}

const void * unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_const_function__SportModeState__foot_force(
  const void * untyped_member, size_t index)
{
  const int16_t * member =
    (const int16_t *)(untyped_member);
  return &member[index];
}

void * unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_function__SportModeState__foot_force(
  void * untyped_member, size_t index)
{
  int16_t * member =
    (int16_t *)(untyped_member);
  return &member[index];
}

void unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__fetch_function__SportModeState__foot_force(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const int16_t * item =
    ((const int16_t *)
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_const_function__SportModeState__foot_force(untyped_member, index));
  int16_t * value =
    (int16_t *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__assign_function__SportModeState__foot_force(
  void * untyped_member, size_t index, const void * untyped_value)
{
  int16_t * item =
    ((int16_t *)
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_function__SportModeState__foot_force(untyped_member, index));
  const int16_t * value =
    (const int16_t *)(untyped_value);
  *item = *value;
}

size_t unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__size_function__SportModeState__foot_position_body(
  const void * untyped_member)
{
  (void)untyped_member;
  return 12;
}

const void * unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_const_function__SportModeState__foot_position_body(
  const void * untyped_member, size_t index)
{
  const float * member =
    (const float *)(untyped_member);
  return &member[index];
}

void * unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_function__SportModeState__foot_position_body(
  void * untyped_member, size_t index)
{
  float * member =
    (float *)(untyped_member);
  return &member[index];
}

void unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__fetch_function__SportModeState__foot_position_body(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_const_function__SportModeState__foot_position_body(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__assign_function__SportModeState__foot_position_body(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_function__SportModeState__foot_position_body(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

size_t unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__size_function__SportModeState__foot_speed_body(
  const void * untyped_member)
{
  (void)untyped_member;
  return 12;
}

const void * unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_const_function__SportModeState__foot_speed_body(
  const void * untyped_member, size_t index)
{
  const float * member =
    (const float *)(untyped_member);
  return &member[index];
}

void * unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_function__SportModeState__foot_speed_body(
  void * untyped_member, size_t index)
{
  float * member =
    (float *)(untyped_member);
  return &member[index];
}

void unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__fetch_function__SportModeState__foot_speed_body(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_const_function__SportModeState__foot_speed_body(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__assign_function__SportModeState__foot_speed_body(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_function__SportModeState__foot_speed_body(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

static rosidl_typesupport_introspection_c__MessageMember unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__SportModeState_message_member_array[15] = {
  {
    "stamp",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__SportModeState, stamp),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "error_code",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__SportModeState, error_code),  // bytes offset in struct
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
    offsetof(unitree_go__msg__SportModeState, imu_state),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "mode",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__SportModeState, mode),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "progress",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__SportModeState, progress),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "gait_type",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__SportModeState, gait_type),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "foot_raise_height",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__SportModeState, foot_raise_height),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "position",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__SportModeState, position),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__size_function__SportModeState__position,  // size() function pointer
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_const_function__SportModeState__position,  // get_const(index) function pointer
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_function__SportModeState__position,  // get(index) function pointer
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__fetch_function__SportModeState__position,  // fetch(index, &value) function pointer
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__assign_function__SportModeState__position,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "body_height",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__SportModeState, body_height),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "velocity",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__SportModeState, velocity),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__size_function__SportModeState__velocity,  // size() function pointer
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_const_function__SportModeState__velocity,  // get_const(index) function pointer
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_function__SportModeState__velocity,  // get(index) function pointer
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__fetch_function__SportModeState__velocity,  // fetch(index, &value) function pointer
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__assign_function__SportModeState__velocity,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "yaw_speed",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__SportModeState, yaw_speed),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "range_obstacle",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    4,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__SportModeState, range_obstacle),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__size_function__SportModeState__range_obstacle,  // size() function pointer
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_const_function__SportModeState__range_obstacle,  // get_const(index) function pointer
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_function__SportModeState__range_obstacle,  // get(index) function pointer
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__fetch_function__SportModeState__range_obstacle,  // fetch(index, &value) function pointer
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__assign_function__SportModeState__range_obstacle,  // assign(index, value) function pointer
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
    offsetof(unitree_go__msg__SportModeState, foot_force),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__size_function__SportModeState__foot_force,  // size() function pointer
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_const_function__SportModeState__foot_force,  // get_const(index) function pointer
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_function__SportModeState__foot_force,  // get(index) function pointer
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__fetch_function__SportModeState__foot_force,  // fetch(index, &value) function pointer
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__assign_function__SportModeState__foot_force,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "foot_position_body",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    12,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__SportModeState, foot_position_body),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__size_function__SportModeState__foot_position_body,  // size() function pointer
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_const_function__SportModeState__foot_position_body,  // get_const(index) function pointer
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_function__SportModeState__foot_position_body,  // get(index) function pointer
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__fetch_function__SportModeState__foot_position_body,  // fetch(index, &value) function pointer
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__assign_function__SportModeState__foot_position_body,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "foot_speed_body",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    12,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__SportModeState, foot_speed_body),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__size_function__SportModeState__foot_speed_body,  // size() function pointer
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_const_function__SportModeState__foot_speed_body,  // get_const(index) function pointer
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__get_function__SportModeState__foot_speed_body,  // get(index) function pointer
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__fetch_function__SportModeState__foot_speed_body,  // fetch(index, &value) function pointer
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__assign_function__SportModeState__foot_speed_body,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__SportModeState_message_members = {
  "unitree_go__msg",  // message namespace
  "SportModeState",  // message name
  15,  // number of fields
  sizeof(unitree_go__msg__SportModeState),
  unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__SportModeState_message_member_array,  // message members
  unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__SportModeState_init_function,  // function to initialize message memory (memory has to be allocated)
  unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__SportModeState_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__SportModeState_message_type_support_handle = {
  0,
  &unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__SportModeState_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_unitree_go
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unitree_go, msg, SportModeState)() {
  unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__SportModeState_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unitree_go, msg, TimeSpec)();
  unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__SportModeState_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unitree_go, msg, IMUState)();
  if (!unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__SportModeState_message_type_support_handle.typesupport_identifier) {
    unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__SportModeState_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &unitree_go__msg__SportModeState__rosidl_typesupport_introspection_c__SportModeState_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
