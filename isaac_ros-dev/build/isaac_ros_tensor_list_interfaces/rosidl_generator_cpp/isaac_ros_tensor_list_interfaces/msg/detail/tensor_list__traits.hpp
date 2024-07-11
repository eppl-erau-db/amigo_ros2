// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from isaac_ros_tensor_list_interfaces:msg/TensorList.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR_LIST__TRAITS_HPP_
#define ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR_LIST__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "isaac_ros_tensor_list_interfaces/msg/detail/tensor_list__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'tensors'
#include "isaac_ros_tensor_list_interfaces/msg/detail/tensor__traits.hpp"

namespace isaac_ros_tensor_list_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const TensorList & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: tensors
  {
    if (msg.tensors.size() == 0) {
      out << "tensors: []";
    } else {
      out << "tensors: [";
      size_t pending_items = msg.tensors.size();
      for (auto item : msg.tensors) {
        to_flow_style_yaml(item, out);
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
  const TensorList & msg,
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

  // member: tensors
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.tensors.size() == 0) {
      out << "tensors: []\n";
    } else {
      out << "tensors:\n";
      for (auto item : msg.tensors) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const TensorList & msg, bool use_flow_style = false)
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
  const isaac_ros_tensor_list_interfaces::msg::TensorList & msg,
  std::ostream & out, size_t indentation = 0)
{
  isaac_ros_tensor_list_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use isaac_ros_tensor_list_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const isaac_ros_tensor_list_interfaces::msg::TensorList & msg)
{
  return isaac_ros_tensor_list_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<isaac_ros_tensor_list_interfaces::msg::TensorList>()
{
  return "isaac_ros_tensor_list_interfaces::msg::TensorList";
}

template<>
inline const char * name<isaac_ros_tensor_list_interfaces::msg::TensorList>()
{
  return "isaac_ros_tensor_list_interfaces/msg/TensorList";
}

template<>
struct has_fixed_size<isaac_ros_tensor_list_interfaces::msg::TensorList>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<isaac_ros_tensor_list_interfaces::msg::TensorList>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<isaac_ros_tensor_list_interfaces::msg::TensorList>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR_LIST__TRAITS_HPP_
