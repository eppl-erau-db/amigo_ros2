// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from nvblox_msgs:msg/DistanceMapSlice.idl
// generated code does not contain a copyright notice

#ifndef NVBLOX_MSGS__MSG__DETAIL__DISTANCE_MAP_SLICE__BUILDER_HPP_
#define NVBLOX_MSGS__MSG__DETAIL__DISTANCE_MAP_SLICE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "nvblox_msgs/msg/detail/distance_map_slice__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace nvblox_msgs
{

namespace msg
{

namespace builder
{

class Init_DistanceMapSlice_data
{
public:
  explicit Init_DistanceMapSlice_data(::nvblox_msgs::msg::DistanceMapSlice & msg)
  : msg_(msg)
  {}
  ::nvblox_msgs::msg::DistanceMapSlice data(::nvblox_msgs::msg::DistanceMapSlice::_data_type arg)
  {
    msg_.data = std::move(arg);
    return std::move(msg_);
  }

private:
  ::nvblox_msgs::msg::DistanceMapSlice msg_;
};

class Init_DistanceMapSlice_unknown_value
{
public:
  explicit Init_DistanceMapSlice_unknown_value(::nvblox_msgs::msg::DistanceMapSlice & msg)
  : msg_(msg)
  {}
  Init_DistanceMapSlice_data unknown_value(::nvblox_msgs::msg::DistanceMapSlice::_unknown_value_type arg)
  {
    msg_.unknown_value = std::move(arg);
    return Init_DistanceMapSlice_data(msg_);
  }

private:
  ::nvblox_msgs::msg::DistanceMapSlice msg_;
};

class Init_DistanceMapSlice_origin
{
public:
  explicit Init_DistanceMapSlice_origin(::nvblox_msgs::msg::DistanceMapSlice & msg)
  : msg_(msg)
  {}
  Init_DistanceMapSlice_unknown_value origin(::nvblox_msgs::msg::DistanceMapSlice::_origin_type arg)
  {
    msg_.origin = std::move(arg);
    return Init_DistanceMapSlice_unknown_value(msg_);
  }

private:
  ::nvblox_msgs::msg::DistanceMapSlice msg_;
};

class Init_DistanceMapSlice_height
{
public:
  explicit Init_DistanceMapSlice_height(::nvblox_msgs::msg::DistanceMapSlice & msg)
  : msg_(msg)
  {}
  Init_DistanceMapSlice_origin height(::nvblox_msgs::msg::DistanceMapSlice::_height_type arg)
  {
    msg_.height = std::move(arg);
    return Init_DistanceMapSlice_origin(msg_);
  }

private:
  ::nvblox_msgs::msg::DistanceMapSlice msg_;
};

class Init_DistanceMapSlice_width
{
public:
  explicit Init_DistanceMapSlice_width(::nvblox_msgs::msg::DistanceMapSlice & msg)
  : msg_(msg)
  {}
  Init_DistanceMapSlice_height width(::nvblox_msgs::msg::DistanceMapSlice::_width_type arg)
  {
    msg_.width = std::move(arg);
    return Init_DistanceMapSlice_height(msg_);
  }

private:
  ::nvblox_msgs::msg::DistanceMapSlice msg_;
};

class Init_DistanceMapSlice_resolution
{
public:
  explicit Init_DistanceMapSlice_resolution(::nvblox_msgs::msg::DistanceMapSlice & msg)
  : msg_(msg)
  {}
  Init_DistanceMapSlice_width resolution(::nvblox_msgs::msg::DistanceMapSlice::_resolution_type arg)
  {
    msg_.resolution = std::move(arg);
    return Init_DistanceMapSlice_width(msg_);
  }

private:
  ::nvblox_msgs::msg::DistanceMapSlice msg_;
};

class Init_DistanceMapSlice_header
{
public:
  Init_DistanceMapSlice_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_DistanceMapSlice_resolution header(::nvblox_msgs::msg::DistanceMapSlice::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_DistanceMapSlice_resolution(msg_);
  }

private:
  ::nvblox_msgs::msg::DistanceMapSlice msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::nvblox_msgs::msg::DistanceMapSlice>()
{
  return nvblox_msgs::msg::builder::Init_DistanceMapSlice_header();
}

}  // namespace nvblox_msgs

#endif  // NVBLOX_MSGS__MSG__DETAIL__DISTANCE_MAP_SLICE__BUILDER_HPP_
