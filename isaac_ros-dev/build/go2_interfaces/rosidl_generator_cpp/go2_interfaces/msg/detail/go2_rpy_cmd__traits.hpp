// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from go2_interfaces:msg/Go2RpyCmd.idl
// generated code does not contain a copyright notice

#ifndef GO2_INTERFACES__MSG__DETAIL__GO2_RPY_CMD__TRAITS_HPP_
#define GO2_INTERFACES__MSG__DETAIL__GO2_RPY_CMD__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "go2_interfaces/msg/detail/go2_rpy_cmd__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace go2_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const Go2RpyCmd & msg,
  std::ostream & out)
{
  out << "{";
  // member: roll
  {
    out << "roll: ";
    rosidl_generator_traits::value_to_yaml(msg.roll, out);
    out << ", ";
  }

  // member: pitch
  {
    out << "pitch: ";
    rosidl_generator_traits::value_to_yaml(msg.pitch, out);
    out << ", ";
  }

  // member: yaw
  {
    out << "yaw: ";
    rosidl_generator_traits::value_to_yaml(msg.yaw, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Go2RpyCmd & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: roll
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "roll: ";
    rosidl_generator_traits::value_to_yaml(msg.roll, out);
    out << "\n";
  }

  // member: pitch
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "pitch: ";
    rosidl_generator_traits::value_to_yaml(msg.pitch, out);
    out << "\n";
  }

  // member: yaw
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "yaw: ";
    rosidl_generator_traits::value_to_yaml(msg.yaw, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Go2RpyCmd & msg, bool use_flow_style = false)
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

}  // namespace go2_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use go2_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const go2_interfaces::msg::Go2RpyCmd & msg,
  std::ostream & out, size_t indentation = 0)
{
  go2_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use go2_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const go2_interfaces::msg::Go2RpyCmd & msg)
{
  return go2_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<go2_interfaces::msg::Go2RpyCmd>()
{
  return "go2_interfaces::msg::Go2RpyCmd";
}

template<>
inline const char * name<go2_interfaces::msg::Go2RpyCmd>()
{
  return "go2_interfaces/msg/Go2RpyCmd";
}

template<>
struct has_fixed_size<go2_interfaces::msg::Go2RpyCmd>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<go2_interfaces::msg::Go2RpyCmd>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<go2_interfaces::msg::Go2RpyCmd>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // GO2_INTERFACES__MSG__DETAIL__GO2_RPY_CMD__TRAITS_HPP_
