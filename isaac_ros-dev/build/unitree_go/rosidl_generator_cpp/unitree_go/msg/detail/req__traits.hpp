// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from unitree_go:msg/Req.idl
// generated code does not contain a copyright notice

#ifndef UNITREE_GO__MSG__DETAIL__REQ__TRAITS_HPP_
#define UNITREE_GO__MSG__DETAIL__REQ__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "unitree_go/msg/detail/req__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace unitree_go
{

namespace msg
{

inline void to_flow_style_yaml(
  const Req & msg,
  std::ostream & out)
{
  out << "{";
  // member: uuid
  {
    out << "uuid: ";
    rosidl_generator_traits::value_to_yaml(msg.uuid, out);
    out << ", ";
  }

  // member: body
  {
    out << "body: ";
    rosidl_generator_traits::value_to_yaml(msg.body, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Req & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: uuid
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "uuid: ";
    rosidl_generator_traits::value_to_yaml(msg.uuid, out);
    out << "\n";
  }

  // member: body
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "body: ";
    rosidl_generator_traits::value_to_yaml(msg.body, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Req & msg, bool use_flow_style = false)
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
  const unitree_go::msg::Req & msg,
  std::ostream & out, size_t indentation = 0)
{
  unitree_go::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use unitree_go::msg::to_yaml() instead")]]
inline std::string to_yaml(const unitree_go::msg::Req & msg)
{
  return unitree_go::msg::to_yaml(msg);
}

template<>
inline const char * data_type<unitree_go::msg::Req>()
{
  return "unitree_go::msg::Req";
}

template<>
inline const char * name<unitree_go::msg::Req>()
{
  return "unitree_go/msg/Req";
}

template<>
struct has_fixed_size<unitree_go::msg::Req>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<unitree_go::msg::Req>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<unitree_go::msg::Req>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // UNITREE_GO__MSG__DETAIL__REQ__TRAITS_HPP_
