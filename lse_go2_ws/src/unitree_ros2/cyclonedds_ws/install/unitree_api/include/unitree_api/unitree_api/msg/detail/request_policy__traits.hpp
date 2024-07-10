// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from unitree_api:msg/RequestPolicy.idl
// generated code does not contain a copyright notice

#ifndef UNITREE_API__MSG__DETAIL__REQUEST_POLICY__TRAITS_HPP_
#define UNITREE_API__MSG__DETAIL__REQUEST_POLICY__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "unitree_api/msg/detail/request_policy__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace unitree_api
{

namespace msg
{

inline void to_flow_style_yaml(
  const RequestPolicy & msg,
  std::ostream & out)
{
  out << "{";
  // member: priority
  {
    out << "priority: ";
    rosidl_generator_traits::value_to_yaml(msg.priority, out);
    out << ", ";
  }

  // member: noreply
  {
    out << "noreply: ";
    rosidl_generator_traits::value_to_yaml(msg.noreply, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const RequestPolicy & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: priority
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "priority: ";
    rosidl_generator_traits::value_to_yaml(msg.priority, out);
    out << "\n";
  }

  // member: noreply
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "noreply: ";
    rosidl_generator_traits::value_to_yaml(msg.noreply, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const RequestPolicy & msg, bool use_flow_style = false)
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

}  // namespace unitree_api

namespace rosidl_generator_traits
{

[[deprecated("use unitree_api::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const unitree_api::msg::RequestPolicy & msg,
  std::ostream & out, size_t indentation = 0)
{
  unitree_api::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use unitree_api::msg::to_yaml() instead")]]
inline std::string to_yaml(const unitree_api::msg::RequestPolicy & msg)
{
  return unitree_api::msg::to_yaml(msg);
}

template<>
inline const char * data_type<unitree_api::msg::RequestPolicy>()
{
  return "unitree_api::msg::RequestPolicy";
}

template<>
inline const char * name<unitree_api::msg::RequestPolicy>()
{
  return "unitree_api/msg/RequestPolicy";
}

template<>
struct has_fixed_size<unitree_api::msg::RequestPolicy>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<unitree_api::msg::RequestPolicy>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<unitree_api::msg::RequestPolicy>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // UNITREE_API__MSG__DETAIL__REQUEST_POLICY__TRAITS_HPP_
