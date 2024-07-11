// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from isaac_ros_nova_interfaces:msg/EncoderTicks.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_NOVA_INTERFACES__MSG__DETAIL__ENCODER_TICKS__TRAITS_HPP_
#define ISAAC_ROS_NOVA_INTERFACES__MSG__DETAIL__ENCODER_TICKS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "isaac_ros_nova_interfaces/msg/detail/encoder_ticks__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace isaac_ros_nova_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const EncoderTicks & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: left_ticks
  {
    out << "left_ticks: ";
    rosidl_generator_traits::value_to_yaml(msg.left_ticks, out);
    out << ", ";
  }

  // member: right_ticks
  {
    out << "right_ticks: ";
    rosidl_generator_traits::value_to_yaml(msg.right_ticks, out);
    out << ", ";
  }

  // member: encoder_timestamp
  {
    out << "encoder_timestamp: ";
    rosidl_generator_traits::value_to_yaml(msg.encoder_timestamp, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const EncoderTicks & msg,
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

  // member: left_ticks
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "left_ticks: ";
    rosidl_generator_traits::value_to_yaml(msg.left_ticks, out);
    out << "\n";
  }

  // member: right_ticks
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "right_ticks: ";
    rosidl_generator_traits::value_to_yaml(msg.right_ticks, out);
    out << "\n";
  }

  // member: encoder_timestamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "encoder_timestamp: ";
    rosidl_generator_traits::value_to_yaml(msg.encoder_timestamp, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const EncoderTicks & msg, bool use_flow_style = false)
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

}  // namespace isaac_ros_nova_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use isaac_ros_nova_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const isaac_ros_nova_interfaces::msg::EncoderTicks & msg,
  std::ostream & out, size_t indentation = 0)
{
  isaac_ros_nova_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use isaac_ros_nova_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const isaac_ros_nova_interfaces::msg::EncoderTicks & msg)
{
  return isaac_ros_nova_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<isaac_ros_nova_interfaces::msg::EncoderTicks>()
{
  return "isaac_ros_nova_interfaces::msg::EncoderTicks";
}

template<>
inline const char * name<isaac_ros_nova_interfaces::msg::EncoderTicks>()
{
  return "isaac_ros_nova_interfaces/msg/EncoderTicks";
}

template<>
struct has_fixed_size<isaac_ros_nova_interfaces::msg::EncoderTicks>
  : std::integral_constant<bool, has_fixed_size<std_msgs::msg::Header>::value> {};

template<>
struct has_bounded_size<isaac_ros_nova_interfaces::msg::EncoderTicks>
  : std::integral_constant<bool, has_bounded_size<std_msgs::msg::Header>::value> {};

template<>
struct is_message<isaac_ros_nova_interfaces::msg::EncoderTicks>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ISAAC_ROS_NOVA_INTERFACES__MSG__DETAIL__ENCODER_TICKS__TRAITS_HPP_
