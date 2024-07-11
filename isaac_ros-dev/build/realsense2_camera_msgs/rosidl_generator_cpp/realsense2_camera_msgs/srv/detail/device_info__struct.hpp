// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from realsense2_camera_msgs:srv/DeviceInfo.idl
// generated code does not contain a copyright notice

#ifndef REALSENSE2_CAMERA_MSGS__SRV__DETAIL__DEVICE_INFO__STRUCT_HPP_
#define REALSENSE2_CAMERA_MSGS__SRV__DETAIL__DEVICE_INFO__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__realsense2_camera_msgs__srv__DeviceInfo_Request __attribute__((deprecated))
#else
# define DEPRECATED__realsense2_camera_msgs__srv__DeviceInfo_Request __declspec(deprecated)
#endif

namespace realsense2_camera_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct DeviceInfo_Request_
{
  using Type = DeviceInfo_Request_<ContainerAllocator>;

  explicit DeviceInfo_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  explicit DeviceInfo_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  // field types and members
  using _structure_needs_at_least_one_member_type =
    uint8_t;
  _structure_needs_at_least_one_member_type structure_needs_at_least_one_member;


  // constant declarations

  // pointer types
  using RawPtr =
    realsense2_camera_msgs::srv::DeviceInfo_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const realsense2_camera_msgs::srv::DeviceInfo_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<realsense2_camera_msgs::srv::DeviceInfo_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<realsense2_camera_msgs::srv::DeviceInfo_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      realsense2_camera_msgs::srv::DeviceInfo_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<realsense2_camera_msgs::srv::DeviceInfo_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      realsense2_camera_msgs::srv::DeviceInfo_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<realsense2_camera_msgs::srv::DeviceInfo_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<realsense2_camera_msgs::srv::DeviceInfo_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<realsense2_camera_msgs::srv::DeviceInfo_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__realsense2_camera_msgs__srv__DeviceInfo_Request
    std::shared_ptr<realsense2_camera_msgs::srv::DeviceInfo_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__realsense2_camera_msgs__srv__DeviceInfo_Request
    std::shared_ptr<realsense2_camera_msgs::srv::DeviceInfo_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const DeviceInfo_Request_ & other) const
  {
    if (this->structure_needs_at_least_one_member != other.structure_needs_at_least_one_member) {
      return false;
    }
    return true;
  }
  bool operator!=(const DeviceInfo_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct DeviceInfo_Request_

// alias to use template instance with default allocator
using DeviceInfo_Request =
  realsense2_camera_msgs::srv::DeviceInfo_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace realsense2_camera_msgs


#ifndef _WIN32
# define DEPRECATED__realsense2_camera_msgs__srv__DeviceInfo_Response __attribute__((deprecated))
#else
# define DEPRECATED__realsense2_camera_msgs__srv__DeviceInfo_Response __declspec(deprecated)
#endif

namespace realsense2_camera_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct DeviceInfo_Response_
{
  using Type = DeviceInfo_Response_<ContainerAllocator>;

  explicit DeviceInfo_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->device_name = "";
      this->serial_number = "";
      this->firmware_version = "";
      this->usb_type_descriptor = "";
      this->firmware_update_id = "";
      this->sensors = "";
    }
  }

  explicit DeviceInfo_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : device_name(_alloc),
    serial_number(_alloc),
    firmware_version(_alloc),
    usb_type_descriptor(_alloc),
    firmware_update_id(_alloc),
    sensors(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->device_name = "";
      this->serial_number = "";
      this->firmware_version = "";
      this->usb_type_descriptor = "";
      this->firmware_update_id = "";
      this->sensors = "";
    }
  }

  // field types and members
  using _device_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _device_name_type device_name;
  using _serial_number_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _serial_number_type serial_number;
  using _firmware_version_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _firmware_version_type firmware_version;
  using _usb_type_descriptor_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _usb_type_descriptor_type usb_type_descriptor;
  using _firmware_update_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _firmware_update_id_type firmware_update_id;
  using _sensors_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _sensors_type sensors;

  // setters for named parameter idiom
  Type & set__device_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->device_name = _arg;
    return *this;
  }
  Type & set__serial_number(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->serial_number = _arg;
    return *this;
  }
  Type & set__firmware_version(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->firmware_version = _arg;
    return *this;
  }
  Type & set__usb_type_descriptor(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->usb_type_descriptor = _arg;
    return *this;
  }
  Type & set__firmware_update_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->firmware_update_id = _arg;
    return *this;
  }
  Type & set__sensors(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->sensors = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    realsense2_camera_msgs::srv::DeviceInfo_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const realsense2_camera_msgs::srv::DeviceInfo_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<realsense2_camera_msgs::srv::DeviceInfo_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<realsense2_camera_msgs::srv::DeviceInfo_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      realsense2_camera_msgs::srv::DeviceInfo_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<realsense2_camera_msgs::srv::DeviceInfo_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      realsense2_camera_msgs::srv::DeviceInfo_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<realsense2_camera_msgs::srv::DeviceInfo_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<realsense2_camera_msgs::srv::DeviceInfo_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<realsense2_camera_msgs::srv::DeviceInfo_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__realsense2_camera_msgs__srv__DeviceInfo_Response
    std::shared_ptr<realsense2_camera_msgs::srv::DeviceInfo_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__realsense2_camera_msgs__srv__DeviceInfo_Response
    std::shared_ptr<realsense2_camera_msgs::srv::DeviceInfo_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const DeviceInfo_Response_ & other) const
  {
    if (this->device_name != other.device_name) {
      return false;
    }
    if (this->serial_number != other.serial_number) {
      return false;
    }
    if (this->firmware_version != other.firmware_version) {
      return false;
    }
    if (this->usb_type_descriptor != other.usb_type_descriptor) {
      return false;
    }
    if (this->firmware_update_id != other.firmware_update_id) {
      return false;
    }
    if (this->sensors != other.sensors) {
      return false;
    }
    return true;
  }
  bool operator!=(const DeviceInfo_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct DeviceInfo_Response_

// alias to use template instance with default allocator
using DeviceInfo_Response =
  realsense2_camera_msgs::srv::DeviceInfo_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace realsense2_camera_msgs

namespace realsense2_camera_msgs
{

namespace srv
{

struct DeviceInfo
{
  using Request = realsense2_camera_msgs::srv::DeviceInfo_Request;
  using Response = realsense2_camera_msgs::srv::DeviceInfo_Response;
};

}  // namespace srv

}  // namespace realsense2_camera_msgs

#endif  // REALSENSE2_CAMERA_MSGS__SRV__DETAIL__DEVICE_INFO__STRUCT_HPP_
