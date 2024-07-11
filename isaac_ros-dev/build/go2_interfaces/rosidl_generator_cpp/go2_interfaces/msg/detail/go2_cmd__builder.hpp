// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from go2_interfaces:msg/Go2Cmd.idl
// generated code does not contain a copyright notice

#ifndef GO2_INTERFACES__MSG__DETAIL__GO2_CMD__BUILDER_HPP_
#define GO2_INTERFACES__MSG__DETAIL__GO2_CMD__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "go2_interfaces/msg/detail/go2_cmd__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace go2_interfaces
{

namespace msg
{

namespace builder
{

class Init_Go2Cmd_cmd
{
public:
  Init_Go2Cmd_cmd()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::go2_interfaces::msg::Go2Cmd cmd(::go2_interfaces::msg::Go2Cmd::_cmd_type arg)
  {
    msg_.cmd = std::move(arg);
    return std::move(msg_);
  }

private:
  ::go2_interfaces::msg::Go2Cmd msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::go2_interfaces::msg::Go2Cmd>()
{
  return go2_interfaces::msg::builder::Init_Go2Cmd_cmd();
}

}  // namespace go2_interfaces

#endif  // GO2_INTERFACES__MSG__DETAIL__GO2_CMD__BUILDER_HPP_
