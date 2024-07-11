// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from nvblox_msgs:msg/MeshBlock.idl
// generated code does not contain a copyright notice
#include "nvblox_msgs/msg/detail/mesh_block__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `vertices`
// Member `normals`
#include "geometry_msgs/msg/detail/point32__functions.h"
// Member `colors`
#include "std_msgs/msg/detail/color_rgba__functions.h"
// Member `triangles`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
nvblox_msgs__msg__MeshBlock__init(nvblox_msgs__msg__MeshBlock * msg)
{
  if (!msg) {
    return false;
  }
  // vertices
  if (!geometry_msgs__msg__Point32__Sequence__init(&msg->vertices, 0)) {
    nvblox_msgs__msg__MeshBlock__fini(msg);
    return false;
  }
  // normals
  if (!geometry_msgs__msg__Point32__Sequence__init(&msg->normals, 0)) {
    nvblox_msgs__msg__MeshBlock__fini(msg);
    return false;
  }
  // colors
  if (!std_msgs__msg__ColorRGBA__Sequence__init(&msg->colors, 0)) {
    nvblox_msgs__msg__MeshBlock__fini(msg);
    return false;
  }
  // triangles
  if (!rosidl_runtime_c__int32__Sequence__init(&msg->triangles, 0)) {
    nvblox_msgs__msg__MeshBlock__fini(msg);
    return false;
  }
  return true;
}

void
nvblox_msgs__msg__MeshBlock__fini(nvblox_msgs__msg__MeshBlock * msg)
{
  if (!msg) {
    return;
  }
  // vertices
  geometry_msgs__msg__Point32__Sequence__fini(&msg->vertices);
  // normals
  geometry_msgs__msg__Point32__Sequence__fini(&msg->normals);
  // colors
  std_msgs__msg__ColorRGBA__Sequence__fini(&msg->colors);
  // triangles
  rosidl_runtime_c__int32__Sequence__fini(&msg->triangles);
}

bool
nvblox_msgs__msg__MeshBlock__are_equal(const nvblox_msgs__msg__MeshBlock * lhs, const nvblox_msgs__msg__MeshBlock * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // vertices
  if (!geometry_msgs__msg__Point32__Sequence__are_equal(
      &(lhs->vertices), &(rhs->vertices)))
  {
    return false;
  }
  // normals
  if (!geometry_msgs__msg__Point32__Sequence__are_equal(
      &(lhs->normals), &(rhs->normals)))
  {
    return false;
  }
  // colors
  if (!std_msgs__msg__ColorRGBA__Sequence__are_equal(
      &(lhs->colors), &(rhs->colors)))
  {
    return false;
  }
  // triangles
  if (!rosidl_runtime_c__int32__Sequence__are_equal(
      &(lhs->triangles), &(rhs->triangles)))
  {
    return false;
  }
  return true;
}

bool
nvblox_msgs__msg__MeshBlock__copy(
  const nvblox_msgs__msg__MeshBlock * input,
  nvblox_msgs__msg__MeshBlock * output)
{
  if (!input || !output) {
    return false;
  }
  // vertices
  if (!geometry_msgs__msg__Point32__Sequence__copy(
      &(input->vertices), &(output->vertices)))
  {
    return false;
  }
  // normals
  if (!geometry_msgs__msg__Point32__Sequence__copy(
      &(input->normals), &(output->normals)))
  {
    return false;
  }
  // colors
  if (!std_msgs__msg__ColorRGBA__Sequence__copy(
      &(input->colors), &(output->colors)))
  {
    return false;
  }
  // triangles
  if (!rosidl_runtime_c__int32__Sequence__copy(
      &(input->triangles), &(output->triangles)))
  {
    return false;
  }
  return true;
}

nvblox_msgs__msg__MeshBlock *
nvblox_msgs__msg__MeshBlock__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  nvblox_msgs__msg__MeshBlock * msg = (nvblox_msgs__msg__MeshBlock *)allocator.allocate(sizeof(nvblox_msgs__msg__MeshBlock), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(nvblox_msgs__msg__MeshBlock));
  bool success = nvblox_msgs__msg__MeshBlock__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
nvblox_msgs__msg__MeshBlock__destroy(nvblox_msgs__msg__MeshBlock * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    nvblox_msgs__msg__MeshBlock__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
nvblox_msgs__msg__MeshBlock__Sequence__init(nvblox_msgs__msg__MeshBlock__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  nvblox_msgs__msg__MeshBlock * data = NULL;

  if (size) {
    data = (nvblox_msgs__msg__MeshBlock *)allocator.zero_allocate(size, sizeof(nvblox_msgs__msg__MeshBlock), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = nvblox_msgs__msg__MeshBlock__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        nvblox_msgs__msg__MeshBlock__fini(&data[i - 1]);
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
nvblox_msgs__msg__MeshBlock__Sequence__fini(nvblox_msgs__msg__MeshBlock__Sequence * array)
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
      nvblox_msgs__msg__MeshBlock__fini(&array->data[i]);
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

nvblox_msgs__msg__MeshBlock__Sequence *
nvblox_msgs__msg__MeshBlock__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  nvblox_msgs__msg__MeshBlock__Sequence * array = (nvblox_msgs__msg__MeshBlock__Sequence *)allocator.allocate(sizeof(nvblox_msgs__msg__MeshBlock__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = nvblox_msgs__msg__MeshBlock__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
nvblox_msgs__msg__MeshBlock__Sequence__destroy(nvblox_msgs__msg__MeshBlock__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    nvblox_msgs__msg__MeshBlock__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
nvblox_msgs__msg__MeshBlock__Sequence__are_equal(const nvblox_msgs__msg__MeshBlock__Sequence * lhs, const nvblox_msgs__msg__MeshBlock__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!nvblox_msgs__msg__MeshBlock__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
nvblox_msgs__msg__MeshBlock__Sequence__copy(
  const nvblox_msgs__msg__MeshBlock__Sequence * input,
  nvblox_msgs__msg__MeshBlock__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(nvblox_msgs__msg__MeshBlock);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    nvblox_msgs__msg__MeshBlock * data =
      (nvblox_msgs__msg__MeshBlock *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!nvblox_msgs__msg__MeshBlock__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          nvblox_msgs__msg__MeshBlock__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!nvblox_msgs__msg__MeshBlock__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
