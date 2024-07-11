// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from realsense2_camera_msgs:msg/Extrinsics.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "realsense2_camera_msgs/msg/detail/extrinsics__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace realsense2_camera_msgs
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void Extrinsics_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) realsense2_camera_msgs::msg::Extrinsics(_init);
}

void Extrinsics_fini_function(void * message_memory)
{
  auto typed_message = static_cast<realsense2_camera_msgs::msg::Extrinsics *>(message_memory);
  typed_message->~Extrinsics();
}

size_t size_function__Extrinsics__rotation(const void * untyped_member)
{
  (void)untyped_member;
  return 9;
}

const void * get_const_function__Extrinsics__rotation(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<double, 9> *>(untyped_member);
  return &member[index];
}

void * get_function__Extrinsics__rotation(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<double, 9> *>(untyped_member);
  return &member[index];
}

void fetch_function__Extrinsics__rotation(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__Extrinsics__rotation(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__Extrinsics__rotation(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__Extrinsics__rotation(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

size_t size_function__Extrinsics__translation(const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * get_const_function__Extrinsics__translation(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<double, 3> *>(untyped_member);
  return &member[index];
}

void * get_function__Extrinsics__translation(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<double, 3> *>(untyped_member);
  return &member[index];
}

void fetch_function__Extrinsics__translation(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__Extrinsics__translation(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__Extrinsics__translation(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__Extrinsics__translation(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember Extrinsics_message_member_array[2] = {
  {
    "rotation",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    9,  // array size
    false,  // is upper bound
    offsetof(realsense2_camera_msgs::msg::Extrinsics, rotation),  // bytes offset in struct
    nullptr,  // default value
    size_function__Extrinsics__rotation,  // size() function pointer
    get_const_function__Extrinsics__rotation,  // get_const(index) function pointer
    get_function__Extrinsics__rotation,  // get(index) function pointer
    fetch_function__Extrinsics__rotation,  // fetch(index, &value) function pointer
    assign_function__Extrinsics__rotation,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "translation",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(realsense2_camera_msgs::msg::Extrinsics, translation),  // bytes offset in struct
    nullptr,  // default value
    size_function__Extrinsics__translation,  // size() function pointer
    get_const_function__Extrinsics__translation,  // get_const(index) function pointer
    get_function__Extrinsics__translation,  // get(index) function pointer
    fetch_function__Extrinsics__translation,  // fetch(index, &value) function pointer
    assign_function__Extrinsics__translation,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers Extrinsics_message_members = {
  "realsense2_camera_msgs::msg",  // message namespace
  "Extrinsics",  // message name
  2,  // number of fields
  sizeof(realsense2_camera_msgs::msg::Extrinsics),
  Extrinsics_message_member_array,  // message members
  Extrinsics_init_function,  // function to initialize message memory (memory has to be allocated)
  Extrinsics_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t Extrinsics_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &Extrinsics_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace realsense2_camera_msgs


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<realsense2_camera_msgs::msg::Extrinsics>()
{
  return &::realsense2_camera_msgs::msg::rosidl_typesupport_introspection_cpp::Extrinsics_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, realsense2_camera_msgs, msg, Extrinsics)() {
  return &::realsense2_camera_msgs::msg::rosidl_typesupport_introspection_cpp::Extrinsics_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
