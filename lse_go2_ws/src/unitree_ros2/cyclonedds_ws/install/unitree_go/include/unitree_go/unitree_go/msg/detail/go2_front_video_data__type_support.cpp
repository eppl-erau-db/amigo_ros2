// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from unitree_go:msg/Go2FrontVideoData.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "unitree_go/msg/detail/go2_front_video_data__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace unitree_go
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void Go2FrontVideoData_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) unitree_go::msg::Go2FrontVideoData(_init);
}

void Go2FrontVideoData_fini_function(void * message_memory)
{
  auto typed_message = static_cast<unitree_go::msg::Go2FrontVideoData *>(message_memory);
  typed_message->~Go2FrontVideoData();
}

size_t size_function__Go2FrontVideoData__video720p(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<uint8_t> *>(untyped_member);
  return member->size();
}

const void * get_const_function__Go2FrontVideoData__video720p(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<uint8_t> *>(untyped_member);
  return &member[index];
}

void * get_function__Go2FrontVideoData__video720p(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<uint8_t> *>(untyped_member);
  return &member[index];
}

void fetch_function__Go2FrontVideoData__video720p(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const uint8_t *>(
    get_const_function__Go2FrontVideoData__video720p(untyped_member, index));
  auto & value = *reinterpret_cast<uint8_t *>(untyped_value);
  value = item;
}

void assign_function__Go2FrontVideoData__video720p(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<uint8_t *>(
    get_function__Go2FrontVideoData__video720p(untyped_member, index));
  const auto & value = *reinterpret_cast<const uint8_t *>(untyped_value);
  item = value;
}

void resize_function__Go2FrontVideoData__video720p(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<uint8_t> *>(untyped_member);
  member->resize(size);
}

size_t size_function__Go2FrontVideoData__video360p(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<uint8_t> *>(untyped_member);
  return member->size();
}

const void * get_const_function__Go2FrontVideoData__video360p(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<uint8_t> *>(untyped_member);
  return &member[index];
}

void * get_function__Go2FrontVideoData__video360p(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<uint8_t> *>(untyped_member);
  return &member[index];
}

void fetch_function__Go2FrontVideoData__video360p(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const uint8_t *>(
    get_const_function__Go2FrontVideoData__video360p(untyped_member, index));
  auto & value = *reinterpret_cast<uint8_t *>(untyped_value);
  value = item;
}

void assign_function__Go2FrontVideoData__video360p(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<uint8_t *>(
    get_function__Go2FrontVideoData__video360p(untyped_member, index));
  const auto & value = *reinterpret_cast<const uint8_t *>(untyped_value);
  item = value;
}

void resize_function__Go2FrontVideoData__video360p(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<uint8_t> *>(untyped_member);
  member->resize(size);
}

size_t size_function__Go2FrontVideoData__video180p(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<uint8_t> *>(untyped_member);
  return member->size();
}

const void * get_const_function__Go2FrontVideoData__video180p(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<uint8_t> *>(untyped_member);
  return &member[index];
}

void * get_function__Go2FrontVideoData__video180p(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<uint8_t> *>(untyped_member);
  return &member[index];
}

void fetch_function__Go2FrontVideoData__video180p(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const uint8_t *>(
    get_const_function__Go2FrontVideoData__video180p(untyped_member, index));
  auto & value = *reinterpret_cast<uint8_t *>(untyped_value);
  value = item;
}

void assign_function__Go2FrontVideoData__video180p(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<uint8_t *>(
    get_function__Go2FrontVideoData__video180p(untyped_member, index));
  const auto & value = *reinterpret_cast<const uint8_t *>(untyped_value);
  item = value;
}

void resize_function__Go2FrontVideoData__video180p(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<uint8_t> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember Go2FrontVideoData_message_member_array[4] = {
  {
    "time_frame",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT64,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go::msg::Go2FrontVideoData, time_frame),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "video720p",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go::msg::Go2FrontVideoData, video720p),  // bytes offset in struct
    nullptr,  // default value
    size_function__Go2FrontVideoData__video720p,  // size() function pointer
    get_const_function__Go2FrontVideoData__video720p,  // get_const(index) function pointer
    get_function__Go2FrontVideoData__video720p,  // get(index) function pointer
    fetch_function__Go2FrontVideoData__video720p,  // fetch(index, &value) function pointer
    assign_function__Go2FrontVideoData__video720p,  // assign(index, value) function pointer
    resize_function__Go2FrontVideoData__video720p  // resize(index) function pointer
  },
  {
    "video360p",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go::msg::Go2FrontVideoData, video360p),  // bytes offset in struct
    nullptr,  // default value
    size_function__Go2FrontVideoData__video360p,  // size() function pointer
    get_const_function__Go2FrontVideoData__video360p,  // get_const(index) function pointer
    get_function__Go2FrontVideoData__video360p,  // get(index) function pointer
    fetch_function__Go2FrontVideoData__video360p,  // fetch(index, &value) function pointer
    assign_function__Go2FrontVideoData__video360p,  // assign(index, value) function pointer
    resize_function__Go2FrontVideoData__video360p  // resize(index) function pointer
  },
  {
    "video180p",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(unitree_go::msg::Go2FrontVideoData, video180p),  // bytes offset in struct
    nullptr,  // default value
    size_function__Go2FrontVideoData__video180p,  // size() function pointer
    get_const_function__Go2FrontVideoData__video180p,  // get_const(index) function pointer
    get_function__Go2FrontVideoData__video180p,  // get(index) function pointer
    fetch_function__Go2FrontVideoData__video180p,  // fetch(index, &value) function pointer
    assign_function__Go2FrontVideoData__video180p,  // assign(index, value) function pointer
    resize_function__Go2FrontVideoData__video180p  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers Go2FrontVideoData_message_members = {
  "unitree_go::msg",  // message namespace
  "Go2FrontVideoData",  // message name
  4,  // number of fields
  sizeof(unitree_go::msg::Go2FrontVideoData),
  Go2FrontVideoData_message_member_array,  // message members
  Go2FrontVideoData_init_function,  // function to initialize message memory (memory has to be allocated)
  Go2FrontVideoData_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t Go2FrontVideoData_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &Go2FrontVideoData_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace unitree_go


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<unitree_go::msg::Go2FrontVideoData>()
{
  return &::unitree_go::msg::rosidl_typesupport_introspection_cpp::Go2FrontVideoData_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, unitree_go, msg, Go2FrontVideoData)() {
  return &::unitree_go::msg::rosidl_typesupport_introspection_cpp::Go2FrontVideoData_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
