// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from nvblox_msgs:msg/DistanceMapSlice.idl
// generated code does not contain a copyright notice

#ifndef NVBLOX_MSGS__MSG__DETAIL__DISTANCE_MAP_SLICE__STRUCT_HPP_
#define NVBLOX_MSGS__MSG__DETAIL__DISTANCE_MAP_SLICE__STRUCT_HPP_

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
// Member 'origin'
#include "geometry_msgs/msg/detail/point__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__nvblox_msgs__msg__DistanceMapSlice __attribute__((deprecated))
#else
# define DEPRECATED__nvblox_msgs__msg__DistanceMapSlice __declspec(deprecated)
#endif

namespace nvblox_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct DistanceMapSlice_
{
  using Type = DistanceMapSlice_<ContainerAllocator>;

  explicit DistanceMapSlice_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init),
    origin(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->resolution = 0.0f;
      this->width = 0ul;
      this->height = 0ul;
      this->unknown_value = 0.0f;
    }
  }

  explicit DistanceMapSlice_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    origin(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->resolution = 0.0f;
      this->width = 0ul;
      this->height = 0ul;
      this->unknown_value = 0.0f;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _resolution_type =
    float;
  _resolution_type resolution;
  using _width_type =
    uint32_t;
  _width_type width;
  using _height_type =
    uint32_t;
  _height_type height;
  using _origin_type =
    geometry_msgs::msg::Point_<ContainerAllocator>;
  _origin_type origin;
  using _unknown_value_type =
    float;
  _unknown_value_type unknown_value;
  using _data_type =
    std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>>;
  _data_type data;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__resolution(
    const float & _arg)
  {
    this->resolution = _arg;
    return *this;
  }
  Type & set__width(
    const uint32_t & _arg)
  {
    this->width = _arg;
    return *this;
  }
  Type & set__height(
    const uint32_t & _arg)
  {
    this->height = _arg;
    return *this;
  }
  Type & set__origin(
    const geometry_msgs::msg::Point_<ContainerAllocator> & _arg)
  {
    this->origin = _arg;
    return *this;
  }
  Type & set__unknown_value(
    const float & _arg)
  {
    this->unknown_value = _arg;
    return *this;
  }
  Type & set__data(
    const std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>> & _arg)
  {
    this->data = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    nvblox_msgs::msg::DistanceMapSlice_<ContainerAllocator> *;
  using ConstRawPtr =
    const nvblox_msgs::msg::DistanceMapSlice_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<nvblox_msgs::msg::DistanceMapSlice_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<nvblox_msgs::msg::DistanceMapSlice_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      nvblox_msgs::msg::DistanceMapSlice_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<nvblox_msgs::msg::DistanceMapSlice_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      nvblox_msgs::msg::DistanceMapSlice_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<nvblox_msgs::msg::DistanceMapSlice_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<nvblox_msgs::msg::DistanceMapSlice_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<nvblox_msgs::msg::DistanceMapSlice_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__nvblox_msgs__msg__DistanceMapSlice
    std::shared_ptr<nvblox_msgs::msg::DistanceMapSlice_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__nvblox_msgs__msg__DistanceMapSlice
    std::shared_ptr<nvblox_msgs::msg::DistanceMapSlice_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const DistanceMapSlice_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->resolution != other.resolution) {
      return false;
    }
    if (this->width != other.width) {
      return false;
    }
    if (this->height != other.height) {
      return false;
    }
    if (this->origin != other.origin) {
      return false;
    }
    if (this->unknown_value != other.unknown_value) {
      return false;
    }
    if (this->data != other.data) {
      return false;
    }
    return true;
  }
  bool operator!=(const DistanceMapSlice_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct DistanceMapSlice_

// alias to use template instance with default allocator
using DistanceMapSlice =
  nvblox_msgs::msg::DistanceMapSlice_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace nvblox_msgs

#endif  // NVBLOX_MSGS__MSG__DETAIL__DISTANCE_MAP_SLICE__STRUCT_HPP_
