// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from isaac_ros_tensor_list_interfaces:msg/TensorShape.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "isaac_ros_tensor_list_interfaces/msg/detail/tensor_shape__rosidl_typesupport_introspection_c.h"
#include "isaac_ros_tensor_list_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "isaac_ros_tensor_list_interfaces/msg/detail/tensor_shape__functions.h"
#include "isaac_ros_tensor_list_interfaces/msg/detail/tensor_shape__struct.h"


// Include directives for member types
// Member `dims`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void isaac_ros_tensor_list_interfaces__msg__TensorShape__rosidl_typesupport_introspection_c__TensorShape_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  isaac_ros_tensor_list_interfaces__msg__TensorShape__init(message_memory);
}

void isaac_ros_tensor_list_interfaces__msg__TensorShape__rosidl_typesupport_introspection_c__TensorShape_fini_function(void * message_memory)
{
  isaac_ros_tensor_list_interfaces__msg__TensorShape__fini(message_memory);
}

size_t isaac_ros_tensor_list_interfaces__msg__TensorShape__rosidl_typesupport_introspection_c__size_function__TensorShape__dims(
  const void * untyped_member)
{
  const rosidl_runtime_c__uint32__Sequence * member =
    (const rosidl_runtime_c__uint32__Sequence *)(untyped_member);
  return member->size;
}

const void * isaac_ros_tensor_list_interfaces__msg__TensorShape__rosidl_typesupport_introspection_c__get_const_function__TensorShape__dims(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__uint32__Sequence * member =
    (const rosidl_runtime_c__uint32__Sequence *)(untyped_member);
  return &member->data[index];
}

void * isaac_ros_tensor_list_interfaces__msg__TensorShape__rosidl_typesupport_introspection_c__get_function__TensorShape__dims(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__uint32__Sequence * member =
    (rosidl_runtime_c__uint32__Sequence *)(untyped_member);
  return &member->data[index];
}

void isaac_ros_tensor_list_interfaces__msg__TensorShape__rosidl_typesupport_introspection_c__fetch_function__TensorShape__dims(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint32_t * item =
    ((const uint32_t *)
    isaac_ros_tensor_list_interfaces__msg__TensorShape__rosidl_typesupport_introspection_c__get_const_function__TensorShape__dims(untyped_member, index));
  uint32_t * value =
    (uint32_t *)(untyped_value);
  *value = *item;
}

void isaac_ros_tensor_list_interfaces__msg__TensorShape__rosidl_typesupport_introspection_c__assign_function__TensorShape__dims(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint32_t * item =
    ((uint32_t *)
    isaac_ros_tensor_list_interfaces__msg__TensorShape__rosidl_typesupport_introspection_c__get_function__TensorShape__dims(untyped_member, index));
  const uint32_t * value =
    (const uint32_t *)(untyped_value);
  *item = *value;
}

bool isaac_ros_tensor_list_interfaces__msg__TensorShape__rosidl_typesupport_introspection_c__resize_function__TensorShape__dims(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__uint32__Sequence * member =
    (rosidl_runtime_c__uint32__Sequence *)(untyped_member);
  rosidl_runtime_c__uint32__Sequence__fini(member);
  return rosidl_runtime_c__uint32__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember isaac_ros_tensor_list_interfaces__msg__TensorShape__rosidl_typesupport_introspection_c__TensorShape_message_member_array[2] = {
  {
    "rank",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(isaac_ros_tensor_list_interfaces__msg__TensorShape, rank),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "dims",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(isaac_ros_tensor_list_interfaces__msg__TensorShape, dims),  // bytes offset in struct
    NULL,  // default value
    isaac_ros_tensor_list_interfaces__msg__TensorShape__rosidl_typesupport_introspection_c__size_function__TensorShape__dims,  // size() function pointer
    isaac_ros_tensor_list_interfaces__msg__TensorShape__rosidl_typesupport_introspection_c__get_const_function__TensorShape__dims,  // get_const(index) function pointer
    isaac_ros_tensor_list_interfaces__msg__TensorShape__rosidl_typesupport_introspection_c__get_function__TensorShape__dims,  // get(index) function pointer
    isaac_ros_tensor_list_interfaces__msg__TensorShape__rosidl_typesupport_introspection_c__fetch_function__TensorShape__dims,  // fetch(index, &value) function pointer
    isaac_ros_tensor_list_interfaces__msg__TensorShape__rosidl_typesupport_introspection_c__assign_function__TensorShape__dims,  // assign(index, value) function pointer
    isaac_ros_tensor_list_interfaces__msg__TensorShape__rosidl_typesupport_introspection_c__resize_function__TensorShape__dims  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers isaac_ros_tensor_list_interfaces__msg__TensorShape__rosidl_typesupport_introspection_c__TensorShape_message_members = {
  "isaac_ros_tensor_list_interfaces__msg",  // message namespace
  "TensorShape",  // message name
  2,  // number of fields
  sizeof(isaac_ros_tensor_list_interfaces__msg__TensorShape),
  isaac_ros_tensor_list_interfaces__msg__TensorShape__rosidl_typesupport_introspection_c__TensorShape_message_member_array,  // message members
  isaac_ros_tensor_list_interfaces__msg__TensorShape__rosidl_typesupport_introspection_c__TensorShape_init_function,  // function to initialize message memory (memory has to be allocated)
  isaac_ros_tensor_list_interfaces__msg__TensorShape__rosidl_typesupport_introspection_c__TensorShape_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t isaac_ros_tensor_list_interfaces__msg__TensorShape__rosidl_typesupport_introspection_c__TensorShape_message_type_support_handle = {
  0,
  &isaac_ros_tensor_list_interfaces__msg__TensorShape__rosidl_typesupport_introspection_c__TensorShape_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_isaac_ros_tensor_list_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, isaac_ros_tensor_list_interfaces, msg, TensorShape)() {
  if (!isaac_ros_tensor_list_interfaces__msg__TensorShape__rosidl_typesupport_introspection_c__TensorShape_message_type_support_handle.typesupport_identifier) {
    isaac_ros_tensor_list_interfaces__msg__TensorShape__rosidl_typesupport_introspection_c__TensorShape_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &isaac_ros_tensor_list_interfaces__msg__TensorShape__rosidl_typesupport_introspection_c__TensorShape_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
