// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from nvblox_msgs:msg/SemanticLabelsStamped.idl
// generated code does not contain a copyright notice

#ifndef NVBLOX_MSGS__MSG__DETAIL__SEMANTIC_LABELS_STAMPED__TRAITS_HPP_
#define NVBLOX_MSGS__MSG__DETAIL__SEMANTIC_LABELS_STAMPED__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "nvblox_msgs/msg/detail/semantic_labels_stamped__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace nvblox_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const SemanticLabelsStamped & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: labels
  {
    out << "labels: ";
    rosidl_generator_traits::value_to_yaml(msg.labels, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SemanticLabelsStamped & msg,
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

  // member: labels
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "labels: ";
    rosidl_generator_traits::value_to_yaml(msg.labels, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SemanticLabelsStamped & msg, bool use_flow_style = false)
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

}  // namespace nvblox_msgs

namespace rosidl_generator_traits
{

[[deprecated("use nvblox_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const nvblox_msgs::msg::SemanticLabelsStamped & msg,
  std::ostream & out, size_t indentation = 0)
{
  nvblox_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use nvblox_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const nvblox_msgs::msg::SemanticLabelsStamped & msg)
{
  return nvblox_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<nvblox_msgs::msg::SemanticLabelsStamped>()
{
  return "nvblox_msgs::msg::SemanticLabelsStamped";
}

template<>
inline const char * name<nvblox_msgs::msg::SemanticLabelsStamped>()
{
  return "nvblox_msgs/msg/SemanticLabelsStamped";
}

template<>
struct has_fixed_size<nvblox_msgs::msg::SemanticLabelsStamped>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<nvblox_msgs::msg::SemanticLabelsStamped>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<nvblox_msgs::msg::SemanticLabelsStamped>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // NVBLOX_MSGS__MSG__DETAIL__SEMANTIC_LABELS_STAMPED__TRAITS_HPP_
