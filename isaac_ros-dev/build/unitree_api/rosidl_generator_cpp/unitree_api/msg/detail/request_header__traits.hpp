// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from unitree_api:msg/RequestHeader.idl
// generated code does not contain a copyright notice

#ifndef UNITREE_API__MSG__DETAIL__REQUEST_HEADER__TRAITS_HPP_
#define UNITREE_API__MSG__DETAIL__REQUEST_HEADER__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "unitree_api/msg/detail/request_header__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'identity'
#include "unitree_api/msg/detail/request_identity__traits.hpp"
// Member 'lease'
#include "unitree_api/msg/detail/request_lease__traits.hpp"
// Member 'policy'
#include "unitree_api/msg/detail/request_policy__traits.hpp"

namespace unitree_api
{

namespace msg
{

inline void to_flow_style_yaml(
  const RequestHeader & msg,
  std::ostream & out)
{
  out << "{";
  // member: identity
  {
    out << "identity: ";
    to_flow_style_yaml(msg.identity, out);
    out << ", ";
  }

  // member: lease
  {
    out << "lease: ";
    to_flow_style_yaml(msg.lease, out);
    out << ", ";
  }

  // member: policy
  {
    out << "policy: ";
    to_flow_style_yaml(msg.policy, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const RequestHeader & msg,
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

  // member: lease
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "lease:\n";
    to_block_style_yaml(msg.lease, out, indentation + 2);
  }

  // member: policy
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "policy:\n";
    to_block_style_yaml(msg.policy, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const RequestHeader & msg, bool use_flow_style = false)
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
  const unitree_api::msg::RequestHeader & msg,
  std::ostream & out, size_t indentation = 0)
{
  unitree_api::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use unitree_api::msg::to_yaml() instead")]]
inline std::string to_yaml(const unitree_api::msg::RequestHeader & msg)
{
  return unitree_api::msg::to_yaml(msg);
}

template<>
inline const char * data_type<unitree_api::msg::RequestHeader>()
{
  return "unitree_api::msg::RequestHeader";
}

template<>
inline const char * name<unitree_api::msg::RequestHeader>()
{
  return "unitree_api/msg/RequestHeader";
}

template<>
struct has_fixed_size<unitree_api::msg::RequestHeader>
  : std::integral_constant<bool, has_fixed_size<unitree_api::msg::RequestIdentity>::value && has_fixed_size<unitree_api::msg::RequestLease>::value && has_fixed_size<unitree_api::msg::RequestPolicy>::value> {};

template<>
struct has_bounded_size<unitree_api::msg::RequestHeader>
  : std::integral_constant<bool, has_bounded_size<unitree_api::msg::RequestIdentity>::value && has_bounded_size<unitree_api::msg::RequestLease>::value && has_bounded_size<unitree_api::msg::RequestPolicy>::value> {};

template<>
struct is_message<unitree_api::msg::RequestHeader>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // UNITREE_API__MSG__DETAIL__REQUEST_HEADER__TRAITS_HPP_
