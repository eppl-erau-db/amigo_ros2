// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from isaac_ros_tensor_list_interfaces:msg/TensorShape.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR_SHAPE__BUILDER_HPP_
#define ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR_SHAPE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "isaac_ros_tensor_list_interfaces/msg/detail/tensor_shape__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace isaac_ros_tensor_list_interfaces
{

namespace msg
{

namespace builder
{

class Init_TensorShape_dims
{
public:
  explicit Init_TensorShape_dims(::isaac_ros_tensor_list_interfaces::msg::TensorShape & msg)
  : msg_(msg)
  {}
  ::isaac_ros_tensor_list_interfaces::msg::TensorShape dims(::isaac_ros_tensor_list_interfaces::msg::TensorShape::_dims_type arg)
  {
    msg_.dims = std::move(arg);
    return std::move(msg_);
  }

private:
  ::isaac_ros_tensor_list_interfaces::msg::TensorShape msg_;
};

class Init_TensorShape_rank
{
public:
  Init_TensorShape_rank()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_TensorShape_dims rank(::isaac_ros_tensor_list_interfaces::msg::TensorShape::_rank_type arg)
  {
    msg_.rank = std::move(arg);
    return Init_TensorShape_dims(msg_);
  }

private:
  ::isaac_ros_tensor_list_interfaces::msg::TensorShape msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::isaac_ros_tensor_list_interfaces::msg::TensorShape>()
{
  return isaac_ros_tensor_list_interfaces::msg::builder::Init_TensorShape_rank();
}

}  // namespace isaac_ros_tensor_list_interfaces

#endif  // ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR_SHAPE__BUILDER_HPP_
