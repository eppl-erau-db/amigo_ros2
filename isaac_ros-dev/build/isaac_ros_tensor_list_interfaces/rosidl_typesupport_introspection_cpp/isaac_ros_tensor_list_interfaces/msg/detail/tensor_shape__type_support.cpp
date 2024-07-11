// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from isaac_ros_tensor_list_interfaces:msg/TensorShape.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "isaac_ros_tensor_list_interfaces/msg/detail/tensor_shape__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace isaac_ros_tensor_list_interfaces
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void TensorShape_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) isaac_ros_tensor_list_interfaces::msg::TensorShape(_init);
}

void TensorShape_fini_function(void * message_memory)
{
  auto typed_message = static_cast<isaac_ros_tensor_list_interfaces::msg::TensorShape *>(message_memory);
  typed_message->~TensorShape();
}

size_t size_function__TensorShape__dims(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<uint32_t> *>(untyped_member);
  return member->size();
}

const void * get_const_function__TensorShape__dims(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<uint32_t> *>(untyped_member);
  return &member[index];
}

void * get_function__TensorShape__dims(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<uint32_t> *>(untyped_member);
  return &member[index];
}

void fetch_function__TensorShape__dims(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const uint32_t *>(
    get_const_function__TensorShape__dims(untyped_member, index));
  auto & value = *reinterpret_cast<uint32_t *>(untyped_value);
  value = item;
}

void assign_function__TensorShape__dims(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<uint32_t *>(
    get_function__TensorShape__dims(untyped_member, index));
  const auto & value = *reinterpret_cast<const uint32_t *>(untyped_value);
  item = value;
}

void resize_function__TensorShape__dims(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<uint32_t> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember TensorShape_message_member_array[2] = {
  {
    "rank",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(isaac_ros_tensor_list_interfaces::msg::TensorShape, rank),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "dims",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(isaac_ros_tensor_list_interfaces::msg::TensorShape, dims),  // bytes offset in struct
    nullptr,  // default value
    size_function__TensorShape__dims,  // size() function pointer
    get_const_function__TensorShape__dims,  // get_const(index) function pointer
    get_function__TensorShape__dims,  // get(index) function pointer
    fetch_function__TensorShape__dims,  // fetch(index, &value) function pointer
    assign_function__TensorShape__dims,  // assign(index, value) function pointer
    resize_function__TensorShape__dims  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers TensorShape_message_members = {
  "isaac_ros_tensor_list_interfaces::msg",  // message namespace
  "TensorShape",  // message name
  2,  // number of fields
  sizeof(isaac_ros_tensor_list_interfaces::msg::TensorShape),
  TensorShape_message_member_array,  // message members
  TensorShape_init_function,  // function to initialize message memory (memory has to be allocated)
  TensorShape_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t TensorShape_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &TensorShape_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace isaac_ros_tensor_list_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<isaac_ros_tensor_list_interfaces::msg::TensorShape>()
{
  return &::isaac_ros_tensor_list_interfaces::msg::rosidl_typesupport_introspection_cpp::TensorShape_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, isaac_ros_tensor_list_interfaces, msg, TensorShape)() {
  return &::isaac_ros_tensor_list_interfaces::msg::rosidl_typesupport_introspection_cpp::TensorShape_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
