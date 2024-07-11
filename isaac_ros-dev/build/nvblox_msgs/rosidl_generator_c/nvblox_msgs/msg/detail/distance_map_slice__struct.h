// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from nvblox_msgs:msg/DistanceMapSlice.idl
// generated code does not contain a copyright notice

#ifndef NVBLOX_MSGS__MSG__DETAIL__DISTANCE_MAP_SLICE__STRUCT_H_
#define NVBLOX_MSGS__MSG__DETAIL__DISTANCE_MAP_SLICE__STRUCT_H_

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
// Member 'origin'
#include "geometry_msgs/msg/detail/point__struct.h"
// Member 'data'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/DistanceMapSlice in the package nvblox_msgs.
/**
  * A distance map slice is effectively a floating point image where the 
  * value of each pixel represents the distance in meters to the closest
  * surface, in 2 dimensions. Pixels covering space which have not been
  * observed in the mapping process are given a sentinal value which
  * indicates their unknown state.
 */
typedef struct nvblox_msgs__msg__DistanceMapSlice
{
  std_msgs__msg__Header header;
  /// How big each "pixel" in the map is in meters.
  /// In other words the side length of each cell.
  float resolution;
  /// Width is along the x axis and height is along the y axis.
  uint32_t width;
  uint32_t height;
  /// The location of the origin of the distance map slice image.
  /// This point coincides with the upper-left corner of the upper-left most pixel.
  /// The distance map slice is effectively an axis-aligned image, attached to
  /// this point in the world frame.
  geometry_msgs__msg__Point origin;
  /// Which value is used for "unknown" cells.
  /// These cells have not been observed by the camera during the mapping process.
  float unknown_value;
  /// The flattened 2D costmap data. Data is stored as floating point values in meters.
  /// The data is stored row-major such that each row of the image/slice sits contiguous
  /// in memory.
  rosidl_runtime_c__float__Sequence data;
} nvblox_msgs__msg__DistanceMapSlice;

// Struct for a sequence of nvblox_msgs__msg__DistanceMapSlice.
typedef struct nvblox_msgs__msg__DistanceMapSlice__Sequence
{
  nvblox_msgs__msg__DistanceMapSlice * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} nvblox_msgs__msg__DistanceMapSlice__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // NVBLOX_MSGS__MSG__DETAIL__DISTANCE_MAP_SLICE__STRUCT_H_
