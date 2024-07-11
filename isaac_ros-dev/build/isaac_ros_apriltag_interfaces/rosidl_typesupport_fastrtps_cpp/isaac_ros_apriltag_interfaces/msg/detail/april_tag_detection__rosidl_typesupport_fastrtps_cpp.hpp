// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from isaac_ros_apriltag_interfaces:msg/AprilTagDetection.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_APRILTAG_INTERFACES__MSG__DETAIL__APRIL_TAG_DETECTION__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define ISAAC_ROS_APRILTAG_INTERFACES__MSG__DETAIL__APRIL_TAG_DETECTION__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "isaac_ros_apriltag_interfaces/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "isaac_ros_apriltag_interfaces/msg/detail/april_tag_detection__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace isaac_ros_apriltag_interfaces
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_isaac_ros_apriltag_interfaces
cdr_serialize(
  const isaac_ros_apriltag_interfaces::msg::AprilTagDetection & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_isaac_ros_apriltag_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  isaac_ros_apriltag_interfaces::msg::AprilTagDetection & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_isaac_ros_apriltag_interfaces
get_serialized_size(
  const isaac_ros_apriltag_interfaces::msg::AprilTagDetection & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_isaac_ros_apriltag_interfaces
max_serialized_size_AprilTagDetection(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace isaac_ros_apriltag_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_isaac_ros_apriltag_interfaces
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, isaac_ros_apriltag_interfaces, msg, AprilTagDetection)();

#ifdef __cplusplus
}
#endif

#endif  // ISAAC_ROS_APRILTAG_INTERFACES__MSG__DETAIL__APRIL_TAG_DETECTION__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
