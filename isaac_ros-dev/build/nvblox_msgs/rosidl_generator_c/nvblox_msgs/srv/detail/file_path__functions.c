// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from nvblox_msgs:srv/FilePath.idl
// generated code does not contain a copyright notice
#include "nvblox_msgs/srv/detail/file_path__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `file_path`
#include "rosidl_runtime_c/string_functions.h"

bool
nvblox_msgs__srv__FilePath_Request__init(nvblox_msgs__srv__FilePath_Request * msg)
{
  if (!msg) {
    return false;
  }
  // file_path
  if (!rosidl_runtime_c__String__init(&msg->file_path)) {
    nvblox_msgs__srv__FilePath_Request__fini(msg);
    return false;
  }
  return true;
}

void
nvblox_msgs__srv__FilePath_Request__fini(nvblox_msgs__srv__FilePath_Request * msg)
{
  if (!msg) {
    return;
  }
  // file_path
  rosidl_runtime_c__String__fini(&msg->file_path);
}

bool
nvblox_msgs__srv__FilePath_Request__are_equal(const nvblox_msgs__srv__FilePath_Request * lhs, const nvblox_msgs__srv__FilePath_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // file_path
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->file_path), &(rhs->file_path)))
  {
    return false;
  }
  return true;
}

bool
nvblox_msgs__srv__FilePath_Request__copy(
  const nvblox_msgs__srv__FilePath_Request * input,
  nvblox_msgs__srv__FilePath_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // file_path
  if (!rosidl_runtime_c__String__copy(
      &(input->file_path), &(output->file_path)))
  {
    return false;
  }
  return true;
}

nvblox_msgs__srv__FilePath_Request *
nvblox_msgs__srv__FilePath_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  nvblox_msgs__srv__FilePath_Request * msg = (nvblox_msgs__srv__FilePath_Request *)allocator.allocate(sizeof(nvblox_msgs__srv__FilePath_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(nvblox_msgs__srv__FilePath_Request));
  bool success = nvblox_msgs__srv__FilePath_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
nvblox_msgs__srv__FilePath_Request__destroy(nvblox_msgs__srv__FilePath_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    nvblox_msgs__srv__FilePath_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
nvblox_msgs__srv__FilePath_Request__Sequence__init(nvblox_msgs__srv__FilePath_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  nvblox_msgs__srv__FilePath_Request * data = NULL;

  if (size) {
    data = (nvblox_msgs__srv__FilePath_Request *)allocator.zero_allocate(size, sizeof(nvblox_msgs__srv__FilePath_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = nvblox_msgs__srv__FilePath_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        nvblox_msgs__srv__FilePath_Request__fini(&data[i - 1]);
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
nvblox_msgs__srv__FilePath_Request__Sequence__fini(nvblox_msgs__srv__FilePath_Request__Sequence * array)
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
      nvblox_msgs__srv__FilePath_Request__fini(&array->data[i]);
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

nvblox_msgs__srv__FilePath_Request__Sequence *
nvblox_msgs__srv__FilePath_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  nvblox_msgs__srv__FilePath_Request__Sequence * array = (nvblox_msgs__srv__FilePath_Request__Sequence *)allocator.allocate(sizeof(nvblox_msgs__srv__FilePath_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = nvblox_msgs__srv__FilePath_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
nvblox_msgs__srv__FilePath_Request__Sequence__destroy(nvblox_msgs__srv__FilePath_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    nvblox_msgs__srv__FilePath_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
nvblox_msgs__srv__FilePath_Request__Sequence__are_equal(const nvblox_msgs__srv__FilePath_Request__Sequence * lhs, const nvblox_msgs__srv__FilePath_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!nvblox_msgs__srv__FilePath_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
nvblox_msgs__srv__FilePath_Request__Sequence__copy(
  const nvblox_msgs__srv__FilePath_Request__Sequence * input,
  nvblox_msgs__srv__FilePath_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(nvblox_msgs__srv__FilePath_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    nvblox_msgs__srv__FilePath_Request * data =
      (nvblox_msgs__srv__FilePath_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!nvblox_msgs__srv__FilePath_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          nvblox_msgs__srv__FilePath_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!nvblox_msgs__srv__FilePath_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


bool
nvblox_msgs__srv__FilePath_Response__init(nvblox_msgs__srv__FilePath_Response * msg)
{
  if (!msg) {
    return false;
  }
  // success
  return true;
}

void
nvblox_msgs__srv__FilePath_Response__fini(nvblox_msgs__srv__FilePath_Response * msg)
{
  if (!msg) {
    return;
  }
  // success
}

bool
nvblox_msgs__srv__FilePath_Response__are_equal(const nvblox_msgs__srv__FilePath_Response * lhs, const nvblox_msgs__srv__FilePath_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  return true;
}

bool
nvblox_msgs__srv__FilePath_Response__copy(
  const nvblox_msgs__srv__FilePath_Response * input,
  nvblox_msgs__srv__FilePath_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // success
  output->success = input->success;
  return true;
}

nvblox_msgs__srv__FilePath_Response *
nvblox_msgs__srv__FilePath_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  nvblox_msgs__srv__FilePath_Response * msg = (nvblox_msgs__srv__FilePath_Response *)allocator.allocate(sizeof(nvblox_msgs__srv__FilePath_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(nvblox_msgs__srv__FilePath_Response));
  bool success = nvblox_msgs__srv__FilePath_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
nvblox_msgs__srv__FilePath_Response__destroy(nvblox_msgs__srv__FilePath_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    nvblox_msgs__srv__FilePath_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
nvblox_msgs__srv__FilePath_Response__Sequence__init(nvblox_msgs__srv__FilePath_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  nvblox_msgs__srv__FilePath_Response * data = NULL;

  if (size) {
    data = (nvblox_msgs__srv__FilePath_Response *)allocator.zero_allocate(size, sizeof(nvblox_msgs__srv__FilePath_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = nvblox_msgs__srv__FilePath_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        nvblox_msgs__srv__FilePath_Response__fini(&data[i - 1]);
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
nvblox_msgs__srv__FilePath_Response__Sequence__fini(nvblox_msgs__srv__FilePath_Response__Sequence * array)
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
      nvblox_msgs__srv__FilePath_Response__fini(&array->data[i]);
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

nvblox_msgs__srv__FilePath_Response__Sequence *
nvblox_msgs__srv__FilePath_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  nvblox_msgs__srv__FilePath_Response__Sequence * array = (nvblox_msgs__srv__FilePath_Response__Sequence *)allocator.allocate(sizeof(nvblox_msgs__srv__FilePath_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = nvblox_msgs__srv__FilePath_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
nvblox_msgs__srv__FilePath_Response__Sequence__destroy(nvblox_msgs__srv__FilePath_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    nvblox_msgs__srv__FilePath_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
nvblox_msgs__srv__FilePath_Response__Sequence__are_equal(const nvblox_msgs__srv__FilePath_Response__Sequence * lhs, const nvblox_msgs__srv__FilePath_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!nvblox_msgs__srv__FilePath_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
nvblox_msgs__srv__FilePath_Response__Sequence__copy(
  const nvblox_msgs__srv__FilePath_Response__Sequence * input,
  nvblox_msgs__srv__FilePath_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(nvblox_msgs__srv__FilePath_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    nvblox_msgs__srv__FilePath_Response * data =
      (nvblox_msgs__srv__FilePath_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!nvblox_msgs__srv__FilePath_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          nvblox_msgs__srv__FilePath_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!nvblox_msgs__srv__FilePath_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
