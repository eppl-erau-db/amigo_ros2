// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from nvblox_msgs:msg/Mesh.idl
// generated code does not contain a copyright notice

#ifndef NVBLOX_MSGS__MSG__DETAIL__MESH__STRUCT_HPP_
#define NVBLOX_MSGS__MSG__DETAIL__MESH__STRUCT_HPP_

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
// Member 'block_indices'
#include "nvblox_msgs/msg/detail/index3_d__struct.hpp"
// Member 'blocks'
#include "nvblox_msgs/msg/detail/mesh_block__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__nvblox_msgs__msg__Mesh __attribute__((deprecated))
#else
# define DEPRECATED__nvblox_msgs__msg__Mesh __declspec(deprecated)
#endif

namespace nvblox_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Mesh_
{
  using Type = Mesh_<ContainerAllocator>;

  explicit Mesh_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->block_size = 0.0f;
      this->clear = false;
    }
  }

  explicit Mesh_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->block_size = 0.0f;
      this->clear = false;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _block_size_type =
    float;
  _block_size_type block_size;
  using _block_indices_type =
    std::vector<nvblox_msgs::msg::Index3D_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<nvblox_msgs::msg::Index3D_<ContainerAllocator>>>;
  _block_indices_type block_indices;
  using _blocks_type =
    std::vector<nvblox_msgs::msg::MeshBlock_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<nvblox_msgs::msg::MeshBlock_<ContainerAllocator>>>;
  _blocks_type blocks;
  using _clear_type =
    bool;
  _clear_type clear;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__block_size(
    const float & _arg)
  {
    this->block_size = _arg;
    return *this;
  }
  Type & set__block_indices(
    const std::vector<nvblox_msgs::msg::Index3D_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<nvblox_msgs::msg::Index3D_<ContainerAllocator>>> & _arg)
  {
    this->block_indices = _arg;
    return *this;
  }
  Type & set__blocks(
    const std::vector<nvblox_msgs::msg::MeshBlock_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<nvblox_msgs::msg::MeshBlock_<ContainerAllocator>>> & _arg)
  {
    this->blocks = _arg;
    return *this;
  }
  Type & set__clear(
    const bool & _arg)
  {
    this->clear = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    nvblox_msgs::msg::Mesh_<ContainerAllocator> *;
  using ConstRawPtr =
    const nvblox_msgs::msg::Mesh_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<nvblox_msgs::msg::Mesh_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<nvblox_msgs::msg::Mesh_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      nvblox_msgs::msg::Mesh_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<nvblox_msgs::msg::Mesh_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      nvblox_msgs::msg::Mesh_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<nvblox_msgs::msg::Mesh_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<nvblox_msgs::msg::Mesh_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<nvblox_msgs::msg::Mesh_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__nvblox_msgs__msg__Mesh
    std::shared_ptr<nvblox_msgs::msg::Mesh_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__nvblox_msgs__msg__Mesh
    std::shared_ptr<nvblox_msgs::msg::Mesh_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Mesh_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->block_size != other.block_size) {
      return false;
    }
    if (this->block_indices != other.block_indices) {
      return false;
    }
    if (this->blocks != other.blocks) {
      return false;
    }
    if (this->clear != other.clear) {
      return false;
    }
    return true;
  }
  bool operator!=(const Mesh_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Mesh_

// alias to use template instance with default allocator
using Mesh =
  nvblox_msgs::msg::Mesh_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace nvblox_msgs

#endif  // NVBLOX_MSGS__MSG__DETAIL__MESH__STRUCT_HPP_
