// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from isaac_ros_bi3d_interfaces:msg/Bi3DInferenceParametersArray.idl
// generated code does not contain a copyright notice
#include "isaac_ros_bi3d_interfaces/msg/detail/bi3_d_inference_parameters_array__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `disparity_values`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__init(isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__fini(msg);
    return false;
  }
  // disparity_values
  if (!rosidl_runtime_c__int32__Sequence__init(&msg->disparity_values, 0)) {
    isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__fini(msg);
    return false;
  }
  return true;
}

void
isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__fini(isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // disparity_values
  rosidl_runtime_c__int32__Sequence__fini(&msg->disparity_values);
}

bool
isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__are_equal(const isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray * lhs, const isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray * rhs)
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
  // disparity_values
  if (!rosidl_runtime_c__int32__Sequence__are_equal(
      &(lhs->disparity_values), &(rhs->disparity_values)))
  {
    return false;
  }
  return true;
}

bool
isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__copy(
  const isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray * input,
  isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray * output)
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
  // disparity_values
  if (!rosidl_runtime_c__int32__Sequence__copy(
      &(input->disparity_values), &(output->disparity_values)))
  {
    return false;
  }
  return true;
}

isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray *
isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray * msg = (isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray *)allocator.allocate(sizeof(isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray));
  bool success = isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__destroy(isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__Sequence__init(isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray * data = NULL;

  if (size) {
    data = (isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray *)allocator.zero_allocate(size, sizeof(isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__fini(&data[i - 1]);
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
isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__Sequence__fini(isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__Sequence * array)
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
      isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__fini(&array->data[i]);
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

isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__Sequence *
isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__Sequence * array = (isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__Sequence *)allocator.allocate(sizeof(isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__Sequence__destroy(isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__Sequence__are_equal(const isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__Sequence * lhs, const isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__Sequence__copy(
  const isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__Sequence * input,
  isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray * data =
      (isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!isaac_ros_bi3d_interfaces__msg__Bi3DInferenceParametersArray__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
