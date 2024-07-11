// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from go2_interfaces:msg/Go2RpyCmd.idl
// generated code does not contain a copyright notice

#ifndef GO2_INTERFACES__MSG__DETAIL__GO2_RPY_CMD__BUILDER_HPP_
#define GO2_INTERFACES__MSG__DETAIL__GO2_RPY_CMD__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "go2_interfaces/msg/detail/go2_rpy_cmd__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace go2_interfaces
{

namespace msg
{

namespace builder
{

class Init_Go2RpyCmd_yaw
{
public:
  explicit Init_Go2RpyCmd_yaw(::go2_interfaces::msg::Go2RpyCmd & msg)
  : msg_(msg)
  {}
  ::go2_interfaces::msg::Go2RpyCmd yaw(::go2_interfaces::msg::Go2RpyCmd::_yaw_type arg)
  {
    msg_.yaw = std::move(arg);
    return std::move(msg_);
  }

private:
  ::go2_interfaces::msg::Go2RpyCmd msg_;
};

class Init_Go2RpyCmd_pitch
{
public:
  explicit Init_Go2RpyCmd_pitch(::go2_interfaces::msg::Go2RpyCmd & msg)
  : msg_(msg)
  {}
  Init_Go2RpyCmd_yaw pitch(::go2_interfaces::msg::Go2RpyCmd::_pitch_type arg)
  {
    msg_.pitch = std::move(arg);
    return Init_Go2RpyCmd_yaw(msg_);
  }

private:
  ::go2_interfaces::msg::Go2RpyCmd msg_;
};

class Init_Go2RpyCmd_roll
{
public:
  Init_Go2RpyCmd_roll()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Go2RpyCmd_pitch roll(::go2_interfaces::msg::Go2RpyCmd::_roll_type arg)
  {
    msg_.roll = std::move(arg);
    return Init_Go2RpyCmd_pitch(msg_);
  }

private:
  ::go2_interfaces::msg::Go2RpyCmd msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::go2_interfaces::msg::Go2RpyCmd>()
{
  return go2_interfaces::msg::builder::Init_Go2RpyCmd_roll();
}

}  // namespace go2_interfaces

#endif  // GO2_INTERFACES__MSG__DETAIL__GO2_RPY_CMD__BUILDER_HPP_
