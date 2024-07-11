// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from nvblox_msgs:msg/Mesh.idl
// generated code does not contain a copyright notice

#ifndef NVBLOX_MSGS__MSG__DETAIL__MESH__STRUCT_H_
#define NVBLOX_MSGS__MSG__DETAIL__MESH__STRUCT_H_

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
// Member 'block_indices'
#include "nvblox_msgs/msg/detail/index3_d__struct.h"
// Member 'blocks'
#include "nvblox_msgs/msg/detail/mesh_block__struct.h"

/// Struct defined in msg/Mesh in the package nvblox_msgs.
typedef struct nvblox_msgs__msg__Mesh
{
  std_msgs__msg__Header header;
  /// Block origins and block sizes must match.
  /// Block size is the physical size (in meters) of a block of the mesh.
  float block_size;
  /// Block indices are the 3D indices of the blocks; to get the origin of the
  /// block, simply multiply its index by the block size.
  /// Note that we consider a block's origin to be the low-side corner of
  /// the low-side voxel.
  nvblox_msgs__msg__Index3D__Sequence block_indices;
  /// Blocks contains the actual mesh within the block, including triangles,
  /// vertex positions, and vertex colors.
  nvblox_msgs__msg__MeshBlock__Sequence blocks;
  /// Whether to clear the entire previous map. This is set to true when
  /// the *entire* map rather than only the pieces that changed are published.
  bool clear;
} nvblox_msgs__msg__Mesh;

// Struct for a sequence of nvblox_msgs__msg__Mesh.
typedef struct nvblox_msgs__msg__Mesh__Sequence
{
  nvblox_msgs__msg__Mesh * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} nvblox_msgs__msg__Mesh__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // NVBLOX_MSGS__MSG__DETAIL__MESH__STRUCT_H_
