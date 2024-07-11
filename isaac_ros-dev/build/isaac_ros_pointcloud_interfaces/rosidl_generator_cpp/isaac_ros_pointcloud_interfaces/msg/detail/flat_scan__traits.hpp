// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from isaac_ros_pointcloud_interfaces:msg/FlatScan.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_POINTCLOUD_INTERFACES__MSG__DETAIL__FLAT_SCAN__TRAITS_HPP_
#define ISAAC_ROS_POINTCLOUD_INTERFACES__MSG__DETAIL__FLAT_SCAN__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "isaac_ros_pointcloud_interfaces/msg/detail/flat_scan__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace isaac_ros_pointcloud_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const FlatScan & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: range_min
  {
    out << "range_min: ";
    rosidl_generator_traits::value_to_yaml(msg.range_min, out);
    out << ", ";
  }

  // member: range_max
  {
    out << "range_max: ";
    rosidl_generator_traits::value_to_yaml(msg.range_max, out);
    out << ", ";
  }

  // member: angles
  {
    if (msg.angles.size() == 0) {
      out << "angles: []";
    } else {
      out << "angles: [";
      size_t pending_items = msg.angles.size();
      for (auto item : msg.angles) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: ranges
  {
    if (msg.ranges.size() == 0) {
      out << "ranges: []";
    } else {
      out << "ranges: [";
      size_t pending_items = msg.ranges.size();
      for (auto item : msg.ranges) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: intensities
  {
    if (msg.intensities.size() == 0) {
      out << "intensities: []";
    } else {
      out << "intensities: [";
      size_t pending_items = msg.intensities.size();
      for (auto item : msg.intensities) {
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
  const FlatScan & msg,
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

  // member: range_min
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "range_min: ";
    rosidl_generator_traits::value_to_yaml(msg.range_min, out);
    out << "\n";
  }

  // member: range_max
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "range_max: ";
    rosidl_generator_traits::value_to_yaml(msg.range_max, out);
    out << "\n";
  }

  // member: angles
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.angles.size() == 0) {
      out << "angles: []\n";
    } else {
      out << "angles:\n";
      for (auto item : msg.angles) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: ranges
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.ranges.size() == 0) {
      out << "ranges: []\n";
    } else {
      out << "ranges:\n";
      for (auto item : msg.ranges) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: intensities
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.intensities.size() == 0) {
      out << "intensities: []\n";
    } else {
      out << "intensities:\n";
      for (auto item : msg.intensities) {
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

inline std::string to_yaml(const FlatScan & msg, bool use_flow_style = false)
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

}  // namespace isaac_ros_pointcloud_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use isaac_ros_pointcloud_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const isaac_ros_pointcloud_interfaces::msg::FlatScan & msg,
  std::ostream & out, size_t indentation = 0)
{
  isaac_ros_pointcloud_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use isaac_ros_pointcloud_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const isaac_ros_pointcloud_interfaces::msg::FlatScan & msg)
{
  return isaac_ros_pointcloud_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<isaac_ros_pointcloud_interfaces::msg::FlatScan>()
{
  return "isaac_ros_pointcloud_interfaces::msg::FlatScan";
}

template<>
inline const char * name<isaac_ros_pointcloud_interfaces::msg::FlatScan>()
{
  return "isaac_ros_pointcloud_interfaces/msg/FlatScan";
}

template<>
struct has_fixed_size<isaac_ros_pointcloud_interfaces::msg::FlatScan>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<isaac_ros_pointcloud_interfaces::msg::FlatScan>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<isaac_ros_pointcloud_interfaces::msg::FlatScan>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ISAAC_ROS_POINTCLOUD_INTERFACES__MSG__DETAIL__FLAT_SCAN__TRAITS_HPP_
