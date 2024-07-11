// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from isaac_ros_nova_interfaces:msg/CorrelatedTimestamp.idl
// generated code does not contain a copyright notice
#include "isaac_ros_nova_interfaces/msg/detail/correlated_timestamp__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"

bool
isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__init(isaac_ros_nova_interfaces__msg__CorrelatedTimestamp * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__fini(msg);
    return false;
  }
  // phc_val
  // tsc_val
  // phc2_val
  // sys_val
  // phc_latency
  return true;
}

void
isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__fini(isaac_ros_nova_interfaces__msg__CorrelatedTimestamp * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // phc_val
  // tsc_val
  // phc2_val
  // sys_val
  // phc_latency
}

bool
isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__are_equal(const isaac_ros_nova_interfaces__msg__CorrelatedTimestamp * lhs, const isaac_ros_nova_interfaces__msg__CorrelatedTimestamp * rhs)
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
  // phc_val
  if (lhs->phc_val != rhs->phc_val) {
    return false;
  }
  // tsc_val
  if (lhs->tsc_val != rhs->tsc_val) {
    return false;
  }
  // phc2_val
  if (lhs->phc2_val != rhs->phc2_val) {
    return false;
  }
  // sys_val
  if (lhs->sys_val != rhs->sys_val) {
    return false;
  }
  // phc_latency
  if (lhs->phc_latency != rhs->phc_latency) {
    return false;
  }
  return true;
}

bool
isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__copy(
  const isaac_ros_nova_interfaces__msg__CorrelatedTimestamp * input,
  isaac_ros_nova_interfaces__msg__CorrelatedTimestamp * output)
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
  // phc_val
  output->phc_val = input->phc_val;
  // tsc_val
  output->tsc_val = input->tsc_val;
  // phc2_val
  output->phc2_val = input->phc2_val;
  // sys_val
  output->sys_val = input->sys_val;
  // phc_latency
  output->phc_latency = input->phc_latency;
  return true;
}

isaac_ros_nova_interfaces__msg__CorrelatedTimestamp *
isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  isaac_ros_nova_interfaces__msg__CorrelatedTimestamp * msg = (isaac_ros_nova_interfaces__msg__CorrelatedTimestamp *)allocator.allocate(sizeof(isaac_ros_nova_interfaces__msg__CorrelatedTimestamp), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(isaac_ros_nova_interfaces__msg__CorrelatedTimestamp));
  bool success = isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__destroy(isaac_ros_nova_interfaces__msg__CorrelatedTimestamp * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__Sequence__init(isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  isaac_ros_nova_interfaces__msg__CorrelatedTimestamp * data = NULL;

  if (size) {
    data = (isaac_ros_nova_interfaces__msg__CorrelatedTimestamp *)allocator.zero_allocate(size, sizeof(isaac_ros_nova_interfaces__msg__CorrelatedTimestamp), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__fini(&data[i - 1]);
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
isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__Sequence__fini(isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__Sequence * array)
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
      isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__fini(&array->data[i]);
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

isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__Sequence *
isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__Sequence * array = (isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__Sequence *)allocator.allocate(sizeof(isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__Sequence__destroy(isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__Sequence__are_equal(const isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__Sequence * lhs, const isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__Sequence__copy(
  const isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__Sequence * input,
  isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(isaac_ros_nova_interfaces__msg__CorrelatedTimestamp);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    isaac_ros_nova_interfaces__msg__CorrelatedTimestamp * data =
      (isaac_ros_nova_interfaces__msg__CorrelatedTimestamp *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!isaac_ros_nova_interfaces__msg__CorrelatedTimestamp__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
