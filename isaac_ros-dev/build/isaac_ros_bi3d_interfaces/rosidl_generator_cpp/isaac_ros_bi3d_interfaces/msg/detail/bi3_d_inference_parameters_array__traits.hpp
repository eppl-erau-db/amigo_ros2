// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from isaac_ros_bi3d_interfaces:msg/Bi3DInferenceParametersArray.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_BI3D_INTERFACES__MSG__DETAIL__BI3_D_INFERENCE_PARAMETERS_ARRAY__TRAITS_HPP_
#define ISAAC_ROS_BI3D_INTERFACES__MSG__DETAIL__BI3_D_INFERENCE_PARAMETERS_ARRAY__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "isaac_ros_bi3d_interfaces/msg/detail/bi3_d_inference_parameters_array__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace isaac_ros_bi3d_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const Bi3DInferenceParametersArray & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: disparity_values
  {
    if (msg.disparity_values.size() == 0) {
      out << "disparity_values: []";
    } else {
      out << "disparity_values: [";
      size_t pending_items = msg.disparity_values.size();
      for (auto item : msg.disparity_values) {
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
  const Bi3DInferenceParametersArray & msg,
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

  // member: disparity_values
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.disparity_values.size() == 0) {
      out << "disparity_values: []\n";
    } else {
      out << "disparity_values:\n";
      for (auto item : msg.disparity_values) {
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

inline std::string to_yaml(const Bi3DInferenceParametersArray & msg, bool use_flow_style = false)
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

}  // namespace isaac_ros_bi3d_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use isaac_ros_bi3d_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const isaac_ros_bi3d_interfaces::msg::Bi3DInferenceParametersArray & msg,
  std::ostream & out, size_t indentation = 0)
{
  isaac_ros_bi3d_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use isaac_ros_bi3d_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const isaac_ros_bi3d_interfaces::msg::Bi3DInferenceParametersArray & msg)
{
  return isaac_ros_bi3d_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<isaac_ros_bi3d_interfaces::msg::Bi3DInferenceParametersArray>()
{
  return "isaac_ros_bi3d_interfaces::msg::Bi3DInferenceParametersArray";
}

template<>
inline const char * name<isaac_ros_bi3d_interfaces::msg::Bi3DInferenceParametersArray>()
{
  return "isaac_ros_bi3d_interfaces/msg/Bi3DInferenceParametersArray";
}

template<>
struct has_fixed_size<isaac_ros_bi3d_interfaces::msg::Bi3DInferenceParametersArray>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<isaac_ros_bi3d_interfaces::msg::Bi3DInferenceParametersArray>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<isaac_ros_bi3d_interfaces::msg::Bi3DInferenceParametersArray>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ISAAC_ROS_BI3D_INTERFACES__MSG__DETAIL__BI3_D_INFERENCE_PARAMETERS_ARRAY__TRAITS_HPP_
