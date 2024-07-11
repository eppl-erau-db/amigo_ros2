// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from nvblox_msgs:srv/EsdfAndGradients.idl
// generated code does not contain a copyright notice

#ifndef NVBLOX_MSGS__SRV__DETAIL__ESDF_AND_GRADIENTS__STRUCT_H_
#define NVBLOX_MSGS__SRV__DETAIL__ESDF_AND_GRADIENTS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'aabb_min_m'
#include "geometry_msgs/msg/detail/point__struct.h"
// Member 'aabb_size_m'
#include "geometry_msgs/msg/detail/vector3__struct.h"

/// Struct defined in srv/EsdfAndGradients in the package nvblox_msgs.
typedef struct nvblox_msgs__srv__EsdfAndGradients_Request
{
  geometry_msgs__msg__Point aabb_min_m;
  geometry_msgs__msg__Vector3 aabb_size_m;
} nvblox_msgs__srv__EsdfAndGradients_Request;

// Struct for a sequence of nvblox_msgs__srv__EsdfAndGradients_Request.
typedef struct nvblox_msgs__srv__EsdfAndGradients_Request__Sequence
{
  nvblox_msgs__srv__EsdfAndGradients_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} nvblox_msgs__srv__EsdfAndGradients_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'voxel_size'
#include "std_msgs/msg/detail/float32__struct.h"
// Member 'esdf_and_gradients'
#include "std_msgs/msg/detail/float32_multi_array__struct.h"

/// Struct defined in srv/EsdfAndGradients in the package nvblox_msgs.
typedef struct nvblox_msgs__srv__EsdfAndGradients_Response
{
  std_msgs__msg__Float32 voxel_size;
  std_msgs__msg__Float32MultiArray esdf_and_gradients;
} nvblox_msgs__srv__EsdfAndGradients_Response;

// Struct for a sequence of nvblox_msgs__srv__EsdfAndGradients_Response.
typedef struct nvblox_msgs__srv__EsdfAndGradients_Response__Sequence
{
  nvblox_msgs__srv__EsdfAndGradients_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} nvblox_msgs__srv__EsdfAndGradients_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // NVBLOX_MSGS__SRV__DETAIL__ESDF_AND_GRADIENTS__STRUCT_H_
