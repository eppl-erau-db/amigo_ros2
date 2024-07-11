// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from unitree_go:msg/InterfaceConfig.idl
// generated code does not contain a copyright notice

#ifndef UNITREE_GO__MSG__DETAIL__INTERFACE_CONFIG__TRAITS_HPP_
#define UNITREE_GO__MSG__DETAIL__INTERFACE_CONFIG__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "unitree_go/msg/detail/interface_config__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace unitree_go
{

namespace msg
{

inline void to_flow_style_yaml(
  const InterfaceConfig & msg,
  std::ostream & out)
{
  out << "{";
  // member: mode
  {
    out << "mode: ";
    rosidl_generator_traits::value_to_yaml(msg.mode, out);
    out << ", ";
  }

  // member: value
  {
    out << "value: ";
    rosidl_generator_traits::value_to_yaml(msg.value, out);
    out << ", ";
  }

  // member: reserve
  {
    if (msg.reserve.size() == 0) {
      out << "reserve: []";
    } else {
      out << "reserve: [";
      size_t pending_items = msg.reserve.size();
      for (auto item : msg.reserve) {
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
  const InterfaceConfig & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: mode
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "mode: ";
    rosidl_generator_traits::value_to_yaml(msg.mode, out);
    out << "\n";
  }

  // member: value
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "value: ";
    rosidl_generator_traits::value_to_yaml(msg.value, out);
    out << "\n";
  }

  // member: reserve
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.reserve.size() == 0) {
      out << "reserve: []\n";
    } else {
      out << "reserve:\n";
      for (auto item : msg.reserve) {
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

inline std::string to_yaml(const InterfaceConfig & msg, bool use_flow_style = false)
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
  const unitree_go::msg::InterfaceConfig & msg,
  std::ostream & out, size_t indentation = 0)
{
  unitree_go::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use unitree_go::msg::to_yaml() instead")]]
inline std::string to_yaml(const unitree_go::msg::InterfaceConfig & msg)
{
  return unitree_go::msg::to_yaml(msg);
}

template<>
inline const char * data_type<unitree_go::msg::InterfaceConfig>()
{
  return "unitree_go::msg::InterfaceConfig";
}

template<>
inline const char * name<unitree_go::msg::InterfaceConfig>()
{
  return "unitree_go/msg/InterfaceConfig";
}

template<>
struct has_fixed_size<unitree_go::msg::InterfaceConfig>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<unitree_go::msg::InterfaceConfig>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<unitree_go::msg::InterfaceConfig>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // UNITREE_GO__MSG__DETAIL__INTERFACE_CONFIG__TRAITS_HPP_
