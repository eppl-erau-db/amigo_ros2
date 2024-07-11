// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from unitree_go:msg/SportModeCmd.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "unitree_go/msg/detail/sport_mode_cmd__rosidl_typesupport_introspection_c.h"
#include "unitree_go/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "unitree_go/msg/detail/sport_mode_cmd__functions.h"
#include "unitree_go/msg/detail/sport_mode_cmd__struct.h"


// Include directives for member types
// Member `bms_cmd`
#include "unitree_go/msg/bms_cmd.h"
// Member `bms_cmd`
#include "unitree_go/msg/detail/bms_cmd__rosidl_typesupport_introspection_c.h"
// Member `path_point`
#include "unitree_go/msg/path_point.h"
// Member `path_point`
#include "unitree_go/msg/detail/path_point__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__SportModeCmd_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  unitree_go__msg__SportModeCmd__init(message_memory);
}

void unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__SportModeCmd_fini_function(void * message_memory)
{
  unitree_go__msg__SportModeCmd__fini(message_memory);
}

size_t unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__size_function__SportModeCmd__position(
  const void * untyped_member)
{
  (void)untyped_member;
  return 2;
}

const void * unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__get_const_function__SportModeCmd__position(
  const void * untyped_member, size_t index)
{
  const float * member =
    (const float *)(untyped_member);
  return &member[index];
}

void * unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__get_function__SportModeCmd__position(
  void * untyped_member, size_t index)
{
  float * member =
    (float *)(untyped_member);
  return &member[index];
}

void unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__fetch_function__SportModeCmd__position(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__get_const_function__SportModeCmd__position(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__assign_function__SportModeCmd__position(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__get_function__SportModeCmd__position(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

size_t unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__size_function__SportModeCmd__euler(
  const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__get_const_function__SportModeCmd__euler(
  const void * untyped_member, size_t index)
{
  const float * member =
    (const float *)(untyped_member);
  return &member[index];
}

void * unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__get_function__SportModeCmd__euler(
  void * untyped_member, size_t index)
{
  float * member =
    (float *)(untyped_member);
  return &member[index];
}

void unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__fetch_function__SportModeCmd__euler(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__get_const_function__SportModeCmd__euler(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__assign_function__SportModeCmd__euler(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__get_function__SportModeCmd__euler(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

size_t unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__size_function__SportModeCmd__velocity(
  const void * untyped_member)
{
  (void)untyped_member;
  return 2;
}

const void * unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__get_const_function__SportModeCmd__velocity(
  const void * untyped_member, size_t index)
{
  const float * member =
    (const float *)(untyped_member);
  return &member[index];
}

void * unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__get_function__SportModeCmd__velocity(
  void * untyped_member, size_t index)
{
  float * member =
    (float *)(untyped_member);
  return &member[index];
}

void unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__fetch_function__SportModeCmd__velocity(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__get_const_function__SportModeCmd__velocity(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__assign_function__SportModeCmd__velocity(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__get_function__SportModeCmd__velocity(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

size_t unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__size_function__SportModeCmd__path_point(
  const void * untyped_member)
{
  (void)untyped_member;
  return 30;
}

const void * unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__get_const_function__SportModeCmd__path_point(
  const void * untyped_member, size_t index)
{
  const unitree_go__msg__PathPoint * member =
    (const unitree_go__msg__PathPoint *)(untyped_member);
  return &member[index];
}

void * unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__get_function__SportModeCmd__path_point(
  void * untyped_member, size_t index)
{
  unitree_go__msg__PathPoint * member =
    (unitree_go__msg__PathPoint *)(untyped_member);
  return &member[index];
}

void unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__fetch_function__SportModeCmd__path_point(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const unitree_go__msg__PathPoint * item =
    ((const unitree_go__msg__PathPoint *)
    unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__get_const_function__SportModeCmd__path_point(untyped_member, index));
  unitree_go__msg__PathPoint * value =
    (unitree_go__msg__PathPoint *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__assign_function__SportModeCmd__path_point(
  void * untyped_member, size_t index, const void * untyped_value)
{
  unitree_go__msg__PathPoint * item =
    ((unitree_go__msg__PathPoint *)
    unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__get_function__SportModeCmd__path_point(untyped_member, index));
  const unitree_go__msg__PathPoint * value =
    (const unitree_go__msg__PathPoint *)(untyped_value);
  *item = *value;
}

static rosidl_typesupport_introspection_c__MessageMember unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__SportModeCmd_message_member_array[11] = {
  {
    "mode",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__SportModeCmd, mode),  // bytes offset in struct
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
    offsetof(unitree_go__msg__SportModeCmd, gait_type),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "speed_level",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__SportModeCmd, speed_level),  // bytes offset in struct
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
    offsetof(unitree_go__msg__SportModeCmd, foot_raise_height),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
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
    offsetof(unitree_go__msg__SportModeCmd, body_height),  // bytes offset in struct
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
    2,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__SportModeCmd, position),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__size_function__SportModeCmd__position,  // size() function pointer
    unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__get_const_function__SportModeCmd__position,  // get_const(index) function pointer
    unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__get_function__SportModeCmd__position,  // get(index) function pointer
    unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__fetch_function__SportModeCmd__position,  // fetch(index, &value) function pointer
    unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__assign_function__SportModeCmd__position,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "euler",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__SportModeCmd, euler),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__size_function__SportModeCmd__euler,  // size() function pointer
    unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__get_const_function__SportModeCmd__euler,  // get_const(index) function pointer
    unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__get_function__SportModeCmd__euler,  // get(index) function pointer
    unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__fetch_function__SportModeCmd__euler,  // fetch(index, &value) function pointer
    unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__assign_function__SportModeCmd__euler,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "velocity",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    2,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__SportModeCmd, velocity),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__size_function__SportModeCmd__velocity,  // size() function pointer
    unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__get_const_function__SportModeCmd__velocity,  // get_const(index) function pointer
    unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__get_function__SportModeCmd__velocity,  // get(index) function pointer
    unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__fetch_function__SportModeCmd__velocity,  // fetch(index, &value) function pointer
    unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__assign_function__SportModeCmd__velocity,  // assign(index, value) function pointer
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
    offsetof(unitree_go__msg__SportModeCmd, yaw_speed),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
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
    offsetof(unitree_go__msg__SportModeCmd, bms_cmd),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "path_point",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    30,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__SportModeCmd, path_point),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__size_function__SportModeCmd__path_point,  // size() function pointer
    unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__get_const_function__SportModeCmd__path_point,  // get_const(index) function pointer
    unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__get_function__SportModeCmd__path_point,  // get(index) function pointer
    unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__fetch_function__SportModeCmd__path_point,  // fetch(index, &value) function pointer
    unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__assign_function__SportModeCmd__path_point,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__SportModeCmd_message_members = {
  "unitree_go__msg",  // message namespace
  "SportModeCmd",  // message name
  11,  // number of fields
  sizeof(unitree_go__msg__SportModeCmd),
  unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__SportModeCmd_message_member_array,  // message members
  unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__SportModeCmd_init_function,  // function to initialize message memory (memory has to be allocated)
  unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__SportModeCmd_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__SportModeCmd_message_type_support_handle = {
  0,
  &unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__SportModeCmd_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_unitree_go
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unitree_go, msg, SportModeCmd)() {
  unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__SportModeCmd_message_member_array[9].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unitree_go, msg, BmsCmd)();
  unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__SportModeCmd_message_member_array[10].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unitree_go, msg, PathPoint)();
  if (!unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__SportModeCmd_message_type_support_handle.typesupport_identifier) {
    unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__SportModeCmd_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &unitree_go__msg__SportModeCmd__rosidl_typesupport_introspection_c__SportModeCmd_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
