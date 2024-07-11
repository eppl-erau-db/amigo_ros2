// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from isaac_ros_tensor_list_interfaces:msg/TensorShape.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR_SHAPE__STRUCT_HPP_
#define ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR_SHAPE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__isaac_ros_tensor_list_interfaces__msg__TensorShape __attribute__((deprecated))
#else
# define DEPRECATED__isaac_ros_tensor_list_interfaces__msg__TensorShape __declspec(deprecated)
#endif

namespace isaac_ros_tensor_list_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct TensorShape_
{
  using Type = TensorShape_<ContainerAllocator>;

  explicit TensorShape_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->rank = 0;
    }
  }

  explicit TensorShape_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->rank = 0;
    }
  }

  // field types and members
  using _rank_type =
    uint8_t;
  _rank_type rank;
  using _dims_type =
    std::vector<uint32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint32_t>>;
  _dims_type dims;

  // setters for named parameter idiom
  Type & set__rank(
    const uint8_t & _arg)
  {
    this->rank = _arg;
    return *this;
  }
  Type & set__dims(
    const std::vector<uint32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint32_t>> & _arg)
  {
    this->dims = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    isaac_ros_tensor_list_interfaces::msg::TensorShape_<ContainerAllocator> *;
  using ConstRawPtr =
    const isaac_ros_tensor_list_interfaces::msg::TensorShape_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<isaac_ros_tensor_list_interfaces::msg::TensorShape_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<isaac_ros_tensor_list_interfaces::msg::TensorShape_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      isaac_ros_tensor_list_interfaces::msg::TensorShape_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<isaac_ros_tensor_list_interfaces::msg::TensorShape_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      isaac_ros_tensor_list_interfaces::msg::TensorShape_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<isaac_ros_tensor_list_interfaces::msg::TensorShape_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<isaac_ros_tensor_list_interfaces::msg::TensorShape_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<isaac_ros_tensor_list_interfaces::msg::TensorShape_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__isaac_ros_tensor_list_interfaces__msg__TensorShape
    std::shared_ptr<isaac_ros_tensor_list_interfaces::msg::TensorShape_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__isaac_ros_tensor_list_interfaces__msg__TensorShape
    std::shared_ptr<isaac_ros_tensor_list_interfaces::msg::TensorShape_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const TensorShape_ & other) const
  {
    if (this->rank != other.rank) {
      return false;
    }
    if (this->dims != other.dims) {
      return false;
    }
    return true;
  }
  bool operator!=(const TensorShape_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct TensorShape_

// alias to use template instance with default allocator
using TensorShape =
  isaac_ros_tensor_list_interfaces::msg::TensorShape_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace isaac_ros_tensor_list_interfaces

#endif  // ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR_SHAPE__STRUCT_HPP_
