// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from unitree_go:msg/Go2FrontVideoData.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "unitree_go/msg/detail/go2_front_video_data__rosidl_typesupport_introspection_c.h"
#include "unitree_go/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "unitree_go/msg/detail/go2_front_video_data__functions.h"
#include "unitree_go/msg/detail/go2_front_video_data__struct.h"


// Include directives for member types
// Member `video720p`
// Member `video360p`
// Member `video180p`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__Go2FrontVideoData_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  unitree_go__msg__Go2FrontVideoData__init(message_memory);
}

void unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__Go2FrontVideoData_fini_function(void * message_memory)
{
  unitree_go__msg__Go2FrontVideoData__fini(message_memory);
}

size_t unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__size_function__Go2FrontVideoData__video720p(
  const void * untyped_member)
{
  const rosidl_runtime_c__uint8__Sequence * member =
    (const rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return member->size;
}

const void * unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__get_const_function__Go2FrontVideoData__video720p(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__uint8__Sequence * member =
    (const rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return &member->data[index];
}

void * unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__get_function__Go2FrontVideoData__video720p(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__uint8__Sequence * member =
    (rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return &member->data[index];
}

void unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__fetch_function__Go2FrontVideoData__video720p(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint8_t * item =
    ((const uint8_t *)
    unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__get_const_function__Go2FrontVideoData__video720p(untyped_member, index));
  uint8_t * value =
    (uint8_t *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__assign_function__Go2FrontVideoData__video720p(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint8_t * item =
    ((uint8_t *)
    unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__get_function__Go2FrontVideoData__video720p(untyped_member, index));
  const uint8_t * value =
    (const uint8_t *)(untyped_value);
  *item = *value;
}

bool unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__resize_function__Go2FrontVideoData__video720p(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__uint8__Sequence * member =
    (rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  rosidl_runtime_c__uint8__Sequence__fini(member);
  return rosidl_runtime_c__uint8__Sequence__init(member, size);
}

size_t unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__size_function__Go2FrontVideoData__video360p(
  const void * untyped_member)
{
  const rosidl_runtime_c__uint8__Sequence * member =
    (const rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return member->size;
}

const void * unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__get_const_function__Go2FrontVideoData__video360p(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__uint8__Sequence * member =
    (const rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return &member->data[index];
}

void * unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__get_function__Go2FrontVideoData__video360p(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__uint8__Sequence * member =
    (rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return &member->data[index];
}

void unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__fetch_function__Go2FrontVideoData__video360p(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint8_t * item =
    ((const uint8_t *)
    unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__get_const_function__Go2FrontVideoData__video360p(untyped_member, index));
  uint8_t * value =
    (uint8_t *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__assign_function__Go2FrontVideoData__video360p(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint8_t * item =
    ((uint8_t *)
    unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__get_function__Go2FrontVideoData__video360p(untyped_member, index));
  const uint8_t * value =
    (const uint8_t *)(untyped_value);
  *item = *value;
}

bool unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__resize_function__Go2FrontVideoData__video360p(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__uint8__Sequence * member =
    (rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  rosidl_runtime_c__uint8__Sequence__fini(member);
  return rosidl_runtime_c__uint8__Sequence__init(member, size);
}

size_t unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__size_function__Go2FrontVideoData__video180p(
  const void * untyped_member)
{
  const rosidl_runtime_c__uint8__Sequence * member =
    (const rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return member->size;
}

const void * unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__get_const_function__Go2FrontVideoData__video180p(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__uint8__Sequence * member =
    (const rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return &member->data[index];
}

void * unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__get_function__Go2FrontVideoData__video180p(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__uint8__Sequence * member =
    (rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return &member->data[index];
}

void unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__fetch_function__Go2FrontVideoData__video180p(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint8_t * item =
    ((const uint8_t *)
    unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__get_const_function__Go2FrontVideoData__video180p(untyped_member, index));
  uint8_t * value =
    (uint8_t *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__assign_function__Go2FrontVideoData__video180p(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint8_t * item =
    ((uint8_t *)
    unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__get_function__Go2FrontVideoData__video180p(untyped_member, index));
  const uint8_t * value =
    (const uint8_t *)(untyped_value);
  *item = *value;
}

bool unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__resize_function__Go2FrontVideoData__video180p(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__uint8__Sequence * member =
    (rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  rosidl_runtime_c__uint8__Sequence__fini(member);
  return rosidl_runtime_c__uint8__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__Go2FrontVideoData_message_member_array[4] = {
  {
    "time_frame",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT64,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__Go2FrontVideoData, time_frame),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "video720p",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__Go2FrontVideoData, video720p),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__size_function__Go2FrontVideoData__video720p,  // size() function pointer
    unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__get_const_function__Go2FrontVideoData__video720p,  // get_const(index) function pointer
    unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__get_function__Go2FrontVideoData__video720p,  // get(index) function pointer
    unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__fetch_function__Go2FrontVideoData__video720p,  // fetch(index, &value) function pointer
    unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__assign_function__Go2FrontVideoData__video720p,  // assign(index, value) function pointer
    unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__resize_function__Go2FrontVideoData__video720p  // resize(index) function pointer
  },
  {
    "video360p",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__Go2FrontVideoData, video360p),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__size_function__Go2FrontVideoData__video360p,  // size() function pointer
    unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__get_const_function__Go2FrontVideoData__video360p,  // get_const(index) function pointer
    unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__get_function__Go2FrontVideoData__video360p,  // get(index) function pointer
    unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__fetch_function__Go2FrontVideoData__video360p,  // fetch(index, &value) function pointer
    unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__assign_function__Go2FrontVideoData__video360p,  // assign(index, value) function pointer
    unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__resize_function__Go2FrontVideoData__video360p  // resize(index) function pointer
  },
  {
    "video180p",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__Go2FrontVideoData, video180p),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__size_function__Go2FrontVideoData__video180p,  // size() function pointer
    unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__get_const_function__Go2FrontVideoData__video180p,  // get_const(index) function pointer
    unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__get_function__Go2FrontVideoData__video180p,  // get(index) function pointer
    unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__fetch_function__Go2FrontVideoData__video180p,  // fetch(index, &value) function pointer
    unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__assign_function__Go2FrontVideoData__video180p,  // assign(index, value) function pointer
    unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__resize_function__Go2FrontVideoData__video180p  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__Go2FrontVideoData_message_members = {
  "unitree_go__msg",  // message namespace
  "Go2FrontVideoData",  // message name
  4,  // number of fields
  sizeof(unitree_go__msg__Go2FrontVideoData),
  unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__Go2FrontVideoData_message_member_array,  // message members
  unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__Go2FrontVideoData_init_function,  // function to initialize message memory (memory has to be allocated)
  unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__Go2FrontVideoData_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__Go2FrontVideoData_message_type_support_handle = {
  0,
  &unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__Go2FrontVideoData_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_unitree_go
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unitree_go, msg, Go2FrontVideoData)() {
  if (!unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__Go2FrontVideoData_message_type_support_handle.typesupport_identifier) {
    unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__Go2FrontVideoData_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &unitree_go__msg__Go2FrontVideoData__rosidl_typesupport_introspection_c__Go2FrontVideoData_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
