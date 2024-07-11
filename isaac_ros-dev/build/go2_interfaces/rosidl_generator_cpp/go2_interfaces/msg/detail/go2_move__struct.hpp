// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from go2_interfaces:msg/Go2Move.idl
// generated code does not contain a copyright notice

#ifndef GO2_INTERFACES__MSG__DETAIL__GO2_MOVE__STRUCT_HPP_
#define GO2_INTERFACES__MSG__DETAIL__GO2_MOVE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__go2_interfaces__msg__Go2Move __attribute__((deprecated))
#else
# define DEPRECATED__go2_interfaces__msg__Go2Move __declspec(deprecated)
#endif

namespace go2_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Go2Move_
{
  using Type = Go2Move_<ContainerAllocator>;

  explicit Go2Move_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0.0f;
      this->y = 0.0f;
      this->z = 0.0f;
    }
  }

  explicit Go2Move_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0.0f;
      this->y = 0.0f;
      this->z = 0.0f;
    }
  }

  // field types and members
  using _x_type =
    float;
  _x_type x;
  using _y_type =
    float;
  _y_type y;
  using _z_type =
    float;
  _z_type z;

  // setters for named parameter idiom
  Type & set__x(
    const float & _arg)
  {
    this->x = _arg;
    return *this;
  }
  Type & set__y(
    const float & _arg)
  {
    this->y = _arg;
    return *this;
  }
  Type & set__z(
    const float & _arg)
  {
    this->z = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    go2_interfaces::msg::Go2Move_<ContainerAllocator> *;
  using ConstRawPtr =
    const go2_interfaces::msg::Go2Move_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<go2_interfaces::msg::Go2Move_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<go2_interfaces::msg::Go2Move_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      go2_interfaces::msg::Go2Move_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<go2_interfaces::msg::Go2Move_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      go2_interfaces::msg::Go2Move_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<go2_interfaces::msg::Go2Move_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<go2_interfaces::msg::Go2Move_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<go2_interfaces::msg::Go2Move_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__go2_interfaces__msg__Go2Move
    std::shared_ptr<go2_interfaces::msg::Go2Move_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__go2_interfaces__msg__Go2Move
    std::shared_ptr<go2_interfaces::msg::Go2Move_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Go2Move_ & other) const
  {
    if (this->x != other.x) {
      return false;
    }
    if (this->y != other.y) {
      return false;
    }
    if (this->z != other.z) {
      return false;
    }
    return true;
  }
  bool operator!=(const Go2Move_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Go2Move_

// alias to use template instance with default allocator
using Go2Move =
  go2_interfaces::msg::Go2Move_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace go2_interfaces

#endif  // GO2_INTERFACES__MSG__DETAIL__GO2_MOVE__STRUCT_HPP_
