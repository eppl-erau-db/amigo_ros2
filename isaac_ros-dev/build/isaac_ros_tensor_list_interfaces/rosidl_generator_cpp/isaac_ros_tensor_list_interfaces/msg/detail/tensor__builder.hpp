// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from isaac_ros_tensor_list_interfaces:msg/Tensor.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR__BUILDER_HPP_
#define ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "isaac_ros_tensor_list_interfaces/msg/detail/tensor__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace isaac_ros_tensor_list_interfaces
{

namespace msg
{

namespace builder
{

class Init_Tensor_data
{
public:
  explicit Init_Tensor_data(::isaac_ros_tensor_list_interfaces::msg::Tensor & msg)
  : msg_(msg)
  {}
  ::isaac_ros_tensor_list_interfaces::msg::Tensor data(::isaac_ros_tensor_list_interfaces::msg::Tensor::_data_type arg)
  {
    msg_.data = std::move(arg);
    return std::move(msg_);
  }

private:
  ::isaac_ros_tensor_list_interfaces::msg::Tensor msg_;
};

class Init_Tensor_strides
{
public:
  explicit Init_Tensor_strides(::isaac_ros_tensor_list_interfaces::msg::Tensor & msg)
  : msg_(msg)
  {}
  Init_Tensor_data strides(::isaac_ros_tensor_list_interfaces::msg::Tensor::_strides_type arg)
  {
    msg_.strides = std::move(arg);
    return Init_Tensor_data(msg_);
  }

private:
  ::isaac_ros_tensor_list_interfaces::msg::Tensor msg_;
};

class Init_Tensor_data_type
{
public:
  explicit Init_Tensor_data_type(::isaac_ros_tensor_list_interfaces::msg::Tensor & msg)
  : msg_(msg)
  {}
  Init_Tensor_strides data_type(::isaac_ros_tensor_list_interfaces::msg::Tensor::_data_type_type arg)
  {
    msg_.data_type = std::move(arg);
    return Init_Tensor_strides(msg_);
  }

private:
  ::isaac_ros_tensor_list_interfaces::msg::Tensor msg_;
};

class Init_Tensor_shape
{
public:
  explicit Init_Tensor_shape(::isaac_ros_tensor_list_interfaces::msg::Tensor & msg)
  : msg_(msg)
  {}
  Init_Tensor_data_type shape(::isaac_ros_tensor_list_interfaces::msg::Tensor::_shape_type arg)
  {
    msg_.shape = std::move(arg);
    return Init_Tensor_data_type(msg_);
  }

private:
  ::isaac_ros_tensor_list_interfaces::msg::Tensor msg_;
};

class Init_Tensor_name
{
public:
  Init_Tensor_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Tensor_shape name(::isaac_ros_tensor_list_interfaces::msg::Tensor::_name_type arg)
  {
    msg_.name = std::move(arg);
    return Init_Tensor_shape(msg_);
  }

private:
  ::isaac_ros_tensor_list_interfaces::msg::Tensor msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::isaac_ros_tensor_list_interfaces::msg::Tensor>()
{
  return isaac_ros_tensor_list_interfaces::msg::builder::Init_Tensor_name();
}

}  // namespace isaac_ros_tensor_list_interfaces

#endif  // ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR__BUILDER_HPP_
