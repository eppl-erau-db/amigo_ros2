// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from nvblox_msgs:msg/Mesh.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "nvblox_msgs/msg/detail/mesh__struct.hpp"
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

void Mesh_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) nvblox_msgs::msg::Mesh(_init);
}

void Mesh_fini_function(void * message_memory)
{
  auto typed_message = static_cast<nvblox_msgs::msg::Mesh *>(message_memory);
  typed_message->~Mesh();
}

size_t size_function__Mesh__block_indices(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<nvblox_msgs::msg::Index3D> *>(untyped_member);
  return member->size();
}

const void * get_const_function__Mesh__block_indices(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<nvblox_msgs::msg::Index3D> *>(untyped_member);
  return &member[index];
}

void * get_function__Mesh__block_indices(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<nvblox_msgs::msg::Index3D> *>(untyped_member);
  return &member[index];
}

void fetch_function__Mesh__block_indices(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const nvblox_msgs::msg::Index3D *>(
    get_const_function__Mesh__block_indices(untyped_member, index));
  auto & value = *reinterpret_cast<nvblox_msgs::msg::Index3D *>(untyped_value);
  value = item;
}

void assign_function__Mesh__block_indices(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<nvblox_msgs::msg::Index3D *>(
    get_function__Mesh__block_indices(untyped_member, index));
  const auto & value = *reinterpret_cast<const nvblox_msgs::msg::Index3D *>(untyped_value);
  item = value;
}

void resize_function__Mesh__block_indices(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<nvblox_msgs::msg::Index3D> *>(untyped_member);
  member->resize(size);
}

size_t size_function__Mesh__blocks(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<nvblox_msgs::msg::MeshBlock> *>(untyped_member);
  return member->size();
}

const void * get_const_function__Mesh__blocks(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<nvblox_msgs::msg::MeshBlock> *>(untyped_member);
  return &member[index];
}

void * get_function__Mesh__blocks(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<nvblox_msgs::msg::MeshBlock> *>(untyped_member);
  return &member[index];
}

void fetch_function__Mesh__blocks(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const nvblox_msgs::msg::MeshBlock *>(
    get_const_function__Mesh__blocks(untyped_member, index));
  auto & value = *reinterpret_cast<nvblox_msgs::msg::MeshBlock *>(untyped_value);
  value = item;
}

void assign_function__Mesh__blocks(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<nvblox_msgs::msg::MeshBlock *>(
    get_function__Mesh__blocks(untyped_member, index));
  const auto & value = *reinterpret_cast<const nvblox_msgs::msg::MeshBlock *>(untyped_value);
  item = value;
}

void resize_function__Mesh__blocks(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<nvblox_msgs::msg::MeshBlock> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember Mesh_message_member_array[5] = {
  {
    "header",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<std_msgs::msg::Header>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(nvblox_msgs::msg::Mesh, header),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "block_size",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(nvblox_msgs::msg::Mesh, block_size),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "block_indices",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<nvblox_msgs::msg::Index3D>(),  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(nvblox_msgs::msg::Mesh, block_indices),  // bytes offset in struct
    nullptr,  // default value
    size_function__Mesh__block_indices,  // size() function pointer
    get_const_function__Mesh__block_indices,  // get_const(index) function pointer
    get_function__Mesh__block_indices,  // get(index) function pointer
    fetch_function__Mesh__block_indices,  // fetch(index, &value) function pointer
    assign_function__Mesh__block_indices,  // assign(index, value) function pointer
    resize_function__Mesh__block_indices  // resize(index) function pointer
  },
  {
    "blocks",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<nvblox_msgs::msg::MeshBlock>(),  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(nvblox_msgs::msg::Mesh, blocks),  // bytes offset in struct
    nullptr,  // default value
    size_function__Mesh__blocks,  // size() function pointer
    get_const_function__Mesh__blocks,  // get_const(index) function pointer
    get_function__Mesh__blocks,  // get(index) function pointer
    fetch_function__Mesh__blocks,  // fetch(index, &value) function pointer
    assign_function__Mesh__blocks,  // assign(index, value) function pointer
    resize_function__Mesh__blocks  // resize(index) function pointer
  },
  {
    "clear",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(nvblox_msgs::msg::Mesh, clear),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers Mesh_message_members = {
  "nvblox_msgs::msg",  // message namespace
  "Mesh",  // message name
  5,  // number of fields
  sizeof(nvblox_msgs::msg::Mesh),
  Mesh_message_member_array,  // message members
  Mesh_init_function,  // function to initialize message memory (memory has to be allocated)
  Mesh_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t Mesh_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &Mesh_message_members,
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
get_message_type_support_handle<nvblox_msgs::msg::Mesh>()
{
  return &::nvblox_msgs::msg::rosidl_typesupport_introspection_cpp::Mesh_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, nvblox_msgs, msg, Mesh)() {
  return &::nvblox_msgs::msg::rosidl_typesupport_introspection_cpp::Mesh_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
