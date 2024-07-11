// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from isaac_ros_apriltag_interfaces:msg/AprilTagDetectionArray.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_APRILTAG_INTERFACES__MSG__DETAIL__APRIL_TAG_DETECTION_ARRAY__BUILDER_HPP_
#define ISAAC_ROS_APRILTAG_INTERFACES__MSG__DETAIL__APRIL_TAG_DETECTION_ARRAY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "isaac_ros_apriltag_interfaces/msg/detail/april_tag_detection_array__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace isaac_ros_apriltag_interfaces
{

namespace msg
{

namespace builder
{

class Init_AprilTagDetectionArray_detections
{
public:
  explicit Init_AprilTagDetectionArray_detections(::isaac_ros_apriltag_interfaces::msg::AprilTagDetectionArray & msg)
  : msg_(msg)
  {}
  ::isaac_ros_apriltag_interfaces::msg::AprilTagDetectionArray detections(::isaac_ros_apriltag_interfaces::msg::AprilTagDetectionArray::_detections_type arg)
  {
    msg_.detections = std::move(arg);
    return std::move(msg_);
  }

private:
  ::isaac_ros_apriltag_interfaces::msg::AprilTagDetectionArray msg_;
};

class Init_AprilTagDetectionArray_header
{
public:
  Init_AprilTagDetectionArray_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_AprilTagDetectionArray_detections header(::isaac_ros_apriltag_interfaces::msg::AprilTagDetectionArray::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_AprilTagDetectionArray_detections(msg_);
  }

private:
  ::isaac_ros_apriltag_interfaces::msg::AprilTagDetectionArray msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::isaac_ros_apriltag_interfaces::msg::AprilTagDetectionArray>()
{
  return isaac_ros_apriltag_interfaces::msg::builder::Init_AprilTagDetectionArray_header();
}

}  // namespace isaac_ros_apriltag_interfaces

#endif  // ISAAC_ROS_APRILTAG_INTERFACES__MSG__DETAIL__APRIL_TAG_DETECTION_ARRAY__BUILDER_HPP_
