// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from isaac_ros_tensor_list_interfaces:msg/TensorList.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR_LIST__BUILDER_HPP_
#define ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR_LIST__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "isaac_ros_tensor_list_interfaces/msg/detail/tensor_list__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace isaac_ros_tensor_list_interfaces
{

namespace msg
{

namespace builder
{

class Init_TensorList_tensors
{
public:
  explicit Init_TensorList_tensors(::isaac_ros_tensor_list_interfaces::msg::TensorList & msg)
  : msg_(msg)
  {}
  ::isaac_ros_tensor_list_interfaces::msg::TensorList tensors(::isaac_ros_tensor_list_interfaces::msg::TensorList::_tensors_type arg)
  {
    msg_.tensors = std::move(arg);
    return std::move(msg_);
  }

private:
  ::isaac_ros_tensor_list_interfaces::msg::TensorList msg_;
};

class Init_TensorList_header
{
public:
  Init_TensorList_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_TensorList_tensors header(::isaac_ros_tensor_list_interfaces::msg::TensorList::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_TensorList_tensors(msg_);
  }

private:
  ::isaac_ros_tensor_list_interfaces::msg::TensorList msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::isaac_ros_tensor_list_interfaces::msg::TensorList>()
{
  return isaac_ros_tensor_list_interfaces::msg::builder::Init_TensorList_header();
}

}  // namespace isaac_ros_tensor_list_interfaces

#endif  // ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR_LIST__BUILDER_HPP_
