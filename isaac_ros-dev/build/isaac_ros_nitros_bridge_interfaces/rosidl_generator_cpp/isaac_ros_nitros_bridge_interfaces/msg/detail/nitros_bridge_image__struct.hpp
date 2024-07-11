// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from isaac_ros_nitros_bridge_interfaces:msg/NitrosBridgeImage.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_NITROS_BRIDGE_INTERFACES__MSG__DETAIL__NITROS_BRIDGE_IMAGE__STRUCT_HPP_
#define ISAAC_ROS_NITROS_BRIDGE_INTERFACES__MSG__DETAIL__NITROS_BRIDGE_IMAGE__STRUCT_HPP_

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
# define DEPRECATED__isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage __attribute__((deprecated))
#else
# define DEPRECATED__isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage __declspec(deprecated)
#endif

namespace isaac_ros_nitros_bridge_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct NitrosBridgeImage_
{
  using Type = NitrosBridgeImage_<ContainerAllocator>;

  explicit NitrosBridgeImage_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->height = 0ul;
      this->width = 0ul;
      this->encoding = "";
      this->is_bigendian = 0;
      this->step = 0ul;
    }
  }

  explicit NitrosBridgeImage_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    encoding(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->height = 0ul;
      this->width = 0ul;
      this->encoding = "";
      this->is_bigendian = 0;
      this->step = 0ul;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _height_type =
    uint32_t;
  _height_type height;
  using _width_type =
    uint32_t;
  _width_type width;
  using _encoding_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _encoding_type encoding;
  using _is_bigendian_type =
    uint8_t;
  _is_bigendian_type is_bigendian;
  using _step_type =
    uint32_t;
  _step_type step;
  using _data_type =
    std::vector<int32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int32_t>>;
  _data_type data;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__height(
    const uint32_t & _arg)
  {
    this->height = _arg;
    return *this;
  }
  Type & set__width(
    const uint32_t & _arg)
  {
    this->width = _arg;
    return *this;
  }
  Type & set__encoding(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->encoding = _arg;
    return *this;
  }
  Type & set__is_bigendian(
    const uint8_t & _arg)
  {
    this->is_bigendian = _arg;
    return *this;
  }
  Type & set__step(
    const uint32_t & _arg)
  {
    this->step = _arg;
    return *this;
  }
  Type & set__data(
    const std::vector<int32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int32_t>> & _arg)
  {
    this->data = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage_<ContainerAllocator> *;
  using ConstRawPtr =
    const isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage
    std::shared_ptr<isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage
    std::shared_ptr<isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const NitrosBridgeImage_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->height != other.height) {
      return false;
    }
    if (this->width != other.width) {
      return false;
    }
    if (this->encoding != other.encoding) {
      return false;
    }
    if (this->is_bigendian != other.is_bigendian) {
      return false;
    }
    if (this->step != other.step) {
      return false;
    }
    if (this->data != other.data) {
      return false;
    }
    return true;
  }
  bool operator!=(const NitrosBridgeImage_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct NitrosBridgeImage_

// alias to use template instance with default allocator
using NitrosBridgeImage =
  isaac_ros_nitros_bridge_interfaces::msg::NitrosBridgeImage_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace isaac_ros_nitros_bridge_interfaces

#endif  // ISAAC_ROS_NITROS_BRIDGE_INTERFACES__MSG__DETAIL__NITROS_BRIDGE_IMAGE__STRUCT_HPP_
