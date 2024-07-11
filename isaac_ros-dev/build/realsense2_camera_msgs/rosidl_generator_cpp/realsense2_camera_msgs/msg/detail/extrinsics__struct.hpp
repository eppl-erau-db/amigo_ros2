// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from realsense2_camera_msgs:msg/Extrinsics.idl
// generated code does not contain a copyright notice

#ifndef REALSENSE2_CAMERA_MSGS__MSG__DETAIL__EXTRINSICS__STRUCT_HPP_
#define REALSENSE2_CAMERA_MSGS__MSG__DETAIL__EXTRINSICS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__realsense2_camera_msgs__msg__Extrinsics __attribute__((deprecated))
#else
# define DEPRECATED__realsense2_camera_msgs__msg__Extrinsics __declspec(deprecated)
#endif

namespace realsense2_camera_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Extrinsics_
{
  using Type = Extrinsics_<ContainerAllocator>;

  explicit Extrinsics_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 9>::iterator, double>(this->rotation.begin(), this->rotation.end(), 0.0);
      std::fill<typename std::array<double, 3>::iterator, double>(this->translation.begin(), this->translation.end(), 0.0);
    }
  }

  explicit Extrinsics_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : rotation(_alloc),
    translation(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 9>::iterator, double>(this->rotation.begin(), this->rotation.end(), 0.0);
      std::fill<typename std::array<double, 3>::iterator, double>(this->translation.begin(), this->translation.end(), 0.0);
    }
  }

  // field types and members
  using _rotation_type =
    std::array<double, 9>;
  _rotation_type rotation;
  using _translation_type =
    std::array<double, 3>;
  _translation_type translation;

  // setters for named parameter idiom
  Type & set__rotation(
    const std::array<double, 9> & _arg)
  {
    this->rotation = _arg;
    return *this;
  }
  Type & set__translation(
    const std::array<double, 3> & _arg)
  {
    this->translation = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    realsense2_camera_msgs::msg::Extrinsics_<ContainerAllocator> *;
  using ConstRawPtr =
    const realsense2_camera_msgs::msg::Extrinsics_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<realsense2_camera_msgs::msg::Extrinsics_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<realsense2_camera_msgs::msg::Extrinsics_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      realsense2_camera_msgs::msg::Extrinsics_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<realsense2_camera_msgs::msg::Extrinsics_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      realsense2_camera_msgs::msg::Extrinsics_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<realsense2_camera_msgs::msg::Extrinsics_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<realsense2_camera_msgs::msg::Extrinsics_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<realsense2_camera_msgs::msg::Extrinsics_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__realsense2_camera_msgs__msg__Extrinsics
    std::shared_ptr<realsense2_camera_msgs::msg::Extrinsics_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__realsense2_camera_msgs__msg__Extrinsics
    std::shared_ptr<realsense2_camera_msgs::msg::Extrinsics_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Extrinsics_ & other) const
  {
    if (this->rotation != other.rotation) {
      return false;
    }
    if (this->translation != other.translation) {
      return false;
    }
    return true;
  }
  bool operator!=(const Extrinsics_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Extrinsics_

// alias to use template instance with default allocator
using Extrinsics =
  realsense2_camera_msgs::msg::Extrinsics_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace realsense2_camera_msgs

#endif  // REALSENSE2_CAMERA_MSGS__MSG__DETAIL__EXTRINSICS__STRUCT_HPP_
