// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from unitree_go:msg/InterfaceConfig.idl
// generated code does not contain a copyright notice
#include "unitree_go/msg/detail/interface_config__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "unitree_go/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "unitree_go/msg/detail/interface_config__struct.h"
#include "unitree_go/msg/detail/interface_config__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif


// forward declare type support functions


using _InterfaceConfig__ros_msg_type = unitree_go__msg__InterfaceConfig;

static bool _InterfaceConfig__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _InterfaceConfig__ros_msg_type * ros_message = static_cast<const _InterfaceConfig__ros_msg_type *>(untyped_ros_message);
  // Field name: mode
  {
    cdr << ros_message->mode;
  }

  // Field name: value
  {
    cdr << ros_message->value;
  }

  // Field name: reserve
  {
    size_t size = 2;
    auto array_ptr = ros_message->reserve;
    cdr.serializeArray(array_ptr, size);
  }

  return true;
}

static bool _InterfaceConfig__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _InterfaceConfig__ros_msg_type * ros_message = static_cast<_InterfaceConfig__ros_msg_type *>(untyped_ros_message);
  // Field name: mode
  {
    cdr >> ros_message->mode;
  }

  // Field name: value
  {
    cdr >> ros_message->value;
  }

  // Field name: reserve
  {
    size_t size = 2;
    auto array_ptr = ros_message->reserve;
    cdr.deserializeArray(array_ptr, size);
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_unitree_go
size_t get_serialized_size_unitree_go__msg__InterfaceConfig(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _InterfaceConfig__ros_msg_type * ros_message = static_cast<const _InterfaceConfig__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name mode
  {
    size_t item_size = sizeof(ros_message->mode);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name value
  {
    size_t item_size = sizeof(ros_message->value);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name reserve
  {
    size_t array_size = 2;
    auto array_ptr = ros_message->reserve;
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _InterfaceConfig__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_unitree_go__msg__InterfaceConfig(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_unitree_go
size_t max_serialized_size_unitree_go__msg__InterfaceConfig(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: mode
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: value
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: reserve
  {
    size_t array_size = 2;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = unitree_go__msg__InterfaceConfig;
    is_plain =
      (
      offsetof(DataType, reserve) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _InterfaceConfig__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_unitree_go__msg__InterfaceConfig(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_InterfaceConfig = {
  "unitree_go::msg",
  "InterfaceConfig",
  _InterfaceConfig__cdr_serialize,
  _InterfaceConfig__cdr_deserialize,
  _InterfaceConfig__get_serialized_size,
  _InterfaceConfig__max_serialized_size
};

static rosidl_message_type_support_t _InterfaceConfig__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_InterfaceConfig,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, unitree_go, msg, InterfaceConfig)() {
  return &_InterfaceConfig__type_support;
}

#if defined(__cplusplus)
}
#endif
