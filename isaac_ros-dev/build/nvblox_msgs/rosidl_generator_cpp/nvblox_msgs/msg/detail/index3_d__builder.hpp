// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from nvblox_msgs:msg/Index3D.idl
// generated code does not contain a copyright notice

#ifndef NVBLOX_MSGS__MSG__DETAIL__INDEX3_D__BUILDER_HPP_
#define NVBLOX_MSGS__MSG__DETAIL__INDEX3_D__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "nvblox_msgs/msg/detail/index3_d__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace nvblox_msgs
{

namespace msg
{

namespace builder
{

class Init_Index3D_z
{
public:
  explicit Init_Index3D_z(::nvblox_msgs::msg::Index3D & msg)
  : msg_(msg)
  {}
  ::nvblox_msgs::msg::Index3D z(::nvblox_msgs::msg::Index3D::_z_type arg)
  {
    msg_.z = std::move(arg);
    return std::move(msg_);
  }

private:
  ::nvblox_msgs::msg::Index3D msg_;
};

class Init_Index3D_y
{
public:
  explicit Init_Index3D_y(::nvblox_msgs::msg::Index3D & msg)
  : msg_(msg)
  {}
  Init_Index3D_z y(::nvblox_msgs::msg::Index3D::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_Index3D_z(msg_);
  }

private:
  ::nvblox_msgs::msg::Index3D msg_;
};

class Init_Index3D_x
{
public:
  Init_Index3D_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Index3D_y x(::nvblox_msgs::msg::Index3D::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_Index3D_y(msg_);
  }

private:
  ::nvblox_msgs::msg::Index3D msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::nvblox_msgs::msg::Index3D>()
{
  return nvblox_msgs::msg::builder::Init_Index3D_x();
}

}  // namespace nvblox_msgs

#endif  // NVBLOX_MSGS__MSG__DETAIL__INDEX3_D__BUILDER_HPP_
