// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from isaac_ros_tensor_list_interfaces:msg/Tensor.idl
// generated code does not contain a copyright notice
#include "isaac_ros_tensor_list_interfaces/msg/detail/tensor__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `name`
#include "rosidl_runtime_c/string_functions.h"
// Member `shape`
#include "isaac_ros_tensor_list_interfaces/msg/detail/tensor_shape__functions.h"
// Member `strides`
// Member `data`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
isaac_ros_tensor_list_interfaces__msg__Tensor__init(isaac_ros_tensor_list_interfaces__msg__Tensor * msg)
{
  if (!msg) {
    return false;
  }
  // name
  if (!rosidl_runtime_c__String__init(&msg->name)) {
    isaac_ros_tensor_list_interfaces__msg__Tensor__fini(msg);
    return false;
  }
  // shape
  if (!isaac_ros_tensor_list_interfaces__msg__TensorShape__init(&msg->shape)) {
    isaac_ros_tensor_list_interfaces__msg__Tensor__fini(msg);
    return false;
  }
  // data_type
  // strides
  if (!rosidl_runtime_c__uint64__Sequence__init(&msg->strides, 0)) {
    isaac_ros_tensor_list_interfaces__msg__Tensor__fini(msg);
    return false;
  }
  // data
  if (!rosidl_runtime_c__uint8__Sequence__init(&msg->data, 0)) {
    isaac_ros_tensor_list_interfaces__msg__Tensor__fini(msg);
    return false;
  }
  return true;
}

void
isaac_ros_tensor_list_interfaces__msg__Tensor__fini(isaac_ros_tensor_list_interfaces__msg__Tensor * msg)
{
  if (!msg) {
    return;
  }
  // name
  rosidl_runtime_c__String__fini(&msg->name);
  // shape
  isaac_ros_tensor_list_interfaces__msg__TensorShape__fini(&msg->shape);
  // data_type
  // strides
  rosidl_runtime_c__uint64__Sequence__fini(&msg->strides);
  // data
  rosidl_runtime_c__uint8__Sequence__fini(&msg->data);
}

bool
isaac_ros_tensor_list_interfaces__msg__Tensor__are_equal(const isaac_ros_tensor_list_interfaces__msg__Tensor * lhs, const isaac_ros_tensor_list_interfaces__msg__Tensor * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->name), &(rhs->name)))
  {
    return false;
  }
  // shape
  if (!isaac_ros_tensor_list_interfaces__msg__TensorShape__are_equal(
      &(lhs->shape), &(rhs->shape)))
  {
    return false;
  }
  // data_type
  if (lhs->data_type != rhs->data_type) {
    return false;
  }
  // strides
  if (!rosidl_runtime_c__uint64__Sequence__are_equal(
      &(lhs->strides), &(rhs->strides)))
  {
    return false;
  }
  // data
  if (!rosidl_runtime_c__uint8__Sequence__are_equal(
      &(lhs->data), &(rhs->data)))
  {
    return false;
  }
  return true;
}

bool
isaac_ros_tensor_list_interfaces__msg__Tensor__copy(
  const isaac_ros_tensor_list_interfaces__msg__Tensor * input,
  isaac_ros_tensor_list_interfaces__msg__Tensor * output)
{
  if (!input || !output) {
    return false;
  }
  // name
  if (!rosidl_runtime_c__String__copy(
      &(input->name), &(output->name)))
  {
    return false;
  }
  // shape
  if (!isaac_ros_tensor_list_interfaces__msg__TensorShape__copy(
      &(input->shape), &(output->shape)))
  {
    return false;
  }
  // data_type
  output->data_type = input->data_type;
  // strides
  if (!rosidl_runtime_c__uint64__Sequence__copy(
      &(input->strides), &(output->strides)))
  {
    return false;
  }
  // data
  if (!rosidl_runtime_c__uint8__Sequence__copy(
      &(input->data), &(output->data)))
  {
    return false;
  }
  return true;
}

isaac_ros_tensor_list_interfaces__msg__Tensor *
isaac_ros_tensor_list_interfaces__msg__Tensor__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  isaac_ros_tensor_list_interfaces__msg__Tensor * msg = (isaac_ros_tensor_list_interfaces__msg__Tensor *)allocator.allocate(sizeof(isaac_ros_tensor_list_interfaces__msg__Tensor), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(isaac_ros_tensor_list_interfaces__msg__Tensor));
  bool success = isaac_ros_tensor_list_interfaces__msg__Tensor__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
isaac_ros_tensor_list_interfaces__msg__Tensor__destroy(isaac_ros_tensor_list_interfaces__msg__Tensor * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    isaac_ros_tensor_list_interfaces__msg__Tensor__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence__init(isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  isaac_ros_tensor_list_interfaces__msg__Tensor * data = NULL;

  if (size) {
    data = (isaac_ros_tensor_list_interfaces__msg__Tensor *)allocator.zero_allocate(size, sizeof(isaac_ros_tensor_list_interfaces__msg__Tensor), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = isaac_ros_tensor_list_interfaces__msg__Tensor__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        isaac_ros_tensor_list_interfaces__msg__Tensor__fini(&data[i - 1]);
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
isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence__fini(isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence * array)
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
      isaac_ros_tensor_list_interfaces__msg__Tensor__fini(&array->data[i]);
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

isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence *
isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence * array = (isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence *)allocator.allocate(sizeof(isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence__destroy(isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence__are_equal(const isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence * lhs, const isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!isaac_ros_tensor_list_interfaces__msg__Tensor__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence__copy(
  const isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence * input,
  isaac_ros_tensor_list_interfaces__msg__Tensor__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(isaac_ros_tensor_list_interfaces__msg__Tensor);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    isaac_ros_tensor_list_interfaces__msg__Tensor * data =
      (isaac_ros_tensor_list_interfaces__msg__Tensor *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!isaac_ros_tensor_list_interfaces__msg__Tensor__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          isaac_ros_tensor_list_interfaces__msg__Tensor__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!isaac_ros_tensor_list_interfaces__msg__Tensor__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
