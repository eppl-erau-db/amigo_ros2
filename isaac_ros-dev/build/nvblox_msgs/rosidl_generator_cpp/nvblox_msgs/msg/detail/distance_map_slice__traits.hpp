// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from nvblox_msgs:msg/DistanceMapSlice.idl
// generated code does not contain a copyright notice

#ifndef NVBLOX_MSGS__MSG__DETAIL__DISTANCE_MAP_SLICE__TRAITS_HPP_
#define NVBLOX_MSGS__MSG__DETAIL__DISTANCE_MAP_SLICE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "nvblox_msgs/msg/detail/distance_map_slice__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'origin'
#include "geometry_msgs/msg/detail/point__traits.hpp"

namespace nvblox_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const DistanceMapSlice & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: resolution
  {
    out << "resolution: ";
    rosidl_generator_traits::value_to_yaml(msg.resolution, out);
    out << ", ";
  }

  // member: width
  {
    out << "width: ";
    rosidl_generator_traits::value_to_yaml(msg.width, out);
    out << ", ";
  }

  // member: height
  {
    out << "height: ";
    rosidl_generator_traits::value_to_yaml(msg.height, out);
    out << ", ";
  }

  // member: origin
  {
    out << "origin: ";
    to_flow_style_yaml(msg.origin, out);
    out << ", ";
  }

  // member: unknown_value
  {
    out << "unknown_value: ";
    rosidl_generator_traits::value_to_yaml(msg.unknown_value, out);
    out << ", ";
  }

  // member: data
  {
    if (msg.data.size() == 0) {
      out << "data: []";
    } else {
      out << "data: [";
      size_t pending_items = msg.data.size();
      for (auto item : msg.data) {
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
  const DistanceMapSlice & msg,
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

  // member: resolution
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "resolution: ";
    rosidl_generator_traits::value_to_yaml(msg.resolution, out);
    out << "\n";
  }

  // member: width
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "width: ";
    rosidl_generator_traits::value_to_yaml(msg.width, out);
    out << "\n";
  }

  // member: height
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "height: ";
    rosidl_generator_traits::value_to_yaml(msg.height, out);
    out << "\n";
  }

  // member: origin
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "origin:\n";
    to_block_style_yaml(msg.origin, out, indentation + 2);
  }

  // member: unknown_value
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "unknown_value: ";
    rosidl_generator_traits::value_to_yaml(msg.unknown_value, out);
    out << "\n";
  }

  // member: data
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.data.size() == 0) {
      out << "data: []\n";
    } else {
      out << "data:\n";
      for (auto item : msg.data) {
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

inline std::string to_yaml(const DistanceMapSlice & msg, bool use_flow_style = false)
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
  const nvblox_msgs::msg::DistanceMapSlice & msg,
  std::ostream & out, size_t indentation = 0)
{
  nvblox_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use nvblox_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const nvblox_msgs::msg::DistanceMapSlice & msg)
{
  return nvblox_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<nvblox_msgs::msg::DistanceMapSlice>()
{
  return "nvblox_msgs::msg::DistanceMapSlice";
}

template<>
inline const char * name<nvblox_msgs::msg::DistanceMapSlice>()
{
  return "nvblox_msgs/msg/DistanceMapSlice";
}

template<>
struct has_fixed_size<nvblox_msgs::msg::DistanceMapSlice>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<nvblox_msgs::msg::DistanceMapSlice>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<nvblox_msgs::msg::DistanceMapSlice>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // NVBLOX_MSGS__MSG__DETAIL__DISTANCE_MAP_SLICE__TRAITS_HPP_
