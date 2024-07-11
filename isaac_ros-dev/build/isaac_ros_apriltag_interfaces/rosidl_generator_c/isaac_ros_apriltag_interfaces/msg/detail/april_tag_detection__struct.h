// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from isaac_ros_apriltag_interfaces:msg/AprilTagDetection.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_APRILTAG_INTERFACES__MSG__DETAIL__APRIL_TAG_DETECTION__STRUCT_H_
#define ISAAC_ROS_APRILTAG_INTERFACES__MSG__DETAIL__APRIL_TAG_DETECTION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'family'
#include "rosidl_runtime_c/string.h"
// Member 'center'
// Member 'corners'
#include "geometry_msgs/msg/detail/point__struct.h"
// Member 'pose'
#include "geometry_msgs/msg/detail/pose_with_covariance_stamped__struct.h"

/// Struct defined in msg/AprilTagDetection in the package isaac_ros_apriltag_interfaces.
typedef struct isaac_ros_apriltag_interfaces__msg__AprilTagDetection
{
  rosidl_runtime_c__String family;
  int32_t id;
  /// centre in (x,y) pixel coordinates
  geometry_msgs__msg__Point center;
  /// corners of tag ((x1,y1),(x2,y2),...)
  geometry_msgs__msg__Point corners[4];
  geometry_msgs__msg__PoseWithCovarianceStamped pose;
} isaac_ros_apriltag_interfaces__msg__AprilTagDetection;

// Struct for a sequence of isaac_ros_apriltag_interfaces__msg__AprilTagDetection.
typedef struct isaac_ros_apriltag_interfaces__msg__AprilTagDetection__Sequence
{
  isaac_ros_apriltag_interfaces__msg__AprilTagDetection * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} isaac_ros_apriltag_interfaces__msg__AprilTagDetection__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ISAAC_ROS_APRILTAG_INTERFACES__MSG__DETAIL__APRIL_TAG_DETECTION__STRUCT_H_
