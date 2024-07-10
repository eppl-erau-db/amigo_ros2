// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from unitree_api:msg/Request.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "unitree_api/msg/detail/request__rosidl_typesupport_introspection_c.h"
#include "unitree_api/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "unitree_api/msg/detail/request__functions.h"
#include "unitree_api/msg/detail/request__struct.h"


// Include directives for member types
// Member `header`
#include "unitree_api/msg/request_header.h"
// Member `header`
#include "unitree_api/msg/detail/request_header__rosidl_typesupport_introspection_c.h"
// Member `parameter`
#include "rosidl_runtime_c/string_functions.h"
// Member `binary`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void unitree_api__msg__Request__rosidl_typesupport_introspection_c__Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  unitree_api__msg__Request__init(message_memory);
}

void unitree_api__msg__Request__rosidl_typesupport_introspection_c__Request_fini_function(void * message_memory)
{
  unitree_api__msg__Request__fini(message_memory);
}

size_t unitree_api__msg__Request__rosidl_typesupport_introspection_c__size_function__Request__binary(
  const void * untyped_member)
{
  const rosidl_runtime_c__uint8__Sequence * member =
    (const rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return member->size;
}

const void * unitree_api__msg__Request__rosidl_typesupport_introspection_c__get_const_function__Request__binary(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__uint8__Sequence * member =
    (const rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return &member->data[index];
}

void * unitree_api__msg__Request__rosidl_typesupport_introspection_c__get_function__Request__binary(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__uint8__Sequence * member =
    (rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return &member->data[index];
}

void unitree_api__msg__Request__rosidl_typesupport_introspection_c__fetch_function__Request__binary(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint8_t * item =
    ((const uint8_t *)
    unitree_api__msg__Request__rosidl_typesupport_introspection_c__get_const_function__Request__binary(untyped_member, index));
  uint8_t * value =
    (uint8_t *)(untyped_value);
  *value = *item;
}

void unitree_api__msg__Request__rosidl_typesupport_introspection_c__assign_function__Request__binary(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint8_t * item =
    ((uint8_t *)
    unitree_api__msg__Request__rosidl_typesupport_introspection_c__get_function__Request__binary(untyped_member, index));
  const uint8_t * value =
    (const uint8_t *)(untyped_value);
  *item = *value;
}

bool unitree_api__msg__Request__rosidl_typesupport_introspection_c__resize_function__Request__binary(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__uint8__Sequence * member =
    (rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  rosidl_runtime_c__uint8__Sequence__fini(member);
  return rosidl_runtime_c__uint8__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember unitree_api__msg__Request__rosidl_typesupport_introspection_c__Request_message_member_array[3] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_api__msg__Request, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "parameter",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_api__msg__Request, parameter),  // bytes offset in struct
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
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_api__msg__Request, binary),  // bytes offset in struct
    NULL,  // default value
    unitree_api__msg__Request__rosidl_typesupport_introspection_c__size_function__Request__binary,  // size() function pointer
    unitree_api__msg__Request__rosidl_typesupport_introspection_c__get_const_function__Request__binary,  // get_const(index) function pointer
    unitree_api__msg__Request__rosidl_typesupport_introspection_c__get_function__Request__binary,  // get(index) function pointer
    unitree_api__msg__Request__rosidl_typesupport_introspection_c__fetch_function__Request__binary,  // fetch(index, &value) function pointer
    unitree_api__msg__Request__rosidl_typesupport_introspection_c__assign_function__Request__binary,  // assign(index, value) function pointer
    unitree_api__msg__Request__rosidl_typesupport_introspection_c__resize_function__Request__binary  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers unitree_api__msg__Request__rosidl_typesupport_introspection_c__Request_message_members = {
  "unitree_api__msg",  // message namespace
  "Request",  // message name
  3,  // number of fields
  sizeof(unitree_api__msg__Request),
  unitree_api__msg__Request__rosidl_typesupport_introspection_c__Request_message_member_array,  // message members
  unitree_api__msg__Request__rosidl_typesupport_introspection_c__Request_init_function,  // function to initialize message memory (memory has to be allocated)
  unitree_api__msg__Request__rosidl_typesupport_introspection_c__Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t unitree_api__msg__Request__rosidl_typesupport_introspection_c__Request_message_type_support_handle = {
  0,
  &unitree_api__msg__Request__rosidl_typesupport_introspection_c__Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_unitree_api
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unitree_api, msg, Request)() {
  unitree_api__msg__Request__rosidl_typesupport_introspection_c__Request_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unitree_api, msg, RequestHeader)();
  if (!unitree_api__msg__Request__rosidl_typesupport_introspection_c__Request_message_type_support_handle.typesupport_identifier) {
    unitree_api__msg__Request__rosidl_typesupport_introspection_c__Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &unitree_api__msg__Request__rosidl_typesupport_introspection_c__Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
