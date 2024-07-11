// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from nvblox_msgs:srv/EsdfAndGradients.idl
// generated code does not contain a copyright notice

#ifndef NVBLOX_MSGS__SRV__DETAIL__ESDF_AND_GRADIENTS__STRUCT_HPP_
#define NVBLOX_MSGS__SRV__DETAIL__ESDF_AND_GRADIENTS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'aabb_min_m'
#include "geometry_msgs/msg/detail/point__struct.hpp"
// Member 'aabb_size_m'
#include "geometry_msgs/msg/detail/vector3__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__nvblox_msgs__srv__EsdfAndGradients_Request __attribute__((deprecated))
#else
# define DEPRECATED__nvblox_msgs__srv__EsdfAndGradients_Request __declspec(deprecated)
#endif

namespace nvblox_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct EsdfAndGradients_Request_
{
  using Type = EsdfAndGradients_Request_<ContainerAllocator>;

  explicit EsdfAndGradients_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : aabb_min_m(_init),
    aabb_size_m(_init)
  {
    (void)_init;
  }

  explicit EsdfAndGradients_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : aabb_min_m(_alloc, _init),
    aabb_size_m(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _aabb_min_m_type =
    geometry_msgs::msg::Point_<ContainerAllocator>;
  _aabb_min_m_type aabb_min_m;
  using _aabb_size_m_type =
    geometry_msgs::msg::Vector3_<ContainerAllocator>;
  _aabb_size_m_type aabb_size_m;

  // setters for named parameter idiom
  Type & set__aabb_min_m(
    const geometry_msgs::msg::Point_<ContainerAllocator> & _arg)
  {
    this->aabb_min_m = _arg;
    return *this;
  }
  Type & set__aabb_size_m(
    const geometry_msgs::msg::Vector3_<ContainerAllocator> & _arg)
  {
    this->aabb_size_m = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    nvblox_msgs::srv::EsdfAndGradients_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const nvblox_msgs::srv::EsdfAndGradients_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<nvblox_msgs::srv::EsdfAndGradients_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<nvblox_msgs::srv::EsdfAndGradients_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      nvblox_msgs::srv::EsdfAndGradients_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<nvblox_msgs::srv::EsdfAndGradients_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      nvblox_msgs::srv::EsdfAndGradients_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<nvblox_msgs::srv::EsdfAndGradients_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<nvblox_msgs::srv::EsdfAndGradients_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<nvblox_msgs::srv::EsdfAndGradients_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__nvblox_msgs__srv__EsdfAndGradients_Request
    std::shared_ptr<nvblox_msgs::srv::EsdfAndGradients_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__nvblox_msgs__srv__EsdfAndGradients_Request
    std::shared_ptr<nvblox_msgs::srv::EsdfAndGradients_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const EsdfAndGradients_Request_ & other) const
  {
    if (this->aabb_min_m != other.aabb_min_m) {
      return false;
    }
    if (this->aabb_size_m != other.aabb_size_m) {
      return false;
    }
    return true;
  }
  bool operator!=(const EsdfAndGradients_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct EsdfAndGradients_Request_

// alias to use template instance with default allocator
using EsdfAndGradients_Request =
  nvblox_msgs::srv::EsdfAndGradients_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace nvblox_msgs


// Include directives for member types
// Member 'voxel_size'
#include "std_msgs/msg/detail/float32__struct.hpp"
// Member 'esdf_and_gradients'
#include "std_msgs/msg/detail/float32_multi_array__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__nvblox_msgs__srv__EsdfAndGradients_Response __attribute__((deprecated))
#else
# define DEPRECATED__nvblox_msgs__srv__EsdfAndGradients_Response __declspec(deprecated)
#endif

namespace nvblox_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct EsdfAndGradients_Response_
{
  using Type = EsdfAndGradients_Response_<ContainerAllocator>;

  explicit EsdfAndGradients_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : voxel_size(_init),
    esdf_and_gradients(_init)
  {
    (void)_init;
  }

  explicit EsdfAndGradients_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : voxel_size(_alloc, _init),
    esdf_and_gradients(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _voxel_size_type =
    std_msgs::msg::Float32_<ContainerAllocator>;
  _voxel_size_type voxel_size;
  using _esdf_and_gradients_type =
    std_msgs::msg::Float32MultiArray_<ContainerAllocator>;
  _esdf_and_gradients_type esdf_and_gradients;

  // setters for named parameter idiom
  Type & set__voxel_size(
    const std_msgs::msg::Float32_<ContainerAllocator> & _arg)
  {
    this->voxel_size = _arg;
    return *this;
  }
  Type & set__esdf_and_gradients(
    const std_msgs::msg::Float32MultiArray_<ContainerAllocator> & _arg)
  {
    this->esdf_and_gradients = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    nvblox_msgs::srv::EsdfAndGradients_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const nvblox_msgs::srv::EsdfAndGradients_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<nvblox_msgs::srv::EsdfAndGradients_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<nvblox_msgs::srv::EsdfAndGradients_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      nvblox_msgs::srv::EsdfAndGradients_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<nvblox_msgs::srv::EsdfAndGradients_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      nvblox_msgs::srv::EsdfAndGradients_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<nvblox_msgs::srv::EsdfAndGradients_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<nvblox_msgs::srv::EsdfAndGradients_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<nvblox_msgs::srv::EsdfAndGradients_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__nvblox_msgs__srv__EsdfAndGradients_Response
    std::shared_ptr<nvblox_msgs::srv::EsdfAndGradients_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__nvblox_msgs__srv__EsdfAndGradients_Response
    std::shared_ptr<nvblox_msgs::srv::EsdfAndGradients_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const EsdfAndGradients_Response_ & other) const
  {
    if (this->voxel_size != other.voxel_size) {
      return false;
    }
    if (this->esdf_and_gradients != other.esdf_and_gradients) {
      return false;
    }
    return true;
  }
  bool operator!=(const EsdfAndGradients_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct EsdfAndGradients_Response_

// alias to use template instance with default allocator
using EsdfAndGradients_Response =
  nvblox_msgs::srv::EsdfAndGradients_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace nvblox_msgs

namespace nvblox_msgs
{

namespace srv
{

struct EsdfAndGradients
{
  using Request = nvblox_msgs::srv::EsdfAndGradients_Request;
  using Response = nvblox_msgs::srv::EsdfAndGradients_Response;
};

}  // namespace srv

}  // namespace nvblox_msgs

#endif  // NVBLOX_MSGS__SRV__DETAIL__ESDF_AND_GRADIENTS__STRUCT_HPP_
