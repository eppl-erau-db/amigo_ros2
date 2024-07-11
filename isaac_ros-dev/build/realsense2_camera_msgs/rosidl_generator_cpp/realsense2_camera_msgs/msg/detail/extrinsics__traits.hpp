// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from realsense2_camera_msgs:msg/Extrinsics.idl
// generated code does not contain a copyright notice

#ifndef REALSENSE2_CAMERA_MSGS__MSG__DETAIL__EXTRINSICS__TRAITS_HPP_
#define REALSENSE2_CAMERA_MSGS__MSG__DETAIL__EXTRINSICS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "realsense2_camera_msgs/msg/detail/extrinsics__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace realsense2_camera_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const Extrinsics & msg,
  std::ostream & out)
{
  out << "{";
  // member: rotation
  {
    if (msg.rotation.size() == 0) {
      out << "rotation: []";
    } else {
      out << "rotation: [";
      size_t pending_items = msg.rotation.size();
      for (auto item : msg.rotation) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: translation
  {
    if (msg.translation.size() == 0) {
      out << "translation: []";
    } else {
      out << "translation: [";
      size_t pending_items = msg.translation.size();
      for (auto item : msg.translation) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Extrinsics & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: rotation
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.rotation.size() == 0) {
      out << "rotation: []\n";
    } else {
      out << "rotation:\n";
      for (auto item : msg.rotation) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: translation
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.translation.size() == 0) {
      out << "translation: []\n";
    } else {
      out << "translation:\n";
      for (auto item : msg.translation) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Extrinsics & msg, bool use_flow_style = false)
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

}  // namespace realsense2_camera_msgs

namespace rosidl_generator_traits
{

[[deprecated("use realsense2_camera_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const realsense2_camera_msgs::msg::Extrinsics & msg,
  std::ostream & out, size_t indentation = 0)
{
  realsense2_camera_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use realsense2_camera_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const realsense2_camera_msgs::msg::Extrinsics & msg)
{
  return realsense2_camera_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<realsense2_camera_msgs::msg::Extrinsics>()
{
  return "realsense2_camera_msgs::msg::Extrinsics";
}

template<>
inline const char * name<realsense2_camera_msgs::msg::Extrinsics>()
{
  return "realsense2_camera_msgs/msg/Extrinsics";
}

template<>
struct has_fixed_size<realsense2_camera_msgs::msg::Extrinsics>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<realsense2_camera_msgs::msg::Extrinsics>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<realsense2_camera_msgs::msg::Extrinsics>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // REALSENSE2_CAMERA_MSGS__MSG__DETAIL__EXTRINSICS__TRAITS_HPP_
