// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from isaac_ros_tensor_list_interfaces:msg/Tensor.idl
// generated code does not contain a copyright notice
#include "isaac_ros_tensor_list_interfaces/msg/detail/tensor__rosidl_typesupport_fastrtps_cpp.hpp"
#include "isaac_ros_tensor_list_interfaces/msg/detail/tensor__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions
namespace isaac_ros_tensor_list_interfaces
{
namespace msg
{
namespace typesupport_fastrtps_cpp
{
bool cdr_serialize(
  const isaac_ros_tensor_list_interfaces::msg::TensorShape &,
  eprosima::fastcdr::Cdr &);
bool cdr_deserialize(
  eprosima::fastcdr::Cdr &,
  isaac_ros_tensor_list_interfaces::msg::TensorShape &);
size_t get_serialized_size(
  const isaac_ros_tensor_list_interfaces::msg::TensorShape &,
  size_t current_alignment);
size_t
max_serialized_size_TensorShape(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
}  // namespace typesupport_fastrtps_cpp
}  // namespace msg
}  // namespace isaac_ros_tensor_list_interfaces


namespace isaac_ros_tensor_list_interfaces
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_isaac_ros_tensor_list_interfaces
cdr_serialize(
  const isaac_ros_tensor_list_interfaces::msg::Tensor & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: name
  cdr << ros_message.name;
  // Member: shape
  isaac_ros_tensor_list_interfaces::msg::typesupport_fastrtps_cpp::cdr_serialize(
    ros_message.shape,
    cdr);
  // Member: data_type
  cdr << ros_message.data_type;
  // Member: strides
  {
    cdr << ros_message.strides;
  }
  // Member: data
  {
    cdr << ros_message.data;
  }
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_isaac_ros_tensor_list_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  isaac_ros_tensor_list_interfaces::msg::Tensor & ros_message)
{
  // Member: name
  cdr >> ros_message.name;

  // Member: shape
  isaac_ros_tensor_list_interfaces::msg::typesupport_fastrtps_cpp::cdr_deserialize(
    cdr, ros_message.shape);

  // Member: data_type
  cdr >> ros_message.data_type;

  // Member: strides
  {
    cdr >> ros_message.strides;
  }

  // Member: data
  {
    cdr >> ros_message.data;
  }

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_isaac_ros_tensor_list_interfaces
get_serialized_size(
  const isaac_ros_tensor_list_interfaces::msg::Tensor & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: name
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.name.size() + 1);
  // Member: shape

  current_alignment +=
    isaac_ros_tensor_list_interfaces::msg::typesupport_fastrtps_cpp::get_serialized_size(
    ros_message.shape, current_alignment);
  // Member: data_type
  {
    size_t item_size = sizeof(ros_message.data_type);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: strides
  {
    size_t array_size = ros_message.strides.size();

    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    size_t item_size = sizeof(ros_message.strides[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: data
  {
    size_t array_size = ros_message.data.size();

    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    size_t item_size = sizeof(ros_message.data[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_isaac_ros_tensor_list_interfaces
max_serialized_size_Tensor(
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


  // Member: name
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  // Member: shape
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        isaac_ros_tensor_list_interfaces::msg::typesupport_fastrtps_cpp::max_serialized_size_TensorShape(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Member: data_type
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: strides
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: data
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = isaac_ros_tensor_list_interfaces::msg::Tensor;
    is_plain =
      (
      offsetof(DataType, data) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _Tensor__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const isaac_ros_tensor_list_interfaces::msg::Tensor *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _Tensor__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<isaac_ros_tensor_list_interfaces::msg::Tensor *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _Tensor__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const isaac_ros_tensor_list_interfaces::msg::Tensor *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _Tensor__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_Tensor(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _Tensor__callbacks = {
  "isaac_ros_tensor_list_interfaces::msg",
  "Tensor",
  _Tensor__cdr_serialize,
  _Tensor__cdr_deserialize,
  _Tensor__get_serialized_size,
  _Tensor__max_serialized_size
};

static rosidl_message_type_support_t _Tensor__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_Tensor__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace isaac_ros_tensor_list_interfaces

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_isaac_ros_tensor_list_interfaces
const rosidl_message_type_support_t *
get_message_type_support_handle<isaac_ros_tensor_list_interfaces::msg::Tensor>()
{
  return &isaac_ros_tensor_list_interfaces::msg::typesupport_fastrtps_cpp::_Tensor__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, isaac_ros_tensor_list_interfaces, msg, Tensor)() {
  return &isaac_ros_tensor_list_interfaces::msg::typesupport_fastrtps_cpp::_Tensor__handle;
}

#ifdef __cplusplus
}
#endif
