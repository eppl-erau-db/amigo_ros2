// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from isaac_ros_apriltag_interfaces:msg/AprilTagDetection.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_APRILTAG_INTERFACES__MSG__DETAIL__APRIL_TAG_DETECTION__BUILDER_HPP_
#define ISAAC_ROS_APRILTAG_INTERFACES__MSG__DETAIL__APRIL_TAG_DETECTION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "isaac_ros_apriltag_interfaces/msg/detail/april_tag_detection__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace isaac_ros_apriltag_interfaces
{

namespace msg
{

namespace builder
{

class Init_AprilTagDetection_pose
{
public:
  explicit Init_AprilTagDetection_pose(::isaac_ros_apriltag_interfaces::msg::AprilTagDetection & msg)
  : msg_(msg)
  {}
  ::isaac_ros_apriltag_interfaces::msg::AprilTagDetection pose(::isaac_ros_apriltag_interfaces::msg::AprilTagDetection::_pose_type arg)
  {
    msg_.pose = std::move(arg);
    return std::move(msg_);
  }

private:
  ::isaac_ros_apriltag_interfaces::msg::AprilTagDetection msg_;
};

class Init_AprilTagDetection_corners
{
public:
  explicit Init_AprilTagDetection_corners(::isaac_ros_apriltag_interfaces::msg::AprilTagDetection & msg)
  : msg_(msg)
  {}
  Init_AprilTagDetection_pose corners(::isaac_ros_apriltag_interfaces::msg::AprilTagDetection::_corners_type arg)
  {
    msg_.corners = std::move(arg);
    return Init_AprilTagDetection_pose(msg_);
  }

private:
  ::isaac_ros_apriltag_interfaces::msg::AprilTagDetection msg_;
};

class Init_AprilTagDetection_center
{
public:
  explicit Init_AprilTagDetection_center(::isaac_ros_apriltag_interfaces::msg::AprilTagDetection & msg)
  : msg_(msg)
  {}
  Init_AprilTagDetection_corners center(::isaac_ros_apriltag_interfaces::msg::AprilTagDetection::_center_type arg)
  {
    msg_.center = std::move(arg);
    return Init_AprilTagDetection_corners(msg_);
  }

private:
  ::isaac_ros_apriltag_interfaces::msg::AprilTagDetection msg_;
};

class Init_AprilTagDetection_id
{
public:
  explicit Init_AprilTagDetection_id(::isaac_ros_apriltag_interfaces::msg::AprilTagDetection & msg)
  : msg_(msg)
  {}
  Init_AprilTagDetection_center id(::isaac_ros_apriltag_interfaces::msg::AprilTagDetection::_id_type arg)
  {
    msg_.id = std::move(arg);
    return Init_AprilTagDetection_center(msg_);
  }

private:
  ::isaac_ros_apriltag_interfaces::msg::AprilTagDetection msg_;
};

class Init_AprilTagDetection_family
{
public:
  Init_AprilTagDetection_family()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_AprilTagDetection_id family(::isaac_ros_apriltag_interfaces::msg::AprilTagDetection::_family_type arg)
  {
    msg_.family = std::move(arg);
    return Init_AprilTagDetection_id(msg_);
  }

private:
  ::isaac_ros_apriltag_interfaces::msg::AprilTagDetection msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::isaac_ros_apriltag_interfaces::msg::AprilTagDetection>()
{
  return isaac_ros_apriltag_interfaces::msg::builder::Init_AprilTagDetection_family();
}

}  // namespace isaac_ros_apriltag_interfaces

#endif  // ISAAC_ROS_APRILTAG_INTERFACES__MSG__DETAIL__APRIL_TAG_DETECTION__BUILDER_HPP_
