// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from nvblox_msgs:msg/SemanticLabelsStamped.idl
// generated code does not contain a copyright notice

#ifndef NVBLOX_MSGS__MSG__DETAIL__SEMANTIC_LABELS_STAMPED__STRUCT_H_
#define NVBLOX_MSGS__MSG__DETAIL__SEMANTIC_LABELS_STAMPED__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'labels'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/SemanticLabelsStamped in the package nvblox_msgs.
typedef struct nvblox_msgs__msg__SemanticLabelsStamped
{
  std_msgs__msg__Header header;
  rosidl_runtime_c__String labels;
} nvblox_msgs__msg__SemanticLabelsStamped;

// Struct for a sequence of nvblox_msgs__msg__SemanticLabelsStamped.
typedef struct nvblox_msgs__msg__SemanticLabelsStamped__Sequence
{
  nvblox_msgs__msg__SemanticLabelsStamped * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} nvblox_msgs__msg__SemanticLabelsStamped__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // NVBLOX_MSGS__MSG__DETAIL__SEMANTIC_LABELS_STAMPED__STRUCT_H_
