// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from isaac_ros_bi3d_interfaces:msg/Bi3DInferenceParametersArray.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_BI3D_INTERFACES__MSG__DETAIL__BI3_D_INFERENCE_PARAMETERS_ARRAY__STRUCT_HPP_
#define ISAAC_ROS_BI3D_INTERFACES__MSG__DETAIL__BI3_D_INFERENCE_PARAMETERS_ARRAY__STRUCT_HPP_

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
# define DEPRECATED__isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray __attribute__((deprecated))
#else
# define DEPRECATED__isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray __declspec(deprecated)
#endif

namespace isaac_ros_bi3d_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Bi3DInferenceParametersArray_
{
  using Type = Bi3DInferenceParametersArray_<ContainerAllocator>;

  explicit Bi3DInferenceParametersArray_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    (void)_init;
  }

  explicit Bi3DInferenceParametersArray_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _disparity_values_type =
    std::vector<int32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int32_t>>;
  _disparity_values_type disparity_values;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__disparity_values(
    const std::vector<int32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int32_t>> & _arg)
  {
    this->disparity_values = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    isaac_ros_bi3d_interfaces::msg::Bi3DInferenceParametersArray_<ContainerAllocator> *;
  using ConstRawPtr =
    const isaac_ros_bi3d_interfaces::msg::Bi3DInferenceParametersArray_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<isaac_ros_bi3d_interfaces::msg::Bi3DInferenceParametersArray_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<isaac_ros_bi3d_interfaces::msg::Bi3DInferenceParametersArray_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      isaac_ros_bi3d_interfaces::msg::Bi3DInferenceParametersArray_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<isaac_ros_bi3d_interfaces::msg::Bi3DInferenceParametersArray_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      isaac_ros_bi3d_interfaces::msg::Bi3DInferenceParametersArray_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<isaac_ros_bi3d_interfaces::msg::Bi3DInferenceParametersArray_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<isaac_ros_bi3d_interfaces::msg::Bi3DInferenceParametersArray_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<isaac_ros_bi3d_interfaces::msg::Bi3DInferenceParametersArray_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray
    std::shared_ptr<isaac_ros_bi3d_interfaces::msg::Bi3DInferenceParametersArray_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray
    std::shared_ptr<isaac_ros_bi3d_interfaces::msg::Bi3DInferenceParametersArray_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Bi3DInferenceParametersArray_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->disparity_values != other.disparity_values) {
      return false;
    }
    return true;
  }
  bool operator!=(const Bi3DInferenceParametersArray_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Bi3DInferenceParametersArray_

// alias to use template instance with default allocator
using Bi3DInferenceParametersArray =
  isaac_ros_bi3d_interfaces::msg::Bi3DInferenceParametersArray_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace isaac_ros_bi3d_interfaces

#endif  // ISAAC_ROS_BI3D_INTERFACES__MSG__DETAIL__BI3_D_INFERENCE_PARAMETERS_ARRAY__STRUCT_HPP_
