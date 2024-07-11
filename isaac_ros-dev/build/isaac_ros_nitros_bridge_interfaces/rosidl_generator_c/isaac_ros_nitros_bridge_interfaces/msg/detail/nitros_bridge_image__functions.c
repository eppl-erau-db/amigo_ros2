// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from isaac_ros_nitros_bridge_interfaces:msg/NitrosBridgeImage.idl
// generated code does not contain a copyright notice
#include "isaac_ros_nitros_bridge_interfaces/msg/detail/nitros_bridge_image__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `encoding`
#include "rosidl_runtime_c/string_functions.h"
// Member `data`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__init(isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__fini(msg);
    return false;
  }
  // height
  // width
  // encoding
  if (!rosidl_runtime_c__String__init(&msg->encoding)) {
    isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__fini(msg);
    return false;
  }
  // is_bigendian
  // step
  // data
  if (!rosidl_runtime_c__int32__Sequence__init(&msg->data, 0)) {
    isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__fini(msg);
    return false;
  }
  return true;
}

void
isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__fini(isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // height
  // width
  // encoding
  rosidl_runtime_c__String__fini(&msg->encoding);
  // is_bigendian
  // step
  // data
  rosidl_runtime_c__int32__Sequence__fini(&msg->data);
}

bool
isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__are_equal(const isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage * lhs, const isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // height
  if (lhs->height != rhs->height) {
    return false;
  }
  // width
  if (lhs->width != rhs->width) {
    return false;
  }
  // encoding
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->encoding), &(rhs->encoding)))
  {
    return false;
  }
  // is_bigendian
  if (lhs->is_bigendian != rhs->is_bigendian) {
    return false;
  }
  // step
  if (lhs->step != rhs->step) {
    return false;
  }
  // data
  if (!rosidl_runtime_c__int32__Sequence__are_equal(
      &(lhs->data), &(rhs->data)))
  {
    return false;
  }
  return true;
}

bool
isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__copy(
  const isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage * input,
  isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // height
  output->height = input->height;
  // width
  output->width = input->width;
  // encoding
  if (!rosidl_runtime_c__String__copy(
      &(input->encoding), &(output->encoding)))
  {
    return false;
  }
  // is_bigendian
  output->is_bigendian = input->is_bigendian;
  // step
  output->step = input->step;
  // data
  if (!rosidl_runtime_c__int32__Sequence__copy(
      &(input->data), &(output->data)))
  {
    return false;
  }
  return true;
}

isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage *
isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage * msg = (isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage *)allocator.allocate(sizeof(isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage));
  bool success = isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__destroy(isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__Sequence__init(isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage * data = NULL;

  if (size) {
    data = (isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage *)allocator.zero_allocate(size, sizeof(isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__Sequence__fini(isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__Sequence *
isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__Sequence * array = (isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__Sequence *)allocator.allocate(sizeof(isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__Sequence__destroy(isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__Sequence__are_equal(const isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__Sequence * lhs, const isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__Sequence__copy(
  const isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__Sequence * input,
  isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage * data =
      (isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!isaac_ros_nitros_bridge_interfaces__msg__NitrosBridgeImage__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
