// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from nvblox_msgs:msg/MeshBlock.idl
// generated code does not contain a copyright notice

#ifndef NVBLOX_MSGS__MSG__DETAIL__MESH_BLOCK__TRAITS_HPP_
#define NVBLOX_MSGS__MSG__DETAIL__MESH_BLOCK__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "nvblox_msgs/msg/detail/mesh_block__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'vertices'
// Member 'normals'
#include "geometry_msgs/msg/detail/point32__traits.hpp"
// Member 'colors'
#include "std_msgs/msg/detail/color_rgba__traits.hpp"

namespace nvblox_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const MeshBlock & msg,
  std::ostream & out)
{
  out << "{";
  // member: vertices
  {
    if (msg.vertices.size() == 0) {
      out << "vertices: []";
    } else {
      out << "vertices: [";
      size_t pending_items = msg.vertices.size();
      for (auto item : msg.vertices) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: normals
  {
    if (msg.normals.size() == 0) {
      out << "normals: []";
    } else {
      out << "normals: [";
      size_t pending_items = msg.normals.size();
      for (auto item : msg.normals) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: colors
  {
    if (msg.colors.size() == 0) {
      out << "colors: []";
    } else {
      out << "colors: [";
      size_t pending_items = msg.colors.size();
      for (auto item : msg.colors) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: triangles
  {
    if (msg.triangles.size() == 0) {
      out << "triangles: []";
    } else {
      out << "triangles: [";
      size_t pending_items = msg.triangles.size();
      for (auto item : msg.triangles) {
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
  const MeshBlock & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: vertices
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.vertices.size() == 0) {
      out << "vertices: []\n";
    } else {
      out << "vertices:\n";
      for (auto item : msg.vertices) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: normals
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.normals.size() == 0) {
      out << "normals: []\n";
    } else {
      out << "normals:\n";
      for (auto item : msg.normals) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: colors
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.colors.size() == 0) {
      out << "colors: []\n";
    } else {
      out << "colors:\n";
      for (auto item : msg.colors) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: triangles
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.triangles.size() == 0) {
      out << "triangles: []\n";
    } else {
      out << "triangles:\n";
      for (auto item : msg.triangles) {
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

inline std::string to_yaml(const MeshBlock & msg, bool use_flow_style = false)
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
  const nvblox_msgs::msg::MeshBlock & msg,
  std::ostream & out, size_t indentation = 0)
{
  nvblox_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use nvblox_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const nvblox_msgs::msg::MeshBlock & msg)
{
  return nvblox_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<nvblox_msgs::msg::MeshBlock>()
{
  return "nvblox_msgs::msg::MeshBlock";
}

template<>
inline const char * name<nvblox_msgs::msg::MeshBlock>()
{
  return "nvblox_msgs/msg/MeshBlock";
}

template<>
struct has_fixed_size<nvblox_msgs::msg::MeshBlock>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<nvblox_msgs::msg::MeshBlock>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<nvblox_msgs::msg::MeshBlock>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // NVBLOX_MSGS__MSG__DETAIL__MESH_BLOCK__TRAITS_HPP_
