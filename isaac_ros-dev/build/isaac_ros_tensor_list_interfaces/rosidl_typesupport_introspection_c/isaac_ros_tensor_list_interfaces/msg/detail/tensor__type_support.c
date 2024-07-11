// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from isaac_ros_tensor_list_interfaces:msg/Tensor.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "isaac_ros_tensor_list_interfaces/msg/detail/tensor__rosidl_typesupport_introspection_c.h"
#include "isaac_ros_tensor_list_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "isaac_ros_tensor_list_interfaces/msg/detail/tensor__functions.h"
#include "isaac_ros_tensor_list_interfaces/msg/detail/tensor__struct.h"


// Include directives for member types
// Member `name`
#include "rosidl_runtime_c/string_functions.h"
// Member `shape`
#include "isaac_ros_tensor_list_interfaces/msg/tensor_shape.h"
// Member `shape`
#include "isaac_ros_tensor_list_interfaces/msg/detail/tensor_shape__rosidl_typesupport_introspection_c.h"
// Member `strides`
// Member `data`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__Tensor_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  isaac_ros_tensor_list_interfaces__msg__Tensor__init(message_memory);
}

void isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__Tensor_fini_function(void * message_memory)
{
  isaac_ros_tensor_list_interfaces__msg__Tensor__fini(message_memory);
}

size_t isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__size_function__Tensor__strides(
  const void * untyped_member)
{
  const rosidl_runtime_c__uint64__Sequence * member =
    (const rosidl_runtime_c__uint64__Sequence *)(untyped_member);
  return member->size;
}

const void * isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__get_const_function__Tensor__strides(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__uint64__Sequence * member =
    (const rosidl_runtime_c__uint64__Sequence *)(untyped_member);
  return &member->data[index];
}

void * isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__get_function__Tensor__strides(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__uint64__Sequence * member =
    (rosidl_runtime_c__uint64__Sequence *)(untyped_member);
  return &member->data[index];
}

void isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__fetch_function__Tensor__strides(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint64_t * item =
    ((const uint64_t *)
    isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__get_const_function__Tensor__strides(untyped_member, index));
  uint64_t * value =
    (uint64_t *)(untyped_value);
  *value = *item;
}

void isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__assign_function__Tensor__strides(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint64_t * item =
    ((uint64_t *)
    isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__get_function__Tensor__strides(untyped_member, index));
  const uint64_t * value =
    (const uint64_t *)(untyped_value);
  *item = *value;
}

bool isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__resize_function__Tensor__strides(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__uint64__Sequence * member =
    (rosidl_runtime_c__uint64__Sequence *)(untyped_member);
  rosidl_runtime_c__uint64__Sequence__fini(member);
  return rosidl_runtime_c__uint64__Sequence__init(member, size);
}

size_t isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__size_function__Tensor__data(
  const void * untyped_member)
{
  const rosidl_runtime_c__uint8__Sequence * member =
    (const rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return member->size;
}

const void * isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__get_const_function__Tensor__data(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__uint8__Sequence * member =
    (const rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return &member->data[index];
}

void * isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__get_function__Tensor__data(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__uint8__Sequence * member =
    (rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return &member->data[index];
}

void isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__fetch_function__Tensor__data(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint8_t * item =
    ((const uint8_t *)
    isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__get_const_function__Tensor__data(untyped_member, index));
  uint8_t * value =
    (uint8_t *)(untyped_value);
  *value = *item;
}

void isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__assign_function__Tensor__data(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint8_t * item =
    ((uint8_t *)
    isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__get_function__Tensor__data(untyped_member, index));
  const uint8_t * value =
    (const uint8_t *)(untyped_value);
  *item = *value;
}

bool isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__resize_function__Tensor__data(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__uint8__Sequence * member =
    (rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  rosidl_runtime_c__uint8__Sequence__fini(member);
  return rosidl_runtime_c__uint8__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__Tensor_message_member_array[5] = {
  {
    "name",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(isaac_ros_tensor_list_interfaces__msg__Tensor, name),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "shape",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(isaac_ros_tensor_list_interfaces__msg__Tensor, shape),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "data_type",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(isaac_ros_tensor_list_interfaces__msg__Tensor, data_type),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "strides",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT64,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(isaac_ros_tensor_list_interfaces__msg__Tensor, strides),  // bytes offset in struct
    NULL,  // default value
    isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__size_function__Tensor__strides,  // size() function pointer
    isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__get_const_function__Tensor__strides,  // get_const(index) function pointer
    isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__get_function__Tensor__strides,  // get(index) function pointer
    isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__fetch_function__Tensor__strides,  // fetch(index, &value) function pointer
    isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__assign_function__Tensor__strides,  // assign(index, value) function pointer
    isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__resize_function__Tensor__strides  // resize(index) function pointer
  },
  {
    "data",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(isaac_ros_tensor_list_interfaces__msg__Tensor, data),  // bytes offset in struct
    NULL,  // default value
    isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__size_function__Tensor__data,  // size() function pointer
    isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__get_const_function__Tensor__data,  // get_const(index) function pointer
    isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__get_function__Tensor__data,  // get(index) function pointer
    isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__fetch_function__Tensor__data,  // fetch(index, &value) function pointer
    isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__assign_function__Tensor__data,  // assign(index, value) function pointer
    isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__resize_function__Tensor__data  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__Tensor_message_members = {
  "isaac_ros_tensor_list_interfaces__msg",  // message namespace
  "Tensor",  // message name
  5,  // number of fields
  sizeof(isaac_ros_tensor_list_interfaces__msg__Tensor),
  isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__Tensor_message_member_array,  // message members
  isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__Tensor_init_function,  // function to initialize message memory (memory has to be allocated)
  isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__Tensor_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__Tensor_message_type_support_handle = {
  0,
  &isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__Tensor_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_isaac_ros_tensor_list_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, isaac_ros_tensor_list_interfaces, msg, Tensor)() {
  isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__Tensor_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, isaac_ros_tensor_list_interfaces, msg, TensorShape)();
  if (!isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__Tensor_message_type_support_handle.typesupport_identifier) {
    isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__Tensor_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &isaac_ros_tensor_list_interfaces__msg__Tensor__rosidl_typesupport_introspection_c__Tensor_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
