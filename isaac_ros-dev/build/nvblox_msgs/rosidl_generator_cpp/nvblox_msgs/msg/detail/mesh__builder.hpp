// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from nvblox_msgs:msg/Mesh.idl
// generated code does not contain a copyright notice

#ifndef NVBLOX_MSGS__MSG__DETAIL__MESH__BUILDER_HPP_
#define NVBLOX_MSGS__MSG__DETAIL__MESH__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "nvblox_msgs/msg/detail/mesh__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace nvblox_msgs
{

namespace msg
{

namespace builder
{

class Init_Mesh_clear
{
public:
  explicit Init_Mesh_clear(::nvblox_msgs::msg::Mesh & msg)
  : msg_(msg)
  {}
  ::nvblox_msgs::msg::Mesh clear(::nvblox_msgs::msg::Mesh::_clear_type arg)
  {
    msg_.clear = std::move(arg);
    return std::move(msg_);
  }

private:
  ::nvblox_msgs::msg::Mesh msg_;
};

class Init_Mesh_blocks
{
public:
  explicit Init_Mesh_blocks(::nvblox_msgs::msg::Mesh & msg)
  : msg_(msg)
  {}
  Init_Mesh_clear blocks(::nvblox_msgs::msg::Mesh::_blocks_type arg)
  {
    msg_.blocks = std::move(arg);
    return Init_Mesh_clear(msg_);
  }

private:
  ::nvblox_msgs::msg::Mesh msg_;
};

class Init_Mesh_block_indices
{
public:
  explicit Init_Mesh_block_indices(::nvblox_msgs::msg::Mesh & msg)
  : msg_(msg)
  {}
  Init_Mesh_blocks block_indices(::nvblox_msgs::msg::Mesh::_block_indices_type arg)
  {
    msg_.block_indices = std::move(arg);
    return Init_Mesh_blocks(msg_);
  }

private:
  ::nvblox_msgs::msg::Mesh msg_;
};

class Init_Mesh_block_size
{
public:
  explicit Init_Mesh_block_size(::nvblox_msgs::msg::Mesh & msg)
  : msg_(msg)
  {}
  Init_Mesh_block_indices block_size(::nvblox_msgs::msg::Mesh::_block_size_type arg)
  {
    msg_.block_size = std::move(arg);
    return Init_Mesh_block_indices(msg_);
  }

private:
  ::nvblox_msgs::msg::Mesh msg_;
};

class Init_Mesh_header
{
public:
  Init_Mesh_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Mesh_block_size header(::nvblox_msgs::msg::Mesh::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_Mesh_block_size(msg_);
  }

private:
  ::nvblox_msgs::msg::Mesh msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::nvblox_msgs::msg::Mesh>()
{
  return nvblox_msgs::msg::builder::Init_Mesh_header();
}

}  // namespace nvblox_msgs

#endif  // NVBLOX_MSGS__MSG__DETAIL__MESH__BUILDER_HPP_
