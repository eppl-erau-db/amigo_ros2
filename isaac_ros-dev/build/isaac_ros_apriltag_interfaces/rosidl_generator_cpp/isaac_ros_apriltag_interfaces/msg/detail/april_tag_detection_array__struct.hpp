// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from isaac_ros_apriltag_interfaces:msg/AprilTagDetectionArray.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_APRILTAG_INTERFACES__MSG__DETAIL__APRIL_TAG_DETECTION_ARRAY__STRUCT_HPP_
#define ISAAC_ROS_APRILTAG_INTERFACES__MSG__DETAIL__APRIL_TAG_DETECTION_ARRAY__STRUCT_HPP_

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
// Member 'detections'
#include "isaac_ros_apriltag_interfaces/msg/detail/april_tag_detection__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__isaac_ros_apriltag_interfaces__msg__AprilTagDetectionArray __attribute__((deprecated))
#else
# define DEPRECATED__isaac_ros_apriltag_interfaces__msg__AprilTagDetectionArray __declspec(deprecated)
#endif

namespace isaac_ros_apriltag_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct AprilTagDetectionArray_
{
  using Type = AprilTagDetectionArray_<ContainerAllocator>;

  explicit AprilTagDetectionArray_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    (void)_init;
  }

  explicit AprilTagDetectionArray_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _detections_type =
    std::vector<isaac_ros_apriltag_interfaces::msg::AprilTagDetection_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<isaac_ros_apriltag_interfaces::msg::AprilTagDetection_<ContainerAllocator>>>;
  _detections_type detections;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__detections(
    const std::vector<isaac_ros_apriltag_interfaces::msg::AprilTagDetection_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<isaac_ros_apriltag_interfaces::msg::AprilTagDetection_<ContainerAllocator>>> & _arg)
  {
    this->detections = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    isaac_ros_apriltag_interfaces::msg::AprilTagDetectionArray_<ContainerAllocator> *;
  using ConstRawPtr =
    const isaac_ros_apriltag_interfaces::msg::AprilTagDetectionArray_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<isaac_ros_apriltag_interfaces::msg::AprilTagDetectionArray_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<isaac_ros_apriltag_interfaces::msg::AprilTagDetectionArray_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      isaac_ros_apriltag_interfaces::msg::AprilTagDetectionArray_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<isaac_ros_apriltag_interfaces::msg::AprilTagDetectionArray_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      isaac_ros_apriltag_interfaces::msg::AprilTagDetectionArray_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<isaac_ros_apriltag_interfaces::msg::AprilTagDetectionArray_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<isaac_ros_apriltag_interfaces::msg::AprilTagDetectionArray_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<isaac_ros_apriltag_interfaces::msg::AprilTagDetectionArray_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__isaac_ros_apriltag_interfaces__msg__AprilTagDetectionArray
    std::shared_ptr<isaac_ros_apriltag_interfaces::msg::AprilTagDetectionArray_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__isaac_ros_apriltag_interfaces__msg__AprilTagDetectionArray
    std::shared_ptr<isaac_ros_apriltag_interfaces::msg::AprilTagDetectionArray_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const AprilTagDetectionArray_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->detections != other.detections) {
      return false;
    }
    return true;
  }
  bool operator!=(const AprilTagDetectionArray_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct AprilTagDetectionArray_

// alias to use template instance with default allocator
using AprilTagDetectionArray =
  isaac_ros_apriltag_interfaces::msg::AprilTagDetectionArray_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace isaac_ros_apriltag_interfaces

#endif  // ISAAC_ROS_APRILTAG_INTERFACES__MSG__DETAIL__APRIL_TAG_DETECTION_ARRAY__STRUCT_HPP_
