// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from unitree_go:msg/PathPoint.idl
// generated code does not contain a copyright notice

#ifndef UNITREE_GO__MSG__DETAIL__PATH_POINT__TRAITS_HPP_
#define UNITREE_GO__MSG__DETAIL__PATH_POINT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "unitree_go/msg/detail/path_point__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace unitree_go
{

namespace msg
{

inline void to_flow_style_yaml(
  const PathPoint & msg,
  std::ostream & out)
{
  out << "{";
  // member: t_from_start
  {
    out << "t_from_start: ";
    rosidl_generator_traits::value_to_yaml(msg.t_from_start, out);
    out << ", ";
  }

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

  // member: yaw
  {
    out << "yaw: ";
    rosidl_generator_traits::value_to_yaml(msg.yaw, out);
    out << ", ";
  }

  // member: vx
  {
    out << "vx: ";
    rosidl_generator_traits::value_to_yaml(msg.vx, out);
    out << ", ";
  }

  // member: vy
  {
    out << "vy: ";
    rosidl_generator_traits::value_to_yaml(msg.vy, out);
    out << ", ";
  }

  // member: vyaw
  {
    out << "vyaw: ";
    rosidl_generator_traits::value_to_yaml(msg.vyaw, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const PathPoint & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: t_from_start
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "t_from_start: ";
    rosidl_generator_traits::value_to_yaml(msg.t_from_start, out);
    out << "\n";
  }

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

  // member: yaw
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "yaw: ";
    rosidl_generator_traits::value_to_yaml(msg.yaw, out);
    out << "\n";
  }

  // member: vx
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "vx: ";
    rosidl_generator_traits::value_to_yaml(msg.vx, out);
    out << "\n";
  }

  // member: vy
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "vy: ";
    rosidl_generator_traits::value_to_yaml(msg.vy, out);
    out << "\n";
  }

  // member: vyaw
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "vyaw: ";
    rosidl_generator_traits::value_to_yaml(msg.vyaw, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const PathPoint & msg, bool use_flow_style = false)
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

}  // namespace unitree_go

namespace rosidl_generator_traits
{

[[deprecated("use unitree_go::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const unitree_go::msg::PathPoint & msg,
  std::ostream & out, size_t indentation = 0)
{
  unitree_go::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use unitree_go::msg::to_yaml() instead")]]
inline std::string to_yaml(const unitree_go::msg::PathPoint & msg)
{
  return unitree_go::msg::to_yaml(msg);
}

template<>
inline const char * data_type<unitree_go::msg::PathPoint>()
{
  return "unitree_go::msg::PathPoint";
}

template<>
inline const char * name<unitree_go::msg::PathPoint>()
{
  return "unitree_go/msg/PathPoint";
}

template<>
struct has_fixed_size<unitree_go::msg::PathPoint>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<unitree_go::msg::PathPoint>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<unitree_go::msg::PathPoint>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // UNITREE_GO__MSG__DETAIL__PATH_POINT__TRAITS_HPP_
