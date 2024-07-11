// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from nvblox_msgs:srv/EsdfAndGradients.idl
// generated code does not contain a copyright notice

#ifndef NVBLOX_MSGS__SRV__DETAIL__ESDF_AND_GRADIENTS__BUILDER_HPP_
#define NVBLOX_MSGS__SRV__DETAIL__ESDF_AND_GRADIENTS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "nvblox_msgs/srv/detail/esdf_and_gradients__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace nvblox_msgs
{

namespace srv
{

namespace builder
{

class Init_EsdfAndGradients_Request_aabb_size_m
{
public:
  explicit Init_EsdfAndGradients_Request_aabb_size_m(::nvblox_msgs::srv::EsdfAndGradients_Request & msg)
  : msg_(msg)
  {}
  ::nvblox_msgs::srv::EsdfAndGradients_Request aabb_size_m(::nvblox_msgs::srv::EsdfAndGradients_Request::_aabb_size_m_type arg)
  {
    msg_.aabb_size_m = std::move(arg);
    return std::move(msg_);
  }

private:
  ::nvblox_msgs::srv::EsdfAndGradients_Request msg_;
};

class Init_EsdfAndGradients_Request_aabb_min_m
{
public:
  Init_EsdfAndGradients_Request_aabb_min_m()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_EsdfAndGradients_Request_aabb_size_m aabb_min_m(::nvblox_msgs::srv::EsdfAndGradients_Request::_aabb_min_m_type arg)
  {
    msg_.aabb_min_m = std::move(arg);
    return Init_EsdfAndGradients_Request_aabb_size_m(msg_);
  }

private:
  ::nvblox_msgs::srv::EsdfAndGradients_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::nvblox_msgs::srv::EsdfAndGradients_Request>()
{
  return nvblox_msgs::srv::builder::Init_EsdfAndGradients_Request_aabb_min_m();
}

}  // namespace nvblox_msgs


namespace nvblox_msgs
{

namespace srv
{

namespace builder
{

class Init_EsdfAndGradients_Response_esdf_and_gradients
{
public:
  explicit Init_EsdfAndGradients_Response_esdf_and_gradients(::nvblox_msgs::srv::EsdfAndGradients_Response & msg)
  : msg_(msg)
  {}
  ::nvblox_msgs::srv::EsdfAndGradients_Response esdf_and_gradients(::nvblox_msgs::srv::EsdfAndGradients_Response::_esdf_and_gradients_type arg)
  {
    msg_.esdf_and_gradients = std::move(arg);
    return std::move(msg_);
  }

private:
  ::nvblox_msgs::srv::EsdfAndGradients_Response msg_;
};

class Init_EsdfAndGradients_Response_voxel_size
{
public:
  Init_EsdfAndGradients_Response_voxel_size()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_EsdfAndGradients_Response_esdf_and_gradients voxel_size(::nvblox_msgs::srv::EsdfAndGradients_Response::_voxel_size_type arg)
  {
    msg_.voxel_size = std::move(arg);
    return Init_EsdfAndGradients_Response_esdf_and_gradients(msg_);
  }

private:
  ::nvblox_msgs::srv::EsdfAndGradients_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::nvblox_msgs::srv::EsdfAndGradients_Response>()
{
  return nvblox_msgs::srv::builder::Init_EsdfAndGradients_Response_voxel_size();
}

}  // namespace nvblox_msgs

#endif  // NVBLOX_MSGS__SRV__DETAIL__ESDF_AND_GRADIENTS__BUILDER_HPP_
