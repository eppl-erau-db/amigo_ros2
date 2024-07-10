// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from unitree_api:msg/ResponseHeader.idl
// generated code does not contain a copyright notice

#ifndef UNITREE_API__MSG__DETAIL__RESPONSE_HEADER__TRAITS_HPP_
#define UNITREE_API__MSG__DETAIL__RESPONSE_HEADER__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "unitree_api/msg/detail/response_header__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'identity'
#include "unitree_api/msg/detail/request_identity__traits.hpp"
// Member 'status'
#include "unitree_api/msg/detail/response_status__traits.hpp"

namespace unitree_api
{

namespace msg
{

inline void to_flow_style_yaml(
  const ResponseHeader & msg,
  std::ostream & out)
{
  out << "{";
  // member: identity
  {
    out << "identity: ";
    to_flow_style_yaml(msg.identity, out);
    out << ", ";
  }

  // member: status
  {
    out << "status: ";
    to_flow_style_yaml(msg.status, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ResponseHeader & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: identity
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "identity:\n";
    to_block_style_yaml(msg.identity, out, indentation + 2);
  }

  // member: status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "status:\n";
    to_block_style_yaml(msg.status, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ResponseHeader & msg, bool use_flow_style = false)
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
  const unitree_api::msg::ResponseHeader & msg,
  std::ostream & out, size_t indentation = 0)
{
  unitree_api::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use unitree_api::msg::to_yaml() instead")]]
inline std::string to_yaml(const unitree_api::msg::ResponseHeader & msg)
{
  return unitree_api::msg::to_yaml(msg);
}

template<>
inline const char * data_type<unitree_api::msg::ResponseHeader>()
{
  return "unitree_api::msg::ResponseHeader";
}

template<>
inline const char * name<unitree_api::msg::ResponseHeader>()
{
  return "unitree_api/msg/ResponseHeader";
}

template<>
struct has_fixed_size<unitree_api::msg::ResponseHeader>
  : std::integral_constant<bool, has_fixed_size<unitree_api::msg::RequestIdentity>::value && has_fixed_size<unitree_api::msg::ResponseStatus>::value> {};

template<>
struct has_bounded_size<unitree_api::msg::ResponseHeader>
  : std::integral_constant<bool, has_bounded_size<unitree_api::msg::RequestIdentity>::value && has_bounded_size<unitree_api::msg::ResponseStatus>::value> {};

template<>
struct is_message<unitree_api::msg::ResponseHeader>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // UNITREE_API__MSG__DETAIL__RESPONSE_HEADER__TRAITS_HPP_
