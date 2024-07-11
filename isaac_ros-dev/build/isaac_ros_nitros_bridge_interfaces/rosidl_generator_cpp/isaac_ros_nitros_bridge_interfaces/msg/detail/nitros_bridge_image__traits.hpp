// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from isaac_ros_nitros_bridge_interfaces:msg/NitrosBridgeImage.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_NITROS_BRIDGE_INTERFACES__MSG__DETAIL__NITROS_BRIDGE_IMAGE__TRAITS_HPP_
#define ISAAC_ROS_NITROS_BRIDGE_INTERFACES__MSG__DETAIL__NITROS_BRIDGE_IMAGE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "isaac_ros_nitros_bridge_interfaces/msg/detail/nitros_bridge_image__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace isaac_ros_nitros_bridge_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const NitrosBridgeImage & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: height
  {
    out << "height: ";
    rosidl_generator_traits::value_to_yaml(msg.height, out);
    out << ", ";
  }

  // member: width
  {
    out << "width: ";
    rosidl_generator_traits::value_to_yaml(msg.width, out);
    out << ", ";
  }

  // member: encoding
  {
    out << "encoding: ";
    rosidl_generator_traits::value_to_yaml(msg.encoding, out);
    out << ", ";
  }

  // member: is_bigendian
  {
    out << "is_bigendian: ";
    rosidl_generator_traits::value_to_yaml(msg.is_bigendian, out);
    out << ", ";
  }

  // member: step
  {
    out << "step: ";
    rosidl_generator_traits::value_to_yaml(msg.step, out);
    out << ", ";
  }

  // member: data
  {
    if (msg.data.size() == 0) {
      out << "data: []";
    } else {
      out << "data: [";
      size_t pending_items = msg.data.size();
      for (auto item : msg.data) {
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
  const NitrosBridgeImage & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: height
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "height: ";
    rosidl_generator_traits::value_to_yaml(msg.height, out);
    out << "\n";
  }

  // member: width
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "width: ";
    rosidl_generator_traits::value_to_yaml(msg.width, out);
    out << "\n";
  }

  // member: encoding
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "encoding: ";
    rosidl_generator_traits::value_to_yaml(msg.encoding, out);
    out << "\n";
  }

  // member: is_bigendian
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "is_bigendian: ";
    rosidl_generator_traits::value_to_yaml(msg.is_bigendian, out);
    out << "\n";
  }

  // member: step
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "step: ";
    rosidl_generator_traits::value_to_yaml(msg.step, out);
    out << "\n";
  }

  // member: data
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.data.size() == 0) {
      out << "data: []\n";
    } else {
      out << "data:\n";
      for (auto item : msg.data) {
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

inline std::string to_yaml(const NitrosBridgeImage & msg, bool use_flow_style = false)
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

}  // namespace isaac_ros_nitros_bridge_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use isaac_ros_nitros_bridge_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage & msg,
  std::ostream & out, size_t indentation = 0)
{
  isaac_ros_nitros_bridge_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use isaac_ros_nitros_bridge_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage & msg)
{
  return isaac_ros_nitros_bridge_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage>()
{
  return "isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage";
}

template<>
inline const char * name<isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage>()
{
  return "isaac_ros_nitros_bridge_interfaces/msg/NitrosBridgeImage";
}

template<>
struct has_fixed_size<isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ISAAC_ROS_NITROS_BRIDGE_INTERFACES__MSG__DETAIL__NITROS_BRIDGE_IMAGE__TRAITS_HPP_
