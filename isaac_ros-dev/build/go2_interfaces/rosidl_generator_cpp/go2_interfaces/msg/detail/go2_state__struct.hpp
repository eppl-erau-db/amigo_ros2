// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from go2_interfaces:msg/Go2State.idl
// generated code does not contain a copyright notice

#ifndef GO2_INTERFACES__MSG__DETAIL__GO2_STATE__STRUCT_HPP_
#define GO2_INTERFACES__MSG__DETAIL__GO2_STATE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__go2_interfaces__msg__Go2State __attribute__((deprecated))
#else
# define DEPRECATED__go2_interfaces__msg__Go2State __declspec(deprecated)
#endif

namespace go2_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Go2State_
{
  using Type = Go2State_<ContainerAllocator>;

  explicit Go2State_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->mode = 0;
      this->progress = 0l;
      this->gait_type = 0;
      this->foot_raise_height = 0.0f;
      std::fill<typename std::array<float, 3>::iterator, float>(this->position.begin(), this->position.end(), 0.0f);
      this->body_height = 0.0f;
      std::fill<typename std::array<float, 3>::iterator, float>(this->velocity.begin(), this->velocity.end(), 0.0f);
      std::fill<typename std::array<float, 4>::iterator, float>(this->range_obstacle.begin(), this->range_obstacle.end(), 0.0f);
      std::fill<typename std::array<int16_t, 4>::iterator, int16_t>(this->foot_force.begin(), this->foot_force.end(), 0);
      std::fill<typename std::array<float, 12>::iterator, float>(this->foot_position_body.begin(), this->foot_position_body.end(), 0.0f);
      std::fill<typename std::array<float, 12>::iterator, float>(this->foot_speed_body.begin(), this->foot_speed_body.end(), 0.0f);
    }
  }

  explicit Go2State_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : position(_alloc),
    velocity(_alloc),
    range_obstacle(_alloc),
    foot_force(_alloc),
    foot_position_body(_alloc),
    foot_speed_body(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->mode = 0;
      this->progress = 0l;
      this->gait_type = 0;
      this->foot_raise_height = 0.0f;
      std::fill<typename std::array<float, 3>::iterator, float>(this->position.begin(), this->position.end(), 0.0f);
      this->body_height = 0.0f;
      std::fill<typename std::array<float, 3>::iterator, float>(this->velocity.begin(), this->velocity.end(), 0.0f);
      std::fill<typename std::array<float, 4>::iterator, float>(this->range_obstacle.begin(), this->range_obstacle.end(), 0.0f);
      std::fill<typename std::array<int16_t, 4>::iterator, int16_t>(this->foot_force.begin(), this->foot_force.end(), 0);
      std::fill<typename std::array<float, 12>::iterator, float>(this->foot_position_body.begin(), this->foot_position_body.end(), 0.0f);
      std::fill<typename std::array<float, 12>::iterator, float>(this->foot_speed_body.begin(), this->foot_speed_body.end(), 0.0f);
    }
  }

  // field types and members
  using _mode_type =
    uint8_t;
  _mode_type mode;
  using _progress_type =
    int32_t;
  _progress_type progress;
  using _gait_type_type =
    uint8_t;
  _gait_type_type gait_type;
  using _foot_raise_height_type =
    float;
  _foot_raise_height_type foot_raise_height;
  using _position_type =
    std::array<float, 3>;
  _position_type position;
  using _body_height_type =
    float;
  _body_height_type body_height;
  using _velocity_type =
    std::array<float, 3>;
  _velocity_type velocity;
  using _range_obstacle_type =
    std::array<float, 4>;
  _range_obstacle_type range_obstacle;
  using _foot_force_type =
    std::array<int16_t, 4>;
  _foot_force_type foot_force;
  using _foot_position_body_type =
    std::array<float, 12>;
  _foot_position_body_type foot_position_body;
  using _foot_speed_body_type =
    std::array<float, 12>;
  _foot_speed_body_type foot_speed_body;

  // setters for named parameter idiom
  Type & set__mode(
    const uint8_t & _arg)
  {
    this->mode = _arg;
    return *this;
  }
  Type & set__progress(
    const int32_t & _arg)
  {
    this->progress = _arg;
    return *this;
  }
  Type & set__gait_type(
    const uint8_t & _arg)
  {
    this->gait_type = _arg;
    return *this;
  }
  Type & set__foot_raise_height(
    const float & _arg)
  {
    this->foot_raise_height = _arg;
    return *this;
  }
  Type & set__position(
    const std::array<float, 3> & _arg)
  {
    this->position = _arg;
    return *this;
  }
  Type & set__body_height(
    const float & _arg)
  {
    this->body_height = _arg;
    return *this;
  }
  Type & set__velocity(
    const std::array<float, 3> & _arg)
  {
    this->velocity = _arg;
    return *this;
  }
  Type & set__range_obstacle(
    const std::array<float, 4> & _arg)
  {
    this->range_obstacle = _arg;
    return *this;
  }
  Type & set__foot_force(
    const std::array<int16_t, 4> & _arg)
  {
    this->foot_force = _arg;
    return *this;
  }
  Type & set__foot_position_body(
    const std::array<float, 12> & _arg)
  {
    this->foot_position_body = _arg;
    return *this;
  }
  Type & set__foot_speed_body(
    const std::array<float, 12> & _arg)
  {
    this->foot_speed_body = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    go2_interfaces::msg::Go2State_<ContainerAllocator> *;
  using ConstRawPtr =
    const go2_interfaces::msg::Go2State_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<go2_interfaces::msg::Go2State_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<go2_interfaces::msg::Go2State_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      go2_interfaces::msg::Go2State_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<go2_interfaces::msg::Go2State_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      go2_interfaces::msg::Go2State_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<go2_interfaces::msg::Go2State_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<go2_interfaces::msg::Go2State_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<go2_interfaces::msg::Go2State_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__go2_interfaces__msg__Go2State
    std::shared_ptr<go2_interfaces::msg::Go2State_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__go2_interfaces__msg__Go2State
    std::shared_ptr<go2_interfaces::msg::Go2State_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Go2State_ & other) const
  {
    if (this->mode != other.mode) {
      return false;
    }
    if (this->progress != other.progress) {
      return false;
    }
    if (this->gait_type != other.gait_type) {
      return false;
    }
    if (this->foot_raise_height != other.foot_raise_height) {
      return false;
    }
    if (this->position != other.position) {
      return false;
    }
    if (this->body_height != other.body_height) {
      return false;
    }
    if (this->velocity != other.velocity) {
      return false;
    }
    if (this->range_obstacle != other.range_obstacle) {
      return false;
    }
    if (this->foot_force != other.foot_force) {
      return false;
    }
    if (this->foot_position_body != other.foot_position_body) {
      return false;
    }
    if (this->foot_speed_body != other.foot_speed_body) {
      return false;
    }
    return true;
  }
  bool operator!=(const Go2State_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Go2State_

// alias to use template instance with default allocator
using Go2State =
  go2_interfaces::msg::Go2State_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace go2_interfaces

#endif  // GO2_INTERFACES__MSG__DETAIL__GO2_STATE__STRUCT_HPP_
