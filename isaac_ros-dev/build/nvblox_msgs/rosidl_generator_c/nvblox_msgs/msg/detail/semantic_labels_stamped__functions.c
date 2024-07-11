// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from nvblox_msgs:msg/SemanticLabelsStamped.idl
// generated code does not contain a copyright notice
#include "nvblox_msgs/msg/detail/semantic_labels_stamped__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `labels`
#include "rosidl_runtime_c/string_functions.h"

bool
nvblox_msgs__msg__SemanticLabelsStamped__init(nvblox_msgs__msg__SemanticLabelsStamped * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    nvblox_msgs__msg__SemanticLabelsStamped__fini(msg);
    return false;
  }
  // labels
  if (!rosidl_runtime_c__String__init(&msg->labels)) {
    nvblox_msgs__msg__SemanticLabelsStamped__fini(msg);
    return false;
  }
  return true;
}

void
nvblox_msgs__msg__SemanticLabelsStamped__fini(nvblox_msgs__msg__SemanticLabelsStamped * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // labels
  rosidl_runtime_c__String__fini(&msg->labels);
}

bool
nvblox_msgs__msg__SemanticLabelsStamped__are_equal(const nvblox_msgs__msg__SemanticLabelsStamped * lhs, const nvblox_msgs__msg__SemanticLabelsStamped * rhs)
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
  // labels
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->labels), &(rhs->labels)))
  {
    return false;
  }
  return true;
}

bool
nvblox_msgs__msg__SemanticLabelsStamped__copy(
  const nvblox_msgs__msg__SemanticLabelsStamped * input,
  nvblox_msgs__msg__SemanticLabelsStamped * output)
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
  // labels
  if (!rosidl_runtime_c__String__copy(
      &(input->labels), &(output->labels)))
  {
    return false;
  }
  return true;
}

nvblox_msgs__msg__SemanticLabelsStamped *
nvblox_msgs__msg__SemanticLabelsStamped__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  nvblox_msgs__msg__SemanticLabelsStamped * msg = (nvblox_msgs__msg__SemanticLabelsStamped *)allocator.allocate(sizeof(nvblox_msgs__msg__SemanticLabelsStamped), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(nvblox_msgs__msg__SemanticLabelsStamped));
  bool success = nvblox_msgs__msg__SemanticLabelsStamped__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
nvblox_msgs__msg__SemanticLabelsStamped__destroy(nvblox_msgs__msg__SemanticLabelsStamped * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    nvblox_msgs__msg__SemanticLabelsStamped__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
nvblox_msgs__msg__SemanticLabelsStamped__Sequence__init(nvblox_msgs__msg__SemanticLabelsStamped__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  nvblox_msgs__msg__SemanticLabelsStamped * data = NULL;

  if (size) {
    data = (nvblox_msgs__msg__SemanticLabelsStamped *)allocator.zero_allocate(size, sizeof(nvblox_msgs__msg__SemanticLabelsStamped), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = nvblox_msgs__msg__SemanticLabelsStamped__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        nvblox_msgs__msg__SemanticLabelsStamped__fini(&data[i - 1]);
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
nvblox_msgs__msg__SemanticLabelsStamped__Sequence__fini(nvblox_msgs__msg__SemanticLabelsStamped__Sequence * array)
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
      nvblox_msgs__msg__SemanticLabelsStamped__fini(&array->data[i]);
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

nvblox_msgs__msg__SemanticLabelsStamped__Sequence *
nvblox_msgs__msg__SemanticLabelsStamped__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  nvblox_msgs__msg__SemanticLabelsStamped__Sequence * array = (nvblox_msgs__msg__SemanticLabelsStamped__Sequence *)allocator.allocate(sizeof(nvblox_msgs__msg__SemanticLabelsStamped__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = nvblox_msgs__msg__SemanticLabelsStamped__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
nvblox_msgs__msg__SemanticLabelsStamped__Sequence__destroy(nvblox_msgs__msg__SemanticLabelsStamped__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    nvblox_msgs__msg__SemanticLabelsStamped__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
nvblox_msgs__msg__SemanticLabelsStamped__Sequence__are_equal(const nvblox_msgs__msg__SemanticLabelsStamped__Sequence * lhs, const nvblox_msgs__msg__SemanticLabelsStamped__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!nvblox_msgs__msg__SemanticLabelsStamped__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
nvblox_msgs__msg__SemanticLabelsStamped__Sequence__copy(
  const nvblox_msgs__msg__SemanticLabelsStamped__Sequence * input,
  nvblox_msgs__msg__SemanticLabelsStamped__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(nvblox_msgs__msg__SemanticLabelsStamped);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    nvblox_msgs__msg__SemanticLabelsStamped * data =
      (nvblox_msgs__msg__SemanticLabelsStamped *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!nvblox_msgs__msg__SemanticLabelsStamped__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          nvblox_msgs__msg__SemanticLabelsStamped__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!nvblox_msgs__msg__SemanticLabelsStamped__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
