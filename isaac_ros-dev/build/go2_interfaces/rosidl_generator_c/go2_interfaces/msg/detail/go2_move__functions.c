// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from go2_interfaces:msg/Go2Move.idl
// generated code does not contain a copyright notice
#include "go2_interfaces/msg/detail/go2_move__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
go2_interfaces__msg__Go2Move__init(go2_interfaces__msg__Go2Move * msg)
{
  if (!msg) {
    return false;
  }
  // x
  // y
  // z
  return true;
}

void
go2_interfaces__msg__Go2Move__fini(go2_interfaces__msg__Go2Move * msg)
{
  if (!msg) {
    return;
  }
  // x
  // y
  // z
}

bool
go2_interfaces__msg__Go2Move__are_equal(const go2_interfaces__msg__Go2Move * lhs, const go2_interfaces__msg__Go2Move * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // x
  if (lhs->x != rhs->x) {
    return false;
  }
  // y
  if (lhs->y != rhs->y) {
    return false;
  }
  // z
  if (lhs->z != rhs->z) {
    return false;
  }
  return true;
}

bool
go2_interfaces__msg__Go2Move__copy(
  const go2_interfaces__msg__Go2Move * input,
  go2_interfaces__msg__Go2Move * output)
{
  if (!input || !output) {
    return false;
  }
  // x
  output->x = input->x;
  // y
  output->y = input->y;
  // z
  output->z = input->z;
  return true;
}

go2_interfaces__msg__Go2Move *
go2_interfaces__msg__Go2Move__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  go2_interfaces__msg__Go2Move * msg = (go2_interfaces__msg__Go2Move *)allocator.allocate(sizeof(go2_interfaces__msg__Go2Move), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(go2_interfaces__msg__Go2Move));
  bool success = go2_interfaces__msg__Go2Move__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
go2_interfaces__msg__Go2Move__destroy(go2_interfaces__msg__Go2Move * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    go2_interfaces__msg__Go2Move__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
go2_interfaces__msg__Go2Move__Sequence__init(go2_interfaces__msg__Go2Move__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  go2_interfaces__msg__Go2Move * data = NULL;

  if (size) {
    data = (go2_interfaces__msg__Go2Move *)allocator.zero_allocate(size, sizeof(go2_interfaces__msg__Go2Move), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = go2_interfaces__msg__Go2Move__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        go2_interfaces__msg__Go2Move__fini(&data[i - 1]);
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
go2_interfaces__msg__Go2Move__Sequence__fini(go2_interfaces__msg__Go2Move__Sequence * array)
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
      go2_interfaces__msg__Go2Move__fini(&array->data[i]);
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

go2_interfaces__msg__Go2Move__Sequence *
go2_interfaces__msg__Go2Move__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  go2_interfaces__msg__Go2Move__Sequence * array = (go2_interfaces__msg__Go2Move__Sequence *)allocator.allocate(sizeof(go2_interfaces__msg__Go2Move__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = go2_interfaces__msg__Go2Move__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
go2_interfaces__msg__Go2Move__Sequence__destroy(go2_interfaces__msg__Go2Move__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    go2_interfaces__msg__Go2Move__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
go2_interfaces__msg__Go2Move__Sequence__are_equal(const go2_interfaces__msg__Go2Move__Sequence * lhs, const go2_interfaces__msg__Go2Move__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!go2_interfaces__msg__Go2Move__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
go2_interfaces__msg__Go2Move__Sequence__copy(
  const go2_interfaces__msg__Go2Move__Sequence * input,
  go2_interfaces__msg__Go2Move__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(go2_interfaces__msg__Go2Move);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    go2_interfaces__msg__Go2Move * data =
      (go2_interfaces__msg__Go2Move *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!go2_interfaces__msg__Go2Move__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          go2_interfaces__msg__Go2Move__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!go2_interfaces__msg__Go2Move__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
