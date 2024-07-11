// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from isaac_ros_pointcloud_interfaces:msg/FlatScan.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_POINTCLOUD_INTERFACES__MSG__DETAIL__FLAT_SCAN__STRUCT_HPP_
#define ISAAC_ROS_POINTCLOUD_INTERFACES__MSG__DETAIL__FLAT_SCAN__STRUCT_HPP_

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
# define DEPRECATED__isaac_ros_pointcloud_interfaces__msg__FlatScan __attribute__((deprecated))
#else
# define DEPRECATED__isaac_ros_pointcloud_interfaces__msg__FlatScan __declspec(deprecated)
#endif

namespace isaac_ros_pointcloud_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct FlatScan_
{
  using Type = FlatScan_<ContainerAllocator>;

  explicit FlatScan_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->range_min = 0.0f;
      this->range_max = 0.0f;
    }
  }

  explicit FlatScan_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->range_min = 0.0f;
      this->range_max = 0.0f;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _range_min_type =
    float;
  _range_min_type range_min;
  using _range_max_type =
    float;
  _range_max_type range_max;
  using _angles_type =
    std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>>;
  _angles_type angles;
  using _ranges_type =
    std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>>;
  _ranges_type ranges;
  using _intensities_type =
    std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>>;
  _intensities_type intensities;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__range_min(
    const float & _arg)
  {
    this->range_min = _arg;
    return *this;
  }
  Type & set__range_max(
    const float & _arg)
  {
    this->range_max = _arg;
    return *this;
  }
  Type & set__angles(
    const std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>> & _arg)
  {
    this->angles = _arg;
    return *this;
  }
  Type & set__ranges(
    const std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>> & _arg)
  {
    this->ranges = _arg;
    return *this;
  }
  Type & set__intensities(
    const std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>> & _arg)
  {
    this->intensities = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    isaac_ros_pointcloud_interfaces::msg::FlatScan_<ContainerAllocator> *;
  using ConstRawPtr =
    const isaac_ros_pointcloud_interfaces::msg::FlatScan_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<isaac_ros_pointcloud_interfaces::msg::FlatScan_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<isaac_ros_pointcloud_interfaces::msg::FlatScan_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      isaac_ros_pointcloud_interfaces::msg::FlatScan_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<isaac_ros_pointcloud_interfaces::msg::FlatScan_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      isaac_ros_pointcloud_interfaces::msg::FlatScan_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<isaac_ros_pointcloud_interfaces::msg::FlatScan_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<isaac_ros_pointcloud_interfaces::msg::FlatScan_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<isaac_ros_pointcloud_interfaces::msg::FlatScan_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__isaac_ros_pointcloud_interfaces__msg__FlatScan
    std::shared_ptr<isaac_ros_pointcloud_interfaces::msg::FlatScan_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__isaac_ros_pointcloud_interfaces__msg__FlatScan
    std::shared_ptr<isaac_ros_pointcloud_interfaces::msg::FlatScan_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const FlatScan_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->range_min != other.range_min) {
      return false;
    }
    if (this->range_max != other.range_max) {
      return false;
    }
    if (this->angles != other.angles) {
      return false;
    }
    if (this->ranges != other.ranges) {
      return false;
    }
    if (this->intensities != other.intensities) {
      return false;
    }
    return true;
  }
  bool operator!=(const FlatScan_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct FlatScan_

// alias to use template instance with default allocator
using FlatScan =
  isaac_ros_pointcloud_interfaces::msg::FlatScan_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace isaac_ros_pointcloud_interfaces

#endif  // ISAAC_ROS_POINTCLOUD_INTERFACES__MSG__DETAIL__FLAT_SCAN__STRUCT_HPP_
