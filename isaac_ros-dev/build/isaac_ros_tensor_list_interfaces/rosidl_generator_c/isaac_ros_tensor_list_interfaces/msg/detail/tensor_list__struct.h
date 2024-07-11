// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from isaac_ros_tensor_list_interfaces:msg/TensorList.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR_LIST__STRUCT_H_
#define ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR_LIST__STRUCT_H_

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
// Member 'tensors'
#include "isaac_ros_tensor_list_interfaces/msg/detail/tensor__struct.h"

/// Struct defined in msg/TensorList in the package isaac_ros_tensor_list_interfaces.
typedef struct isaac_ros_tensor_list_interfaces__msg__TensorList
{
  std_msgs__msg__Header header;
  /// A list of tensors
  isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence tensors;
} isaac_ros_tensor_list_interfaces__msg__TensorList;

// Struct for a sequence of isaac_ros_tensor_list_interfaces__msg__TensorList.
typedef struct isaac_ros_tensor_list_interfaces__msg__TensorList__Sequence
{
  isaac_ros_tensor_list_interfaces__msg__TensorList * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} isaac_ros_tensor_list_interfaces__msg__TensorList__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ISAAC_ROS_TENSOR_LIST_INTERFACES__MSG__DETAIL__TENSOR_LIST__STRUCT_H_
