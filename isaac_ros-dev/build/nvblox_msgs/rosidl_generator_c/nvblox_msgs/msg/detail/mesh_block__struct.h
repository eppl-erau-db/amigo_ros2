// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from nvblox_msgs:msg/MeshBlock.idl
// generated code does not contain a copyright notice

#ifndef NVBLOX_MSGS__MSG__DETAIL__MESH_BLOCK__STRUCT_H_
#define NVBLOX_MSGS__MSG__DETAIL__MESH_BLOCK__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'vertices'
// Member 'normals'
#include "geometry_msgs/msg/detail/point32__struct.h"
// Member 'colors'
#include "std_msgs/msg/detail/color_rgba__struct.h"
// Member 'triangles'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/MeshBlock in the package nvblox_msgs.
/**
  * All of the constituent parts must either have the same length or be length 0.
 */
typedef struct nvblox_msgs__msg__MeshBlock
{
  geometry_msgs__msg__Point32__Sequence vertices;
  geometry_msgs__msg__Point32__Sequence normals;
  std_msgs__msg__ColorRGBA__Sequence colors;
  rosidl_runtime_c__int32__Sequence triangles;
} nvblox_msgs__msg__MeshBlock;

// Struct for a sequence of nvblox_msgs__msg__MeshBlock.
typedef struct nvblox_msgs__msg__MeshBlock__Sequence
{
  nvblox_msgs__msg__MeshBlock * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} nvblox_msgs__msg__MeshBlock__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // NVBLOX_MSGS__MSG__DETAIL__MESH_BLOCK__STRUCT_H_
