// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from nvblox_msgs:msg/MeshBlock.idl
// generated code does not contain a copyright notice

#ifndef NVBLOX_MSGS__MSG__DETAIL__MESH_BLOCK__STRUCT_HPP_
#define NVBLOX_MSGS__MSG__DETAIL__MESH_BLOCK__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'vertices'
// Member 'normals'
#include "geometry_msgs/msg/detail/point32__struct.hpp"
// Member 'colors'
#include "std_msgs/msg/detail/color_rgba__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__nvblox_msgs__msg__MeshBlock __attribute__((deprecated))
#else
# define DEPRECATED__nvblox_msgs__msg__MeshBlock __declspec(deprecated)
#endif

namespace nvblox_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct MeshBlock_
{
  using Type = MeshBlock_<ContainerAllocator>;

  explicit MeshBlock_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit MeshBlock_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _vertices_type =
    std::vector<geometry_msgs::msg::Point32_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<geometry_msgs::msg::Point32_<ContainerAllocator>>>;
  _vertices_type vertices;
  using _normals_type =
    std::vector<geometry_msgs::msg::Point32_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<geometry_msgs::msg::Point32_<ContainerAllocator>>>;
  _normals_type normals;
  using _colors_type =
    std::vector<std_msgs::msg::ColorRGBA_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std_msgs::msg::ColorRGBA_<ContainerAllocator>>>;
  _colors_type colors;
  using _triangles_type =
    std::vector<int32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int32_t>>;
  _triangles_type triangles;

  // setters for named parameter idiom
  Type & set__vertices(
    const std::vector<geometry_msgs::msg::Point32_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<geometry_msgs::msg::Point32_<ContainerAllocator>>> & _arg)
  {
    this->vertices = _arg;
    return *this;
  }
  Type & set__normals(
    const std::vector<geometry_msgs::msg::Point32_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<geometry_msgs::msg::Point32_<ContainerAllocator>>> & _arg)
  {
    this->normals = _arg;
    return *this;
  }
  Type & set__colors(
    const std::vector<std_msgs::msg::ColorRGBA_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std_msgs::msg::ColorRGBA_<ContainerAllocator>>> & _arg)
  {
    this->colors = _arg;
    return *this;
  }
  Type & set__triangles(
    const std::vector<int32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int32_t>> & _arg)
  {
    this->triangles = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    nvblox_msgs::msg::MeshBlock_<ContainerAllocator> *;
  using ConstRawPtr =
    const nvblox_msgs::msg::MeshBlock_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<nvblox_msgs::msg::MeshBlock_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<nvblox_msgs::msg::MeshBlock_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      nvblox_msgs::msg::MeshBlock_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<nvblox_msgs::msg::MeshBlock_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      nvblox_msgs::msg::MeshBlock_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<nvblox_msgs::msg::MeshBlock_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<nvblox_msgs::msg::MeshBlock_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<nvblox_msgs::msg::MeshBlock_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__nvblox_msgs__msg__MeshBlock
    std::shared_ptr<nvblox_msgs::msg::MeshBlock_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__nvblox_msgs__msg__MeshBlock
    std::shared_ptr<nvblox_msgs::msg::MeshBlock_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MeshBlock_ & other) const
  {
    if (this->vertices != other.vertices) {
      return false;
    }
    if (this->normals != other.normals) {
      return false;
    }
    if (this->colors != other.colors) {
      return false;
    }
    if (this->triangles != other.triangles) {
      return false;
    }
    return true;
  }
  bool operator!=(const MeshBlock_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MeshBlock_

// alias to use template instance with default allocator
using MeshBlock =
  nvblox_msgs::msg::MeshBlock_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace nvblox_msgs

#endif  // NVBLOX_MSGS__MSG__DETAIL__MESH_BLOCK__STRUCT_HPP_
