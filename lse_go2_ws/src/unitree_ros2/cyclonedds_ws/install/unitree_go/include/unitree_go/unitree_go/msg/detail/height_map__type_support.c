// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from unitree_go:msg/HeightMap.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "unitree_go/msg/detail/height_map__rosidl_typesupport_introspection_c.h"
#include "unitree_go/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "unitree_go/msg/detail/height_map__functions.h"
#include "unitree_go/msg/detail/height_map__struct.h"


// Include directives for member types
// Member `frame_id`
#include "rosidl_runtime_c/string_functions.h"
// Member `data`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__HeightMap_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  unitree_go__msg__HeightMap__init(message_memory);
}

void unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__HeightMap_fini_function(void * message_memory)
{
  unitree_go__msg__HeightMap__fini(message_memory);
}

size_t unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__size_function__HeightMap__origin(
  const void * untyped_member)
{
  (void)untyped_member;
  return 2;
}

const void * unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__get_const_function__HeightMap__origin(
  const void * untyped_member, size_t index)
{
  const float * member =
    (const float *)(untyped_member);
  return &member[index];
}

void * unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__get_function__HeightMap__origin(
  void * untyped_member, size_t index)
{
  float * member =
    (float *)(untyped_member);
  return &member[index];
}

void unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__fetch_function__HeightMap__origin(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__get_const_function__HeightMap__origin(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__assign_function__HeightMap__origin(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__get_function__HeightMap__origin(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

size_t unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__size_function__HeightMap__data(
  const void * untyped_member)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return member->size;
}

const void * unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__get_const_function__HeightMap__data(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void * unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__get_function__HeightMap__data(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__fetch_function__HeightMap__data(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__get_const_function__HeightMap__data(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__assign_function__HeightMap__data(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__get_function__HeightMap__data(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

bool unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__resize_function__HeightMap__data(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  rosidl_runtime_c__float__Sequence__fini(member);
  return rosidl_runtime_c__float__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__HeightMap_message_member_array[7] = {
  {
    "stamp",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__HeightMap, stamp),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "frame_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__HeightMap, frame_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "resolution",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__HeightMap, resolution),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "width",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__HeightMap, width),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "height",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__HeightMap, height),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "origin",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    2,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__HeightMap, origin),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__size_function__HeightMap__origin,  // size() function pointer
    unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__get_const_function__HeightMap__origin,  // get_const(index) function pointer
    unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__get_function__HeightMap__origin,  // get(index) function pointer
    unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__fetch_function__HeightMap__origin,  // fetch(index, &value) function pointer
    unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__assign_function__HeightMap__origin,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "data",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__HeightMap, data),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__size_function__HeightMap__data,  // size() function pointer
    unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__get_const_function__HeightMap__data,  // get_const(index) function pointer
    unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__get_function__HeightMap__data,  // get(index) function pointer
    unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__fetch_function__HeightMap__data,  // fetch(index, &value) function pointer
    unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__assign_function__HeightMap__data,  // assign(index, value) function pointer
    unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__resize_function__HeightMap__data  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__HeightMap_message_members = {
  "unitree_go__msg",  // message namespace
  "HeightMap",  // message name
  7,  // number of fields
  sizeof(unitree_go__msg__HeightMap),
  unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__HeightMap_message_member_array,  // message members
  unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__HeightMap_init_function,  // function to initialize message memory (memory has to be allocated)
  unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__HeightMap_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__HeightMap_message_type_support_handle = {
  0,
  &unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__HeightMap_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_unitree_go
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unitree_go, msg, HeightMap)() {
  if (!unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__HeightMap_message_type_support_handle.typesupport_identifier) {
    unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__HeightMap_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &unitree_go__msg__HeightMap__rosidl_typesupport_introspection_c__HeightMap_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
