// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from isaac_ros_nitros_bridge_interfaces:msg/NitrosBridgeImage.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "isaac_ros_nitros_bridge_interfaces/msg/detail/nitros_bridge_image__rosidl_typesupport_introspection_c.h"
#include "isaac_ros_nitros_bridge_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "isaac_ros_nitros_bridge_interfaces/msg/detail/nitros_bridge_image__functions.h"
#include "isaac_ros_nitros_bridge_interfaces/msg/detail/nitros_bridge_image__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `encoding`
#include "rosidl_runtime_c/string_functions.h"
// Member `data`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__rosidl_typesupport_introspection_c__NitrosBridgeImage_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__init(message_memory);
}

void isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__rosidl_typesupport_introspection_c__NitrosBridgeImage_fini_function(void * message_memory)
{
  isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__fini(message_memory);
}

size_t isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__rosidl_typesupport_introspection_c__size_function__NitrosBridgeImage__data(
  const void * untyped_member)
{
  const rosidl_runtime_c__int32__Sequence * member =
    (const rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return member->size;
}

const void * isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__rosidl_typesupport_introspection_c__get_const_function__NitrosBridgeImage__data(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__int32__Sequence * member =
    (const rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return &member->data[index];
}

void * isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__rosidl_typesupport_introspection_c__get_function__NitrosBridgeImage__data(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__int32__Sequence * member =
    (rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return &member->data[index];
}

void isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__rosidl_typesupport_introspection_c__fetch_function__NitrosBridgeImage__data(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const int32_t * item =
    ((const int32_t *)
    isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__rosidl_typesupport_introspection_c__get_const_function__NitrosBridgeImage__data(untyped_member, index));
  int32_t * value =
    (int32_t *)(untyped_value);
  *value = *item;
}

void isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__rosidl_typesupport_introspection_c__assign_function__NitrosBridgeImage__data(
  void * untyped_member, size_t index, const void * untyped_value)
{
  int32_t * item =
    ((int32_t *)
    isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__rosidl_typesupport_introspection_c__get_function__NitrosBridgeImage__data(untyped_member, index));
  const int32_t * value =
    (const int32_t *)(untyped_value);
  *item = *value;
}

bool isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__rosidl_typesupport_introspection_c__resize_function__NitrosBridgeImage__data(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__int32__Sequence * member =
    (rosidl_runtime_c__int32__Sequence *)(untyped_member);
  rosidl_runtime_c__int32__Sequence__fini(member);
  return rosidl_runtime_c__int32__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__rosidl_typesupport_introspection_c__NitrosBridgeImage_message_member_array[7] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage, header),  // bytes offset in struct
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
    offsetof(isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage, height),  // bytes offset in struct
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
    offsetof(isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage, width),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "encoding",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage, encoding),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "is_bigendian",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage, is_bigendian),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "step",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage, step),  // bytes offset in struct
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
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage, data),  // bytes offset in struct
    NULL,  // default value
    isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__rosidl_typesupport_introspection_c__size_function__NitrosBridgeImage__data,  // size() function pointer
    isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__rosidl_typesupport_introspection_c__get_const_function__NitrosBridgeImage__data,  // get_const(index) function pointer
    isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__rosidl_typesupport_introspection_c__get_function__NitrosBridgeImage__data,  // get(index) function pointer
    isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__rosidl_typesupport_introspection_c__fetch_function__NitrosBridgeImage__data,  // fetch(index, &value) function pointer
    isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__rosidl_typesupport_introspection_c__assign_function__NitrosBridgeImage__data,  // assign(index, value) function pointer
    isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__rosidl_typesupport_introspection_c__resize_function__NitrosBridgeImage__data  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__rosidl_typesupport_introspection_c__NitrosBridgeImage_message_members = {
  "isaac_ros_nitros_bridge_interfaces__msg",  // message namespace
  "NitrosBridgeImage",  // message name
  7,  // number of fields
  sizeof(isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage),
  isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__rosidl_typesupport_introspection_c__NitrosBridgeImage_message_member_array,  // message members
  isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__rosidl_typesupport_introspection_c__NitrosBridgeImage_init_function,  // function to initialize message memory (memory has to be allocated)
  isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__rosidl_typesupport_introspection_c__NitrosBridgeImage_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__rosidl_typesupport_introspection_c__NitrosBridgeImage_message_type_support_handle = {
  0,
  &isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__rosidl_typesupport_introspection_c__NitrosBridgeImage_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_isaac_ros_nitros_bridge_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, isaac_ros_nitros_bridge_interfaces, msg, NitrosBridgeImage)() {
  isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__rosidl_typesupport_introspection_c__NitrosBridgeImage_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  if (!isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__rosidl_typesupport_introspection_c__NitrosBridgeImage_message_type_support_handle.typesupport_identifier) {
    isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__rosidl_typesupport_introspection_c__NitrosBridgeImage_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__rosidl_typesupport_introspection_c__NitrosBridgeImage_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
