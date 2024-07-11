// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from isaac_ros_apriltag_interfaces:msg/AprilTagDetection.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_APRILTAG_INTERFACES__MSG__DETAIL__APRIL_TAG_DETECTION__TRAITS_HPP_
#define ISAAC_ROS_APRILTAG_INTERFACES__MSG__DETAIL__APRIL_TAG_DETECTION__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "isaac_ros_apriltag_interfaces/msg/detail/april_tag_detection__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'center'
// Member 'corners'
#include "geometry_msgs/msg/detail/point__traits.hpp"
// Member 'pose'
#include "geometry_msgs/msg/detail/pose_with_covariance_stamped__traits.hpp"

namespace isaac_ros_apriltag_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const AprilTagDetection & msg,
  std::ostream & out)
{
  out << "{";
  // member: family
  {
    out << "family: ";
    rosidl_generator_traits::value_to_yaml(msg.family, out);
    out << ", ";
  }

  // member: id
  {
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
    out << ", ";
  }

  // member: center
  {
    out << "center: ";
    to_flow_style_yaml(msg.center, out);
    out << ", ";
  }

  // member: corners
  {
    if (msg.corners.size() == 0) {
      out << "corners: []";
    } else {
      out << "corners: [";
      size_t pending_items = msg.corners.size();
      for (auto item : msg.corners) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: pose
  {
    out << "pose: ";
    to_flow_style_yaml(msg.pose, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const AprilTagDetection & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: family
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "family: ";
    rosidl_generator_traits::value_to_yaml(msg.family, out);
    out << "\n";
  }

  // member: id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
    out << "\n";
  }

  // member: center
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "center:\n";
    to_block_style_yaml(msg.center, out, indentation + 2);
  }

  // member: corners
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.corners.size() == 0) {
      out << "corners: []\n";
    } else {
      out << "corners:\n";
      for (auto item : msg.corners) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "pose:\n";
    to_block_style_yaml(msg.pose, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const AprilTagDetection & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace isaac_ros_apriltag_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use isaac_ros_apriltag_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const isaac_ros_apriltag_interfaces::msg::AprilTagDetection & msg,
  std::ostream & out, size_t indentation = 0)
{
  isaac_ros_apriltag_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use isaac_ros_apriltag_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const isaac_ros_apriltag_interfaces::msg::AprilTagDetection & msg)
{
  return isaac_ros_apriltag_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<isaac_ros_apriltag_interfaces::msg::AprilTagDetection>()
{
  return "isaac_ros_apriltag_interfaces::msg::AprilTagDetection";
}

template<>
inline const char * name<isaac_ros_apriltag_interfaces::msg::AprilTagDetection>()
{
  return "isaac_ros_apriltag_interfaces/msg/AprilTagDetection";
}

template<>
struct has_fixed_size<isaac_ros_apriltag_interfaces::msg::AprilTagDetection>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<isaac_ros_apriltag_interfaces::msg::AprilTagDetection>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<isaac_ros_apriltag_interfaces::msg::AprilTagDetection>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ISAAC_ROS_APRILTAG_INTERFACES__MSG__DETAIL__APRIL_TAG_DETECTION__TRAITS_HPP_
