// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from realsense2_camera_msgs:msg/IMUInfo.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "realsense2_camera_msgs/msg/detail/imu_info__rosidl_typesupport_introspection_c.h"
#include "realsense2_camera_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "realsense2_camera_msgs/msg/detail/imu_info__functions.h"
#include "realsense2_camera_msgs/msg/detail/imu_info__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__IMUInfo_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  realsense2_camera_msgs__msg__IMUInfo__init(message_memory);
}

void realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__IMUInfo_fini_function(void * message_memory)
{
  realsense2_camera_msgs__msg__IMUInfo__fini(message_memory);
}

size_t realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__size_function__IMUInfo__data(
  const void * untyped_member)
{
  (void)untyped_member;
  return 12;
}

const void * realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__get_const_function__IMUInfo__data(
  const void * untyped_member, size_t index)
{
  const double * member =
    (const double *)(untyped_member);
  return &member[index];
}

void * realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__get_function__IMUInfo__data(
  void * untyped_member, size_t index)
{
  double * member =
    (double *)(untyped_member);
  return &member[index];
}

void realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__fetch_function__IMUInfo__data(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__get_const_function__IMUInfo__data(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__assign_function__IMUInfo__data(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__get_function__IMUInfo__data(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

size_t realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__size_function__IMUInfo__noise_variances(
  const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__get_const_function__IMUInfo__noise_variances(
  const void * untyped_member, size_t index)
{
  const double * member =
    (const double *)(untyped_member);
  return &member[index];
}

void * realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__get_function__IMUInfo__noise_variances(
  void * untyped_member, size_t index)
{
  double * member =
    (double *)(untyped_member);
  return &member[index];
}

void realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__fetch_function__IMUInfo__noise_variances(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__get_const_function__IMUInfo__noise_variances(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__assign_function__IMUInfo__noise_variances(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__get_function__IMUInfo__noise_variances(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

size_t realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__size_function__IMUInfo__bias_variances(
  const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__get_const_function__IMUInfo__bias_variances(
  const void * untyped_member, size_t index)
{
  const double * member =
    (const double *)(untyped_member);
  return &member[index];
}

void * realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__get_function__IMUInfo__bias_variances(
  void * untyped_member, size_t index)
{
  double * member =
    (double *)(untyped_member);
  return &member[index];
}

void realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__fetch_function__IMUInfo__bias_variances(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__get_const_function__IMUInfo__bias_variances(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__assign_function__IMUInfo__bias_variances(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__get_function__IMUInfo__bias_variances(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

static rosidl_typesupport_introspection_c__MessageMember realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__IMUInfo_message_member_array[4] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(realsense2_camera_msgs__msg__IMUInfo, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "data",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    12,  // array size
    false,  // is upper bound
    offsetof(realsense2_camera_msgs__msg__IMUInfo, data),  // bytes offset in struct
    NULL,  // default value
    realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__size_function__IMUInfo__data,  // size() function pointer
    realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__get_const_function__IMUInfo__data,  // get_const(index) function pointer
    realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__get_function__IMUInfo__data,  // get(index) function pointer
    realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__fetch_function__IMUInfo__data,  // fetch(index, &value) function pointer
    realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__assign_function__IMUInfo__data,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "noise_variances",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(realsense2_camera_msgs__msg__IMUInfo, noise_variances),  // bytes offset in struct
    NULL,  // default value
    realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__size_function__IMUInfo__noise_variances,  // size() function pointer
    realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__get_const_function__IMUInfo__noise_variances,  // get_const(index) function pointer
    realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__get_function__IMUInfo__noise_variances,  // get(index) function pointer
    realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__fetch_function__IMUInfo__noise_variances,  // fetch(index, &value) function pointer
    realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__assign_function__IMUInfo__noise_variances,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "bias_variances",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(realsense2_camera_msgs__msg__IMUInfo, bias_variances),  // bytes offset in struct
    NULL,  // default value
    realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__size_function__IMUInfo__bias_variances,  // size() function pointer
    realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__get_const_function__IMUInfo__bias_variances,  // get_const(index) function pointer
    realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__get_function__IMUInfo__bias_variances,  // get(index) function pointer
    realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__fetch_function__IMUInfo__bias_variances,  // fetch(index, &value) function pointer
    realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__assign_function__IMUInfo__bias_variances,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__IMUInfo_message_members = {
  "realsense2_camera_msgs__msg",  // message namespace
  "IMUInfo",  // message name
  4,  // number of fields
  sizeof(realsense2_camera_msgs__msg__IMUInfo),
  realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__IMUInfo_message_member_array,  // message members
  realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__IMUInfo_init_function,  // function to initialize message memory (memory has to be allocated)
  realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__IMUInfo_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__IMUInfo_message_type_support_handle = {
  0,
  &realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__IMUInfo_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_realsense2_camera_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, realsense2_camera_msgs, msg, IMUInfo)() {
  realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__IMUInfo_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  if (!realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__IMUInfo_message_type_support_handle.typesupport_identifier) {
    realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__IMUInfo_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &realsense2_camera_msgs__msg__IMUInfo__rosidl_typesupport_introspection_c__IMUInfo_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
