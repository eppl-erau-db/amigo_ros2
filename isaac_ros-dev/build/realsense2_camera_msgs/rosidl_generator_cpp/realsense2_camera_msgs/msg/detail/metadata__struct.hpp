// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from realsense2_camera_msgs:msg/Metadata.idl
// generated code does not contain a copyright notice

#ifndef REALSENSE2_CAMERA_MSGS__MSG__DETAIL__METADATA__STRUCT_HPP_
#define REALSENSE2_CAMERA_MSGS__MSG__DETAIL__METADATA__STRUCT_HPP_

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
# define DEPRECATED__realsense2_camera_msgs__msg__Metadata __attribute__((deprecated))
#else
# define DEPRECATED__realsense2_camera_msgs__msg__Metadata __declspec(deprecated)
#endif

namespace realsense2_camera_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Metadata_
{
  using Type = Metadata_<ContainerAllocator>;

  explicit Metadata_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->json_data = "";
    }
  }

  explicit Metadata_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    json_data(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->json_data = "";
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _json_data_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _json_data_type json_data;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__json_data(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->json_data = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    realsense2_camera_msgs::msg::Metadata_<ContainerAllocator> *;
  using ConstRawPtr =
    const realsense2_camera_msgs::msg::Metadata_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<realsense2_camera_msgs::msg::Metadata_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<realsense2_camera_msgs::msg::Metadata_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      realsense2_camera_msgs::msg::Metadata_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<realsense2_camera_msgs::msg::Metadata_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      realsense2_camera_msgs::msg::Metadata_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<realsense2_camera_msgs::msg::Metadata_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<realsense2_camera_msgs::msg::Metadata_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<realsense2_camera_msgs::msg::Metadata_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__realsense2_camera_msgs__msg__Metadata
    std::shared_ptr<realsense2_camera_msgs::msg::Metadata_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__realsense2_camera_msgs__msg__Metadata
    std::shared_ptr<realsense2_camera_msgs::msg::Metadata_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Metadata_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->json_data != other.json_data) {
      return false;
    }
    return true;
  }
  bool operator!=(const Metadata_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Metadata_

// alias to use template instance with default allocator
using Metadata =
  realsense2_camera_msgs::msg::Metadata_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace realsense2_camera_msgs

#endif  // REALSENSE2_CAMERA_MSGS__MSG__DETAIL__METADATA__STRUCT_HPP_
