// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from nvblox_msgs:msg/Index3D.idl
// generated code does not contain a copyright notice

#ifndef NVBLOX_MSGS__MSG__DETAIL__INDEX3_D__STRUCT_HPP_
#define NVBLOX_MSGS__MSG__DETAIL__INDEX3_D__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__nvblox_msgs__msg__Index3D __attribute__((deprecated))
#else
# define DEPRECATED__nvblox_msgs__msg__Index3D __declspec(deprecated)
#endif

namespace nvblox_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Index3D_
{
  using Type = Index3D_<ContainerAllocator>;

  explicit Index3D_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0l;
      this->y = 0l;
      this->z = 0l;
    }
  }

  explicit Index3D_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0l;
      this->y = 0l;
      this->z = 0l;
    }
  }

  // field types and members
  using _x_type =
    int32_t;
  _x_type x;
  using _y_type =
    int32_t;
  _y_type y;
  using _z_type =
    int32_t;
  _z_type z;

  // setters for named parameter idiom
  Type & set__x(
    const int32_t & _arg)
  {
    this->x = _arg;
    return *this;
  }
  Type & set__y(
    const int32_t & _arg)
  {
    this->y = _arg;
    return *this;
  }
  Type & set__z(
    const int32_t & _arg)
  {
    this->z = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    nvblox_msgs::msg::Index3D_<ContainerAllocator> *;
  using ConstRawPtr =
    const nvblox_msgs::msg::Index3D_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<nvblox_msgs::msg::Index3D_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<nvblox_msgs::msg::Index3D_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      nvblox_msgs::msg::Index3D_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<nvblox_msgs::msg::Index3D_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      nvblox_msgs::msg::Index3D_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<nvblox_msgs::msg::Index3D_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<nvblox_msgs::msg::Index3D_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<nvblox_msgs::msg::Index3D_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__nvblox_msgs__msg__Index3D
    std::shared_ptr<nvblox_msgs::msg::Index3D_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__nvblox_msgs__msg__Index3D
    std::shared_ptr<nvblox_msgs::msg::Index3D_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Index3D_ & other) const
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
  bool operator!=(const Index3D_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Index3D_

// alias to use template instance with default allocator
using Index3D =
  nvblox_msgs::msg::Index3D_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace nvblox_msgs

#endif  // NVBLOX_MSGS__MSG__DETAIL__INDEX3_D__STRUCT_HPP_
