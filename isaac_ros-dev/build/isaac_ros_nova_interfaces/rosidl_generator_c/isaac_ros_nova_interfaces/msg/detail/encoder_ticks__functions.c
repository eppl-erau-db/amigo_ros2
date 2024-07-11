// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from isaac_ros_nova_interfaces:msg/EncoderTicks.idl
// generated code does not contain a copyright notice
#include "isaac_ros_nova_interfaces/msg/detail/encoder_ticks__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"

bool
isaac_ros_nova_interfaces__msg__EncoderTicks__init(isaac_ros_nova_interfaces__msg__EncoderTicks * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    isaac_ros_nova_interfaces__msg__EncoderTicks__fini(msg);
    return false;
  }
  // left_ticks
  // right_ticks
  // encoder_timestamp
  return true;
}

void
isaac_ros_nova_interfaces__msg__EncoderTicks__fini(isaac_ros_nova_interfaces__msg__EncoderTicks * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // left_ticks
  // right_ticks
  // encoder_timestamp
}

bool
isaac_ros_nova_interfaces__msg__EncoderTicks__are_equal(const isaac_ros_nova_interfaces__msg__EncoderTicks * lhs, const isaac_ros_nova_interfaces__msg__EncoderTicks * rhs)
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
  // left_ticks
  if (lhs->left_ticks != rhs->left_ticks) {
    return false;
  }
  // right_ticks
  if (lhs->right_ticks != rhs->right_ticks) {
    return false;
  }
  // encoder_timestamp
  if (lhs->encoder_timestamp != rhs->encoder_timestamp) {
    return false;
  }
  return true;
}

bool
isaac_ros_nova_interfaces__msg__EncoderTicks__copy(
  const isaac_ros_nova_interfaces__msg__EncoderTicks * input,
  isaac_ros_nova_interfaces__msg__EncoderTicks * output)
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
  // left_ticks
  output->left_ticks = input->left_ticks;
  // right_ticks
  output->right_ticks = input->right_ticks;
  // encoder_timestamp
  output->encoder_timestamp = input->encoder_timestamp;
  return true;
}

isaac_ros_nova_interfaces__msg__EncoderTicks *
isaac_ros_nova_interfaces__msg__EncoderTicks__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  isaac_ros_nova_interfaces__msg__EncoderTicks * msg = (isaac_ros_nova_interfaces__msg__EncoderTicks *)allocator.allocate(sizeof(isaac_ros_nova_interfaces__msg__EncoderTicks), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(isaac_ros_nova_interfaces__msg__EncoderTicks));
  bool success = isaac_ros_nova_interfaces__msg__EncoderTicks__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
isaac_ros_nova_interfaces__msg__EncoderTicks__destroy(isaac_ros_nova_interfaces__msg__EncoderTicks * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    isaac_ros_nova_interfaces__msg__EncoderTicks__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
isaac_ros_nova_interfaces__msg__EncoderTicks__Sequence__init(isaac_ros_nova_interfaces__msg__EncoderTicks__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  isaac_ros_nova_interfaces__msg__EncoderTicks * data = NULL;

  if (size) {
    data = (isaac_ros_nova_interfaces__msg__EncoderTicks *)allocator.zero_allocate(size, sizeof(isaac_ros_nova_interfaces__msg__EncoderTicks), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = isaac_ros_nova_interfaces__msg__EncoderTicks__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        isaac_ros_nova_interfaces__msg__EncoderTicks__fini(&data[i - 1]);
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
isaac_ros_nova_interfaces__msg__EncoderTicks__Sequence__fini(isaac_ros_nova_interfaces__msg__EncoderTicks__Sequence * array)
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
      isaac_ros_nova_interfaces__msg__EncoderTicks__fini(&array->data[i]);
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

isaac_ros_nova_interfaces__msg__EncoderTicks__Sequence *
isaac_ros_nova_interfaces__msg__EncoderTicks__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  isaac_ros_nova_interfaces__msg__EncoderTicks__Sequence * array = (isaac_ros_nova_interfaces__msg__EncoderTicks__Sequence *)allocator.allocate(sizeof(isaac_ros_nova_interfaces__msg__EncoderTicks__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = isaac_ros_nova_interfaces__msg__EncoderTicks__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
isaac_ros_nova_interfaces__msg__EncoderTicks__Sequence__destroy(isaac_ros_nova_interfaces__msg__EncoderTicks__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    isaac_ros_nova_interfaces__msg__EncoderTicks__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
isaac_ros_nova_interfaces__msg__EncoderTicks__Sequence__are_equal(const isaac_ros_nova_interfaces__msg__EncoderTicks__Sequence * lhs, const isaac_ros_nova_interfaces__msg__EncoderTicks__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!isaac_ros_nova_interfaces__msg__EncoderTicks__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
isaac_ros_nova_interfaces__msg__EncoderTicks__Sequence__copy(
  const isaac_ros_nova_interfaces__msg__EncoderTicks__Sequence * input,
  isaac_ros_nova_interfaces__msg__EncoderTicks__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(isaac_ros_nova_interfaces__msg__EncoderTicks);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    isaac_ros_nova_interfaces__msg__EncoderTicks * data =
      (isaac_ros_nova_interfaces__msg__EncoderTicks *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!isaac_ros_nova_interfaces__msg__EncoderTicks__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          isaac_ros_nova_interfaces__msg__EncoderTicks__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!isaac_ros_nova_interfaces__msg__EncoderTicks__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
