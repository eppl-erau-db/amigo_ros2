// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from nvblox_msgs:msg/MeshBlock.idl
// generated code does not contain a copyright notice

#ifndef NVBLOX_MSGS__MSG__DETAIL__MESH_BLOCK__BUILDER_HPP_
#define NVBLOX_MSGS__MSG__DETAIL__MESH_BLOCK__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "nvblox_msgs/msg/detail/mesh_block__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace nvblox_msgs
{

namespace msg
{

namespace builder
{

class Init_MeshBlock_triangles
{
public:
  explicit Init_MeshBlock_triangles(::nvblox_msgs::msg::MeshBlock & msg)
  : msg_(msg)
  {}
  ::nvblox_msgs::msg::MeshBlock triangles(::nvblox_msgs::msg::MeshBlock::_triangles_type arg)
  {
    msg_.triangles = std::move(arg);
    return std::move(msg_);
  }

private:
  ::nvblox_msgs::msg::MeshBlock msg_;
};

class Init_MeshBlock_colors
{
public:
  explicit Init_MeshBlock_colors(::nvblox_msgs::msg::MeshBlock & msg)
  : msg_(msg)
  {}
  Init_MeshBlock_triangles colors(::nvblox_msgs::msg::MeshBlock::_colors_type arg)
  {
    msg_.colors = std::move(arg);
    return Init_MeshBlock_triangles(msg_);
  }

private:
  ::nvblox_msgs::msg::MeshBlock msg_;
};

class Init_MeshBlock_normals
{
public:
  explicit Init_MeshBlock_normals(::nvblox_msgs::msg::MeshBlock & msg)
  : msg_(msg)
  {}
  Init_MeshBlock_colors normals(::nvblox_msgs::msg::MeshBlock::_normals_type arg)
  {
    msg_.normals = std::move(arg);
    return Init_MeshBlock_colors(msg_);
  }

private:
  ::nvblox_msgs::msg::MeshBlock msg_;
};

class Init_MeshBlock_vertices
{
public:
  Init_MeshBlock_vertices()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MeshBlock_normals vertices(::nvblox_msgs::msg::MeshBlock::_vertices_type arg)
  {
    msg_.vertices = std::move(arg);
    return Init_MeshBlock_normals(msg_);
  }

private:
  ::nvblox_msgs::msg::MeshBlock msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::nvblox_msgs::msg::MeshBlock>()
{
  return nvblox_msgs::msg::builder::Init_MeshBlock_vertices();
}

}  // namespace nvblox_msgs

#endif  // NVBLOX_MSGS__MSG__DETAIL__MESH_BLOCK__BUILDER_HPP_
