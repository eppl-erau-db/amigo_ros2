// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from unitree_api:msg/Response.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "unitree_api/msg/detail/response__rosidl_typesupport_introspection_c.h"
#include "unitree_api/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "unitree_api/msg/detail/response__functions.h"
#include "unitree_api/msg/detail/response__struct.h"


// Include directives for member types
// Member `header`
#include "unitree_api/msg/response_header.h"
// Member `header`
#include "unitree_api/msg/detail/response_header__rosidl_typesupport_introspection_c.h"
// Member `data`
#include "rosidl_runtime_c/string_functions.h"
// Member `binary`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void unitree_api__msg__Response__rosidl_typesupport_introspection_c__Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  unitree_api__msg__Response__init(message_memory);
}

void unitree_api__msg__Response__rosidl_typesupport_introspection_c__Response_fini_function(void * message_memory)
{
  unitree_api__msg__Response__fini(message_memory);
}

size_t unitree_api__msg__Response__rosidl_typesupport_introspection_c__size_function__Response__binary(
  const void * untyped_member)
{
  const rosidl_runtime_c__int8__Sequence * member =
    (const rosidl_runtime_c__int8__Sequence *)(untyped_member);
  return member->size;
}

const void * unitree_api__msg__Response__rosidl_typesupport_introspection_c__get_const_function__Response__binary(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__int8__Sequence * member =
    (const rosidl_runtime_c__int8__Sequence *)(untyped_member);
  return &member->data[index];
}

void * unitree_api__msg__Response__rosidl_typesupport_introspection_c__get_function__Response__binary(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__int8__Sequence * member =
    (rosidl_runtime_c__int8__Sequence *)(untyped_member);
  return &member->data[index];
}

void unitree_api__msg__Response__rosidl_typesupport_introspection_c__fetch_function__Response__binary(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const int8_t * item =
    ((const int8_t *)
    unitree_api__msg__Response__rosidl_typesupport_introspection_c__get_const_function__Response__binary(untyped_member, index));
  int8_t * value =
    (int8_t *)(untyped_value);
  *value = *item;
}

void unitree_api__msg__Response__rosidl_typesupport_introspection_c__assign_function__Response__binary(
  void * untyped_member, size_t index, const void * untyped_value)
{
  int8_t * item =
    ((int8_t *)
    unitree_api__msg__Response__rosidl_typesupport_introspection_c__get_function__Response__binary(untyped_member, index));
  const int8_t * value =
    (const int8_t *)(untyped_value);
  *item = *value;
}

bool unitree_api__msg__Response__rosidl_typesupport_introspection_c__resize_function__Response__binary(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__int8__Sequence * member =
    (rosidl_runtime_c__int8__Sequence *)(untyped_member);
  rosidl_runtime_c__int8__Sequence__fini(member);
  return rosidl_runtime_c__int8__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember unitree_api__msg__Response__rosidl_typesupport_introspection_c__Response_message_member_array[3] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_api__msg__Response, header),  // bytes offset in struct
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
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_api__msg__Response, data),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "binary",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_api__msg__Response, binary),  // bytes offset in struct
    NULL,  // default value
    unitree_api__msg__Response__rosidl_typesupport_introspection_c__size_function__Response__binary,  // size() function pointer
    unitree_api__msg__Response__rosidl_typesupport_introspection_c__get_const_function__Response__binary,  // get_const(index) function pointer
    unitree_api__msg__Response__rosidl_typesupport_introspection_c__get_function__Response__binary,  // get(index) function pointer
    unitree_api__msg__Response__rosidl_typesupport_introspection_c__fetch_function__Response__binary,  // fetch(index, &value) function pointer
    unitree_api__msg__Response__rosidl_typesupport_introspection_c__assign_function__Response__binary,  // assign(index, value) function pointer
    unitree_api__msg__Response__rosidl_typesupport_introspection_c__resize_function__Response__binary  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers unitree_api__msg__Response__rosidl_typesupport_introspection_c__Response_message_members = {
  "unitree_api__msg",  // message namespace
  "Response",  // message name
  3,  // number of fields
  sizeof(unitree_api__msg__Response),
  unitree_api__msg__Response__rosidl_typesupport_introspection_c__Response_message_member_array,  // message members
  unitree_api__msg__Response__rosidl_typesupport_introspection_c__Response_init_function,  // function to initialize message memory (memory has to be allocated)
  unitree_api__msg__Response__rosidl_typesupport_introspection_c__Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t unitree_api__msg__Response__rosidl_typesupport_introspection_c__Response_message_type_support_handle = {
  0,
  &unitree_api__msg__Response__rosidl_typesupport_introspection_c__Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_unitree_api
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unitree_api, msg, Response)() {
  unitree_api__msg__Response__rosidl_typesupport_introspection_c__Response_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unitree_api, msg, ResponseHeader)();
  if (!unitree_api__msg__Response__rosidl_typesupport_introspection_c__Response_message_type_support_handle.typesupport_identifier) {
    unitree_api__msg__Response__rosidl_typesupport_introspection_c__Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &unitree_api__msg__Response__rosidl_typesupport_introspection_c__Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
