// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from nvblox_msgs:msg/Mesh.idl
// generated code does not contain a copyright notice

#ifndef NVBLOX_MSGS__MSG__DETAIL__MESH__TRAITS_HPP_
#define NVBLOX_MSGS__MSG__DETAIL__MESH__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "nvblox_msgs/msg/detail/mesh__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'block_indices'
#include "nvblox_msgs/msg/detail/index3_d__traits.hpp"
// Member 'blocks'
#include "nvblox_msgs/msg/detail/mesh_block__traits.hpp"

namespace nvblox_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const Mesh & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: block_size
  {
    out << "block_size: ";
    rosidl_generator_traits::value_to_yaml(msg.block_size, out);
    out << ", ";
  }

  // member: block_indices
  {
    if (msg.block_indices.size() == 0) {
      out << "block_indices: []";
    } else {
      out << "block_indices: [";
      size_t pending_items = msg.block_indices.size();
      for (auto item : msg.block_indices) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: blocks
  {
    if (msg.blocks.size() == 0) {
      out << "blocks: []";
    } else {
      out << "blocks: [";
      size_t pending_items = msg.blocks.size();
      for (auto item : msg.blocks) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: clear
  {
    out << "clear: ";
    rosidl_generator_traits::value_to_yaml(msg.clear, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Mesh & msg,
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

  // member: block_size
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "block_size: ";
    rosidl_generator_traits::value_to_yaml(msg.block_size, out);
    out << "\n";
  }

  // member: block_indices
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.block_indices.size() == 0) {
      out << "block_indices: []\n";
    } else {
      out << "block_indices:\n";
      for (auto item : msg.block_indices) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: blocks
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.blocks.size() == 0) {
      out << "blocks: []\n";
    } else {
      out << "blocks:\n";
      for (auto item : msg.blocks) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: clear
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "clear: ";
    rosidl_generator_traits::value_to_yaml(msg.clear, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Mesh & msg, bool use_flow_style = false)
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
  const nvblox_msgs::msg::Mesh & msg,
  std::ostream & out, size_t indentation = 0)
{
  nvblox_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use nvblox_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const nvblox_msgs::msg::Mesh & msg)
{
  return nvblox_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<nvblox_msgs::msg::Mesh>()
{
  return "nvblox_msgs::msg::Mesh";
}

template<>
inline const char * name<nvblox_msgs::msg::Mesh>()
{
  return "nvblox_msgs/msg/Mesh";
}

template<>
struct has_fixed_size<nvblox_msgs::msg::Mesh>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<nvblox_msgs::msg::Mesh>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<nvblox_msgs::msg::Mesh>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // NVBLOX_MSGS__MSG__DETAIL__MESH__TRAITS_HPP_
