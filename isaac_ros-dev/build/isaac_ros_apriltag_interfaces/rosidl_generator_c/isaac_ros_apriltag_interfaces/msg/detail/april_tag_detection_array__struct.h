// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from isaac_ros_apriltag_interfaces:msg/AprilTagDetectionArray.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_APRILTAG_INTERFACES__MSG__DETAIL__APRIL_TAG_DETECTION_ARRAY__STRUCT_H_
#define ISAAC_ROS_APRILTAG_INTERFACES__MSG__DETAIL__APRIL_TAG_DETECTION_ARRAY__STRUCT_H_

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
// Member 'detections'
#include "isaac_ros_apriltag_interfaces/msg/detail/april_tag_detection__struct.h"

/// Struct defined in msg/AprilTagDetectionArray in the package isaac_ros_apriltag_interfaces.
typedef struct isaac_ros_apriltag_interfaces__msg__AprilTagDetectionArray
{
  std_msgs__msg__Header header;
  isaac_ros_apriltag_interfaces__msg__AprilTagDetection__Sequence detections;
} isaac_ros_apriltag_interfaces__msg__AprilTagDetectionArray;

// Struct for a sequence of isaac_ros_apriltag_interfaces__msg__AprilTagDetectionArray.
typedef struct isaac_ros_apriltag_interfaces__msg__AprilTagDetectionArray__Sequence
{
  isaac_ros_apriltag_interfaces__msg__AprilTagDetectionArray * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} isaac_ros_apriltag_interfaces__msg__AprilTagDetectionArray__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ISAAC_ROS_APRILTAG_INTERFACES__MSG__DETAIL__APRIL_TAG_DETECTION_ARRAY__STRUCT_H_
