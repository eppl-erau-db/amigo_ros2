// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from isaac_ros_nova_interfaces:msg/CorrelatedTimestamp.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_NOVA_INTERFACES__MSG__DETAIL__CORRELATED_TIMESTAMP__TRAITS_HPP_
#define ISAAC_ROS_NOVA_INTERFACES__MSG__DETAIL__CORRELATED_TIMESTAMP__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "isaac_ros_nova_interfaces/msg/detail/correlated_timestamp__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace isaac_ros_nova_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const CorrelatedTimestamp & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: phc_val
  {
    out << "phc_val: ";
    rosidl_generator_traits::value_to_yaml(msg.phc_val, out);
    out << ", ";
  }

  // member: tsc_val
  {
    out << "tsc_val: ";
    rosidl_generator_traits::value_to_yaml(msg.tsc_val, out);
    out << ", ";
  }

  // member: phc2_val
  {
    out << "phc2_val: ";
    rosidl_generator_traits::value_to_yaml(msg.phc2_val, out);
    out << ", ";
  }

  // member: sys_val
  {
    out << "sys_val: ";
    rosidl_generator_traits::value_to_yaml(msg.sys_val, out);
    out << ", ";
  }

  // member: phc_latency
  {
    out << "phc_latency: ";
    rosidl_generator_traits::value_to_yaml(msg.phc_latency, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const CorrelatedTimestamp & msg,
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

  // member: phc_val
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "phc_val: ";
    rosidl_generator_traits::value_to_yaml(msg.phc_val, out);
    out << "\n";
  }

  // member: tsc_val
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "tsc_val: ";
    rosidl_generator_traits::value_to_yaml(msg.tsc_val, out);
    out << "\n";
  }

  // member: phc2_val
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "phc2_val: ";
    rosidl_generator_traits::value_to_yaml(msg.phc2_val, out);
    out << "\n";
  }

  // member: sys_val
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "sys_val: ";
    rosidl_generator_traits::value_to_yaml(msg.sys_val, out);
    out << "\n";
  }

  // member: phc_latency
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "phc_latency: ";
    rosidl_generator_traits::value_to_yaml(msg.phc_latency, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const CorrelatedTimestamp & msg, bool use_flow_style = false)
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
  const isaac_ros_nova_interfaces::msg::CorrelatedTimestamp & msg,
  std::ostream & out, size_t indentation = 0)
{
  isaac_ros_nova_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use isaac_ros_nova_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const isaac_ros_nova_interfaces::msg::CorrelatedTimestamp & msg)
{
  return isaac_ros_nova_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<isaac_ros_nova_interfaces::msg::CorrelatedTimestamp>()
{
  return "isaac_ros_nova_interfaces::msg::CorrelatedTimestamp";
}

template<>
inline const char * name<isaac_ros_nova_interfaces::msg::CorrelatedTimestamp>()
{
  return "isaac_ros_nova_interfaces/msg/CorrelatedTimestamp";
}

template<>
struct has_fixed_size<isaac_ros_nova_interfaces::msg::CorrelatedTimestamp>
  : std::integral_constant<bool, has_fixed_size<std_msgs::msg::Header>::value> {};

template<>
struct has_bounded_size<isaac_ros_nova_interfaces::msg::CorrelatedTimestamp>
  : std::integral_constant<bool, has_bounded_size<std_msgs::msg::Header>::value> {};

template<>
struct is_message<isaac_ros_nova_interfaces::msg::CorrelatedTimestamp>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ISAAC_ROS_NOVA_INTERFACES__MSG__DETAIL__CORRELATED_TIMESTAMP__TRAITS_HPP_
