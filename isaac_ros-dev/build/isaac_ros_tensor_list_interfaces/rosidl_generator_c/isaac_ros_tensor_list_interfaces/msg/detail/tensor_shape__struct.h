// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from isaac_ros_tensor_list_interfaces:msg/TensorShape.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR_SHAPE__STRUCT_H_
#define ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR_SHAPE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'dims'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/TensorShape in the package isaac_ros_tensor_list_interfaces.
/**
  * Rank of the tensor
 */
typedef struct isaac_ros_tensor_list_interfaces__msg__TensorShape
{
  uint8_t rank;
  /// Number of elements in each dimension
  rosidl_runtime_c__uint32__Sequence dims;
} isaac_ros_tensor_list_interfaces__msg__TensorShape;

// Struct for a sequence of isaac_ros_tensor_list_interfaces__msg__TensorShape.
typedef struct isaac_ros_tensor_list_interfaces__msg__TensorShape__Sequence
{
  isaac_ros_tensor_list_interfaces__msg__TensorShape * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} isaac_ros_tensor_list_interfaces__msg__TensorShape__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR_SHAPE__STRUCT_H_
