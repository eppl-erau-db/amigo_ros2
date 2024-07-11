// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from isaac_ros_nova_interfaces:msg/CorrelatedTimestamp.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_NOVA_INTERFACES__MSG__DETAIL__CORRELATED_TIMESTAMP__STRUCT_HPP_
#define ISAAC_ROS_NOVA_INTERFACES__MSG__DETAIL__CORRELATED_TIMESTAMP__STRUCT_HPP_

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
# define DEPRECATED__isaac_ros_nova_interfaces__msg__CorrelatedTimestamp __attribute__((deprecated))
#else
# define DEPRECATED__isaac_ros_nova_interfaces__msg__CorrelatedTimestamp __declspec(deprecated)
#endif

namespace isaac_ros_nova_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct CorrelatedTimestamp_
{
  using Type = CorrelatedTimestamp_<ContainerAllocator>;

  explicit CorrelatedTimestamp_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->phc_val = 0ull;
      this->tsc_val = 0ull;
      this->phc2_val = 0ull;
      this->sys_val = 0ull;
      this->phc_latency = 0ull;
    }
  }

  explicit CorrelatedTimestamp_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->phc_val = 0ull;
      this->tsc_val = 0ull;
      this->phc2_val = 0ull;
      this->sys_val = 0ull;
      this->phc_latency = 0ull;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _phc_val_type =
    uint64_t;
  _phc_val_type phc_val;
  using _tsc_val_type =
    uint64_t;
  _tsc_val_type tsc_val;
  using _phc2_val_type =
    uint64_t;
  _phc2_val_type phc2_val;
  using _sys_val_type =
    uint64_t;
  _sys_val_type sys_val;
  using _phc_latency_type =
    uint64_t;
  _phc_latency_type phc_latency;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__phc_val(
    const uint64_t & _arg)
  {
    this->phc_val = _arg;
    return *this;
  }
  Type & set__tsc_val(
    const uint64_t & _arg)
  {
    this->tsc_val = _arg;
    return *this;
  }
  Type & set__phc2_val(
    const uint64_t & _arg)
  {
    this->phc2_val = _arg;
    return *this;
  }
  Type & set__sys_val(
    const uint64_t & _arg)
  {
    this->sys_val = _arg;
    return *this;
  }
  Type & set__phc_latency(
    const uint64_t & _arg)
  {
    this->phc_latency = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    isaac_ros_nova_interfaces::msg::CorrelatedTimestamp_<ContainerAllocator> *;
  using ConstRawPtr =
    const isaac_ros_nova_interfaces::msg::CorrelatedTimestamp_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<isaac_ros_nova_interfaces::msg::CorrelatedTimestamp_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<isaac_ros_nova_interfaces::msg::CorrelatedTimestamp_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      isaac_ros_nova_interfaces::msg::CorrelatedTimestamp_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<isaac_ros_nova_interfaces::msg::CorrelatedTimestamp_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      isaac_ros_nova_interfaces::msg::CorrelatedTimestamp_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<isaac_ros_nova_interfaces::msg::CorrelatedTimestamp_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<isaac_ros_nova_interfaces::msg::CorrelatedTimestamp_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<isaac_ros_nova_interfaces::msg::CorrelatedTimestamp_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__isaac_ros_nova_interfaces__msg__CorrelatedTimestamp
    std::shared_ptr<isaac_ros_nova_interfaces::msg::CorrelatedTimestamp_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__isaac_ros_nova_interfaces__msg__CorrelatedTimestamp
    std::shared_ptr<isaac_ros_nova_interfaces::msg::CorrelatedTimestamp_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CorrelatedTimestamp_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->phc_val != other.phc_val) {
      return false;
    }
    if (this->tsc_val != other.tsc_val) {
      return false;
    }
    if (this->phc2_val != other.phc2_val) {
      return false;
    }
    if (this->sys_val != other.sys_val) {
      return false;
    }
    if (this->phc_latency != other.phc_latency) {
      return false;
    }
    return true;
  }
  bool operator!=(const CorrelatedTimestamp_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CorrelatedTimestamp_

// alias to use template instance with default allocator
using CorrelatedTimestamp =
  isaac_ros_nova_interfaces::msg::CorrelatedTimestamp_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace isaac_ros_nova_interfaces

#endif  // ISAAC_ROS_NOVA_INTERFACES__MSG__DETAIL__CORRELATED_TIMESTAMP__STRUCT_HPP_
