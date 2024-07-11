// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from isaac_ros_bi3d_interfaces:msg/Bi3DInferenceParametersArray.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_BI3D_INTERFACES__MSG__DETAIL__BI3_D_INFERENCE_PARAMETERS_ARRAY__BUILDER_HPP_
#define ISAAC_ROS_BI3D_INTERFACES__MSG__DETAIL__BI3_D_INFERENCE_PARAMETERS_ARRAY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "isaac_ros_bi3d_interfaces/msg/detail/bi3_d_inference_parameters_array__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace isaac_ros_bi3d_interfaces
{

namespace msg
{

namespace builder
{

class Init_Bi3DInferenceParametersArray_disparity_values
{
public:
  explicit Init_Bi3DInferenceParametersArray_disparity_values(::isaac_ros_bi3d_interfaces::msg::Bi3DInferenceParametersArray & msg)
  : msg_(msg)
  {}
  ::isaac_ros_bi3d_interfaces::msg::Bi3DInferenceParametersArray disparity_values(::isaac_ros_bi3d_interfaces::msg::Bi3DInferenceParametersArray::_disparity_values_type arg)
  {
    msg_.disparity_values = std::move(arg);
    return std::move(msg_);
  }

private:
  ::isaac_ros_bi3d_interfaces::msg::Bi3DInferenceParametersArray msg_;
};

class Init_Bi3DInferenceParametersArray_header
{
public:
  Init_Bi3DInferenceParametersArray_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Bi3DInferenceParametersArray_disparity_values header(::isaac_ros_bi3d_interfaces::msg::Bi3DInferenceParametersArray::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_Bi3DInferenceParametersArray_disparity_values(msg_);
  }

private:
  ::isaac_ros_bi3d_interfaces::msg::Bi3DInferenceParametersArray msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::isaac_ros_bi3d_interfaces::msg::Bi3DInferenceParametersArray>()
{
  return isaac_ros_bi3d_interfaces::msg::builder::Init_Bi3DInferenceParametersArray_header();
}

}  // namespace isaac_ros_bi3d_interfaces

#endif  // ISAAC_ROS_BI3D_INTERFACES__MSG__DETAIL__BI3_D_INFERENCE_PARAMETERS_ARRAY__BUILDER_HPP_
