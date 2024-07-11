// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from nvblox_msgs:srv/EsdfAndGradients.idl
// generated code does not contain a copyright notice
#include "nvblox_msgs/srv/detail/esdf_and_gradients__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "nvblox_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "nvblox_msgs/srv/detail/esdf_and_gradients__struct.h"
#include "nvblox_msgs/srv/detail/esdf_and_gradients__functions.h"
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

#include "geometry_msgs/msg/detail/point__functions.h"  // aabb_min_m
#include "geometry_msgs/msg/detail/vector3__functions.h"  // aabb_size_m

// forward declare type support functions
ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_nvblox_msgs
size_t get_serialized_size_geometry_msgs__msg__Point(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_nvblox_msgs
size_t max_serialized_size_geometry_msgs__msg__Point(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_nvblox_msgs
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, geometry_msgs, msg, Point)();
ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_nvblox_msgs
size_t get_serialized_size_geometry_msgs__msg__Vector3(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_nvblox_msgs
size_t max_serialized_size_geometry_msgs__msg__Vector3(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_nvblox_msgs
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, geometry_msgs, msg, Vector3)();


using _EsdfAndGradients_Request__ros_msg_type = nvblox_msgs__srv__EsdfAndGradients_Request;

static bool _EsdfAndGradients_Request__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _EsdfAndGradients_Request__ros_msg_type * ros_message = static_cast<const _EsdfAndGradients_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: aabb_min_m
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, geometry_msgs, msg, Point
      )()->data);
    if (!callbacks->cdr_serialize(
        &ros_message->aabb_min_m, cdr))
    {
      return false;
    }
  }

  // Field name: aabb_size_m
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, geometry_msgs, msg, Vector3
      )()->data);
    if (!callbacks->cdr_serialize(
        &ros_message->aabb_size_m, cdr))
    {
      return false;
    }
  }

  return true;
}

static bool _EsdfAndGradients_Request__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _EsdfAndGradients_Request__ros_msg_type * ros_message = static_cast<_EsdfAndGradients_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: aabb_min_m
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, geometry_msgs, msg, Point
      )()->data);
    if (!callbacks->cdr_deserialize(
        cdr, &ros_message->aabb_min_m))
    {
      return false;
    }
  }

  // Field name: aabb_size_m
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, geometry_msgs, msg, Vector3
      )()->data);
    if (!callbacks->cdr_deserialize(
        cdr, &ros_message->aabb_size_m))
    {
      return false;
    }
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_nvblox_msgs
size_t get_serialized_size_nvblox_msgs__srv__EsdfAndGradients_Request(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _EsdfAndGradients_Request__ros_msg_type * ros_message = static_cast<const _EsdfAndGradients_Request__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name aabb_min_m

  current_alignment += get_serialized_size_geometry_msgs__msg__Point(
    &(ros_message->aabb_min_m), current_alignment);
  // field.name aabb_size_m

  current_alignment += get_serialized_size_geometry_msgs__msg__Vector3(
    &(ros_message->aabb_size_m), current_alignment);

  return current_alignment - initial_alignment;
}

static uint32_t _EsdfAndGradients_Request__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_nvblox_msgs__srv__EsdfAndGradients_Request(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_nvblox_msgs
size_t max_serialized_size_nvblox_msgs__srv__EsdfAndGradients_Request(
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

  // member: aabb_min_m
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_geometry_msgs__msg__Point(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }
  // member: aabb_size_m
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_geometry_msgs__msg__Vector3(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = nvblox_msgs__srv__EsdfAndGradients_Request;
    is_plain =
      (
      offsetof(DataType, aabb_size_m) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _EsdfAndGradients_Request__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_nvblox_msgs__srv__EsdfAndGradients_Request(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_EsdfAndGradients_Request = {
  "nvblox_msgs::srv",
  "EsdfAndGradients_Request",
  _EsdfAndGradients_Request__cdr_serialize,
  _EsdfAndGradients_Request__cdr_deserialize,
  _EsdfAndGradients_Request__get_serialized_size,
  _EsdfAndGradients_Request__max_serialized_size
};

static rosidl_message_type_support_t _EsdfAndGradients_Request__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_EsdfAndGradients_Request,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, nvblox_msgs, srv, EsdfAndGradients_Request)() {
  return &_EsdfAndGradients_Request__type_support;
}

#if defined(__cplusplus)
}
#endif

// already included above
// #include <cassert>
// already included above
// #include <limits>
// already included above
// #include <string>
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
// already included above
// #include "nvblox_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
// already included above
// #include "nvblox_msgs/srv/detail/esdf_and_gradients__struct.h"
// already included above
// #include "nvblox_msgs/srv/detail/esdf_and_gradients__functions.h"
// already included above
// #include "fastcdr/Cdr.h"

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

#include "std_msgs/msg/detail/float32__functions.h"  // voxel_size
#include "std_msgs/msg/detail/float32_multi_array__functions.h"  // esdf_and_gradients

// forward declare type support functions
ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_nvblox_msgs
size_t get_serialized_size_std_msgs__msg__Float32(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_nvblox_msgs
size_t max_serialized_size_std_msgs__msg__Float32(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_nvblox_msgs
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, std_msgs, msg, Float32)();
ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_nvblox_msgs
size_t get_serialized_size_std_msgs__msg__Float32MultiArray(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_nvblox_msgs
size_t max_serialized_size_std_msgs__msg__Float32MultiArray(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_nvblox_msgs
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, std_msgs, msg, Float32MultiArray)();


using _EsdfAndGradients_Response__ros_msg_type = nvblox_msgs__srv__EsdfAndGradients_Response;

static bool _EsdfAndGradients_Response__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _EsdfAndGradients_Response__ros_msg_type * ros_message = static_cast<const _EsdfAndGradients_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: voxel_size
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, std_msgs, msg, Float32
      )()->data);
    if (!callbacks->cdr_serialize(
        &ros_message->voxel_size, cdr))
    {
      return false;
    }
  }

  // Field name: esdf_and_gradients
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, std_msgs, msg, Float32MultiArray
      )()->data);
    if (!callbacks->cdr_serialize(
        &ros_message->esdf_and_gradients, cdr))
    {
      return false;
    }
  }

  return true;
}

static bool _EsdfAndGradients_Response__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _EsdfAndGradients_Response__ros_msg_type * ros_message = static_cast<_EsdfAndGradients_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: voxel_size
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, std_msgs, msg, Float32
      )()->data);
    if (!callbacks->cdr_deserialize(
        cdr, &ros_message->voxel_size))
    {
      return false;
    }
  }

  // Field name: esdf_and_gradients
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, std_msgs, msg, Float32MultiArray
      )()->data);
    if (!callbacks->cdr_deserialize(
        cdr, &ros_message->esdf_and_gradients))
    {
      return false;
    }
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_nvblox_msgs
size_t get_serialized_size_nvblox_msgs__srv__EsdfAndGradients_Response(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _EsdfAndGradients_Response__ros_msg_type * ros_message = static_cast<const _EsdfAndGradients_Response__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name voxel_size

  current_alignment += get_serialized_size_std_msgs__msg__Float32(
    &(ros_message->voxel_size), current_alignment);
  // field.name esdf_and_gradients

  current_alignment += get_serialized_size_std_msgs__msg__Float32MultiArray(
    &(ros_message->esdf_and_gradients), current_alignment);

  return current_alignment - initial_alignment;
}

static uint32_t _EsdfAndGradients_Response__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_nvblox_msgs__srv__EsdfAndGradients_Response(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_nvblox_msgs
size_t max_serialized_size_nvblox_msgs__srv__EsdfAndGradients_Response(
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

  // member: voxel_size
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_std_msgs__msg__Float32(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }
  // member: esdf_and_gradients
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_std_msgs__msg__Float32MultiArray(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = nvblox_msgs__srv__EsdfAndGradients_Response;
    is_plain =
      (
      offsetof(DataType, esdf_and_gradients) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _EsdfAndGradients_Response__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_nvblox_msgs__srv__EsdfAndGradients_Response(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_EsdfAndGradients_Response = {
  "nvblox_msgs::srv",
  "EsdfAndGradients_Response",
  _EsdfAndGradients_Response__cdr_serialize,
  _EsdfAndGradients_Response__cdr_deserialize,
  _EsdfAndGradients_Response__get_serialized_size,
  _EsdfAndGradients_Response__max_serialized_size
};

static rosidl_message_type_support_t _EsdfAndGradients_Response__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_EsdfAndGradients_Response,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, nvblox_msgs, srv, EsdfAndGradients_Response)() {
  return &_EsdfAndGradients_Response__type_support;
}

#if defined(__cplusplus)
}
#endif

#include "rosidl_typesupport_fastrtps_cpp/service_type_support.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "nvblox_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "nvblox_msgs/srv/esdf_and_gradients.h"

#if defined(__cplusplus)
extern "C"
{
#endif

static service_type_support_callbacks_t EsdfAndGradients__callbacks = {
  "nvblox_msgs::srv",
  "EsdfAndGradients",
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, nvblox_msgs, srv, EsdfAndGradients_Request)(),
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, nvblox_msgs, srv, EsdfAndGradients_Response)(),
};

static rosidl_service_type_support_t EsdfAndGradients__handle = {
  rosidl_typesupport_fastrtps_c__identifier,
  &EsdfAndGradients__callbacks,
  get_service_typesupport_handle_function,
};

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, nvblox_msgs, srv, EsdfAndGradients)() {
  return &EsdfAndGradients__handle;
}

#if defined(__cplusplus)
}
#endif
