// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from isaac_ros_tensor_list_interfaces:msg/TensorShape.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR_SHAPE__TRAITS_HPP_
#define ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR_SHAPE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "isaac_ros_tensor_list_interfaces/msg/detail/tensor_shape__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace isaac_ros_tensor_list_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const TensorShape & msg,
  std::ostream & out)
{
  out << "{";
  // member: rank
  {
    out << "rank: ";
    rosidl_generator_traits::value_to_yaml(msg.rank, out);
    out << ", ";
  }

  // member: dims
  {
    if (msg.dims.size() == 0) {
      out << "dims: []";
    } else {
      out << "dims: [";
      size_t pending_items = msg.dims.size();
      for (auto item : msg.dims) {
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
  const TensorShape & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: rank
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "rank: ";
    rosidl_generator_traits::value_to_yaml(msg.rank, out);
    out << "\n";
  }

  // member: dims
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.dims.size() == 0) {
      out << "dims: []\n";
    } else {
      out << "dims:\n";
      for (auto item : msg.dims) {
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

inline std::string to_yaml(const TensorShape & msg, bool use_flow_style = false)
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

}  // namespace isaac_ros_tensor_list_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use isaac_ros_tensor_list_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const isaac_ros_tensor_list_interfaces::msg::TensorShape & msg,
  std::ostream & out, size_t indentation = 0)
{
  isaac_ros_tensor_list_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use isaac_ros_tensor_list_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const isaac_ros_tensor_list_interfaces::msg::TensorShape & msg)
{
  return isaac_ros_tensor_list_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<isaac_ros_tensor_list_interfaces::msg::TensorShape>()
{
  return "isaac_ros_tensor_list_interfaces::msg::TensorShape";
}

template<>
inline const char * name<isaac_ros_tensor_list_interfaces::msg::TensorShape>()
{
  return "isaac_ros_tensor_list_interfaces/msg/TensorShape";
}

template<>
struct has_fixed_size<isaac_ros_tensor_list_interfaces::msg::TensorShape>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<isaac_ros_tensor_list_interfaces::msg::TensorShape>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<isaac_ros_tensor_list_interfaces::msg::TensorShape>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR_SHAPE__TRAITS_HPP_
