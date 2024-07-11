// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from isaac_ros_nova_interfaces:msg/CorrelatedTimestamp.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_NOVA_INTERFACES__MSG__DETAIL__CORRELATED_TIMESTAMP__BUILDER_HPP_
#define ISAAC_ROS_NOVA_INTERFACES__MSG__DETAIL__CORRELATED_TIMESTAMP__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "isaac_ros_nova_interfaces/msg/detail/correlated_timestamp__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace isaac_ros_nova_interfaces
{

namespace msg
{

namespace builder
{

class Init_CorrelatedTimestamp_phc_latency
{
public:
  explicit Init_CorrelatedTimestamp_phc_latency(::isaac_ros_nova_interfaces::msg::CorrelatedTimestamp & msg)
  : msg_(msg)
  {}
  ::isaac_ros_nova_interfaces::msg::CorrelatedTimestamp phc_latency(::isaac_ros_nova_interfaces::msg::CorrelatedTimestamp::_phc_latency_type arg)
  {
    msg_.phc_latency = std::move(arg);
    return std::move(msg_);
  }

private:
  ::isaac_ros_nova_interfaces::msg::CorrelatedTimestamp msg_;
};

class Init_CorrelatedTimestamp_sys_val
{
public:
  explicit Init_CorrelatedTimestamp_sys_val(::isaac_ros_nova_interfaces::msg::CorrelatedTimestamp & msg)
  : msg_(msg)
  {}
  Init_CorrelatedTimestamp_phc_latency sys_val(::isaac_ros_nova_interfaces::msg::CorrelatedTimestamp::_sys_val_type arg)
  {
    msg_.sys_val = std::move(arg);
    return Init_CorrelatedTimestamp_phc_latency(msg_);
  }

private:
  ::isaac_ros_nova_interfaces::msg::CorrelatedTimestamp msg_;
};

class Init_CorrelatedTimestamp_phc2_val
{
public:
  explicit Init_CorrelatedTimestamp_phc2_val(::isaac_ros_nova_interfaces::msg::CorrelatedTimestamp & msg)
  : msg_(msg)
  {}
  Init_CorrelatedTimestamp_sys_val phc2_val(::isaac_ros_nova_interfaces::msg::CorrelatedTimestamp::_phc2_val_type arg)
  {
    msg_.phc2_val = std::move(arg);
    return Init_CorrelatedTimestamp_sys_val(msg_);
  }

private:
  ::isaac_ros_nova_interfaces::msg::CorrelatedTimestamp msg_;
};

class Init_CorrelatedTimestamp_tsc_val
{
public:
  explicit Init_CorrelatedTimestamp_tsc_val(::isaac_ros_nova_interfaces::msg::CorrelatedTimestamp & msg)
  : msg_(msg)
  {}
  Init_CorrelatedTimestamp_phc2_val tsc_val(::isaac_ros_nova_interfaces::msg::CorrelatedTimestamp::_tsc_val_type arg)
  {
    msg_.tsc_val = std::move(arg);
    return Init_CorrelatedTimestamp_phc2_val(msg_);
  }

private:
  ::isaac_ros_nova_interfaces::msg::CorrelatedTimestamp msg_;
};

class Init_CorrelatedTimestamp_phc_val
{
public:
  explicit Init_CorrelatedTimestamp_phc_val(::isaac_ros_nova_interfaces::msg::CorrelatedTimestamp & msg)
  : msg_(msg)
  {}
  Init_CorrelatedTimestamp_tsc_val phc_val(::isaac_ros_nova_interfaces::msg::CorrelatedTimestamp::_phc_val_type arg)
  {
    msg_.phc_val = std::move(arg);
    return Init_CorrelatedTimestamp_tsc_val(msg_);
  }

private:
  ::isaac_ros_nova_interfaces::msg::CorrelatedTimestamp msg_;
};

class Init_CorrelatedTimestamp_header
{
public:
  Init_CorrelatedTimestamp_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_CorrelatedTimestamp_phc_val header(::isaac_ros_nova_interfaces::msg::CorrelatedTimestamp::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_CorrelatedTimestamp_phc_val(msg_);
  }

private:
  ::isaac_ros_nova_interfaces::msg::CorrelatedTimestamp msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::isaac_ros_nova_interfaces::msg::CorrelatedTimestamp>()
{
  return isaac_ros_nova_interfaces::msg::builder::Init_CorrelatedTimestamp_header();
}

}  // namespace isaac_ros_nova_interfaces

#endif  // ISAAC_ROS_NOVA_INTERFACES__MSG__DETAIL__CORRELATED_TIMESTAMP__BUILDER_HPP_
