// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from realsense2_camera_msgs:msg/Metadata.idl
// generated code does not contain a copyright notice

#ifndef REALSENSE2_CAMERA_MSGS__MSG__DETAIL__METADATA__BUILDER_HPP_
#define REALSENSE2_CAMERA_MSGS__MSG__DETAIL__METADATA__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "realsense2_camera_msgs/msg/detail/metadata__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace realsense2_camera_msgs
{

namespace msg
{

namespace builder
{

class Init_Metadata_json_data
{
public:
  explicit Init_Metadata_json_data(::realsense2_camera_msgs::msg::Metadata & msg)
  : msg_(msg)
  {}
  ::realsense2_camera_msgs::msg::Metadata json_data(::realsense2_camera_msgs::msg::Metadata::_json_data_type arg)
  {
    msg_.json_data = std::move(arg);
    return std::move(msg_);
  }

private:
  ::realsense2_camera_msgs::msg::Metadata msg_;
};

class Init_Metadata_header
{
public:
  Init_Metadata_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Metadata_json_data header(::realsense2_camera_msgs::msg::Metadata::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_Metadata_json_data(msg_);
  }

private:
  ::realsense2_camera_msgs::msg::Metadata msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::realsense2_camera_msgs::msg::Metadata>()
{
  return realsense2_camera_msgs::msg::builder::Init_Metadata_header();
}

}  // namespace realsense2_camera_msgs

#endif  // REALSENSE2_CAMERA_MSGS__MSG__DETAIL__METADATA__BUILDER_HPP_
