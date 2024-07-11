// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from isaac_ros_nova_interfaces:msg/EncoderTicks.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_NOVA_INTERFACES__MSG__DETAIL__ENCODER_TICKS__BUILDER_HPP_
#define ISAAC_ROS_NOVA_INTERFACES__MSG__DETAIL__ENCODER_TICKS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "isaac_ros_nova_interfaces/msg/detail/encoder_ticks__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace isaac_ros_nova_interfaces
{

namespace msg
{

namespace builder
{

class Init_EncoderTicks_encoder_timestamp
{
public:
  explicit Init_EncoderTicks_encoder_timestamp(::isaac_ros_nova_interfaces::msg::EncoderTicks & msg)
  : msg_(msg)
  {}
  ::isaac_ros_nova_interfaces::msg::EncoderTicks encoder_timestamp(::isaac_ros_nova_interfaces::msg::EncoderTicks::_encoder_timestamp_type arg)
  {
    msg_.encoder_timestamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::isaac_ros_nova_interfaces::msg::EncoderTicks msg_;
};

class Init_EncoderTicks_right_ticks
{
public:
  explicit Init_EncoderTicks_right_ticks(::isaac_ros_nova_interfaces::msg::EncoderTicks & msg)
  : msg_(msg)
  {}
  Init_EncoderTicks_encoder_timestamp right_ticks(::isaac_ros_nova_interfaces::msg::EncoderTicks::_right_ticks_type arg)
  {
    msg_.right_ticks = std::move(arg);
    return Init_EncoderTicks_encoder_timestamp(msg_);
  }

private:
  ::isaac_ros_nova_interfaces::msg::EncoderTicks msg_;
};

class Init_EncoderTicks_left_ticks
{
public:
  explicit Init_EncoderTicks_left_ticks(::isaac_ros_nova_interfaces::msg::EncoderTicks & msg)
  : msg_(msg)
  {}
  Init_EncoderTicks_right_ticks left_ticks(::isaac_ros_nova_interfaces::msg::EncoderTicks::_left_ticks_type arg)
  {
    msg_.left_ticks = std::move(arg);
    return Init_EncoderTicks_right_ticks(msg_);
  }

private:
  ::isaac_ros_nova_interfaces::msg::EncoderTicks msg_;
};

class Init_EncoderTicks_header
{
public:
  Init_EncoderTicks_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_EncoderTicks_left_ticks header(::isaac_ros_nova_interfaces::msg::EncoderTicks::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_EncoderTicks_left_ticks(msg_);
  }

private:
  ::isaac_ros_nova_interfaces::msg::EncoderTicks msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::isaac_ros_nova_interfaces::msg::EncoderTicks>()
{
  return isaac_ros_nova_interfaces::msg::builder::Init_EncoderTicks_header();
}

}  // namespace isaac_ros_nova_interfaces

#endif  // ISAAC_ROS_NOVA_INTERFACES__MSG__DETAIL__ENCODER_TICKS__BUILDER_HPP_
