// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from isaac_ros_pointcloud_interfaces:msg/FlatScan.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_POINTCLOUD_INTERFACES__MSG__DETAIL__FLAT_SCAN__BUILDER_HPP_
#define ISAAC_ROS_POINTCLOUD_INTERFACES__MSG__DETAIL__FLAT_SCAN__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "isaac_ros_pointcloud_interfaces/msg/detail/flat_scan__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace isaac_ros_pointcloud_interfaces
{

namespace msg
{

namespace builder
{

class Init_FlatScan_intensities
{
public:
  explicit Init_FlatScan_intensities(::isaac_ros_pointcloud_interfaces::msg::FlatScan & msg)
  : msg_(msg)
  {}
  ::isaac_ros_pointcloud_interfaces::msg::FlatScan intensities(::isaac_ros_pointcloud_interfaces::msg::FlatScan::_intensities_type arg)
  {
    msg_.intensities = std::move(arg);
    return std::move(msg_);
  }

private:
  ::isaac_ros_pointcloud_interfaces::msg::FlatScan msg_;
};

class Init_FlatScan_ranges
{
public:
  explicit Init_FlatScan_ranges(::isaac_ros_pointcloud_interfaces::msg::FlatScan & msg)
  : msg_(msg)
  {}
  Init_FlatScan_intensities ranges(::isaac_ros_pointcloud_interfaces::msg::FlatScan::_ranges_type arg)
  {
    msg_.ranges = std::move(arg);
    return Init_FlatScan_intensities(msg_);
  }

private:
  ::isaac_ros_pointcloud_interfaces::msg::FlatScan msg_;
};

class Init_FlatScan_angles
{
public:
  explicit Init_FlatScan_angles(::isaac_ros_pointcloud_interfaces::msg::FlatScan & msg)
  : msg_(msg)
  {}
  Init_FlatScan_ranges angles(::isaac_ros_pointcloud_interfaces::msg::FlatScan::_angles_type arg)
  {
    msg_.angles = std::move(arg);
    return Init_FlatScan_ranges(msg_);
  }

private:
  ::isaac_ros_pointcloud_interfaces::msg::FlatScan msg_;
};

class Init_FlatScan_range_max
{
public:
  explicit Init_FlatScan_range_max(::isaac_ros_pointcloud_interfaces::msg::FlatScan & msg)
  : msg_(msg)
  {}
  Init_FlatScan_angles range_max(::isaac_ros_pointcloud_interfaces::msg::FlatScan::_range_max_type arg)
  {
    msg_.range_max = std::move(arg);
    return Init_FlatScan_angles(msg_);
  }

private:
  ::isaac_ros_pointcloud_interfaces::msg::FlatScan msg_;
};

class Init_FlatScan_range_min
{
public:
  explicit Init_FlatScan_range_min(::isaac_ros_pointcloud_interfaces::msg::FlatScan & msg)
  : msg_(msg)
  {}
  Init_FlatScan_range_max range_min(::isaac_ros_pointcloud_interfaces::msg::FlatScan::_range_min_type arg)
  {
    msg_.range_min = std::move(arg);
    return Init_FlatScan_range_max(msg_);
  }

private:
  ::isaac_ros_pointcloud_interfaces::msg::FlatScan msg_;
};

class Init_FlatScan_header
{
public:
  Init_FlatScan_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_FlatScan_range_min header(::isaac_ros_pointcloud_interfaces::msg::FlatScan::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_FlatScan_range_min(msg_);
  }

private:
  ::isaac_ros_pointcloud_interfaces::msg::FlatScan msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::isaac_ros_pointcloud_interfaces::msg::FlatScan>()
{
  return isaac_ros_pointcloud_interfaces::msg::builder::Init_FlatScan_header();
}

}  // namespace isaac_ros_pointcloud_interfaces

#endif  // ISAAC_ROS_POINTCLOUD_INTERFACES__MSG__DETAIL__FLAT_SCAN__BUILDER_HPP_
