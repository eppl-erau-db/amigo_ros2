// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from isaac_ros_tensor_list_interfaces:msg/TensorList.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "isaac_ros_tensor_list_interfaces/msg/detail/tensor_list__rosidl_typesupport_introspection_c.h"
#include "isaac_ros_tensor_list_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "isaac_ros_tensor_list_interfaces/msg/detail/tensor_list__functions.h"
#include "isaac_ros_tensor_list_interfaces/msg/detail/tensor_list__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `tensors`
#include "isaac_ros_tensor_list_interfaces/msg/tensor.h"
// Member `tensors`
#include "isaac_ros_tensor_list_interfaces/msg/detail/tensor__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void isaac_ros_tensor_list_interfaces__msg__TensorList__rosidl_typesupport_introspection_c__TensorList_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  isaac_ros_tensor_list_interfaces__msg__TensorList__init(message_memory);
}

void isaac_ros_tensor_list_interfaces__msg__TensorList__rosidl_typesupport_introspection_c__TensorList_fini_function(void * message_memory)
{
  isaac_ros_tensor_list_interfaces__msg__TensorList__fini(message_memory);
}

size_t isaac_ros_tensor_list_interfaces__msg__TensorList__rosidl_typesupport_introspection_c__size_function__TensorList__tensors(
  const void * untyped_member)
{
  const isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence * member =
    (const isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence *)(untyped_member);
  return member->size;
}

const void * isaac_ros_tensor_list_interfaces__msg__TensorList__rosidl_typesupport_introspection_c__get_const_function__TensorList__tensors(
  const void * untyped_member, size_t index)
{
  const isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence * member =
    (const isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence *)(untyped_member);
  return &member->data[index];
}

void * isaac_ros_tensor_list_interfaces__msg__TensorList__rosidl_typesupport_introspection_c__get_function__TensorList__tensors(
  void * untyped_member, size_t index)
{
  isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence * member =
    (isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence *)(untyped_member);
  return &member->data[index];
}

void isaac_ros_tensor_list_interfaces__msg__TensorList__rosidl_typesupport_introspection_c__fetch_function__TensorList__tensors(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const isaac_ros_tensor_list_interfaces__msg__Tensor * item =
    ((const isaac_ros_tensor_list_interfaces__msg__Tensor *)
    isaac_ros_tensor_list_interfaces__msg__TensorList__rosidl_typesupport_introspection_c__get_const_function__TensorList__tensors(untyped_member, index));
  isaac_ros_tensor_list_interfaces__msg__Tensor * value =
    (isaac_ros_tensor_list_interfaces__msg__Tensor *)(untyped_value);
  *value = *item;
}

void isaac_ros_tensor_list_interfaces__msg__TensorList__rosidl_typesupport_introspection_c__assign_function__TensorList__tensors(
  void * untyped_member, size_t index, const void * untyped_value)
{
  isaac_ros_tensor_list_interfaces__msg__Tensor * item =
    ((isaac_ros_tensor_list_interfaces__msg__Tensor *)
    isaac_ros_tensor_list_interfaces__msg__TensorList__rosidl_typesupport_introspection_c__get_function__TensorList__tensors(untyped_member, index));
  const isaac_ros_tensor_list_interfaces__msg__Tensor * value =
    (const isaac_ros_tensor_list_interfaces__msg__Tensor *)(untyped_value);
  *item = *value;
}

bool isaac_ros_tensor_list_interfaces__msg__TensorList__rosidl_typesupport_introspection_c__resize_function__TensorList__tensors(
  void * untyped_member, size_t size)
{
  isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence * member =
    (isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence *)(untyped_member);
  isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence__fini(member);
  return isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember isaac_ros_tensor_list_interfaces__msg__TensorList__rosidl_typesupport_introspection_c__TensorList_message_member_array[2] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(isaac_ros_tensor_list_interfaces__msg__TensorList, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "tensors",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(isaac_ros_tensor_list_interfaces__msg__TensorList, tensors),  // bytes offset in struct
    NULL,  // default value
    isaac_ros_tensor_list_interfaces__msg__TensorList__rosidl_typesupport_introspection_c__size_function__TensorList__tensors,  // size() function pointer
    isaac_ros_tensor_list_interfaces__msg__TensorList__rosidl_typesupport_introspection_c__get_const_function__TensorList__tensors,  // get_const(index) function pointer
    isaac_ros_tensor_list_interfaces__msg__TensorList__rosidl_typesupport_introspection_c__get_function__TensorList__tensors,  // get(index) function pointer
    isaac_ros_tensor_list_interfaces__msg__TensorList__rosidl_typesupport_introspection_c__fetch_function__TensorList__tensors,  // fetch(index, &value) function pointer
    isaac_ros_tensor_list_interfaces__msg__TensorList__rosidl_typesupport_introspection_c__assign_function__TensorList__tensors,  // assign(index, value) function pointer
    isaac_ros_tensor_list_interfaces__msg__TensorList__rosidl_typesupport_introspection_c__resize_function__TensorList__tensors  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers isaac_ros_tensor_list_interfaces__msg__TensorList__rosidl_typesupport_introspection_c__TensorList_message_members = {
  "isaac_ros_tensor_list_interfaces__msg",  // message namespace
  "TensorList",  // message name
  2,  // number of fields
  sizeof(isaac_ros_tensor_list_interfaces__msg__TensorList),
  isaac_ros_tensor_list_interfaces__msg__TensorList__rosidl_typesupport_introspection_c__TensorList_message_member_array,  // message members
  isaac_ros_tensor_list_interfaces__msg__TensorList__rosidl_typesupport_introspection_c__TensorList_init_function,  // function to initialize message memory (memory has to be allocated)
  isaac_ros_tensor_list_interfaces__msg__TensorList__rosidl_typesupport_introspection_c__TensorList_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t isaac_ros_tensor_list_interfaces__msg__TensorList__rosidl_typesupport_introspection_c__TensorList_message_type_support_handle = {
  0,
  &isaac_ros_tensor_list_interfaces__msg__TensorList__rosidl_typesupport_introspection_c__TensorList_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_isaac_ros_tensor_list_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, isaac_ros_tensor_list_interfaces, msg, TensorList)() {
  isaac_ros_tensor_list_interfaces__msg__TensorList__rosidl_typesupport_introspection_c__TensorList_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  isaac_ros_tensor_list_interfaces__msg__TensorList__rosidl_typesupport_introspection_c__TensorList_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, isaac_ros_tensor_list_interfaces, msg, Tensor)();
  if (!isaac_ros_tensor_list_interfaces__msg__TensorList__rosidl_typesupport_introspection_c__TensorList_message_type_support_handle.typesupport_identifier) {
    isaac_ros_tensor_list_interfaces__msg__TensorList__rosidl_typesupport_introspection_c__TensorList_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &isaac_ros_tensor_list_interfaces__msg__TensorList__rosidl_typesupport_introspection_c__TensorList_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
