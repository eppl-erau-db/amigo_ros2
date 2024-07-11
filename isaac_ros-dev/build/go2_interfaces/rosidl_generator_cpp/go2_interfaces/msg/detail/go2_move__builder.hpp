// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from go2_interfaces:msg/Go2Move.idl
// generated code does not contain a copyright notice

#ifndef GO2_INTERFACES__MSG__DETAIL__GO2_MOVE__BUILDER_HPP_
#define GO2_INTERFACES__MSG__DETAIL__GO2_MOVE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "go2_interfaces/msg/detail/go2_move__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace go2_interfaces
{

namespace msg
{

namespace builder
{

class Init_Go2Move_z
{
public:
  explicit Init_Go2Move_z(::go2_interfaces::msg::Go2Move & msg)
  : msg_(msg)
  {}
  ::go2_interfaces::msg::Go2Move z(::go2_interfaces::msg::Go2Move::_z_type arg)
  {
    msg_.z = std::move(arg);
    return std::move(msg_);
  }

private:
  ::go2_interfaces::msg::Go2Move msg_;
};

class Init_Go2Move_y
{
public:
  explicit Init_Go2Move_y(::go2_interfaces::msg::Go2Move & msg)
  : msg_(msg)
  {}
  Init_Go2Move_z y(::go2_interfaces::msg::Go2Move::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_Go2Move_z(msg_);
  }

private:
  ::go2_interfaces::msg::Go2Move msg_;
};

class Init_Go2Move_x
{
public:
  Init_Go2Move_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Go2Move_y x(::go2_interfaces::msg::Go2Move::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_Go2Move_y(msg_);
  }

private:
  ::go2_interfaces::msg::Go2Move msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::go2_interfaces::msg::Go2Move>()
{
  return go2_interfaces::msg::builder::Init_Go2Move_x();
}

}  // namespace go2_interfaces

#endif  // GO2_INTERFACES__MSG__DETAIL__GO2_MOVE__BUILDER_HPP_
