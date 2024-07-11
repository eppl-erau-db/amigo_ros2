// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from isaac_ros_tensor_list_interfaces:msg/TensorShape.idl
// generated code does not contain a copyright notice
#include "isaac_ros_tensor_list_interfaces/msg/detail/tensor_shape__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `dims`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
isaac_ros_tensor_list_interfaces__msg__TensorShape__init(isaac_ros_tensor_list_interfaces__msg__TensorShape * msg)
{
  if (!msg) {
    return false;
  }
  // rank
  // dims
  if (!rosidl_runtime_c__uint32__Sequence__init(&msg->dims, 0)) {
    isaac_ros_tensor_list_interfaces__msg__TensorShape__fini(msg);
    return false;
  }
  return true;
}

void
isaac_ros_tensor_list_interfaces__msg__TensorShape__fini(isaac_ros_tensor_list_interfaces__msg__TensorShape * msg)
{
  if (!msg) {
    return;
  }
  // rank
  // dims
  rosidl_runtime_c__uint32__Sequence__fini(&msg->dims);
}

bool
isaac_ros_tensor_list_interfaces__msg__TensorShape__are_equal(const isaac_ros_tensor_list_interfaces__msg__TensorShape * lhs, const isaac_ros_tensor_list_interfaces__msg__TensorShape * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // rank
  if (lhs->rank != rhs->rank) {
    return false;
  }
  // dims
  if (!rosidl_runtime_c__uint32__Sequence__are_equal(
      &(lhs->dims), &(rhs->dims)))
  {
    return false;
  }
  return true;
}

bool
isaac_ros_tensor_list_interfaces__msg__TensorShape__copy(
  const isaac_ros_tensor_list_interfaces__msg__TensorShape * input,
  isaac_ros_tensor_list_interfaces__msg__TensorShape * output)
{
  if (!input || !output) {
    return false;
  }
  // rank
  output->rank = input->rank;
  // dims
  if (!rosidl_runtime_c__uint32__Sequence__copy(
      &(input->dims), &(output->dims)))
  {
    return false;
  }
  return true;
}

isaac_ros_tensor_list_interfaces__msg__TensorShape *
isaac_ros_tensor_list_interfaces__msg__TensorShape__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  isaac_ros_tensor_list_interfaces__msg__TensorShape * msg = (isaac_ros_tensor_list_interfaces__msg__TensorShape *)allocator.allocate(sizeof(isaac_ros_tensor_list_interfaces__msg__TensorShape), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(isaac_ros_tensor_list_interfaces__msg__TensorShape));
  bool success = isaac_ros_tensor_list_interfaces__msg__TensorShape__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
isaac_ros_tensor_list_interfaces__msg__TensorShape__destroy(isaac_ros_tensor_list_interfaces__msg__TensorShape * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    isaac_ros_tensor_list_interfaces__msg__TensorShape__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
isaac_ros_tensor_list_interfaces__msg__TensorShape__Sequence__init(isaac_ros_tensor_list_interfaces__msg__TensorShape__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  isaac_ros_tensor_list_interfaces__msg__TensorShape * data = NULL;

  if (size) {
    data = (isaac_ros_tensor_list_interfaces__msg__TensorShape *)allocator.zero_allocate(size, sizeof(isaac_ros_tensor_list_interfaces__msg__TensorShape), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = isaac_ros_tensor_list_interfaces__msg__TensorShape__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        isaac_ros_tensor_list_interfaces__msg__TensorShape__fini(&data[i - 1]);
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
isaac_ros_tensor_list_interfaces__msg__TensorShape__Sequence__fini(isaac_ros_tensor_list_interfaces__msg__TensorShape__Sequence * array)
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
      isaac_ros_tensor_list_interfaces__msg__TensorShape__fini(&array->data[i]);
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

isaac_ros_tensor_list_interfaces__msg__TensorShape__Sequence *
isaac_ros_tensor_list_interfaces__msg__TensorShape__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  isaac_ros_tensor_list_interfaces__msg__TensorShape__Sequence * array = (isaac_ros_tensor_list_interfaces__msg__TensorShape__Sequence *)allocator.allocate(sizeof(isaac_ros_tensor_list_interfaces__msg__TensorShape__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = isaac_ros_tensor_list_interfaces__msg__TensorShape__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
isaac_ros_tensor_list_interfaces__msg__TensorShape__Sequence__destroy(isaac_ros_tensor_list_interfaces__msg__TensorShape__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    isaac_ros_tensor_list_interfaces__msg__TensorShape__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
isaac_ros_tensor_list_interfaces__msg__TensorShape__Sequence__are_equal(const isaac_ros_tensor_list_interfaces__msg__TensorShape__Sequence * lhs, const isaac_ros_tensor_list_interfaces__msg__TensorShape__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!isaac_ros_tensor_list_interfaces__msg__TensorShape__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
isaac_ros_tensor_list_interfaces__msg__TensorShape__Sequence__copy(
  const isaac_ros_tensor_list_interfaces__msg__TensorShape__Sequence * input,
  isaac_ros_tensor_list_interfaces__msg__TensorShape__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(isaac_ros_tensor_list_interfaces__msg__TensorShape);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    isaac_ros_tensor_list_interfaces__msg__TensorShape * data =
      (isaac_ros_tensor_list_interfaces__msg__TensorShape *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!isaac_ros_tensor_list_interfaces__msg__TensorShape__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          isaac_ros_tensor_list_interfaces__msg__TensorShape__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!isaac_ros_tensor_list_interfaces__msg__TensorShape__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
