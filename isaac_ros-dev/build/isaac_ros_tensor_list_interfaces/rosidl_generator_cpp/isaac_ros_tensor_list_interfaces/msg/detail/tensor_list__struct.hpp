// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from isaac_ros_tensor_list_interfaces:msg/TensorList.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR_LIST__STRUCT_HPP_
#define ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR_LIST__STRUCT_HPP_

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
// Member 'tensors'
#include "isaac_ros_tensor_list_interfaces/msg/detail/tensor__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__isaac_ros_tensor_list_interfaces__msg__TensorList __attribute__((deprecated))
#else
# define DEPRECATED__isaac_ros_tensor_list_interfaces__msg__TensorList __declspec(deprecated)
#endif

namespace isaac_ros_tensor_list_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct TensorList_
{
  using Type = TensorList_<ContainerAllocator>;

  explicit TensorList_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    (void)_init;
  }

  explicit TensorList_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _tensors_type =
    std::vector<isaac_ros_tensor_list_interfaces::msg::Tensor_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<isaac_ros_tensor_list_interfaces::msg::Tensor_<ContainerAllocator>>>;
  _tensors_type tensors;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__tensors(
    const std::vector<isaac_ros_tensor_list_interfaces::msg::Tensor_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<isaac_ros_tensor_list_interfaces::msg::Tensor_<ContainerAllocator>>> & _arg)
  {
    this->tensors = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    isaac_ros_tensor_list_interfaces::msg::TensorList_<ContainerAllocator> *;
  using ConstRawPtr =
    const isaac_ros_tensor_list_interfaces::msg::TensorList_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<isaac_ros_tensor_list_interfaces::msg::TensorList_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<isaac_ros_tensor_list_interfaces::msg::TensorList_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      isaac_ros_tensor_list_interfaces::msg::TensorList_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<isaac_ros_tensor_list_interfaces::msg::TensorList_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      isaac_ros_tensor_list_interfaces::msg::TensorList_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<isaac_ros_tensor_list_interfaces::msg::TensorList_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<isaac_ros_tensor_list_interfaces::msg::TensorList_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<isaac_ros_tensor_list_interfaces::msg::TensorList_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__isaac_ros_tensor_list_interfaces__msg__TensorList
    std::shared_ptr<isaac_ros_tensor_list_interfaces::msg::TensorList_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__isaac_ros_tensor_list_interfaces__msg__TensorList
    std::shared_ptr<isaac_ros_tensor_list_interfaces::msg::TensorList_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const TensorList_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->tensors != other.tensors) {
      return false;
    }
    return true;
  }
  bool operator!=(const TensorList_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct TensorList_

// alias to use template instance with default allocator
using TensorList =
  isaac_ros_tensor_list_interfaces::msg::TensorList_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace isaac_ros_tensor_list_interfaces

#endif  // ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR_LIST__STRUCT_HPP_
