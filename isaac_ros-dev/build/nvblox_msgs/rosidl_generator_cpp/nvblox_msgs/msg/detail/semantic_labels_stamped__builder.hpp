// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from nvblox_msgs:msg/SemanticLabelsStamped.idl
// generated code does not contain a copyright notice

#ifndef NVBLOX_MSGS__MSG__DETAIL__SEMANTIC_LABELS_STAMPED__BUILDER_HPP_
#define NVBLOX_MSGS__MSG__DETAIL__SEMANTIC_LABELS_STAMPED__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "nvblox_msgs/msg/detail/semantic_labels_stamped__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace nvblox_msgs
{

namespace msg
{

namespace builder
{

class Init_SemanticLabelsStamped_labels
{
public:
  explicit Init_SemanticLabelsStamped_labels(::nvblox_msgs::msg::SemanticLabelsStamped & msg)
  : msg_(msg)
  {}
  ::nvblox_msgs::msg::SemanticLabelsStamped labels(::nvblox_msgs::msg::SemanticLabelsStamped::_labels_type arg)
  {
    msg_.labels = std::move(arg);
    return std::move(msg_);
  }

private:
  ::nvblox_msgs::msg::SemanticLabelsStamped msg_;
};

class Init_SemanticLabelsStamped_header
{
public:
  Init_SemanticLabelsStamped_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SemanticLabelsStamped_labels header(::nvblox_msgs::msg::SemanticLabelsStamped::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_SemanticLabelsStamped_labels(msg_);
  }

private:
  ::nvblox_msgs::msg::SemanticLabelsStamped msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::nvblox_msgs::msg::SemanticLabelsStamped>()
{
  return nvblox_msgs::msg::builder::Init_SemanticLabelsStamped_header();
}

}  // namespace nvblox_msgs

#endif  // NVBLOX_MSGS__MSG__DETAIL__SEMANTIC_LABELS_STAMPED__BUILDER_HPP_
