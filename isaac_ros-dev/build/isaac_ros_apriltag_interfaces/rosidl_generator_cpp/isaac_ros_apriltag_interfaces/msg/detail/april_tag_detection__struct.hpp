// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from isaac_ros_apriltag_interfaces:msg/AprilTagDetection.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_APRILTAG_INTERFACES__MSG__DETAIL__APRIL_TAG_DETECTION__STRUCT_HPP_
#define ISAAC_ROS_APRILTAG_INTERFACES__MSG__DETAIL__APRIL_TAG_DETECTION__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'center'
// Member 'corners'
#include "geometry_msgs/msg/detail/point__struct.hpp"
// Member 'pose'
#include "geometry_msgs/msg/detail/pose_with_covariance_stamped__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__isaac_ros_apriltag_interfaces__msg__AprilTagDetection __attribute__((deprecated))
#else
# define DEPRECATED__isaac_ros_apriltag_interfaces__msg__AprilTagDetection __declspec(deprecated)
#endif

namespace isaac_ros_apriltag_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct AprilTagDetection_
{
  using Type = AprilTagDetection_<ContainerAllocator>;

  explicit AprilTagDetection_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : center(_init),
    pose(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->family = "";
      this->id = 0l;
      this->corners.fill(geometry_msgs::msg::Point_<ContainerAllocator>{_init});
    }
  }

  explicit AprilTagDetection_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : family(_alloc),
    center(_alloc, _init),
    corners(_alloc),
    pose(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->family = "";
      this->id = 0l;
      this->corners.fill(geometry_msgs::msg::Point_<ContainerAllocator>{_alloc, _init});
    }
  }

  // field types and members
  using _family_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _family_type family;
  using _id_type =
    int32_t;
  _id_type id;
  using _center_type =
    geometry_msgs::msg::Point_<ContainerAllocator>;
  _center_type center;
  using _corners_type =
    std::array<geometry_msgs::msg::Point_<ContainerAllocator>, 4>;
  _corners_type corners;
  using _pose_type =
    geometry_msgs::msg::PoseWithCovarianceStamped_<ContainerAllocator>;
  _pose_type pose;

  // setters for named parameter idiom
  Type & set__family(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->family = _arg;
    return *this;
  }
  Type & set__id(
    const int32_t & _arg)
  {
    this->id = _arg;
    return *this;
  }
  Type & set__center(
    const geometry_msgs::msg::Point_<ContainerAllocator> & _arg)
  {
    this->center = _arg;
    return *this;
  }
  Type & set__corners(
    const std::array<geometry_msgs::msg::Point_<ContainerAllocator>, 4> & _arg)
  {
    this->corners = _arg;
    return *this;
  }
  Type & set__pose(
    const geometry_msgs::msg::PoseWithCovarianceStamped_<ContainerAllocator> & _arg)
  {
    this->pose = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    isaac_ros_apriltag_interfaces::msg::AprilTagDetection_<ContainerAllocator> *;
  using ConstRawPtr =
    const isaac_ros_apriltag_interfaces::msg::AprilTagDetection_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<isaac_ros_apriltag_interfaces::msg::AprilTagDetection_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<isaac_ros_apriltag_interfaces::msg::AprilTagDetection_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      isaac_ros_apriltag_interfaces::msg::AprilTagDetection_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<isaac_ros_apriltag_interfaces::msg::AprilTagDetection_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      isaac_ros_apriltag_interfaces::msg::AprilTagDetection_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<isaac_ros_apriltag_interfaces::msg::AprilTagDetection_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<isaac_ros_apriltag_interfaces::msg::AprilTagDetection_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<isaac_ros_apriltag_interfaces::msg::AprilTagDetection_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__isaac_ros_apriltag_interfaces__msg__AprilTagDetection
    std::shared_ptr<isaac_ros_apriltag_interfaces::msg::AprilTagDetection_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__isaac_ros_apriltag_interfaces__msg__AprilTagDetection
    std::shared_ptr<isaac_ros_apriltag_interfaces::msg::AprilTagDetection_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const AprilTagDetection_ & other) const
  {
    if (this->family != other.family) {
      return false;
    }
    if (this->id != other.id) {
      return false;
    }
    if (this->center != other.center) {
      return false;
    }
    if (this->corners != other.corners) {
      return false;
    }
    if (this->pose != other.pose) {
      return false;
    }
    return true;
  }
  bool operator!=(const AprilTagDetection_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct AprilTagDetection_

// alias to use template instance with default allocator
using AprilTagDetection =
  isaac_ros_apriltag_interfaces::msg::AprilTagDetection_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace isaac_ros_apriltag_interfaces

#endif  // ISAAC_ROS_APRILTAG_INTERFACES__MSG__DETAIL__APRIL_TAG_DETECTION__STRUCT_HPP_
