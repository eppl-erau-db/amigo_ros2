// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from go2_interfaces:msg/Go2State.idl
// generated code does not contain a copyright notice

#ifndef GO2_INTERFACES__MSG__DETAIL__GO2_STATE__BUILDER_HPP_
#define GO2_INTERFACES__MSG__DETAIL__GO2_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "go2_interfaces/msg/detail/go2_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace go2_interfaces
{

namespace msg
{

namespace builder
{

class Init_Go2State_foot_speed_body
{
public:
  explicit Init_Go2State_foot_speed_body(::go2_interfaces::msg::Go2State & msg)
  : msg_(msg)
  {}
  ::go2_interfaces::msg::Go2State foot_speed_body(::go2_interfaces::msg::Go2State::_foot_speed_body_type arg)
  {
    msg_.foot_speed_body = std::move(arg);
    return std::move(msg_);
  }

private:
  ::go2_interfaces::msg::Go2State msg_;
};

class Init_Go2State_foot_position_body
{
public:
  explicit Init_Go2State_foot_position_body(::go2_interfaces::msg::Go2State & msg)
  : msg_(msg)
  {}
  Init_Go2State_foot_speed_body foot_position_body(::go2_interfaces::msg::Go2State::_foot_position_body_type arg)
  {
    msg_.foot_position_body = std::move(arg);
    return Init_Go2State_foot_speed_body(msg_);
  }

private:
  ::go2_interfaces::msg::Go2State msg_;
};

class Init_Go2State_foot_force
{
public:
  explicit Init_Go2State_foot_force(::go2_interfaces::msg::Go2State & msg)
  : msg_(msg)
  {}
  Init_Go2State_foot_position_body foot_force(::go2_interfaces::msg::Go2State::_foot_force_type arg)
  {
    msg_.foot_force = std::move(arg);
    return Init_Go2State_foot_position_body(msg_);
  }

private:
  ::go2_interfaces::msg::Go2State msg_;
};

class Init_Go2State_range_obstacle
{
public:
  explicit Init_Go2State_range_obstacle(::go2_interfaces::msg::Go2State & msg)
  : msg_(msg)
  {}
  Init_Go2State_foot_force range_obstacle(::go2_interfaces::msg::Go2State::_range_obstacle_type arg)
  {
    msg_.range_obstacle = std::move(arg);
    return Init_Go2State_foot_force(msg_);
  }

private:
  ::go2_interfaces::msg::Go2State msg_;
};

class Init_Go2State_velocity
{
public:
  explicit Init_Go2State_velocity(::go2_interfaces::msg::Go2State & msg)
  : msg_(msg)
  {}
  Init_Go2State_range_obstacle velocity(::go2_interfaces::msg::Go2State::_velocity_type arg)
  {
    msg_.velocity = std::move(arg);
    return Init_Go2State_range_obstacle(msg_);
  }

private:
  ::go2_interfaces::msg::Go2State msg_;
};

class Init_Go2State_body_height
{
public:
  explicit Init_Go2State_body_height(::go2_interfaces::msg::Go2State & msg)
  : msg_(msg)
  {}
  Init_Go2State_velocity body_height(::go2_interfaces::msg::Go2State::_body_height_type arg)
  {
    msg_.body_height = std::move(arg);
    return Init_Go2State_velocity(msg_);
  }

private:
  ::go2_interfaces::msg::Go2State msg_;
};

class Init_Go2State_position
{
public:
  explicit Init_Go2State_position(::go2_interfaces::msg::Go2State & msg)
  : msg_(msg)
  {}
  Init_Go2State_body_height position(::go2_interfaces::msg::Go2State::_position_type arg)
  {
    msg_.position = std::move(arg);
    return Init_Go2State_body_height(msg_);
  }

private:
  ::go2_interfaces::msg::Go2State msg_;
};

class Init_Go2State_foot_raise_height
{
public:
  explicit Init_Go2State_foot_raise_height(::go2_interfaces::msg::Go2State & msg)
  : msg_(msg)
  {}
  Init_Go2State_position foot_raise_height(::go2_interfaces::msg::Go2State::_foot_raise_height_type arg)
  {
    msg_.foot_raise_height = std::move(arg);
    return Init_Go2State_position(msg_);
  }

private:
  ::go2_interfaces::msg::Go2State msg_;
};

class Init_Go2State_gait_type
{
public:
  explicit Init_Go2State_gait_type(::go2_interfaces::msg::Go2State & msg)
  : msg_(msg)
  {}
  Init_Go2State_foot_raise_height gait_type(::go2_interfaces::msg::Go2State::_gait_type_type arg)
  {
    msg_.gait_type = std::move(arg);
    return Init_Go2State_foot_raise_height(msg_);
  }

private:
  ::go2_interfaces::msg::Go2State msg_;
};

class Init_Go2State_progress
{
public:
  explicit Init_Go2State_progress(::go2_interfaces::msg::Go2State & msg)
  : msg_(msg)
  {}
  Init_Go2State_gait_type progress(::go2_interfaces::msg::Go2State::_progress_type arg)
  {
    msg_.progress = std::move(arg);
    return Init_Go2State_gait_type(msg_);
  }

private:
  ::go2_interfaces::msg::Go2State msg_;
};

class Init_Go2State_mode
{
public:
  Init_Go2State_mode()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Go2State_progress mode(::go2_interfaces::msg::Go2State::_mode_type arg)
  {
    msg_.mode = std::move(arg);
    return Init_Go2State_progress(msg_);
  }

private:
  ::go2_interfaces::msg::Go2State msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::go2_interfaces::msg::Go2State>()
{
  return go2_interfaces::msg::builder::Init_Go2State_mode();
}

}  // namespace go2_interfaces

#endif  // GO2_INTERFACES__MSG__DETAIL__GO2_STATE__BUILDER_HPP_
