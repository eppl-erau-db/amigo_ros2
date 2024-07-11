// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from unitree_go:msg/LowCmd.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "unitree_go/msg/detail/low_cmd__rosidl_typesupport_introspection_c.h"
#include "unitree_go/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "unitree_go/msg/detail/low_cmd__functions.h"
#include "unitree_go/msg/detail/low_cmd__struct.h"


// Include directives for member types
// Member `motor_cmd`
#include "unitree_go/msg/motor_cmd.h"
// Member `motor_cmd`
#include "unitree_go/msg/detail/motor_cmd__rosidl_typesupport_introspection_c.h"
// Member `bms_cmd`
#include "unitree_go/msg/bms_cmd.h"
// Member `bms_cmd`
#include "unitree_go/msg/detail/bms_cmd__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__LowCmd_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  unitree_go__msg__LowCmd__init(message_memory);
}

void unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__LowCmd_fini_function(void * message_memory)
{
  unitree_go__msg__LowCmd__fini(message_memory);
}

size_t unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__size_function__LowCmd__head(
  const void * untyped_member)
{
  (void)untyped_member;
  return 2;
}

const void * unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_const_function__LowCmd__head(
  const void * untyped_member, size_t index)
{
  const uint8_t * member =
    (const uint8_t *)(untyped_member);
  return &member[index];
}

void * unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_function__LowCmd__head(
  void * untyped_member, size_t index)
{
  uint8_t * member =
    (uint8_t *)(untyped_member);
  return &member[index];
}

void unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__fetch_function__LowCmd__head(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint8_t * item =
    ((const uint8_t *)
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_const_function__LowCmd__head(untyped_member, index));
  uint8_t * value =
    (uint8_t *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__assign_function__LowCmd__head(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint8_t * item =
    ((uint8_t *)
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_function__LowCmd__head(untyped_member, index));
  const uint8_t * value =
    (const uint8_t *)(untyped_value);
  *item = *value;
}

size_t unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__size_function__LowCmd__sn(
  const void * untyped_member)
{
  (void)untyped_member;
  return 2;
}

const void * unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_const_function__LowCmd__sn(
  const void * untyped_member, size_t index)
{
  const uint32_t * member =
    (const uint32_t *)(untyped_member);
  return &member[index];
}

void * unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_function__LowCmd__sn(
  void * untyped_member, size_t index)
{
  uint32_t * member =
    (uint32_t *)(untyped_member);
  return &member[index];
}

void unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__fetch_function__LowCmd__sn(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint32_t * item =
    ((const uint32_t *)
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_const_function__LowCmd__sn(untyped_member, index));
  uint32_t * value =
    (uint32_t *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__assign_function__LowCmd__sn(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint32_t * item =
    ((uint32_t *)
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_function__LowCmd__sn(untyped_member, index));
  const uint32_t * value =
    (const uint32_t *)(untyped_value);
  *item = *value;
}

size_t unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__size_function__LowCmd__version(
  const void * untyped_member)
{
  (void)untyped_member;
  return 2;
}

const void * unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_const_function__LowCmd__version(
  const void * untyped_member, size_t index)
{
  const uint32_t * member =
    (const uint32_t *)(untyped_member);
  return &member[index];
}

void * unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_function__LowCmd__version(
  void * untyped_member, size_t index)
{
  uint32_t * member =
    (uint32_t *)(untyped_member);
  return &member[index];
}

void unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__fetch_function__LowCmd__version(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint32_t * item =
    ((const uint32_t *)
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_const_function__LowCmd__version(untyped_member, index));
  uint32_t * value =
    (uint32_t *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__assign_function__LowCmd__version(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint32_t * item =
    ((uint32_t *)
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_function__LowCmd__version(untyped_member, index));
  const uint32_t * value =
    (const uint32_t *)(untyped_value);
  *item = *value;
}

size_t unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__size_function__LowCmd__motor_cmd(
  const void * untyped_member)
{
  (void)untyped_member;
  return 20;
}

const void * unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_const_function__LowCmd__motor_cmd(
  const void * untyped_member, size_t index)
{
  const unitree_go__msg__MotorCmd * member =
    (const unitree_go__msg__MotorCmd *)(untyped_member);
  return &member[index];
}

void * unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_function__LowCmd__motor_cmd(
  void * untyped_member, size_t index)
{
  unitree_go__msg__MotorCmd * member =
    (unitree_go__msg__MotorCmd *)(untyped_member);
  return &member[index];
}

void unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__fetch_function__LowCmd__motor_cmd(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const unitree_go__msg__MotorCmd * item =
    ((const unitree_go__msg__MotorCmd *)
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_const_function__LowCmd__motor_cmd(untyped_member, index));
  unitree_go__msg__MotorCmd * value =
    (unitree_go__msg__MotorCmd *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__assign_function__LowCmd__motor_cmd(
  void * untyped_member, size_t index, const void * untyped_value)
{
  unitree_go__msg__MotorCmd * item =
    ((unitree_go__msg__MotorCmd *)
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_function__LowCmd__motor_cmd(untyped_member, index));
  const unitree_go__msg__MotorCmd * value =
    (const unitree_go__msg__MotorCmd *)(untyped_value);
  *item = *value;
}

size_t unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__size_function__LowCmd__wireless_remote(
  const void * untyped_member)
{
  (void)untyped_member;
  return 40;
}

const void * unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_const_function__LowCmd__wireless_remote(
  const void * untyped_member, size_t index)
{
  const uint8_t * member =
    (const uint8_t *)(untyped_member);
  return &member[index];
}

void * unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_function__LowCmd__wireless_remote(
  void * untyped_member, size_t index)
{
  uint8_t * member =
    (uint8_t *)(untyped_member);
  return &member[index];
}

void unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__fetch_function__LowCmd__wireless_remote(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint8_t * item =
    ((const uint8_t *)
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_const_function__LowCmd__wireless_remote(untyped_member, index));
  uint8_t * value =
    (uint8_t *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__assign_function__LowCmd__wireless_remote(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint8_t * item =
    ((uint8_t *)
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_function__LowCmd__wireless_remote(untyped_member, index));
  const uint8_t * value =
    (const uint8_t *)(untyped_value);
  *item = *value;
}

size_t unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__size_function__LowCmd__led(
  const void * untyped_member)
{
  (void)untyped_member;
  return 12;
}

const void * unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_const_function__LowCmd__led(
  const void * untyped_member, size_t index)
{
  const uint8_t * member =
    (const uint8_t *)(untyped_member);
  return &member[index];
}

void * unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_function__LowCmd__led(
  void * untyped_member, size_t index)
{
  uint8_t * member =
    (uint8_t *)(untyped_member);
  return &member[index];
}

void unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__fetch_function__LowCmd__led(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint8_t * item =
    ((const uint8_t *)
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_const_function__LowCmd__led(untyped_member, index));
  uint8_t * value =
    (uint8_t *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__assign_function__LowCmd__led(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint8_t * item =
    ((uint8_t *)
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_function__LowCmd__led(untyped_member, index));
  const uint8_t * value =
    (const uint8_t *)(untyped_value);
  *item = *value;
}

size_t unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__size_function__LowCmd__fan(
  const void * untyped_member)
{
  (void)untyped_member;
  return 2;
}

const void * unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_const_function__LowCmd__fan(
  const void * untyped_member, size_t index)
{
  const uint8_t * member =
    (const uint8_t *)(untyped_member);
  return &member[index];
}

void * unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_function__LowCmd__fan(
  void * untyped_member, size_t index)
{
  uint8_t * member =
    (uint8_t *)(untyped_member);
  return &member[index];
}

void unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__fetch_function__LowCmd__fan(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint8_t * item =
    ((const uint8_t *)
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_const_function__LowCmd__fan(untyped_member, index));
  uint8_t * value =
    (uint8_t *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__assign_function__LowCmd__fan(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint8_t * item =
    ((uint8_t *)
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_function__LowCmd__fan(untyped_member, index));
  const uint8_t * value =
    (const uint8_t *)(untyped_value);
  *item = *value;
}

static rosidl_typesupport_introspection_c__MessageMember unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__LowCmd_message_member_array[14] = {
  {
    "head",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    2,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__LowCmd, head),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__size_function__LowCmd__head,  // size() function pointer
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_const_function__LowCmd__head,  // get_const(index) function pointer
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_function__LowCmd__head,  // get(index) function pointer
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__fetch_function__LowCmd__head,  // fetch(index, &value) function pointer
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__assign_function__LowCmd__head,  // assign(index, value) function pointer
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
    offsetof(unitree_go__msg__LowCmd, level_flag),  // bytes offset in struct
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
    offsetof(unitree_go__msg__LowCmd, frame_reserve),  // bytes offset in struct
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
    offsetof(unitree_go__msg__LowCmd, sn),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__size_function__LowCmd__sn,  // size() function pointer
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_const_function__LowCmd__sn,  // get_const(index) function pointer
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_function__LowCmd__sn,  // get(index) function pointer
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__fetch_function__LowCmd__sn,  // fetch(index, &value) function pointer
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__assign_function__LowCmd__sn,  // assign(index, value) function pointer
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
    offsetof(unitree_go__msg__LowCmd, version),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__size_function__LowCmd__version,  // size() function pointer
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_const_function__LowCmd__version,  // get_const(index) function pointer
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_function__LowCmd__version,  // get(index) function pointer
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__fetch_function__LowCmd__version,  // fetch(index, &value) function pointer
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__assign_function__LowCmd__version,  // assign(index, value) function pointer
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
    offsetof(unitree_go__msg__LowCmd, bandwidth),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "motor_cmd",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    20,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__LowCmd, motor_cmd),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__size_function__LowCmd__motor_cmd,  // size() function pointer
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_const_function__LowCmd__motor_cmd,  // get_const(index) function pointer
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_function__LowCmd__motor_cmd,  // get(index) function pointer
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__fetch_function__LowCmd__motor_cmd,  // fetch(index, &value) function pointer
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__assign_function__LowCmd__motor_cmd,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "bms_cmd",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__LowCmd, bms_cmd),  // bytes offset in struct
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
    offsetof(unitree_go__msg__LowCmd, wireless_remote),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__size_function__LowCmd__wireless_remote,  // size() function pointer
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_const_function__LowCmd__wireless_remote,  // get_const(index) function pointer
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_function__LowCmd__wireless_remote,  // get(index) function pointer
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__fetch_function__LowCmd__wireless_remote,  // fetch(index, &value) function pointer
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__assign_function__LowCmd__wireless_remote,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "led",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    12,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__LowCmd, led),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__size_function__LowCmd__led,  // size() function pointer
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_const_function__LowCmd__led,  // get_const(index) function pointer
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_function__LowCmd__led,  // get(index) function pointer
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__fetch_function__LowCmd__led,  // fetch(index, &value) function pointer
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__assign_function__LowCmd__led,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "fan",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    2,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__LowCmd, fan),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__size_function__LowCmd__fan,  // size() function pointer
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_const_function__LowCmd__fan,  // get_const(index) function pointer
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__get_function__LowCmd__fan,  // get(index) function pointer
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__fetch_function__LowCmd__fan,  // fetch(index, &value) function pointer
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__assign_function__LowCmd__fan,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "gpio",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__LowCmd, gpio),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
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
    offsetof(unitree_go__msg__LowCmd, reserve),  // bytes offset in struct
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
    offsetof(unitree_go__msg__LowCmd, crc),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__LowCmd_message_members = {
  "unitree_go__msg",  // message namespace
  "LowCmd",  // message name
  14,  // number of fields
  sizeof(unitree_go__msg__LowCmd),
  unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__LowCmd_message_member_array,  // message members
  unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__LowCmd_init_function,  // function to initialize message memory (memory has to be allocated)
  unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__LowCmd_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__LowCmd_message_type_support_handle = {
  0,
  &unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__LowCmd_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_unitree_go
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unitree_go, msg, LowCmd)() {
  unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__LowCmd_message_member_array[6].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unitree_go, msg, MotorCmd)();
  unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__LowCmd_message_member_array[7].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unitree_go, msg, BmsCmd)();
  if (!unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__LowCmd_message_type_support_handle.typesupport_identifier) {
    unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__LowCmd_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &unitree_go__msg__LowCmd__rosidl_typesupport_introspection_c__LowCmd_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
