// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from nvblox_msgs:srv/EsdfAndGradients.idl
// generated code does not contain a copyright notice

#ifndef NVBLOX_MSGS__SRV__DETAIL__ESDF_AND_GRADIENTS__TRAITS_HPP_
#define NVBLOX_MSGS__SRV__DETAIL__ESDF_AND_GRADIENTS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "nvblox_msgs/srv/detail/esdf_and_gradients__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'aabb_min_m'
#include "geometry_msgs/msg/detail/point__traits.hpp"
// Member 'aabb_size_m'
#include "geometry_msgs/msg/detail/vector3__traits.hpp"

namespace nvblox_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const EsdfAndGradients_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: aabb_min_m
  {
    out << "aabb_min_m: ";
    to_flow_style_yaml(msg.aabb_min_m, out);
    out << ", ";
  }

  // member: aabb_size_m
  {
    out << "aabb_size_m: ";
    to_flow_style_yaml(msg.aabb_size_m, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const EsdfAndGradients_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: aabb_min_m
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "aabb_min_m:\n";
    to_block_style_yaml(msg.aabb_min_m, out, indentation + 2);
  }

  // member: aabb_size_m
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "aabb_size_m:\n";
    to_block_style_yaml(msg.aabb_size_m, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const EsdfAndGradients_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace nvblox_msgs

namespace rosidl_generator_traits
{

[[deprecated("use nvblox_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const nvblox_msgs::srv::EsdfAndGradients_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  nvblox_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use nvblox_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const nvblox_msgs::srv::EsdfAndGradients_Request & msg)
{
  return nvblox_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<nvblox_msgs::srv::EsdfAndGradients_Request>()
{
  return "nvblox_msgs::srv::EsdfAndGradients_Request";
}

template<>
inline const char * name<nvblox_msgs::srv::EsdfAndGradients_Request>()
{
  return "nvblox_msgs/srv/EsdfAndGradients_Request";
}

template<>
struct has_fixed_size<nvblox_msgs::srv::EsdfAndGradients_Request>
  : std::integral_constant<bool, has_fixed_size<geometry_msgs::msg::Point>::value && has_fixed_size<geometry_msgs::msg::Vector3>::value> {};

template<>
struct has_bounded_size<nvblox_msgs::srv::EsdfAndGradients_Request>
  : std::integral_constant<bool, has_bounded_size<geometry_msgs::msg::Point>::value && has_bounded_size<geometry_msgs::msg::Vector3>::value> {};

template<>
struct is_message<nvblox_msgs::srv::EsdfAndGradients_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'voxel_size'
#include "std_msgs/msg/detail/float32__traits.hpp"
// Member 'esdf_and_gradients'
#include "std_msgs/msg/detail/float32_multi_array__traits.hpp"

namespace nvblox_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const EsdfAndGradients_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: voxel_size
  {
    out << "voxel_size: ";
    to_flow_style_yaml(msg.voxel_size, out);
    out << ", ";
  }

  // member: esdf_and_gradients
  {
    out << "esdf_and_gradients: ";
    to_flow_style_yaml(msg.esdf_and_gradients, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const EsdfAndGradients_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: voxel_size
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "voxel_size:\n";
    to_block_style_yaml(msg.voxel_size, out, indentation + 2);
  }

  // member: esdf_and_gradients
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "esdf_and_gradients:\n";
    to_block_style_yaml(msg.esdf_and_gradients, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const EsdfAndGradients_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace nvblox_msgs

namespace rosidl_generator_traits
{

[[deprecated("use nvblox_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const nvblox_msgs::srv::EsdfAndGradients_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  nvblox_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use nvblox_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const nvblox_msgs::srv::EsdfAndGradients_Response & msg)
{
  return nvblox_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<nvblox_msgs::srv::EsdfAndGradients_Response>()
{
  return "nvblox_msgs::srv::EsdfAndGradients_Response";
}

template<>
inline const char * name<nvblox_msgs::srv::EsdfAndGradients_Response>()
{
  return "nvblox_msgs/srv/EsdfAndGradients_Response";
}

template<>
struct has_fixed_size<nvblox_msgs::srv::EsdfAndGradients_Response>
  : std::integral_constant<bool, has_fixed_size<std_msgs::msg::Float32>::value && has_fixed_size<std_msgs::msg::Float32MultiArray>::value> {};

template<>
struct has_bounded_size<nvblox_msgs::srv::EsdfAndGradients_Response>
  : std::integral_constant<bool, has_bounded_size<std_msgs::msg::Float32>::value && has_bounded_size<std_msgs::msg::Float32MultiArray>::value> {};

template<>
struct is_message<nvblox_msgs::srv::EsdfAndGradients_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<nvblox_msgs::srv::EsdfAndGradients>()
{
  return "nvblox_msgs::srv::EsdfAndGradients";
}

template<>
inline const char * name<nvblox_msgs::srv::EsdfAndGradients>()
{
  return "nvblox_msgs/srv/EsdfAndGradients";
}

template<>
struct has_fixed_size<nvblox_msgs::srv::EsdfAndGradients>
  : std::integral_constant<
    bool,
    has_fixed_size<nvblox_msgs::srv::EsdfAndGradients_Request>::value &&
    has_fixed_size<nvblox_msgs::srv::EsdfAndGradients_Response>::value
  >
{
};

template<>
struct has_bounded_size<nvblox_msgs::srv::EsdfAndGradients>
  : std::integral_constant<
    bool,
    has_bounded_size<nvblox_msgs::srv::EsdfAndGradients_Request>::value &&
    has_bounded_size<nvblox_msgs::srv::EsdfAndGradients_Response>::value
  >
{
};

template<>
struct is_service<nvblox_msgs::srv::EsdfAndGradients>
  : std::true_type
{
};

template<>
struct is_service_request<nvblox_msgs::srv::EsdfAndGradients_Request>
  : std::true_type
{
};

template<>
struct is_service_response<nvblox_msgs::srv::EsdfAndGradients_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // NVBLOX_MSGS__SRV__DETAIL__ESDF_AND_GRADIENTS__TRAITS_HPP_
