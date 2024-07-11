// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from realsense2_camera_msgs:srv/DeviceInfo.idl
// generated code does not contain a copyright notice

#ifndef REALSENSE2_CAMERA_MSGS__SRV__DETAIL__DEVICE_INFO__STRUCT_H_
#define REALSENSE2_CAMERA_MSGS__SRV__DETAIL__DEVICE_INFO__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/DeviceInfo in the package realsense2_camera_msgs.
typedef struct realsense2_camera_msgs__srv__DeviceInfo_Request
{
  uint8_t structure_needs_at_least_one_member;
} realsense2_camera_msgs__srv__DeviceInfo_Request;

// Struct for a sequence of realsense2_camera_msgs__srv__DeviceInfo_Request.
typedef struct realsense2_camera_msgs__srv__DeviceInfo_Request__Sequence
{
  realsense2_camera_msgs__srv__DeviceInfo_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} realsense2_camera_msgs__srv__DeviceInfo_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'device_name'
// Member 'serial_number'
// Member 'firmware_version'
// Member 'usb_type_descriptor'
// Member 'firmware_update_id'
// Member 'sensors'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/DeviceInfo in the package realsense2_camera_msgs.
typedef struct realsense2_camera_msgs__srv__DeviceInfo_Response
{
  rosidl_runtime_c__String device_name;
  rosidl_runtime_c__String serial_number;
  rosidl_runtime_c__String firmware_version;
  rosidl_runtime_c__String usb_type_descriptor;
  rosidl_runtime_c__String firmware_update_id;
  rosidl_runtime_c__String sensors;
} realsense2_camera_msgs__srv__DeviceInfo_Response;

// Struct for a sequence of realsense2_camera_msgs__srv__DeviceInfo_Response.
typedef struct realsense2_camera_msgs__srv__DeviceInfo_Response__Sequence
{
  realsense2_camera_msgs__srv__DeviceInfo_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} realsense2_camera_msgs__srv__DeviceInfo_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // REALSENSE2_CAMERA_MSGS__SRV__DETAIL__DEVICE_INFO__STRUCT_H_
