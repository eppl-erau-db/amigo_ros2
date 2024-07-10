// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from unitree_api:msg/Response.idl
// generated code does not contain a copyright notice

#ifndef UNITREE_API__MSG__DETAIL__RESPONSE__STRUCT_HPP_
#define UNITREE_API__MSG__DETAIL__RESPONSE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "unitree_api/msg/detail/response_header__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__unitree_api__msg__Response __attribute__((deprecated))
#else
# define DEPRECATED__unitree_api__msg__Response __declspec(deprecated)
#endif

namespace unitree_api
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Response_
{
  using Type = Response_<ContainerAllocator>;

  explicit Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->data = "";
    }
  }

  explicit Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    data(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->data = "";
    }
  }

  // field types and members
  using _header_type =
    unitree_api::msg::ResponseHeader_<ContainerAllocator>;
  _header_type header;
  using _data_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _data_type data;
  using _binary_type =
    std::vector<int8_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int8_t>>;
  _binary_type binary;

  // setters for named parameter idiom
  Type & set__header(
    const unitree_api::msg::ResponseHeader_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__data(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->data = _arg;
    return *this;
  }
  Type & set__binary(
    const std::vector<int8_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int8_t>> & _arg)
  {
    this->binary = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    unitree_api::msg::Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const unitree_api::msg::Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<unitree_api::msg::Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<unitree_api::msg::Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      unitree_api::msg::Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<unitree_api::msg::Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      unitree_api::msg::Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<unitree_api::msg::Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<unitree_api::msg::Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<unitree_api::msg::Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__unitree_api__msg__Response
    std::shared_ptr<unitree_api::msg::Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__unitree_api__msg__Response
    std::shared_ptr<unitree_api::msg::Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Response_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->data != other.data) {
      return false;
    }
    if (this->binary != other.binary) {
      return false;
    }
    return true;
  }
  bool operator!=(const Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Response_

// alias to use template instance with default allocator
using Response =
  unitree_api::msg::Response_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace unitree_api

#endif  // UNITREE_API__MSG__DETAIL__RESPONSE__STRUCT_HPP_
