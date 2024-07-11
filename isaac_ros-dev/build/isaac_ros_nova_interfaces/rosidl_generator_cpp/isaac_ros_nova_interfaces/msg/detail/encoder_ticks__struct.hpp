// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from isaac_ros_nova_interfaces:msg/EncoderTicks.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_NOVA_INTERFACES__MSG__DETAIL__ENCODER_TICKS__STRUCT_HPP_
#define ISAAC_ROS_NOVA_INTERFACES__MSG__DETAIL__ENCODER_TICKS__STRUCT_HPP_

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
# define DEPRECATED__isaac_ros_nova_interfaces__msg__EncoderTicks __attribute__((deprecated))
#else
# define DEPRECATED__isaac_ros_nova_interfaces__msg__EncoderTicks __declspec(deprecated)
#endif

namespace isaac_ros_nova_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct EncoderTicks_
{
  using Type = EncoderTicks_<ContainerAllocator>;

  explicit EncoderTicks_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->left_ticks = 0ul;
      this->right_ticks = 0ul;
      this->encoder_timestamp = 0ull;
    }
  }

  explicit EncoderTicks_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->left_ticks = 0ul;
      this->right_ticks = 0ul;
      this->encoder_timestamp = 0ull;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _left_ticks_type =
    uint32_t;
  _left_ticks_type left_ticks;
  using _right_ticks_type =
    uint32_t;
  _right_ticks_type right_ticks;
  using _encoder_timestamp_type =
    uint64_t;
  _encoder_timestamp_type encoder_timestamp;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__left_ticks(
    const uint32_t & _arg)
  {
    this->left_ticks = _arg;
    return *this;
  }
  Type & set__right_ticks(
    const uint32_t & _arg)
  {
    this->right_ticks = _arg;
    return *this;
  }
  Type & set__encoder_timestamp(
    const uint64_t & _arg)
  {
    this->encoder_timestamp = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    isaac_ros_nova_interfaces::msg::EncoderTicks_<ContainerAllocator> *;
  using ConstRawPtr =
    const isaac_ros_nova_interfaces::msg::EncoderTicks_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<isaac_ros_nova_interfaces::msg::EncoderTicks_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<isaac_ros_nova_interfaces::msg::EncoderTicks_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      isaac_ros_nova_interfaces::msg::EncoderTicks_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<isaac_ros_nova_interfaces::msg::EncoderTicks_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      isaac_ros_nova_interfaces::msg::EncoderTicks_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<isaac_ros_nova_interfaces::msg::EncoderTicks_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<isaac_ros_nova_interfaces::msg::EncoderTicks_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<isaac_ros_nova_interfaces::msg::EncoderTicks_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__isaac_ros_nova_interfaces__msg__EncoderTicks
    std::shared_ptr<isaac_ros_nova_interfaces::msg::EncoderTicks_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__isaac_ros_nova_interfaces__msg__EncoderTicks
    std::shared_ptr<isaac_ros_nova_interfaces::msg::EncoderTicks_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const EncoderTicks_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->left_ticks != other.left_ticks) {
      return false;
    }
    if (this->right_ticks != other.right_ticks) {
      return false;
    }
    if (this->encoder_timestamp != other.encoder_timestamp) {
      return false;
    }
    return true;
  }
  bool operator!=(const EncoderTicks_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct EncoderTicks_

// alias to use template instance with default allocator
using EncoderTicks =
  isaac_ros_nova_interfaces::msg::EncoderTicks_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace isaac_ros_nova_interfaces

#endif  // ISAAC_ROS_NOVA_INTERFACES__MSG__DETAIL__ENCODER_TICKS__STRUCT_HPP_
