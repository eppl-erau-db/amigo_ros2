// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from go2_interfaces:msg/IMU.idl
// generated code does not contain a copyright notice

#ifndef GO2_INTERFACES__MSG__DETAIL__IMU__BUILDER_HPP_
#define GO2_INTERFACES__MSG__DETAIL__IMU__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "go2_interfaces/msg/detail/imu__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace go2_interfaces
{

namespace msg
{

namespace builder
{

class Init_IMU_temperature
{
public:
  explicit Init_IMU_temperature(::go2_interfaces::msg::IMU & msg)
  : msg_(msg)
  {}
  ::go2_interfaces::msg::IMU temperature(::go2_interfaces::msg::IMU::_temperature_type arg)
  {
    msg_.temperature = std::move(arg);
    return std::move(msg_);
  }

private:
  ::go2_interfaces::msg::IMU msg_;
};

class Init_IMU_rpy
{
public:
  explicit Init_IMU_rpy(::go2_interfaces::msg::IMU & msg)
  : msg_(msg)
  {}
  Init_IMU_temperature rpy(::go2_interfaces::msg::IMU::_rpy_type arg)
  {
    msg_.rpy = std::move(arg);
    return Init_IMU_temperature(msg_);
  }

private:
  ::go2_interfaces::msg::IMU msg_;
};

class Init_IMU_accelerometer
{
public:
  explicit Init_IMU_accelerometer(::go2_interfaces::msg::IMU & msg)
  : msg_(msg)
  {}
  Init_IMU_rpy accelerometer(::go2_interfaces::msg::IMU::_accelerometer_type arg)
  {
    msg_.accelerometer = std::move(arg);
    return Init_IMU_rpy(msg_);
  }

private:
  ::go2_interfaces::msg::IMU msg_;
};

class Init_IMU_gyroscope
{
public:
  explicit Init_IMU_gyroscope(::go2_interfaces::msg::IMU & msg)
  : msg_(msg)
  {}
  Init_IMU_accelerometer gyroscope(::go2_interfaces::msg::IMU::_gyroscope_type arg)
  {
    msg_.gyroscope = std::move(arg);
    return Init_IMU_accelerometer(msg_);
  }

private:
  ::go2_interfaces::msg::IMU msg_;
};

class Init_IMU_quaternion
{
public:
  Init_IMU_quaternion()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_IMU_gyroscope quaternion(::go2_interfaces::msg::IMU::_quaternion_type arg)
  {
    msg_.quaternion = std::move(arg);
    return Init_IMU_gyroscope(msg_);
  }

private:
  ::go2_interfaces::msg::IMU msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::go2_interfaces::msg::IMU>()
{
  return go2_interfaces::msg::builder::Init_IMU_quaternion();
}

}  // namespace go2_interfaces

#endif  // GO2_INTERFACES__MSG__DETAIL__IMU__BUILDER_HPP_
