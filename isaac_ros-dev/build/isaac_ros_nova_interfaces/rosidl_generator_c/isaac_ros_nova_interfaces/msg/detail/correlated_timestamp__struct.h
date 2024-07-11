// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from isaac_ros_nova_interfaces:msg/CorrelatedTimestamp.idl
// generated code does not contain a copyright notice

#ifndef ISAAC_ROS_NOVA_INTERFACES__MSG__DETAIL__CORRELATED_TIMESTAMP__STRUCT_H_
#define ISAAC_ROS_NOVA_INTERFACES__MSG__DETAIL__CORRELATED_TIMESTAMP__STRUCT_H_

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

/// Struct defined in msg/CorrelatedTimestamp in the package isaac_ros_nova_interfaces.
/**
  * Correlated timestamp
  * Nova has three seperate clocks that we must keep track of, the PTP hardware clock (PHC), the
  * Timer's System Counter (TSC), and the system clock mainatined by the kernel (sys).
  * This struct contains two pairs of correlated timestamps, phc_val_ anc tsc_val are taken
  * simultanously, and phc2_val and sys_val_ are taken simultanously.
  * phc and tsc are captured at the same time
 */
typedef struct isaac_ros_nova_interfaces__msg__CorrelatedTimestamp
{
  std_msgs__msg__Header header;
  /// PTP Hardware Clock (PHC)
  uint64_t phc_val;
  /// Timer's System Counter (TSC)
  uint64_t tsc_val;
  /// phc2 and tsc are captures at the same time.
  /// PTP Hardware Clock (PHC), same clock as phc_val_ above, but taken at a
  /// different time
  uint64_t phc2_val;
  /// System Clock (Sys)
  uint64_t sys_val;
  /// Latency of reading the PHC, slightly subtle, as this only applies to PHC2
  /// Basically the simultanous reading of sys<->phc2 within nvpps does not account
  /// The time it takes to read from the PHC, which can be several microseconds.
  /// The value of phc2 published by the correlated_timestamp_driver already accounts for
  /// This value, and phc_latency is provided to expose this value to GXF for sanity checking
  uint64_t phc_latency;
} isaac_ros_nova_interfaces__msg__CorrelatedTimestamp;

// Struct for a sequence of isaac_ros_nova_interfaces__msg__CorrelatedTimestamp.
typedef struct isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__Sequence
{
  isaac_ros_nova_interfaces__msg__CorrelatedTimestamp * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ISAAC_ROS_NOVA_INTERFACES__MSG__DETAIL__CORRELATED_TIMESTAMP__STRUCT_H_
