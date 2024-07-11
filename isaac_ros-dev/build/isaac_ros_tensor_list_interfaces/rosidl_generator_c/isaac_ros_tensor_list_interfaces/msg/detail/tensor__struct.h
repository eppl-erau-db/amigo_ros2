// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from isaac_ros_tensor_list_interfaces:msg/Tensor.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR__STRUCT_H_
#define ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'name'
#include "rosidl_runtime_c/string.h"
// Member 'shape'
#include "isaac_ros_tensor_list_interfaces/msg/detail/tensor_shape__struct.h"
// Member 'strides'
// Member 'data'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/Tensor in the package isaac_ros_tensor_list_interfaces.
/**
  * Name of the tensor
 */
typedef struct isaac_ros_tensor_list_interfaces__msg__Tensor
{
  rosidl_runtime_c__String name;
  /// Shape information for tensor
  isaac_ros_tensor_list_interfaces__msg__TensorShape shape;
  /// Data type for tensor
  /// Use the following values to represent these data types:
  /// -  1: "int8"
  /// -  2: "uint8"
  /// -  3: "int16"
  /// -  4: "uint16"
  /// -  5: "int32"
  /// -  6: "uint32"
  /// -  7: "int64"
  /// -  8: "uint64"
  /// -  9: "float32"
  /// - 10: "float64"
  int32_t data_type;
  /// Strides of tensor (byte size for each dimension)
  rosidl_runtime_c__uint64__Sequence strides;
  /// Data buffer
  rosidl_runtime_c__uint8__Sequence data;
} isaac_ros_tensor_list_interfaces__msg__Tensor;

// Struct for a sequence of isaac_ros_tensor_list_interfaces__msg__Tensor.
typedef struct isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence
{
  isaac_ros_tensor_list_interfaces__msg__Tensor * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR__STRUCT_H_
