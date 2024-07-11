// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from go2_interfaces:msg/Go2State.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "go2_interfaces/msg/detail/go2_state__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace go2_interfaces
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void Go2State_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) go2_interfaces::msg::Go2State(_init);
}

void Go2State_fini_function(void * message_memory)
{
  auto typed_message = static_cast<go2_interfaces::msg::Go2State *>(message_memory);
  typed_message->~Go2State();
}

size_t size_function__Go2State__position(const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * get_const_function__Go2State__position(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<float, 3> *>(untyped_member);
  return &member[index];
}

void * get_function__Go2State__position(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<float, 3> *>(untyped_member);
  return &member[index];
}

void fetch_function__Go2State__position(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const float *>(
    get_const_function__Go2State__position(untyped_member, index));
  auto & value = *reinterpret_cast<float *>(untyped_value);
  value = item;
}

void assign_function__Go2State__position(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<float *>(
    get_function__Go2State__position(untyped_member, index));
  const auto & value = *reinterpret_cast<const float *>(untyped_value);
  item = value;
}

size_t size_function__Go2State__velocity(const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * get_const_function__Go2State__velocity(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<float, 3> *>(untyped_member);
  return &member[index];
}

void * get_function__Go2State__velocity(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<float, 3> *>(untyped_member);
  return &member[index];
}

void fetch_function__Go2State__velocity(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const float *>(
    get_const_function__Go2State__velocity(untyped_member, index));
  auto & value = *reinterpret_cast<float *>(untyped_value);
  value = item;
}

void assign_function__Go2State__velocity(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<float *>(
    get_function__Go2State__velocity(untyped_member, index));
  const auto & value = *reinterpret_cast<const float *>(untyped_value);
  item = value;
}

size_t size_function__Go2State__range_obstacle(const void * untyped_member)
{
  (void)untyped_member;
  return 4;
}

const void * get_const_function__Go2State__range_obstacle(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<float, 4> *>(untyped_member);
  return &member[index];
}

void * get_function__Go2State__range_obstacle(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<float, 4> *>(untyped_member);
  return &member[index];
}

void fetch_function__Go2State__range_obstacle(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const float *>(
    get_const_function__Go2State__range_obstacle(untyped_member, index));
  auto & value = *reinterpret_cast<float *>(untyped_value);
  value = item;
}

void assign_function__Go2State__range_obstacle(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<float *>(
    get_function__Go2State__range_obstacle(untyped_member, index));
  const auto & value = *reinterpret_cast<const float *>(untyped_value);
  item = value;
}

size_t size_function__Go2State__foot_force(const void * untyped_member)
{
  (void)untyped_member;
  return 4;
}

const void * get_const_function__Go2State__foot_force(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<int16_t, 4> *>(untyped_member);
  return &member[index];
}

void * get_function__Go2State__foot_force(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<int16_t, 4> *>(untyped_member);
  return &member[index];
}

void fetch_function__Go2State__foot_force(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const int16_t *>(
    get_const_function__Go2State__foot_force(untyped_member, index));
  auto & value = *reinterpret_cast<int16_t *>(untyped_value);
  value = item;
}

void assign_function__Go2State__foot_force(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<int16_t *>(
    get_function__Go2State__foot_force(untyped_member, index));
  const auto & value = *reinterpret_cast<const int16_t *>(untyped_value);
  item = value;
}

size_t size_function__Go2State__foot_position_body(const void * untyped_member)
{
  (void)untyped_member;
  return 12;
}

const void * get_const_function__Go2State__foot_position_body(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<float, 12> *>(untyped_member);
  return &member[index];
}

void * get_function__Go2State__foot_position_body(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<float, 12> *>(untyped_member);
  return &member[index];
}

void fetch_function__Go2State__foot_position_body(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const float *>(
    get_const_function__Go2State__foot_position_body(untyped_member, index));
  auto & value = *reinterpret_cast<float *>(untyped_value);
  value = item;
}

void assign_function__Go2State__foot_position_body(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<float *>(
    get_function__Go2State__foot_position_body(untyped_member, index));
  const auto & value = *reinterpret_cast<const float *>(untyped_value);
  item = value;
}

size_t size_function__Go2State__foot_speed_body(const void * untyped_member)
{
  (void)untyped_member;
  return 12;
}

const void * get_const_function__Go2State__foot_speed_body(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<float, 12> *>(untyped_member);
  return &member[index];
}

void * get_function__Go2State__foot_speed_body(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<float, 12> *>(untyped_member);
  return &member[index];
}

void fetch_function__Go2State__foot_speed_body(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const float *>(
    get_const_function__Go2State__foot_speed_body(untyped_member, index));
  auto & value = *reinterpret_cast<float *>(untyped_value);
  value = item;
}

void assign_function__Go2State__foot_speed_body(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<float *>(
    get_function__Go2State__foot_speed_body(untyped_member, index));
  const auto & value = *reinterpret_cast<const float *>(untyped_value);
  item = value;
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember Go2State_message_member_array[11] = {
  {
    "mode",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(go2_interfaces::msg::Go2State, mode),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "progress",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(go2_interfaces::msg::Go2State, progress),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "gait_type",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(go2_interfaces::msg::Go2State, gait_type),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "foot_raise_height",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(go2_interfaces::msg::Go2State, foot_raise_height),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "position",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(go2_interfaces::msg::Go2State, position),  // bytes offset in struct
    nullptr,  // default value
    size_function__Go2State__position,  // size() function pointer
    get_const_function__Go2State__position,  // get_const(index) function pointer
    get_function__Go2State__position,  // get(index) function pointer
    fetch_function__Go2State__position,  // fetch(index, &value) function pointer
    assign_function__Go2State__position,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "body_height",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(go2_interfaces::msg::Go2State, body_height),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "velocity",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(go2_interfaces::msg::Go2State, velocity),  // bytes offset in struct
    nullptr,  // default value
    size_function__Go2State__velocity,  // size() function pointer
    get_const_function__Go2State__velocity,  // get_const(index) function pointer
    get_function__Go2State__velocity,  // get(index) function pointer
    fetch_function__Go2State__velocity,  // fetch(index, &value) function pointer
    assign_function__Go2State__velocity,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "range_obstacle",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    4,  // array size
    false,  // is upper bound
    offsetof(go2_interfaces::msg::Go2State, range_obstacle),  // bytes offset in struct
    nullptr,  // default value
    size_function__Go2State__range_obstacle,  // size() function pointer
    get_const_function__Go2State__range_obstacle,  // get_const(index) function pointer
    get_function__Go2State__range_obstacle,  // get(index) function pointer
    fetch_function__Go2State__range_obstacle,  // fetch(index, &value) function pointer
    assign_function__Go2State__range_obstacle,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "foot_force",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT16,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    4,  // array size
    false,  // is upper bound
    offsetof(go2_interfaces::msg::Go2State, foot_force),  // bytes offset in struct
    nullptr,  // default value
    size_function__Go2State__foot_force,  // size() function pointer
    get_const_function__Go2State__foot_force,  // get_const(index) function pointer
    get_function__Go2State__foot_force,  // get(index) function pointer
    fetch_function__Go2State__foot_force,  // fetch(index, &value) function pointer
    assign_function__Go2State__foot_force,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "foot_position_body",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    12,  // array size
    false,  // is upper bound
    offsetof(go2_interfaces::msg::Go2State, foot_position_body),  // bytes offset in struct
    nullptr,  // default value
    size_function__Go2State__foot_position_body,  // size() function pointer
    get_const_function__Go2State__foot_position_body,  // get_const(index) function pointer
    get_function__Go2State__foot_position_body,  // get(index) function pointer
    fetch_function__Go2State__foot_position_body,  // fetch(index, &value) function pointer
    assign_function__Go2State__foot_position_body,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "foot_speed_body",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    12,  // array size
    false,  // is upper bound
    offsetof(go2_interfaces::msg::Go2State, foot_speed_body),  // bytes offset in struct
    nullptr,  // default value
    size_function__Go2State__foot_speed_body,  // size() function pointer
    get_const_function__Go2State__foot_speed_body,  // get_const(index) function pointer
    get_function__Go2State__foot_speed_body,  // get(index) function pointer
    fetch_function__Go2State__foot_speed_body,  // fetch(index, &value) function pointer
    assign_function__Go2State__foot_speed_body,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers Go2State_message_members = {
  "go2_interfaces::msg",  // message namespace
  "Go2State",  // message name
  11,  // number of fields
  sizeof(go2_interfaces::msg::Go2State),
  Go2State_message_member_array,  // message members
  Go2State_init_function,  // function to initialize message memory (memory has to be allocated)
  Go2State_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t Go2State_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &Go2State_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace go2_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<go2_interfaces::msg::Go2State>()
{
  return &::go2_interfaces::msg::rosidl_typesupport_introspection_cpp::Go2State_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, go2_interfaces, msg, Go2State)() {
  return &::go2_interfaces::msg::rosidl_typesupport_introspection_cpp::Go2State_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
