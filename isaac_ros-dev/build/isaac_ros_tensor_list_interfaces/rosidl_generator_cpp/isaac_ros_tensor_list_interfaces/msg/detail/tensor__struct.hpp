// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from isaac_ros_tensor_list_interfaces:msg/Tensor.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR__STRUCT_HPP_
#define ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'shape'
#include "isaac_ros_tensor_list_interfaces/msg/detail/tensor_shape__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__isaac_ros_tensor_list_interfaces__msg__Tensor __attribute__((deprecated))
#else
# define DEPRECATED__isaac_ros_tensor_list_interfaces__msg__Tensor __declspec(deprecated)
#endif

namespace isaac_ros_tensor_list_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Tensor_
{
  using Type = Tensor_<ContainerAllocator>;

  explicit Tensor_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : shape(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->name = "";
      this->data_type = 0l;
    }
  }

  explicit Tensor_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : name(_alloc),
    shape(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->name = "";
      this->data_type = 0l;
    }
  }

  // field types and members
  using _name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _name_type name;
  using _shape_type =
    isaac_ros_tensor_list_interfaces::msg::TensorShape_<ContainerAllocator>;
  _shape_type shape;
  using _data_type_type =
    int32_t;
  _data_type_type data_type;
  using _strides_type =
    std::vector<uint64_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint64_t>>;
  _strides_type strides;
  using _data_type =
    std::vector<uint8_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint8_t>>;
  _data_type data;

  // setters for named parameter idiom
  Type & set__name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->name = _arg;
    return *this;
  }
  Type & set__shape(
    const isaac_ros_tensor_list_interfaces::msg::TensorShape_<ContainerAllocator> & _arg)
  {
    this->shape = _arg;
    return *this;
  }
  Type & set__data_type(
    const int32_t & _arg)
  {
    this->data_type = _arg;
    return *this;
  }
  Type & set__strides(
    const std::vector<uint64_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint64_t>> & _arg)
  {
    this->strides = _arg;
    return *this;
  }
  Type & set__data(
    const std::vector<uint8_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint8_t>> & _arg)
  {
    this->data = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    isaac_ros_tensor_list_interfaces::msg::Tensor_<ContainerAllocator> *;
  using ConstRawPtr =
    const isaac_ros_tensor_list_interfaces::msg::Tensor_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<isaac_ros_tensor_list_interfaces::msg::Tensor_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<isaac_ros_tensor_list_interfaces::msg::Tensor_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      isaac_ros_tensor_list_interfaces::msg::Tensor_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<isaac_ros_tensor_list_interfaces::msg::Tensor_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      isaac_ros_tensor_list_interfaces::msg::Tensor_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<isaac_ros_tensor_list_interfaces::msg::Tensor_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<isaac_ros_tensor_list_interfaces::msg::Tensor_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<isaac_ros_tensor_list_interfaces::msg::Tensor_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__isaac_ros_tensor_list_interfaces__msg__Tensor
    std::shared_ptr<isaac_ros_tensor_list_interfaces::msg::Tensor_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__isaac_ros_tensor_list_interfaces__msg__Tensor
    std::shared_ptr<isaac_ros_tensor_list_interfaces::msg::Tensor_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Tensor_ & other) const
  {
    if (this->name != other.name) {
      return false;
    }
    if (this->shape != other.shape) {
      return false;
    }
    if (this->data_type != other.data_type) {
      return false;
    }
    if (this->strides != other.strides) {
      return false;
    }
    if (this->data != other.data) {
      return false;
    }
    return true;
  }
  bool operator!=(const Tensor_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Tensor_

// alias to use template instance with default allocator
using Tensor =
  isaac_ros_tensor_list_interfaces::msg::Tensor_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace isaac_ros_tensor_list_interfaces

#endif  // ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR__STRUCT_HPP_
