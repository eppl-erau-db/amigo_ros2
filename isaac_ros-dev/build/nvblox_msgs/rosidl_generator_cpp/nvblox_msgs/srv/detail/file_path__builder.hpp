// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from nvblox_msgs:srv/FilePath.idl
// generated code does not contain a copyright notice

#ifndef NVBLOX_MSGS__SRV__DETAIL__FILE_PATH__BUILDER_HPP_
#define NVBLOX_MSGS__SRV__DETAIL__FILE_PATH__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "nvblox_msgs/srv/detail/file_path__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace nvblox_msgs
{

namespace srv
{

namespace builder
{

class Init_FilePath_Request_file_path
{
public:
  Init_FilePath_Request_file_path()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::nvblox_msgs::srv::FilePath_Request file_path(::nvblox_msgs::srv::FilePath_Request::_file_path_type arg)
  {
    msg_.file_path = std::move(arg);
    return std::move(msg_);
  }

private:
  ::nvblox_msgs::srv::FilePath_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::nvblox_msgs::srv::FilePath_Request>()
{
  return nvblox_msgs::srv::builder::Init_FilePath_Request_file_path();
}

}  // namespace nvblox_msgs


namespace nvblox_msgs
{

namespace srv
{

namespace builder
{

class Init_FilePath_Response_success
{
public:
  Init_FilePath_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::nvblox_msgs::srv::FilePath_Response success(::nvblox_msgs::srv::FilePath_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::nvblox_msgs::srv::FilePath_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::nvblox_msgs::srv::FilePath_Response>()
{
  return nvblox_msgs::srv::builder::Init_FilePath_Response_success();
}

}  // namespace nvblox_msgs

#endif  // NVBLOX_MSGS__SRV__DETAIL__FILE_PATH__BUILDER_HPP_
