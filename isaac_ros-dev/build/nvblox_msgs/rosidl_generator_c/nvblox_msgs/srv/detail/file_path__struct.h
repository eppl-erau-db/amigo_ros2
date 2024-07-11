// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from nvblox_msgs:srv/FilePath.idl
// generated code does not contain a copyright notice

#ifndef NVBLOX_MSGS__SRV__DETAIL__FILE_PATH__STRUCT_H_
#define NVBLOX_MSGS__SRV__DETAIL__FILE_PATH__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'file_path'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/FilePath in the package nvblox_msgs.
typedef struct nvblox_msgs__srv__FilePath_Request
{
  rosidl_runtime_c__String file_path;
} nvblox_msgs__srv__FilePath_Request;

// Struct for a sequence of nvblox_msgs__srv__FilePath_Request.
typedef struct nvblox_msgs__srv__FilePath_Request__Sequence
{
  nvblox_msgs__srv__FilePath_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} nvblox_msgs__srv__FilePath_Request__Sequence;


// Constants defined in the message

/// Struct defined in srv/FilePath in the package nvblox_msgs.
typedef struct nvblox_msgs__srv__FilePath_Response
{
  bool success;
} nvblox_msgs__srv__FilePath_Response;

// Struct for a sequence of nvblox_msgs__srv__FilePath_Response.
typedef struct nvblox_msgs__srv__FilePath_Response__Sequence
{
  nvblox_msgs__srv__FilePath_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} nvblox_msgs__srv__FilePath_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // NVBLOX_MSGS__SRV__DETAIL__FILE_PATH__STRUCT_H_
