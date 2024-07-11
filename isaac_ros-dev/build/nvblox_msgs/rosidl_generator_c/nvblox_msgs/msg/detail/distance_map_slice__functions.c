// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from nvblox_msgs:msg/DistanceMapSlice.idl
// generated code does not contain a copyright notice
#include "nvblox_msgs/msg/detail/distance_map_slice__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `origin`
#include "geometry_msgs/msg/detail/point__functions.h"
// Member `data`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
nvblox_msgs__msg__DistanceMapSlice__init(nvblox_msgs__msg__DistanceMapSlice * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    nvblox_msgs__msg__DistanceMapSlice__fini(msg);
    return false;
  }
  // resolution
  // width
  // height
  // origin
  if (!geometry_msgs__msg__Point__init(&msg->origin)) {
    nvblox_msgs__msg__DistanceMapSlice__fini(msg);
    return false;
  }
  // unknown_value
  // data
  if (!rosidl_runtime_c__float__Sequence__init(&msg->data, 0)) {
    nvblox_msgs__msg__DistanceMapSlice__fini(msg);
    return false;
  }
  return true;
}

void
nvblox_msgs__msg__DistanceMapSlice__fini(nvblox_msgs__msg__DistanceMapSlice * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // resolution
  // width
  // height
  // origin
  geometry_msgs__msg__Point__fini(&msg->origin);
  // unknown_value
  // data
  rosidl_runtime_c__float__Sequence__fini(&msg->data);
}

bool
nvblox_msgs__msg__DistanceMapSlice__are_equal(const nvblox_msgs__msg__DistanceMapSlice * lhs, const nvblox_msgs__msg__DistanceMapSlice * rhs)
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
  // resolution
  if (lhs->resolution != rhs->resolution) {
    return false;
  }
  // width
  if (lhs->width != rhs->width) {
    return false;
  }
  // height
  if (lhs->height != rhs->height) {
    return false;
  }
  // origin
  if (!geometry_msgs__msg__Point__are_equal(
      &(lhs->origin), &(rhs->origin)))
  {
    return false;
  }
  // unknown_value
  if (lhs->unknown_value != rhs->unknown_value) {
    return false;
  }
  // data
  if (!rosidl_runtime_c__float__Sequence__are_equal(
      &(lhs->data), &(rhs->data)))
  {
    return false;
  }
  return true;
}

bool
nvblox_msgs__msg__DistanceMapSlice__copy(
  const nvblox_msgs__msg__DistanceMapSlice * input,
  nvblox_msgs__msg__DistanceMapSlice * output)
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
  // resolution
  output->resolution = input->resolution;
  // width
  output->width = input->width;
  // height
  output->height = input->height;
  // origin
  if (!geometry_msgs__msg__Point__copy(
      &(input->origin), &(output->origin)))
  {
    return false;
  }
  // unknown_value
  output->unknown_value = input->unknown_value;
  // data
  if (!rosidl_runtime_c__float__Sequence__copy(
      &(input->data), &(output->data)))
  {
    return false;
  }
  return true;
}

nvblox_msgs__msg__DistanceMapSlice *
nvblox_msgs__msg__DistanceMapSlice__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  nvblox_msgs__msg__DistanceMapSlice * msg = (nvblox_msgs__msg__DistanceMapSlice *)allocator.allocate(sizeof(nvblox_msgs__msg__DistanceMapSlice), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(nvblox_msgs__msg__DistanceMapSlice));
  bool success = nvblox_msgs__msg__DistanceMapSlice__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
nvblox_msgs__msg__DistanceMapSlice__destroy(nvblox_msgs__msg__DistanceMapSlice * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    nvblox_msgs__msg__DistanceMapSlice__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
nvblox_msgs__msg__DistanceMapSlice__Sequence__init(nvblox_msgs__msg__DistanceMapSlice__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  nvblox_msgs__msg__DistanceMapSlice * data = NULL;

  if (size) {
    data = (nvblox_msgs__msg__DistanceMapSlice *)allocator.zero_allocate(size, sizeof(nvblox_msgs__msg__DistanceMapSlice), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = nvblox_msgs__msg__DistanceMapSlice__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        nvblox_msgs__msg__DistanceMapSlice__fini(&data[i - 1]);
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
nvblox_msgs__msg__DistanceMapSlice__Sequence__fini(nvblox_msgs__msg__DistanceMapSlice__Sequence * array)
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
      nvblox_msgs__msg__DistanceMapSlice__fini(&array->data[i]);
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

nvblox_msgs__msg__DistanceMapSlice__Sequence *
nvblox_msgs__msg__DistanceMapSlice__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  nvblox_msgs__msg__DistanceMapSlice__Sequence * array = (nvblox_msgs__msg__DistanceMapSlice__Sequence *)allocator.allocate(sizeof(nvblox_msgs__msg__DistanceMapSlice__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = nvblox_msgs__msg__DistanceMapSlice__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
nvblox_msgs__msg__DistanceMapSlice__Sequence__destroy(nvblox_msgs__msg__DistanceMapSlice__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    nvblox_msgs__msg__DistanceMapSlice__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
nvblox_msgs__msg__DistanceMapSlice__Sequence__are_equal(const nvblox_msgs__msg__DistanceMapSlice__Sequence * lhs, const nvblox_msgs__msg__DistanceMapSlice__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!nvblox_msgs__msg__DistanceMapSlice__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
nvblox_msgs__msg__DistanceMapSlice__Sequence__copy(
  const nvblox_msgs__msg__DistanceMapSlice__Sequence * input,
  nvblox_msgs__msg__DistanceMapSlice__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(nvblox_msgs__msg__DistanceMapSlice);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    nvblox_msgs__msg__DistanceMapSlice * data =
      (nvblox_msgs__msg__DistanceMapSlice *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!nvblox_msgs__msg__DistanceMapSlice__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          nvblox_msgs__msg__DistanceMapSlice__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!nvblox_msgs__msg__DistanceMapSlice__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
