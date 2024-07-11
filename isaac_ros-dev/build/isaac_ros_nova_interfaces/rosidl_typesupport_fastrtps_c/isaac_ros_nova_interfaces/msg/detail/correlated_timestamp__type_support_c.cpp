// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from isaac_ros_nova_interfaces:msg/CorrelatedTimestamp.idl
// generated code does not contain a copyright notice
#include "isaac_ros_nova_interfaces/msg/detail/correlated_timestamp__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "isaac_ros_nova_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "isaac_ros_nova_interfaces/msg/detail/correlated_timestamp__struct.h"
#include "isaac_ros_nova_interfaces/msg/detail/correlated_timestamp__functions.h"
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

#include "std_msgs/msg/detail/header__functions.h"  // header

// forward declare type support functions
ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_isaac_ros_nova_interfaces
size_t get_serialized_size_std_msgs__msg__Header(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_isaac_ros_nova_interfaces
size_t max_serialized_size_std_msgs__msg__Header(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_isaac_ros_nova_interfaces
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, std_msgs, msg, Header)();


using _CorrelatedTimestamp__ros_msg_type = isaac_ros_nova_interfaces__msg__CorrelatedTimestamp;

static bool _CorrelatedTimestamp__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _CorrelatedTimestamp__ros_msg_type * ros_message = static_cast<const _CorrelatedTimestamp__ros_msg_type *>(untyped_ros_message);
  // Field name: header
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, std_msgs, msg, Header
      )()->data);
    if (!callbacks->cdr_serialize(
        &ros_message->header, cdr))
    {
      return false;
    }
  }

  // Field name: phc_val
  {
    cdr << ros_message->phc_val;
  }

  // Field name: tsc_val
  {
    cdr << ros_message->tsc_val;
  }

  // Field name: phc2_val
  {
    cdr << ros_message->phc2_val;
  }

  // Field name: sys_val
  {
    cdr << ros_message->sys_val;
  }

  // Field name: phc_latency
  {
    cdr << ros_message->phc_latency;
  }

  return true;
}

static bool _CorrelatedTimestamp__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _CorrelatedTimestamp__ros_msg_type * ros_message = static_cast<_CorrelatedTimestamp__ros_msg_type *>(untyped_ros_message);
  // Field name: header
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, std_msgs, msg, Header
      )()->data);
    if (!callbacks->cdr_deserialize(
        cdr, &ros_message->header))
    {
      return false;
    }
  }

  // Field name: phc_val
  {
    cdr >> ros_message->phc_val;
  }

  // Field name: tsc_val
  {
    cdr >> ros_message->tsc_val;
  }

  // Field name: phc2_val
  {
    cdr >> ros_message->phc2_val;
  }

  // Field name: sys_val
  {
    cdr >> ros_message->sys_val;
  }

  // Field name: phc_latency
  {
    cdr >> ros_message->phc_latency;
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_isaac_ros_nova_interfaces
size_t get_serialized_size_isaac_ros_nova_interfaces__msg__CorrelatedTimestamp(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _CorrelatedTimestamp__ros_msg_type * ros_message = static_cast<const _CorrelatedTimestamp__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name header

  current_alignment += get_serialized_size_std_msgs__msg__Header(
    &(ros_message->header), current_alignment);
  // field.name phc_val
  {
    size_t item_size = sizeof(ros_message->phc_val);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name tsc_val
  {
    size_t item_size = sizeof(ros_message->tsc_val);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name phc2_val
  {
    size_t item_size = sizeof(ros_message->phc2_val);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name sys_val
  {
    size_t item_size = sizeof(ros_message->sys_val);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name phc_latency
  {
    size_t item_size = sizeof(ros_message->phc_latency);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _CorrelatedTimestamp__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_isaac_ros_nova_interfaces__msg__CorrelatedTimestamp(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_isaac_ros_nova_interfaces
size_t max_serialized_size_isaac_ros_nova_interfaces__msg__CorrelatedTimestamp(
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

  // member: header
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_std_msgs__msg__Header(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }
  // member: phc_val
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: tsc_val
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: phc2_val
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: sys_val
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: phc_latency
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = isaac_ros_nova_interfaces__msg__CorrelatedTimestamp;
    is_plain =
      (
      offsetof(DataType, phc_latency) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _CorrelatedTimestamp__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_isaac_ros_nova_interfaces__msg__CorrelatedTimestamp(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_CorrelatedTimestamp = {
  "isaac_ros_nova_interfaces::msg",
  "CorrelatedTimestamp",
  _CorrelatedTimestamp__cdr_serialize,
  _CorrelatedTimestamp__cdr_deserialize,
  _CorrelatedTimestamp__get_serialized_size,
  _CorrelatedTimestamp__max_serialized_size
};

static rosidl_message_type_support_t _CorrelatedTimestamp__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_CorrelatedTimestamp,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, isaac_ros_nova_interfaces, msg, CorrelatedTimestamp)() {
  return &_CorrelatedTimestamp__type_support;
}

#if defined(__cplusplus)
}
#endif
