// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from nvblox_msgs:msg/Mesh.idl
// generated code does not contain a copyright notice
#include "nvblox_msgs/msg/detail/mesh__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `block_indices`
#include "nvblox_msgs/msg/detail/index3_d__functions.h"
// Member `blocks`
#include "nvblox_msgs/msg/detail/mesh_block__functions.h"

bool
nvblox_msgs__msg__Mesh__init(nvblox_msgs__msg__Mesh * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    nvblox_msgs__msg__Mesh__fini(msg);
    return false;
  }
  // block_size
  // block_indices
  if (!nvblox_msgs__msg__Index3D__Sequence__init(&msg->block_indices, 0)) {
    nvblox_msgs__msg__Mesh__fini(msg);
    return false;
  }
  // blocks
  if (!nvblox_msgs__msg__MeshBlock__Sequence__init(&msg->blocks, 0)) {
    nvblox_msgs__msg__Mesh__fini(msg);
    return false;
  }
  // clear
  return true;
}

void
nvblox_msgs__msg__Mesh__fini(nvblox_msgs__msg__Mesh * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // block_size
  // block_indices
  nvblox_msgs__msg__Index3D__Sequence__fini(&msg->block_indices);
  // blocks
  nvblox_msgs__msg__MeshBlock__Sequence__fini(&msg->blocks);
  // clear
}

bool
nvblox_msgs__msg__Mesh__are_equal(const nvblox_msgs__msg__Mesh * lhs, const nvblox_msgs__msg__Mesh * rhs)
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
  // block_size
  if (lhs->block_size != rhs->block_size) {
    return false;
  }
  // block_indices
  if (!nvblox_msgs__msg__Index3D__Sequence__are_equal(
      &(lhs->block_indices), &(rhs->block_indices)))
  {
    return false;
  }
  // blocks
  if (!nvblox_msgs__msg__MeshBlock__Sequence__are_equal(
      &(lhs->blocks), &(rhs->blocks)))
  {
    return false;
  }
  // clear
  if (lhs->clear != rhs->clear) {
    return false;
  }
  return true;
}

bool
nvblox_msgs__msg__Mesh__copy(
  const nvblox_msgs__msg__Mesh * input,
  nvblox_msgs__msg__Mesh * output)
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
  // block_size
  output->block_size = input->block_size;
  // block_indices
  if (!nvblox_msgs__msg__Index3D__Sequence__copy(
      &(input->block_indices), &(output->block_indices)))
  {
    return false;
  }
  // blocks
  if (!nvblox_msgs__msg__MeshBlock__Sequence__copy(
      &(input->blocks), &(output->blocks)))
  {
    return false;
  }
  // clear
  output->clear = input->clear;
  return true;
}

nvblox_msgs__msg__Mesh *
nvblox_msgs__msg__Mesh__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  nvblox_msgs__msg__Mesh * msg = (nvblox_msgs__msg__Mesh *)allocator.allocate(sizeof(nvblox_msgs__msg__Mesh), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(nvblox_msgs__msg__Mesh));
  bool success = nvblox_msgs__msg__Mesh__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
nvblox_msgs__msg__Mesh__destroy(nvblox_msgs__msg__Mesh * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    nvblox_msgs__msg__Mesh__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
nvblox_msgs__msg__Mesh__Sequence__init(nvblox_msgs__msg__Mesh__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  nvblox_msgs__msg__Mesh * data = NULL;

  if (size) {
    data = (nvblox_msgs__msg__Mesh *)allocator.zero_allocate(size, sizeof(nvblox_msgs__msg__Mesh), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = nvblox_msgs__msg__Mesh__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        nvblox_msgs__msg__Mesh__fini(&data[i - 1]);
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
nvblox_msgs__msg__Mesh__Sequence__fini(nvblox_msgs__msg__Mesh__Sequence * array)
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
      nvblox_msgs__msg__Mesh__fini(&array->data[i]);
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

nvblox_msgs__msg__Mesh__Sequence *
nvblox_msgs__msg__Mesh__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  nvblox_msgs__msg__Mesh__Sequence * array = (nvblox_msgs__msg__Mesh__Sequence *)allocator.allocate(sizeof(nvblox_msgs__msg__Mesh__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = nvblox_msgs__msg__Mesh__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
nvblox_msgs__msg__Mesh__Sequence__destroy(nvblox_msgs__msg__Mesh__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    nvblox_msgs__msg__Mesh__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
nvblox_msgs__msg__Mesh__Sequence__are_equal(const nvblox_msgs__msg__Mesh__Sequence * lhs, const nvblox_msgs__msg__Mesh__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!nvblox_msgs__msg__Mesh__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
nvblox_msgs__msg__Mesh__Sequence__copy(
  const nvblox_msgs__msg__Mesh__Sequence * input,
  nvblox_msgs__msg__Mesh__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(nvblox_msgs__msg__Mesh);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    nvblox_msgs__msg__Mesh * data =
      (nvblox_msgs__msg__Mesh *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!nvblox_msgs__msg__Mesh__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          nvblox_msgs__msg__Mesh__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!nvblox_msgs__msg__Mesh__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
