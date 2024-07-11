// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from isaac_ros_pointcloud_interfaces:msg/FlatScan.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_POINTCLOUD_INTERFACES__MSG__DETAIL__FLAT_SCAN__STRUCT_H_
#define ISAAC_ROS_POINTCLOUD_INTERFACES__MSG__DETAIL__FLAT_SCAN__STRUCT_H_

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
// Member 'angles'
// Member 'ranges'
// Member 'intensities'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/FlatScan in the package isaac_ros_pointcloud_interfaces.
/**
  * 2D points stored as polar coordinates
  * both the angles and ranges arrays should be of the same size
  * the nth points' angle is the nth value in the 'angles' array
  * the nth points' range is the nth value in the 'ranges' array
  * the nth points' intensity is the nth value in the 'intensities' array
 */
typedef struct isaac_ros_pointcloud_interfaces__msg__FlatScan
{
  /// in frame frame_id, angles are measured around
  /// the positive Z axis (counterclockwise, if Z is up)
  /// with zero angle being forward along the x axis
  std_msgs__msg__Header header;
  /// minimum range value
  float range_min;
  /// maximum range value
  float range_max;
  /// value of beam angle with respect to
  /// header.frame_id frame
  rosidl_runtime_c__float__Sequence angles;
  /// range data
  /// (Note: values < range_min or > range_max should be discarded)
  rosidl_runtime_c__float__Sequence ranges;
  /// intensity data.  If your
  /// device does not provide intensities, please leave
  /// the array empty
  rosidl_runtime_c__float__Sequence intensities;
} isaac_ros_pointcloud_interfaces__msg__FlatScan;

// Struct for a sequence of isaac_ros_pointcloud_interfaces__msg__FlatScan.
typedef struct isaac_ros_pointcloud_interfaces__msg__FlatScan__Sequence
{
  isaac_ros_pointcloud_interfaces__msg__FlatScan * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} isaac_ros_pointcloud_interfaces__msg__FlatScan__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ISAAC_ROS_POINTCLOUD_INTERFACES__MSG__DETAIL__FLAT_SCAN__STRUCT_H_
