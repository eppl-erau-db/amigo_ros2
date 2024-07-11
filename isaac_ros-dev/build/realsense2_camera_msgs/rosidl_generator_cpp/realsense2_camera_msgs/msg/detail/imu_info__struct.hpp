// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from realsense2_camera_msgs:msg/IMUInfo.idl
// generated code does not contain a copyright notice

#ifndef REALSENSE2_CAMERA_MSGS__MSG__DETAIL__IMU_INFO__STRUCT_HPP_
#define REALSENSE2_CAMERA_MSGS__MSG__DETAIL__IMU_INFO__STRUCT_HPP_

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
# define DEPRECATED__realsense2_camera_msgs__msg__IMUInfo __attribute__((deprecated))
#else
# define DEPRECATED__realsense2_camera_msgs__msg__IMUInfo __declspec(deprecated)
#endif

namespace realsense2_camera_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct IMUInfo_
{
  using Type = IMUInfo_<ContainerAllocator>;

  explicit IMUInfo_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 12>::iterator, double>(this->data.begin(), this->data.end(), 0.0);
      std::fill<typename std::array<double, 3>::iterator, double>(this->noise_variances.begin(), this->noise_variances.end(), 0.0);
      std::fill<typename std::array<double, 3>::iterator, double>(this->bias_variances.begin(), this->bias_variances.end(), 0.0);
    }
  }

  explicit IMUInfo_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    data(_alloc),
    noise_variances(_alloc),
    bias_variances(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 12>::iterator, double>(this->data.begin(), this->data.end(), 0.0);
      std::fill<typename std::array<double, 3>::iterator, double>(this->noise_variances.begin(), this->noise_variances.end(), 0.0);
      std::fill<typename std::array<double, 3>::iterator, double>(this->bias_variances.begin(), this->bias_variances.end(), 0.0);
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _data_type =
    std::array<double, 12>;
  _data_type data;
  using _noise_variances_type =
    std::array<double, 3>;
  _noise_variances_type noise_variances;
  using _bias_variances_type =
    std::array<double, 3>;
  _bias_variances_type bias_variances;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__data(
    const std::array<double, 12> & _arg)
  {
    this->data = _arg;
    return *this;
  }
  Type & set__noise_variances(
    const std::array<double, 3> & _arg)
  {
    this->noise_variances = _arg;
    return *this;
  }
  Type & set__bias_variances(
    const std::array<double, 3> & _arg)
  {
    this->bias_variances = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    realsense2_camera_msgs::msg::IMUInfo_<ContainerAllocator> *;
  using ConstRawPtr =
    const realsense2_camera_msgs::msg::IMUInfo_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<realsense2_camera_msgs::msg::IMUInfo_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<realsense2_camera_msgs::msg::IMUInfo_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      realsense2_camera_msgs::msg::IMUInfo_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<realsense2_camera_msgs::msg::IMUInfo_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      realsense2_camera_msgs::msg::IMUInfo_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<realsense2_camera_msgs::msg::IMUInfo_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<realsense2_camera_msgs::msg::IMUInfo_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<realsense2_camera_msgs::msg::IMUInfo_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__realsense2_camera_msgs__msg__IMUInfo
    std::shared_ptr<realsense2_camera_msgs::msg::IMUInfo_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__realsense2_camera_msgs__msg__IMUInfo
    std::shared_ptr<realsense2_camera_msgs::msg::IMUInfo_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const IMUInfo_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->data != other.data) {
      return false;
    }
    if (this->noise_variances != other.noise_variances) {
      return false;
    }
    if (this->bias_variances != other.bias_variances) {
      return false;
    }
    return true;
  }
  bool operator!=(const IMUInfo_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct IMUInfo_

// alias to use template instance with default allocator
using IMUInfo =
  realsense2_camera_msgs::msg::IMUInfo_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace realsense2_camera_msgs

#endif  // REALSENSE2_CAMERA_MSGS__MSG__DETAIL__IMU_INFO__STRUCT_HPP_
