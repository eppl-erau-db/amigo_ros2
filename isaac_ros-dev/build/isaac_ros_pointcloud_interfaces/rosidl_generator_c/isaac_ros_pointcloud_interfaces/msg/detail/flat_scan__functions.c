// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from isaac_ros_pointcloud_interfaces:msg/FlatScan.idl
// generated code does not contain a copyright notice
#include "isaac_ros_pointcloud_interfaces/msg/detail/flat_scan__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `angles`
// Member `ranges`
// Member `intensities`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
isaac_ros_pointcloud_interfaces__msg__FlatScan__init(isaac_ros_pointcloud_interfaces__msg__FlatScan * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    isaac_ros_pointcloud_interfaces__msg__FlatScan__fini(msg);
    return false;
  }
  // range_min
  // range_max
  // angles
  if (!rosidl_runtime_c__float__Sequence__init(&msg->angles, 0)) {
    isaac_ros_pointcloud_interfaces__msg__FlatScan__fini(msg);
    return false;
  }
  // ranges
  if (!rosidl_runtime_c__float__Sequence__init(&msg->ranges, 0)) {
    isaac_ros_pointcloud_interfaces__msg__FlatScan__fini(msg);
    return false;
  }
  // intensities
  if (!rosidl_runtime_c__float__Sequence__init(&msg->intensities, 0)) {
    isaac_ros_pointcloud_interfaces__msg__FlatScan__fini(msg);
    return false;
  }
  return true;
}

void
isaac_ros_pointcloud_interfaces__msg__FlatScan__fini(isaac_ros_pointcloud_interfaces__msg__FlatScan * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // range_min
  // range_max
  // angles
  rosidl_runtime_c__float__Sequence__fini(&msg->angles);
  // ranges
  rosidl_runtime_c__float__Sequence__fini(&msg->ranges);
  // intensities
  rosidl_runtime_c__float__Sequence__fini(&msg->intensities);
}

bool
isaac_ros_pointcloud_interfaces__msg__FlatScan__are_equal(const isaac_ros_pointcloud_interfaces__msg__FlatScan * lhs, const isaac_ros_pointcloud_interfaces__msg__FlatScan * rhs)
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
  // range_min
  if (lhs->range_min != rhs->range_min) {
    return false;
  }
  // range_max
  if (lhs->range_max != rhs->range_max) {
    return false;
  }
  // angles
  if (!rosidl_runtime_c__float__Sequence__are_equal(
      &(lhs->angles), &(rhs->angles)))
  {
    return false;
  }
  // ranges
  if (!rosidl_runtime_c__float__Sequence__are_equal(
      &(lhs->ranges), &(rhs->ranges)))
  {
    return false;
  }
  // intensities
  if (!rosidl_runtime_c__float__Sequence__are_equal(
      &(lhs->intensities), &(rhs->intensities)))
  {
    return false;
  }
  return true;
}

bool
isaac_ros_pointcloud_interfaces__msg__FlatScan__copy(
  const isaac_ros_pointcloud_interfaces__msg__FlatScan * input,
  isaac_ros_pointcloud_interfaces__msg__FlatScan * output)
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
  // range_min
  output->range_min = input->range_min;
  // range_max
  output->range_max = input->range_max;
  // angles
  if (!rosidl_runtime_c__float__Sequence__copy(
      &(input->angles), &(output->angles)))
  {
    return false;
  }
  // ranges
  if (!rosidl_runtime_c__float__Sequence__copy(
      &(input->ranges), &(output->ranges)))
  {
    return false;
  }
  // intensities
  if (!rosidl_runtime_c__float__Sequence__copy(
      &(input->intensities), &(output->intensities)))
  {
    return false;
  }
  return true;
}

isaac_ros_pointcloud_interfaces__msg__FlatScan *
isaac_ros_pointcloud_interfaces__msg__FlatScan__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  isaac_ros_pointcloud_interfaces__msg__FlatScan * msg = (isaac_ros_pointcloud_interfaces__msg__FlatScan *)allocator.allocate(sizeof(isaac_ros_pointcloud_interfaces__msg__FlatScan), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(isaac_ros_pointcloud_interfaces__msg__FlatScan));
  bool success = isaac_ros_pointcloud_interfaces__msg__FlatScan__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
isaac_ros_pointcloud_interfaces__msg__FlatScan__destroy(isaac_ros_pointcloud_interfaces__msg__FlatScan * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    isaac_ros_pointcloud_interfaces__msg__FlatScan__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
isaac_ros_pointcloud_interfaces__msg__FlatScan__Sequence__init(isaac_ros_pointcloud_interfaces__msg__FlatScan__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  isaac_ros_pointcloud_interfaces__msg__FlatScan * data = NULL;

  if (size) {
    data = (isaac_ros_pointcloud_interfaces__msg__FlatScan *)allocator.zero_allocate(size, sizeof(isaac_ros_pointcloud_interfaces__msg__FlatScan), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = isaac_ros_pointcloud_interfaces__msg__FlatScan__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        isaac_ros_pointcloud_interfaces__msg__FlatScan__fini(&data[i - 1]);
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
isaac_ros_pointcloud_interfaces__msg__FlatScan__Sequence__fini(isaac_ros_pointcloud_interfaces__msg__FlatScan__Sequence * array)
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
      isaac_ros_pointcloud_interfaces__msg__FlatScan__fini(&array->data[i]);
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

isaac_ros_pointcloud_interfaces__msg__FlatScan__Sequence *
isaac_ros_pointcloud_interfaces__msg__FlatScan__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  isaac_ros_pointcloud_interfaces__msg__FlatScan__Sequence * array = (isaac_ros_pointcloud_interfaces__msg__FlatScan__Sequence *)allocator.allocate(sizeof(isaac_ros_pointcloud_interfaces__msg__FlatScan__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = isaac_ros_pointcloud_interfaces__msg__FlatScan__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
isaac_ros_pointcloud_interfaces__msg__FlatScan__Sequence__destroy(isaac_ros_pointcloud_interfaces__msg__FlatScan__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    isaac_ros_pointcloud_interfaces__msg__FlatScan__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
isaac_ros_pointcloud_interfaces__msg__FlatScan__Sequence__are_equal(const isaac_ros_pointcloud_interfaces__msg__FlatScan__Sequence * lhs, const isaac_ros_pointcloud_interfaces__msg__FlatScan__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!isaac_ros_pointcloud_interfaces__msg__FlatScan__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
isaac_ros_pointcloud_interfaces__msg__FlatScan__Sequence__copy(
  const isaac_ros_pointcloud_interfaces__msg__FlatScan__Sequence * input,
  isaac_ros_pointcloud_interfaces__msg__FlatScan__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(isaac_ros_pointcloud_interfaces__msg__FlatScan);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    isaac_ros_pointcloud_interfaces__msg__FlatScan * data =
      (isaac_ros_pointcloud_interfaces__msg__FlatScan *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!isaac_ros_pointcloud_interfaces__msg__FlatScan__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          isaac_ros_pointcloud_interfaces__msg__FlatScan__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!isaac_ros_pointcloud_interfaces__msg__FlatScan__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
