// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from go2_interfaces:msg/Go2Cmd.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "go2_interfaces/msg/detail/go2_cmd__struct.hpp"
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

void Go2Cmd_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) go2_interfaces::msg::Go2Cmd(_init);
}

void Go2Cmd_fini_function(void * message_memory)
{
  auto typed_message = static_cast<go2_interfaces::msg::Go2Cmd *>(message_memory);
  typed_message->~Go2Cmd();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember Go2Cmd_message_member_array[1] = {
  {
    "cmd",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT16,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(go2_interfaces::msg::Go2Cmd, cmd),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers Go2Cmd_message_members = {
  "go2_interfaces::msg",  // message namespace
  "Go2Cmd",  // message name
  1,  // number of fields
  sizeof(go2_interfaces::msg::Go2Cmd),
  Go2Cmd_message_member_array,  // message members
  Go2Cmd_init_function,  // function to initialize message memory (memory has to be allocated)
  Go2Cmd_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t Go2Cmd_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &Go2Cmd_message_members,
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
get_message_type_support_handle<go2_interfaces::msg::Go2Cmd>()
{
  return &::go2_interfaces::msg::rosidl_typesupport_introspection_cpp::Go2Cmd_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, go2_interfaces, msg, Go2Cmd)() {
  return &::go2_interfaces::msg::rosidl_typesupport_introspection_cpp::Go2Cmd_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
