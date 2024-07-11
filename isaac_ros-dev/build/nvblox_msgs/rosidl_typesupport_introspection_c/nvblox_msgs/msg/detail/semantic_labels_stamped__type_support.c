// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from nvblox_msgs:msg/SemanticLabelsStamped.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "nvblox_msgs/msg/detail/semantic_labels_stamped__rosidl_typesupport_introspection_c.h"
#include "nvblox_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "nvblox_msgs/msg/detail/semantic_labels_stamped__functions.h"
#include "nvblox_msgs/msg/detail/semantic_labels_stamped__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `labels`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void nvblox_msgs__msg__SemanticLabelsStamped__rosidl_typesupport_introspection_c__SemanticLabelsStamped_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  nvblox_msgs__msg__SemanticLabelsStamped__init(message_memory);
}

void nvblox_msgs__msg__SemanticLabelsStamped__rosidl_typesupport_introspection_c__SemanticLabelsStamped_fini_function(void * message_memory)
{
  nvblox_msgs__msg__SemanticLabelsStamped__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember nvblox_msgs__msg__SemanticLabelsStamped__rosidl_typesupport_introspection_c__SemanticLabelsStamped_message_member_array[2] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(nvblox_msgs__msg__SemanticLabelsStamped, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "labels",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(nvblox_msgs__msg__SemanticLabelsStamped, labels),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers nvblox_msgs__msg__SemanticLabelsStamped__rosidl_typesupport_introspection_c__SemanticLabelsStamped_message_members = {
  "nvblox_msgs__msg",  // message namespace
  "SemanticLabelsStamped",  // message name
  2,  // number of fields
  sizeof(nvblox_msgs__msg__SemanticLabelsStamped),
  nvblox_msgs__msg__SemanticLabelsStamped__rosidl_typesupport_introspection_c__SemanticLabelsStamped_message_member_array,  // message members
  nvblox_msgs__msg__SemanticLabelsStamped__rosidl_typesupport_introspection_c__SemanticLabelsStamped_init_function,  // function to initialize message memory (memory has to be allocated)
  nvblox_msgs__msg__SemanticLabelsStamped__rosidl_typesupport_introspection_c__SemanticLabelsStamped_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t nvblox_msgs__msg__SemanticLabelsStamped__rosidl_typesupport_introspection_c__SemanticLabelsStamped_message_type_support_handle = {
  0,
  &nvblox_msgs__msg__SemanticLabelsStamped__rosidl_typesupport_introspection_c__SemanticLabelsStamped_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_nvblox_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, nvblox_msgs, msg, SemanticLabelsStamped)() {
  nvblox_msgs__msg__SemanticLabelsStamped__rosidl_typesupport_introspection_c__SemanticLabelsStamped_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  if (!nvblox_msgs__msg__SemanticLabelsStamped__rosidl_typesupport_introspection_c__SemanticLabelsStamped_message_type_support_handle.typesupport_identifier) {
    nvblox_msgs__msg__SemanticLabelsStamped__rosidl_typesupport_introspection_c__SemanticLabelsStamped_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &nvblox_msgs__msg__SemanticLabelsStamped__rosidl_typesupport_introspection_c__SemanticLabelsStamped_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
