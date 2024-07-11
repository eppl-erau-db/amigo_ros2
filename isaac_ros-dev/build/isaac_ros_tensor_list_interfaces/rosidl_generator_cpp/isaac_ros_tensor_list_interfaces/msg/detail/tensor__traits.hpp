// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from isaac_ros_tensor_list_interfaces:msg/Tensor.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR__TRAITS_HPP_
#define ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "isaac_ros_tensor_list_interfaces/msg/detail/tensor__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'shape'
#include "isaac_ros_tensor_list_interfaces/msg/detail/tensor_shape__traits.hpp"

namespace isaac_ros_tensor_list_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const Tensor & msg,
  std::ostream & out)
{
  out << "{";
  // member: name
  {
    out << "name: ";
    rosidl_generator_traits::value_to_yaml(msg.name, out);
    out << ", ";
  }

  // member: shape
  {
    out << "shape: ";
    to_flow_style_yaml(msg.shape, out);
    out << ", ";
  }

  // member: data_type
  {
    out << "data_type: ";
    rosidl_generator_traits::value_to_yaml(msg.data_type, out);
    out << ", ";
  }

  // member: strides
  {
    if (msg.strides.size() == 0) {
      out << "strides: []";
    } else {
      out << "strides: [";
      size_t pending_items = msg.strides.size();
      for (auto item : msg.strides) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
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
  const Tensor & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "name: ";
    rosidl_generator_traits::value_to_yaml(msg.name, out);
    out << "\n";
  }

  // member: shape
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "shape:\n";
    to_block_style_yaml(msg.shape, out, indentation + 2);
  }

  // member: data_type
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "data_type: ";
    rosidl_generator_traits::value_to_yaml(msg.data_type, out);
    out << "\n";
  }

  // member: strides
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.strides.size() == 0) {
      out << "strides: []\n";
    } else {
      out << "strides:\n";
      for (auto item : msg.strides) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
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

inline std::string to_yaml(const Tensor & msg, bool use_flow_style = false)
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
  const isaac_ros_tensor_list_interfaces::msg::Tensor & msg,
  std::ostream & out, size_t indentation = 0)
{
  isaac_ros_tensor_list_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use isaac_ros_tensor_list_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const isaac_ros_tensor_list_interfaces::msg::Tensor & msg)
{
  return isaac_ros_tensor_list_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<isaac_ros_tensor_list_interfaces::msg::Tensor>()
{
  return "isaac_ros_tensor_list_interfaces::msg::Tensor";
}

template<>
inline const char * name<isaac_ros_tensor_list_interfaces::msg::Tensor>()
{
  return "isaac_ros_tensor_list_interfaces/msg/Tensor";
}

template<>
struct has_fixed_size<isaac_ros_tensor_list_interfaces::msg::Tensor>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<isaac_ros_tensor_list_interfaces::msg::Tensor>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<isaac_ros_tensor_list_interfaces::msg::Tensor>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR__TRAITS_HPP_
