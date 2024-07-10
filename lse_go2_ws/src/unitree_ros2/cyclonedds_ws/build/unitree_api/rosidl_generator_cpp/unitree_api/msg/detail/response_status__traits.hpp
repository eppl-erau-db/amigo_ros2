// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from unitree_api:msg/ResponseStatus.idl
// generated code does not contain a copyright notice

#ifndef UNITREE_API__MSG__DETAIL__RESPONSE_STATUS__TRAITS_HPP_
#define UNITREE_API__MSG__DETAIL__RESPONSE_STATUS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "unitree_api/msg/detail/response_status__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace unitree_api
{

namespace msg
{

inline void to_flow_style_yaml(
  const ResponseStatus & msg,
  std::ostream & out)
{
  out << "{";
  // member: code
  {
    out << "code: ";
    rosidl_generator_traits::value_to_yaml(msg.code, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ResponseStatus & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: code
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "code: ";
    rosidl_generator_traits::value_to_yaml(msg.code, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ResponseStatus & msg, bool use_flow_style = false)
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
  const unitree_api::msg::ResponseStatus & msg,
  std::ostream & out, size_t indentation = 0)
{
  unitree_api::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use unitree_api::msg::to_yaml() instead")]]
inline std::string to_yaml(const unitree_api::msg::ResponseStatus & msg)
{
  return unitree_api::msg::to_yaml(msg);
}

template<>
inline const char * data_type<unitree_api::msg::ResponseStatus>()
{
  return "unitree_api::msg::ResponseStatus";
}

template<>
inline const char * name<unitree_api::msg::ResponseStatus>()
{
  return "unitree_api/msg/ResponseStatus";
}

template<>
struct has_fixed_size<unitree_api::msg::ResponseStatus>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<unitree_api::msg::ResponseStatus>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<unitree_api::msg::ResponseStatus>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // UNITREE_API__MSG__DETAIL__RESPONSE_STATUS__TRAITS_HPP_
