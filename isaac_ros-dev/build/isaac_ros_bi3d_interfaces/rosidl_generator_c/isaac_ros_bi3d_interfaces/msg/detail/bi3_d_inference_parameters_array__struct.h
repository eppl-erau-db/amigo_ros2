// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from isaac_ros_bi3d_interfaces:msg/Bi3DInferenceParametersArray.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_BI3D_INTERFACES__MSG__DETAIL__BI3_D_INFERENCE_PARAMETERS_ARRAY__STRUCT_H_
#define ISAAC_ROS_BI3D_INTERFACES__MSG__DETAIL__BI3_D_INFERENCE_PARAMETERS_ARRAY__STRUCT_H_

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
// Member 'disparity_values'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/Bi3DInferenceParametersArray in the package isaac_ros_bi3d_interfaces.
typedef struct isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray
{
  std_msgs__msg__Header header;
  rosidl_runtime_c__int32__Sequence disparity_values;
} isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray;

// Struct for a sequence of isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray.
typedef struct isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__Sequence
{
  isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ISAAC_ROS_BI3D_INTERFACES__MSG__DETAIL__BI3_D_INFERENCE_PARAMETERS_ARRAY__STRUCT_H_
