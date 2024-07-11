// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from realsense2_camera_msgs:msg/IMUInfo.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "realsense2_camera_msgs/msg/detail/imu_info__struct.hpp"
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

void IMUInfo_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) realsense2_camera_msgs::msg::IMUInfo(_init);
}

void IMUInfo_fini_function(void * message_memory)
{
  auto typed_message = static_cast<realsense2_camera_msgs::msg::IMUInfo *>(message_memory);
  typed_message->~IMUInfo();
}

size_t size_function__IMUInfo__data(const void * untyped_member)
{
  (void)untyped_member;
  return 12;
}

const void * get_const_function__IMUInfo__data(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<double, 12> *>(untyped_member);
  return &member[index];
}

void * get_function__IMUInfo__data(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<double, 12> *>(untyped_member);
  return &member[index];
}

void fetch_function__IMUInfo__data(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__IMUInfo__data(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__IMUInfo__data(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__IMUInfo__data(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

size_t size_function__IMUInfo__noise_variances(const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * get_const_function__IMUInfo__noise_variances(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<double, 3> *>(untyped_member);
  return &member[index];
}

void * get_function__IMUInfo__noise_variances(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<double, 3> *>(untyped_member);
  return &member[index];
}

void fetch_function__IMUInfo__noise_variances(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__IMUInfo__noise_variances(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__IMUInfo__noise_variances(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__IMUInfo__noise_variances(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

size_t size_function__IMUInfo__bias_variances(const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * get_const_function__IMUInfo__bias_variances(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<double, 3> *>(untyped_member);
  return &member[index];
}

void * get_function__IMUInfo__bias_variances(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<double, 3> *>(untyped_member);
  return &member[index];
}

void fetch_function__IMUInfo__bias_variances(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__IMUInfo__bias_variances(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__IMUInfo__bias_variances(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__IMUInfo__bias_variances(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember IMUInfo_message_member_array[4] = {
  {
    "header",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<std_msgs::msg::Header>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(realsense2_camera_msgs::msg::IMUInfo, header),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "data",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    12,  // array size
    false,  // is upper bound
    offsetof(realsense2_camera_msgs::msg::IMUInfo, data),  // bytes offset in struct
    nullptr,  // default value
    size_function__IMUInfo__data,  // size() function pointer
    get_const_function__IMUInfo__data,  // get_const(index) function pointer
    get_function__IMUInfo__data,  // get(index) function pointer
    fetch_function__IMUInfo__data,  // fetch(index, &value) function pointer
    assign_function__IMUInfo__data,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "noise_variances",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(realsense2_camera_msgs::msg::IMUInfo, noise_variances),  // bytes offset in struct
    nullptr,  // default value
    size_function__IMUInfo__noise_variances,  // size() function pointer
    get_const_function__IMUInfo__noise_variances,  // get_const(index) function pointer
    get_function__IMUInfo__noise_variances,  // get(index) function pointer
    fetch_function__IMUInfo__noise_variances,  // fetch(index, &value) function pointer
    assign_function__IMUInfo__noise_variances,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "bias_variances",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(realsense2_camera_msgs::msg::IMUInfo, bias_variances),  // bytes offset in struct
    nullptr,  // default value
    size_function__IMUInfo__bias_variances,  // size() function pointer
    get_const_function__IMUInfo__bias_variances,  // get_const(index) function pointer
    get_function__IMUInfo__bias_variances,  // get(index) function pointer
    fetch_function__IMUInfo__bias_variances,  // fetch(index, &value) function pointer
    assign_function__IMUInfo__bias_variances,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers IMUInfo_message_members = {
  "realsense2_camera_msgs::msg",  // message namespace
  "IMUInfo",  // message name
  4,  // number of fields
  sizeof(realsense2_camera_msgs::msg::IMUInfo),
  IMUInfo_message_member_array,  // message members
  IMUInfo_init_function,  // function to initialize message memory (memory has to be allocated)
  IMUInfo_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t IMUInfo_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &IMUInfo_message_members,
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
get_message_type_support_handle<realsense2_camera_msgs::msg::IMUInfo>()
{
  return &::realsense2_camera_msgs::msg::rosidl_typesupport_introspection_cpp::IMUInfo_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, realsense2_camera_msgs, msg, IMUInfo)() {
  return &::realsense2_camera_msgs::msg::rosidl_typesupport_introspection_cpp::IMUInfo_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
