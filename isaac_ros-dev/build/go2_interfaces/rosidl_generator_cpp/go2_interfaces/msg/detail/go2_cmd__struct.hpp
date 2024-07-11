// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from go2_interfaces:msg/Go2Cmd.idl
// generated code does not contain a copyright notice

#ifndef GO2_INTERFACES__MSG__DETAIL__GO2_CMD__STRUCT_HPP_
#define GO2_INTERFACES__MSG__DETAIL__GO2_CMD__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__go2_interfaces__msg__Go2Cmd __attribute__((deprecated))
#else
# define DEPRECATED__go2_interfaces__msg__Go2Cmd __declspec(deprecated)
#endif

namespace go2_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Go2Cmd_
{
  using Type = Go2Cmd_<ContainerAllocator>;

  explicit Go2Cmd_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->cmd = 0;
    }
  }

  explicit Go2Cmd_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->cmd = 0;
    }
  }

  // field types and members
  using _cmd_type =
    uint16_t;
  _cmd_type cmd;

  // setters for named parameter idiom
  Type & set__cmd(
    const uint16_t & _arg)
  {
    this->cmd = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    go2_interfaces::msg::Go2Cmd_<ContainerAllocator> *;
  using ConstRawPtr =
    const go2_interfaces::msg::Go2Cmd_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<go2_interfaces::msg::Go2Cmd_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<go2_interfaces::msg::Go2Cmd_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      go2_interfaces::msg::Go2Cmd_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<go2_interfaces::msg::Go2Cmd_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      go2_interfaces::msg::Go2Cmd_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<go2_interfaces::msg::Go2Cmd_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<go2_interfaces::msg::Go2Cmd_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<go2_interfaces::msg::Go2Cmd_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__go2_interfaces__msg__Go2Cmd
    std::shared_ptr<go2_interfaces::msg::Go2Cmd_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__go2_interfaces__msg__Go2Cmd
    std::shared_ptr<go2_interfaces::msg::Go2Cmd_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Go2Cmd_ & other) const
  {
    if (this->cmd != other.cmd) {
      return false;
    }
    return true;
  }
  bool operator!=(const Go2Cmd_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Go2Cmd_

// alias to use template instance with default allocator
using Go2Cmd =
  go2_interfaces::msg::Go2Cmd_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace go2_interfaces

#endif  // GO2_INTERFACES__MSG__DETAIL__GO2_CMD__STRUCT_HPP_
