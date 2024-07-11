// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from nvblox_msgs:msg/MeshBlock.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "nvblox_msgs/msg/detail/mesh_block__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace nvblox_msgs
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void MeshBlock_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) nvblox_msgs::msg::MeshBlock(_init);
}

void MeshBlock_fini_function(void * message_memory)
{
  auto typed_message = static_cast<nvblox_msgs::msg::MeshBlock *>(message_memory);
  typed_message->~MeshBlock();
}

size_t size_function__MeshBlock__vertices(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<geometry_msgs::msg::Point32> *>(untyped_member);
  return member->size();
}

const void * get_const_function__MeshBlock__vertices(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<geometry_msgs::msg::Point32> *>(untyped_member);
  return &member[index];
}

void * get_function__MeshBlock__vertices(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<geometry_msgs::msg::Point32> *>(untyped_member);
  return &member[index];
}

void fetch_function__MeshBlock__vertices(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const geometry_msgs::msg::Point32 *>(
    get_const_function__MeshBlock__vertices(untyped_member, index));
  auto & value = *reinterpret_cast<geometry_msgs::msg::Point32 *>(untyped_value);
  value = item;
}

void assign_function__MeshBlock__vertices(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<geometry_msgs::msg::Point32 *>(
    get_function__MeshBlock__vertices(untyped_member, index));
  const auto & value = *reinterpret_cast<const geometry_msgs::msg::Point32 *>(untyped_value);
  item = value;
}

void resize_function__MeshBlock__vertices(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<geometry_msgs::msg::Point32> *>(untyped_member);
  member->resize(size);
}

size_t size_function__MeshBlock__normals(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<geometry_msgs::msg::Point32> *>(untyped_member);
  return member->size();
}

const void * get_const_function__MeshBlock__normals(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<geometry_msgs::msg::Point32> *>(untyped_member);
  return &member[index];
}

void * get_function__MeshBlock__normals(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<geometry_msgs::msg::Point32> *>(untyped_member);
  return &member[index];
}

void fetch_function__MeshBlock__normals(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const geometry_msgs::msg::Point32 *>(
    get_const_function__MeshBlock__normals(untyped_member, index));
  auto & value = *reinterpret_cast<geometry_msgs::msg::Point32 *>(untyped_value);
  value = item;
}

void assign_function__MeshBlock__normals(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<geometry_msgs::msg::Point32 *>(
    get_function__MeshBlock__normals(untyped_member, index));
  const auto & value = *reinterpret_cast<const geometry_msgs::msg::Point32 *>(untyped_value);
  item = value;
}

void resize_function__MeshBlock__normals(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<geometry_msgs::msg::Point32> *>(untyped_member);
  member->resize(size);
}

size_t size_function__MeshBlock__colors(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<std_msgs::msg::ColorRGBA> *>(untyped_member);
  return member->size();
}

const void * get_const_function__MeshBlock__colors(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<std_msgs::msg::ColorRGBA> *>(untyped_member);
  return &member[index];
}

void * get_function__MeshBlock__colors(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<std_msgs::msg::ColorRGBA> *>(untyped_member);
  return &member[index];
}

void fetch_function__MeshBlock__colors(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const std_msgs::msg::ColorRGBA *>(
    get_const_function__MeshBlock__colors(untyped_member, index));
  auto & value = *reinterpret_cast<std_msgs::msg::ColorRGBA *>(untyped_value);
  value = item;
}

void assign_function__MeshBlock__colors(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<std_msgs::msg::ColorRGBA *>(
    get_function__MeshBlock__colors(untyped_member, index));
  const auto & value = *reinterpret_cast<const std_msgs::msg::ColorRGBA *>(untyped_value);
  item = value;
}

void resize_function__MeshBlock__colors(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<std_msgs::msg::ColorRGBA> *>(untyped_member);
  member->resize(size);
}

size_t size_function__MeshBlock__triangles(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<int32_t> *>(untyped_member);
  return member->size();
}

const void * get_const_function__MeshBlock__triangles(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<int32_t> *>(untyped_member);
  return &member[index];
}

void * get_function__MeshBlock__triangles(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<int32_t> *>(untyped_member);
  return &member[index];
}

void fetch_function__MeshBlock__triangles(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const int32_t *>(
    get_const_function__MeshBlock__triangles(untyped_member, index));
  auto & value = *reinterpret_cast<int32_t *>(untyped_value);
  value = item;
}

void assign_function__MeshBlock__triangles(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<int32_t *>(
    get_function__MeshBlock__triangles(untyped_member, index));
  const auto & value = *reinterpret_cast<const int32_t *>(untyped_value);
  item = value;
}

void resize_function__MeshBlock__triangles(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<int32_t> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember MeshBlock_message_member_array[4] = {
  {
    "vertices",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<geometry_msgs::msg::Point32>(),  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(nvblox_msgs::msg::MeshBlock, vertices),  // bytes offset in struct
    nullptr,  // default value
    size_function__MeshBlock__vertices,  // size() function pointer
    get_const_function__MeshBlock__vertices,  // get_const(index) function pointer
    get_function__MeshBlock__vertices,  // get(index) function pointer
    fetch_function__MeshBlock__vertices,  // fetch(index, &value) function pointer
    assign_function__MeshBlock__vertices,  // assign(index, value) function pointer
    resize_function__MeshBlock__vertices  // resize(index) function pointer
  },
  {
    "normals",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<geometry_msgs::msg::Point32>(),  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(nvblox_msgs::msg::MeshBlock, normals),  // bytes offset in struct
    nullptr,  // default value
    size_function__MeshBlock__normals,  // size() function pointer
    get_const_function__MeshBlock__normals,  // get_const(index) function pointer
    get_function__MeshBlock__normals,  // get(index) function pointer
    fetch_function__MeshBlock__normals,  // fetch(index, &value) function pointer
    assign_function__MeshBlock__normals,  // assign(index, value) function pointer
    resize_function__MeshBlock__normals  // resize(index) function pointer
  },
  {
    "colors",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<std_msgs::msg::ColorRGBA>(),  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(nvblox_msgs::msg::MeshBlock, colors),  // bytes offset in struct
    nullptr,  // default value
    size_function__MeshBlock__colors,  // size() function pointer
    get_const_function__MeshBlock__colors,  // get_const(index) function pointer
    get_function__MeshBlock__colors,  // get(index) function pointer
    fetch_function__MeshBlock__colors,  // fetch(index, &value) function pointer
    assign_function__MeshBlock__colors,  // assign(index, value) function pointer
    resize_function__MeshBlock__colors  // resize(index) function pointer
  },
  {
    "triangles",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(nvblox_msgs::msg::MeshBlock, triangles),  // bytes offset in struct
    nullptr,  // default value
    size_function__MeshBlock__triangles,  // size() function pointer
    get_const_function__MeshBlock__triangles,  // get_const(index) function pointer
    get_function__MeshBlock__triangles,  // get(index) function pointer
    fetch_function__MeshBlock__triangles,  // fetch(index, &value) function pointer
    assign_function__MeshBlock__triangles,  // assign(index, value) function pointer
    resize_function__MeshBlock__triangles  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers MeshBlock_message_members = {
  "nvblox_msgs::msg",  // message namespace
  "MeshBlock",  // message name
  4,  // number of fields
  sizeof(nvblox_msgs::msg::MeshBlock),
  MeshBlock_message_member_array,  // message members
  MeshBlock_init_function,  // function to initialize message memory (memory has to be allocated)
  MeshBlock_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t MeshBlock_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &MeshBlock_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace nvblox_msgs


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<nvblox_msgs::msg::MeshBlock>()
{
  return &::nvblox_msgs::msg::rosidl_typesupport_introspection_cpp::MeshBlock_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, nvblox_msgs, msg, MeshBlock)() {
  return &::nvblox_msgs::msg::rosidl_typesupport_introspection_cpp::MeshBlock_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
