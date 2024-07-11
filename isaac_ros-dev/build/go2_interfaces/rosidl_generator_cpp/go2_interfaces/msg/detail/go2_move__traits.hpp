// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from go2_interfaces:msg/Go2Move.idl
// generated code does not contain a copyright notice

#ifndef GO2_INTERFACES__MSG__DETAIL__GO2_MOVE__TRAITS_HPP_
#define GO2_INTERFACES__MSG__DETAIL__GO2_MOVE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "go2_interfaces/msg/detail/go2_move__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace go2_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const Go2Move & msg,
  std::ostream & out)
{
  out << "{";
  // member: x
  {
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << ", ";
  }

  // member: y
  {
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
    out << ", ";
  }

  // member: z
  {
    out << "z: ";
    rosidl_generator_traits::value_to_yaml(msg.z, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Go2Move & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << "\n";
  }

  // member: y
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
    out << "\n";
  }

  // member: z
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "z: ";
    rosidl_generator_traits::value_to_yaml(msg.z, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Go2Move & msg, bool use_flow_style = false)
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
  const go2_interfaces::msg::Go2Move & msg,
  std::ostream & out, size_t indentation = 0)
{
  go2_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use go2_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const go2_interfaces::msg::Go2Move & msg)
{
  return go2_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<go2_interfaces::msg::Go2Move>()
{
  return "go2_interfaces::msg::Go2Move";
}

template<>
inline const char * name<go2_interfaces::msg::Go2Move>()
{
  return "go2_interfaces/msg/Go2Move";
}

template<>
struct has_fixed_size<go2_interfaces::msg::Go2Move>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<go2_interfaces::msg::Go2Move>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<go2_interfaces::msg::Go2Move>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // GO2_INTERFACES__MSG__DETAIL__GO2_MOVE__TRAITS_HPP_
