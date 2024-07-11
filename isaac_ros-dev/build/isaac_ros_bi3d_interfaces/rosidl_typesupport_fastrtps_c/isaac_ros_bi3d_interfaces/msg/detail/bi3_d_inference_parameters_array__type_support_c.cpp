// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from isaac_ros_bi3d_interfaces:msg/Bi3DInferenceParametersArray.idl
// generated code does not contain a copyright notice
#include "isaac_ros_bi3d_interfaces/msg/detail/bi3_d_inference_parameters_array__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "isaac_ros_bi3d_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "isaac_ros_bi3d_interfaces/msg/detail/bi3_d_inference_parameters_array__struct.h"
#include "isaac_ros_bi3d_interfaces/msg/detail/bi3_d_inference_parameters_array__functions.h"
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

#include "rosidl_runtime_c/primitives_sequence.h"  // disparity_values
#include "rosidl_runtime_c/primitives_sequence_functions.h"  // disparity_values
#include "std_msgs/msg/detail/header__functions.h"  // header

// forward declare type support functions
ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_isaac_ros_bi3d_interfaces
size_t get_serialized_size_std_msgs__msg__Header(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_isaac_ros_bi3d_interfaces
size_t max_serialized_size_std_msgs__msg__Header(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_isaac_ros_bi3d_interfaces
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, std_msgs, msg, Header)();


using _Bi3DInferenceParametersArray__ros_msg_type = isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray;

static bool _Bi3DInferenceParametersArray__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _Bi3DInferenceParametersArray__ros_msg_type * ros_message = static_cast<const _Bi3DInferenceParametersArray__ros_msg_type *>(untyped_ros_message);
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

  // Field name: disparity_values
  {
    size_t size = ros_message->disparity_values.size;
    auto array_ptr = ros_message->disparity_values.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serializeArray(array_ptr, size);
  }

  return true;
}

static bool _Bi3DInferenceParametersArray__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _Bi3DInferenceParametersArray__ros_msg_type * ros_message = static_cast<_Bi3DInferenceParametersArray__ros_msg_type *>(untyped_ros_message);
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

  // Field name: disparity_values
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);
    if (ros_message->disparity_values.data) {
      rosidl_runtime_c__int32__Sequence__fini(&ros_message->disparity_values);
    }
    if (!rosidl_runtime_c__int32__Sequence__init(&ros_message->disparity_values, size)) {
      fprintf(stderr, "failed to create array for field 'disparity_values'");
      return false;
    }
    auto array_ptr = ros_message->disparity_values.data;
    cdr.deserializeArray(array_ptr, size);
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_isaac_ros_bi3d_interfaces
size_t get_serialized_size_isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _Bi3DInferenceParametersArray__ros_msg_type * ros_message = static_cast<const _Bi3DInferenceParametersArray__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name header

  current_alignment += get_serialized_size_std_msgs__msg__Header(
    &(ros_message->header), current_alignment);
  // field.name disparity_values
  {
    size_t array_size = ros_message->disparity_values.size;
    auto array_ptr = ros_message->disparity_values.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _Bi3DInferenceParametersArray__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_isaac_ros_bi3d_interfaces
size_t max_serialized_size_isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray(
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
  // member: disparity_values
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray;
    is_plain =
      (
      offsetof(DataType, disparity_values) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _Bi3DInferenceParametersArray__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_Bi3DInferenceParametersArray = {
  "isaac_ros_bi3d_interfaces::msg",
  "Bi3DInferenceParametersArray",
  _Bi3DInferenceParametersArray__cdr_serialize,
  _Bi3DInferenceParametersArray__cdr_deserialize,
  _Bi3DInferenceParametersArray__get_serialized_size,
  _Bi3DInferenceParametersArray__max_serialized_size
};

static rosidl_message_type_support_t _Bi3DInferenceParametersArray__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_Bi3DInferenceParametersArray,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, isaac_ros_bi3d_interfaces, msg, Bi3DInferenceParametersArray)() {
  return &_Bi3DInferenceParametersArray__type_support;
}

#if defined(__cplusplus)
}
#endif
