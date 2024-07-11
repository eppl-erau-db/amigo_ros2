// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from nvblox_msgs:msg/SemanticLabelsStamped.idl
// generated code does not contain a copyright notice

#ifndef NVBLOX_MSGS__MSG__DETAIL__SEMANTIC_LABELS_STAMPED__STRUCT_HPP_
#define NVBLOX_MSGS__MSG__DETAIL__SEMANTIC_LABELS_STAMPED__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__nvblox_msgs__msg__SemanticLabelsStamped __attribute__((deprecated))
#else
# define DEPRECATED__nvblox_msgs__msg__SemanticLabelsStamped __declspec(deprecated)
#endif

namespace nvblox_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct SemanticLabelsStamped_
{
  using Type = SemanticLabelsStamped_<ContainerAllocator>;

  explicit SemanticLabelsStamped_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->labels = "";
    }
  }

  explicit SemanticLabelsStamped_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    labels(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->labels = "";
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _labels_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _labels_type labels;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__labels(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->labels = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    nvblox_msgs::msg::SemanticLabelsStamped_<ContainerAllocator> *;
  using ConstRawPtr =
    const nvblox_msgs::msg::SemanticLabelsStamped_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<nvblox_msgs::msg::SemanticLabelsStamped_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<nvblox_msgs::msg::SemanticLabelsStamped_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      nvblox_msgs::msg::SemanticLabelsStamped_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<nvblox_msgs::msg::SemanticLabelsStamped_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      nvblox_msgs::msg::SemanticLabelsStamped_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<nvblox_msgs::msg::SemanticLabelsStamped_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<nvblox_msgs::msg::SemanticLabelsStamped_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<nvblox_msgs::msg::SemanticLabelsStamped_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__nvblox_msgs__msg__SemanticLabelsStamped
    std::shared_ptr<nvblox_msgs::msg::SemanticLabelsStamped_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__nvblox_msgs__msg__SemanticLabelsStamped
    std::shared_ptr<nvblox_msgs::msg::SemanticLabelsStamped_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SemanticLabelsStamped_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->labels != other.labels) {
      return false;
    }
    return true;
  }
  bool operator!=(const SemanticLabelsStamped_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SemanticLabelsStamped_

// alias to use template instance with default allocator
using SemanticLabelsStamped =
  nvblox_msgs::msg::SemanticLabelsStamped_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace nvblox_msgs

#endif  // NVBLOX_MSGS__MSG__DETAIL__SEMANTIC_LABELS_STAMPED__STRUCT_HPP_
