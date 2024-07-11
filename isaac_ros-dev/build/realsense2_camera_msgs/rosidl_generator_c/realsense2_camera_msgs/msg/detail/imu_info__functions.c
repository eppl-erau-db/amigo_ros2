// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from realsense2_camera_msgs:msg/IMUInfo.idl
// generated code does not contain a copyright notice
#include "realsense2_camera_msgs/msg/detail/imu_info__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"

bool
realsense2_camera_msgs__msg__IMUInfo__init(realsense2_camera_msgs__msg__IMUInfo * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    realsense2_camera_msgs__msg__IMUInfo__fini(msg);
    return false;
  }
  // data
  // noise_variances
  // bias_variances
  return true;
}

void
realsense2_camera_msgs__msg__IMUInfo__fini(realsense2_camera_msgs__msg__IMUInfo * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // data
  // noise_variances
  // bias_variances
}

bool
realsense2_camera_msgs__msg__IMUInfo__are_equal(const realsense2_camera_msgs__msg__IMUInfo * lhs, const realsense2_camera_msgs__msg__IMUInfo * rhs)
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
  // data
  for (size_t i = 0; i < 12; ++i) {
    if (lhs->data[i] != rhs->data[i]) {
      return false;
    }
  }
  // noise_variances
  for (size_t i = 0; i < 3; ++i) {
    if (lhs->noise_variances[i] != rhs->noise_variances[i]) {
      return false;
    }
  }
  // bias_variances
  for (size_t i = 0; i < 3; ++i) {
    if (lhs->bias_variances[i] != rhs->bias_variances[i]) {
      return false;
    }
  }
  return true;
}

bool
realsense2_camera_msgs__msg__IMUInfo__copy(
  const realsense2_camera_msgs__msg__IMUInfo * input,
  realsense2_camera_msgs__msg__IMUInfo * output)
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
  // data
  for (size_t i = 0; i < 12; ++i) {
    output->data[i] = input->data[i];
  }
  // noise_variances
  for (size_t i = 0; i < 3; ++i) {
    output->noise_variances[i] = input->noise_variances[i];
  }
  // bias_variances
  for (size_t i = 0; i < 3; ++i) {
    output->bias_variances[i] = input->bias_variances[i];
  }
  return true;
}

realsense2_camera_msgs__msg__IMUInfo *
realsense2_camera_msgs__msg__IMUInfo__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  realsense2_camera_msgs__msg__IMUInfo * msg = (realsense2_camera_msgs__msg__IMUInfo *)allocator.allocate(sizeof(realsense2_camera_msgs__msg__IMUInfo), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(realsense2_camera_msgs__msg__IMUInfo));
  bool success = realsense2_camera_msgs__msg__IMUInfo__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
realsense2_camera_msgs__msg__IMUInfo__destroy(realsense2_camera_msgs__msg__IMUInfo * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    realsense2_camera_msgs__msg__IMUInfo__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
realsense2_camera_msgs__msg__IMUInfo__Sequence__init(realsense2_camera_msgs__msg__IMUInfo__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  realsense2_camera_msgs__msg__IMUInfo * data = NULL;

  if (size) {
    data = (realsense2_camera_msgs__msg__IMUInfo *)allocator.zero_allocate(size, sizeof(realsense2_camera_msgs__msg__IMUInfo), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = realsense2_camera_msgs__msg__IMUInfo__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        realsense2_camera_msgs__msg__IMUInfo__fini(&data[i - 1]);
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
realsense2_camera_msgs__msg__IMUInfo__Sequence__fini(realsense2_camera_msgs__msg__IMUInfo__Sequence * array)
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
      realsense2_camera_msgs__msg__IMUInfo__fini(&array->data[i]);
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

realsense2_camera_msgs__msg__IMUInfo__Sequence *
realsense2_camera_msgs__msg__IMUInfo__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  realsense2_camera_msgs__msg__IMUInfo__Sequence * array = (realsense2_camera_msgs__msg__IMUInfo__Sequence *)allocator.allocate(sizeof(realsense2_camera_msgs__msg__IMUInfo__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = realsense2_camera_msgs__msg__IMUInfo__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
realsense2_camera_msgs__msg__IMUInfo__Sequence__destroy(realsense2_camera_msgs__msg__IMUInfo__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    realsense2_camera_msgs__msg__IMUInfo__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
realsense2_camera_msgs__msg__IMUInfo__Sequence__are_equal(const realsense2_camera_msgs__msg__IMUInfo__Sequence * lhs, const realsense2_camera_msgs__msg__IMUInfo__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!realsense2_camera_msgs__msg__IMUInfo__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
realsense2_camera_msgs__msg__IMUInfo__Sequence__copy(
  const realsense2_camera_msgs__msg__IMUInfo__Sequence * input,
  realsense2_camera_msgs__msg__IMUInfo__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(realsense2_camera_msgs__msg__IMUInfo);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    realsense2_camera_msgs__msg__IMUInfo * data =
      (realsense2_camera_msgs__msg__IMUInfo *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!realsense2_camera_msgs__msg__IMUInfo__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          realsense2_camera_msgs__msg__IMUInfo__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!realsense2_camera_msgs__msg__IMUInfo__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
