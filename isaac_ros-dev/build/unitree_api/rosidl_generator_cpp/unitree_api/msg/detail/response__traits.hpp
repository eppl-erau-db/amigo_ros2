// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from unitree_api:msg/Response.idl
// generated code does not contain a copyright notice

#ifndef UNITREE_API__MSG__DETAIL__RESPONSE__TRAITS_HPP_
#define UNITREE_API__MSG__DETAIL__RESPONSE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "unitree_api/msg/detail/response__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "unitree_api/msg/detail/response_header__traits.hpp"

namespace unitree_api
{

namespace msg
{

inline void to_flow_style_yaml(
  const Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: data
  {
    out << "data: ";
    rosidl_generator_traits::value_to_yaml(msg.data, out);
    out << ", ";
  }

  // member: binary
  {
    if (msg.binary.size() == 0) {
      out << "binary: []";
    } else {
      out << "binary: [";
      size_t pending_items = msg.binary.size();
      for (auto item : msg.binary) {
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
  const Response & msg,
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

  // member: data
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "data: ";
    rosidl_generator_traits::value_to_yaml(msg.data, out);
    out << "\n";
  }

  // member: binary
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.binary.size() == 0) {
      out << "binary: []\n";
    } else {
      out << "binary:\n";
      for (auto item : msg.binary) {
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

inline std::string to_yaml(const Response & msg, bool use_flow_style = false)
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
  const unitree_api::msg::Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  unitree_api::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use unitree_api::msg::to_yaml() instead")]]
inline std::string to_yaml(const unitree_api::msg::Response & msg)
{
  return unitree_api::msg::to_yaml(msg);
}

template<>
inline const char * data_type<unitree_api::msg::Response>()
{
  return "unitree_api::msg::Response";
}

template<>
inline const char * name<unitree_api::msg::Response>()
{
  return "unitree_api/msg/Response";
}

template<>
struct has_fixed_size<unitree_api::msg::Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<unitree_api::msg::Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<unitree_api::msg::Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // UNITREE_API__MSG__DETAIL__RESPONSE__TRAITS_HPP_
