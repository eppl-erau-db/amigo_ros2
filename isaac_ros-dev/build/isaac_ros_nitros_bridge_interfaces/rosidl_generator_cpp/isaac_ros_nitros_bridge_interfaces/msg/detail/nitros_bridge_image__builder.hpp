// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from isaac_ros_nitros_bridge_interfaces:msg/NitrosBridgeImage.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_NITROS_BRIDGE_INTERFACES__MSG__DETAIL__NITROS_BRIDGE_IMAGE__BUILDER_HPP_
#define ISAAC_ROS_NITROS_BRIDGE_INTERFACES__MSG__DETAIL__NITROS_BRIDGE_IMAGE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "isaac_ros_nitros_bridge_interfaces/msg/detail/nitros_bridge_image__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace isaac_ros_nitros_bridge_interfaces
{

namespace msg
{

namespace builder
{

class Init_NitrosBridgeImage_data
{
public:
  explicit Init_NitrosBridgeImage_data(::isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage & msg)
  : msg_(msg)
  {}
  ::isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage data(::isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage::_data_type arg)
  {
    msg_.data = std::move(arg);
    return std::move(msg_);
  }

private:
  ::isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage msg_;
};

class Init_NitrosBridgeImage_step
{
public:
  explicit Init_NitrosBridgeImage_step(::isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage & msg)
  : msg_(msg)
  {}
  Init_NitrosBridgeImage_data step(::isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage::_step_type arg)
  {
    msg_.step = std::move(arg);
    return Init_NitrosBridgeImage_data(msg_);
  }

private:
  ::isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage msg_;
};

class Init_NitrosBridgeImage_is_bigendian
{
public:
  explicit Init_NitrosBridgeImage_is_bigendian(::isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage & msg)
  : msg_(msg)
  {}
  Init_NitrosBridgeImage_step is_bigendian(::isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage::_is_bigendian_type arg)
  {
    msg_.is_bigendian = std::move(arg);
    return Init_NitrosBridgeImage_step(msg_);
  }

private:
  ::isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage msg_;
};

class Init_NitrosBridgeImage_encoding
{
public:
  explicit Init_NitrosBridgeImage_encoding(::isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage & msg)
  : msg_(msg)
  {}
  Init_NitrosBridgeImage_is_bigendian encoding(::isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage::_encoding_type arg)
  {
    msg_.encoding = std::move(arg);
    return Init_NitrosBridgeImage_is_bigendian(msg_);
  }

private:
  ::isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage msg_;
};

class Init_NitrosBridgeImage_width
{
public:
  explicit Init_NitrosBridgeImage_width(::isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage & msg)
  : msg_(msg)
  {}
  Init_NitrosBridgeImage_encoding width(::isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage::_width_type arg)
  {
    msg_.width = std::move(arg);
    return Init_NitrosBridgeImage_encoding(msg_);
  }

private:
  ::isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage msg_;
};

class Init_NitrosBridgeImage_height
{
public:
  explicit Init_NitrosBridgeImage_height(::isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage & msg)
  : msg_(msg)
  {}
  Init_NitrosBridgeImage_width height(::isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage::_height_type arg)
  {
    msg_.height = std::move(arg);
    return Init_NitrosBridgeImage_width(msg_);
  }

private:
  ::isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage msg_;
};

class Init_NitrosBridgeImage_header
{
public:
  Init_NitrosBridgeImage_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_NitrosBridgeImage_height header(::isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_NitrosBridgeImage_height(msg_);
  }

private:
  ::isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage>()
{
  return isaac_ros_nitros_bridge_interfaces::msg::builder::Init_NitrosBridgeImage_header();
}

}  // namespace isaac_ros_nitros_bridge_interfaces

#endif  // ISAAC_ROS_NITROS_BRIDGE_INTERFACES__MSG__DETAIL__NITROS_BRIDGE_IMAGE__BUILDER_HPP_
