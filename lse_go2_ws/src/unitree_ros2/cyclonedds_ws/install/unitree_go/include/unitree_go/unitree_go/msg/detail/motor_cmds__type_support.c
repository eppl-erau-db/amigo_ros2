// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from unitree_go:msg/MotorCmds.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "unitree_go/msg/detail/motor_cmds__rosidl_typesupport_introspection_c.h"
#include "unitree_go/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "unitree_go/msg/detail/motor_cmds__functions.h"
#include "unitree_go/msg/detail/motor_cmds__struct.h"


// Include directives for member types
// Member `cmds`
#include "unitree_go/msg/motor_cmd.h"
// Member `cmds`
#include "unitree_go/msg/detail/motor_cmd__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void unitree_go__msg__MotorCmds__rosidl_typesupport_introspection_c__MotorCmds_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  unitree_go__msg__MotorCmds__init(message_memory);
}

void unitree_go__msg__MotorCmds__rosidl_typesupport_introspection_c__MotorCmds_fini_function(void * message_memory)
{
  unitree_go__msg__MotorCmds__fini(message_memory);
}

size_t unitree_go__msg__MotorCmds__rosidl_typesupport_introspection_c__size_function__MotorCmds__cmds(
  const void * untyped_member)
{
  const unitree_go__msg__MotorCmd__Sequence * member =
    (const unitree_go__msg__MotorCmd__Sequence *)(untyped_member);
  return member->size;
}

const void * unitree_go__msg__MotorCmds__rosidl_typesupport_introspection_c__get_const_function__MotorCmds__cmds(
  const void * untyped_member, size_t index)
{
  const unitree_go__msg__MotorCmd__Sequence * member =
    (const unitree_go__msg__MotorCmd__Sequence *)(untyped_member);
  return &member->data[index];
}

void * unitree_go__msg__MotorCmds__rosidl_typesupport_introspection_c__get_function__MotorCmds__cmds(
  void * untyped_member, size_t index)
{
  unitree_go__msg__MotorCmd__Sequence * member =
    (unitree_go__msg__MotorCmd__Sequence *)(untyped_member);
  return &member->data[index];
}

void unitree_go__msg__MotorCmds__rosidl_typesupport_introspection_c__fetch_function__MotorCmds__cmds(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const unitree_go__msg__MotorCmd * item =
    ((const unitree_go__msg__MotorCmd *)
    unitree_go__msg__MotorCmds__rosidl_typesupport_introspection_c__get_const_function__MotorCmds__cmds(untyped_member, index));
  unitree_go__msg__MotorCmd * value =
    (unitree_go__msg__MotorCmd *)(untyped_value);
  *value = *item;
}

void unitree_go__msg__MotorCmds__rosidl_typesupport_introspection_c__assign_function__MotorCmds__cmds(
  void * untyped_member, size_t index, const void * untyped_value)
{
  unitree_go__msg__MotorCmd * item =
    ((unitree_go__msg__MotorCmd *)
    unitree_go__msg__MotorCmds__rosidl_typesupport_introspection_c__get_function__MotorCmds__cmds(untyped_member, index));
  const unitree_go__msg__MotorCmd * value =
    (const unitree_go__msg__MotorCmd *)(untyped_value);
  *item = *value;
}

bool unitree_go__msg__MotorCmds__rosidl_typesupport_introspection_c__resize_function__MotorCmds__cmds(
  void * untyped_member, size_t size)
{
  unitree_go__msg__MotorCmd__Sequence * member =
    (unitree_go__msg__MotorCmd__Sequence *)(untyped_member);
  unitree_go__msg__MotorCmd__Sequence__fini(member);
  return unitree_go__msg__MotorCmd__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember unitree_go__msg__MotorCmds__rosidl_typesupport_introspection_c__MotorCmds_message_member_array[1] = {
  {
    "cmds",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go__msg__MotorCmds, cmds),  // bytes offset in struct
    NULL,  // default value
    unitree_go__msg__MotorCmds__rosidl_typesupport_introspection_c__size_function__MotorCmds__cmds,  // size() function pointer
    unitree_go__msg__MotorCmds__rosidl_typesupport_introspection_c__get_const_function__MotorCmds__cmds,  // get_const(index) function pointer
    unitree_go__msg__MotorCmds__rosidl_typesupport_introspection_c__get_function__MotorCmds__cmds,  // get(index) function pointer
    unitree_go__msg__MotorCmds__rosidl_typesupport_introspection_c__fetch_function__MotorCmds__cmds,  // fetch(index, &value) function pointer
    unitree_go__msg__MotorCmds__rosidl_typesupport_introspection_c__assign_function__MotorCmds__cmds,  // assign(index, value) function pointer
    unitree_go__msg__MotorCmds__rosidl_typesupport_introspection_c__resize_function__MotorCmds__cmds  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers unitree_go__msg__MotorCmds__rosidl_typesupport_introspection_c__MotorCmds_message_members = {
  "unitree_go__msg",  // message namespace
  "MotorCmds",  // message name
  1,  // number of fields
  sizeof(unitree_go__msg__MotorCmds),
  unitree_go__msg__MotorCmds__rosidl_typesupport_introspection_c__MotorCmds_message_member_array,  // message members
  unitree_go__msg__MotorCmds__rosidl_typesupport_introspection_c__MotorCmds_init_function,  // function to initialize message memory (memory has to be allocated)
  unitree_go__msg__MotorCmds__rosidl_typesupport_introspection_c__MotorCmds_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t unitree_go__msg__MotorCmds__rosidl_typesupport_introspection_c__MotorCmds_message_type_support_handle = {
  0,
  &unitree_go__msg__MotorCmds__rosidl_typesupport_introspection_c__MotorCmds_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_unitree_go
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unitree_go, msg, MotorCmds)() {
  unitree_go__msg__MotorCmds__rosidl_typesupport_introspection_c__MotorCmds_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unitree_go, msg, MotorCmd)();
  if (!unitree_go__msg__MotorCmds__rosidl_typesupport_introspection_c__MotorCmds_message_type_support_handle.typesupport_identifier) {
    unitree_go__msg__MotorCmds__rosidl_typesupport_introspection_c__MotorCmds_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &unitree_go__msg__MotorCmds__rosidl_typesupport_introspection_c__MotorCmds_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
