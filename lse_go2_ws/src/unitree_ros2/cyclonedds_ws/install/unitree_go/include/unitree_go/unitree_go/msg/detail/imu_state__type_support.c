// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from unitree_go:msg/IMUState.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "unitree_go/msg/detail/imu_state__rosidl_typesupport_introspection_c.h"
#include "unitree_go/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "unitree_go/msg/detail/imu_state__functions.h"
#include "unitree_go/msg/detail/imu_state__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__IMUState_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  unitree_go__msg__IMUState__init(message_memory);
}

void unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__IMUState_fini_function(void * message_memory)
{
  unitree_go__msg__IMUState__fini(message_memory);
}

size_t unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__size_function__IMUState__quaternion(
  const void * untyped_member)
{
  (void)untyped_member;
  return 4;
}

const void * unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__get_const_function__IMUState__quaternion(
  const void * untyped_member, size_t index)
{
  const float * member =
    (const float *)(untyped_member);
  return &member[index];
}

void * unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__get_function__IMUState__quaternion(
  void * untyped_member, size_t index)
{
  float * member =
    (float *)(untyped_member);
  return &member[index];
}

void unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__fetch_function__IMUState__quaternion(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__get_const_function__IMUState__quaternion(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__assign_function__IMUState__quaternion(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__get_function__IMUState__quaternion(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

size_t unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__size_function__IMUState__gyroscope(
  const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__get_const_function__IMUState__gyroscope(
  const void * untyped_member, size_t index)
{
  const float * member =
    (const float *)(untyped_member);
  return &member[index];
}

void * unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__get_function__IMUState__gyroscope(
  void * untyped_member, size_t index)
{
  float * member =
    (float *)(untyped_member);
  return &member[index];
}

void unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__fetch_function__IMUState__gyroscope(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__get_const_function__IMUState__gyroscope(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__assign_function__IMUState__gyroscope(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__get_function__IMUState__gyroscope(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

size_t unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__size_function__IMUState__accelerometer(
  const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__get_const_function__IMUState__accelerometer(
  const void * untyped_member, size_t index)
{
  const float * member =
    (const float *)(untyped_member);
  return &member[index];
}

void * unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__get_function__IMUState__accelerometer(
  void * untyped_member, size_t index)
{
  float * member =
    (float *)(untyped_member);
  return &member[index];
}

void unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__fetch_function__IMUState__accelerometer(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__get_const_function__IMUState__accelerometer(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__assign_function__IMUState__accelerometer(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__get_function__IMUState__accelerometer(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

size_t unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__size_function__IMUState__rpy(
  const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__get_const_function__IMUState__rpy(
  const void * untyped_member, size_t index)
{
  const float * member =
    (const float *)(untyped_member);
  return &member[index];
}

void * unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__get_function__IMUState__rpy(
  void * untyped_member, size_t index)
{
  float * member =
    (float *)(untyped_member);
  return &member[index];
}

void unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__fetch_function__IMUState__rpy(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__get_const_function__IMUState__rpy(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__assign_function__IMUState__rpy(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__get_function__IMUState__rpy(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

static rosidl_typesupport_introspection_c__MessageMember unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__IMUState_message_member_array[5] = {
  {
    "quaternion",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    4,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__IMUState, quaternion),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__size_function__IMUState__quaternion,  // size() function pointer
    unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__get_const_function__IMUState__quaternion,  // get_const(index) function pointer
    unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__get_function__IMUState__quaternion,  // get(index) function pointer
    unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__fetch_function__IMUState__quaternion,  // fetch(index, &value) function pointer
    unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__assign_function__IMUState__quaternion,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "gyroscope",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__IMUState, gyroscope),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__size_function__IMUState__gyroscope,  // size() function pointer
    unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__get_const_function__IMUState__gyroscope,  // get_const(index) function pointer
    unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__get_function__IMUState__gyroscope,  // get(index) function pointer
    unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__fetch_function__IMUState__gyroscope,  // fetch(index, &value) function pointer
    unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__assign_function__IMUState__gyroscope,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "accelerometer",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__IMUState, accelerometer),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__size_function__IMUState__accelerometer,  // size() function pointer
    unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__get_const_function__IMUState__accelerometer,  // get_const(index) function pointer
    unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__get_function__IMUState__accelerometer,  // get(index) function pointer
    unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__fetch_function__IMUState__accelerometer,  // fetch(index, &value) function pointer
    unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__assign_function__IMUState__accelerometer,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "rpy",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__IMUState, rpy),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__size_function__IMUState__rpy,  // size() function pointer
    unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__get_const_function__IMUState__rpy,  // get_const(index) function pointer
    unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__get_function__IMUState__rpy,  // get(index) function pointer
    unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__fetch_function__IMUState__rpy,  // fetch(index, &value) function pointer
    unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__assign_function__IMUState__rpy,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "temperature",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__IMUState, temperature),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__IMUState_message_members = {
  "unitree_go__msg",  // message namespace
  "IMUState",  // message name
  5,  // number of fields
  sizeof(unitree_go__msg__IMUState),
  unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__IMUState_message_member_array,  // message members
  unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__IMUState_init_function,  // function to initialize message memory (memory has to be allocated)
  unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__IMUState_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__IMUState_message_type_support_handle = {
  0,
  &unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__IMUState_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_unitree_go
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unitree_go, msg, IMUState)() {
  if (!unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__IMUState_message_type_support_handle.typesupport_identifier) {
    unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__IMUState_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &unitree_go__msg__IMUState__rosidl_typesupport_introspection_c__IMUState_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
