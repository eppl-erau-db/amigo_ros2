// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from isaac_ros_apriltag_interfaces:msg/AprilTagDetection.idl
// generated code does not contain a copyright notice
#include "isaac_ros_apriltag_interfaces/msg/detail/april_tag_detection__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `family`
#include "rosidl_runtime_c/string_functions.h"
// Member `center`
// Member `corners`
#include "geometry_msgs/msg/detail/point__functions.h"
// Member `pose`
#include "geometry_msgs/msg/detail/pose_with_covariance_stamped__functions.h"

bool
isaac_ros_apriltag_interfaces__msg__AprilTagDetection__init(isaac_ros_apriltag_interfaces__msg__AprilTagDetection * msg)
{
  if (!msg) {
    return false;
  }
  // family
  if (!rosidl_runtime_c__String__init(&msg->family)) {
    isaac_ros_apriltag_interfaces__msg__AprilTagDetection__fini(msg);
    return false;
  }
  // id
  // center
  if (!geometry_msgs__msg__Point__init(&msg->center)) {
    isaac_ros_apriltag_interfaces__msg__AprilTagDetection__fini(msg);
    return false;
  }
  // corners
  for (size_t i = 0; i < 4; ++i) {
    if (!geometry_msgs__msg__Point__init(&msg->corners[i])) {
      isaac_ros_apriltag_interfaces__msg__AprilTagDetection__fini(msg);
      return false;
    }
  }
  // pose
  if (!geometry_msgs__msg__PoseWithCovarianceStamped__init(&msg->pose)) {
    isaac_ros_apriltag_interfaces__msg__AprilTagDetection__fini(msg);
    return false;
  }
  return true;
}

void
isaac_ros_apriltag_interfaces__msg__AprilTagDetection__fini(isaac_ros_apriltag_interfaces__msg__AprilTagDetection * msg)
{
  if (!msg) {
    return;
  }
  // family
  rosidl_runtime_c__String__fini(&msg->family);
  // id
  // center
  geometry_msgs__msg__Point__fini(&msg->center);
  // corners
  for (size_t i = 0; i < 4; ++i) {
    geometry_msgs__msg__Point__fini(&msg->corners[i]);
  }
  // pose
  geometry_msgs__msg__PoseWithCovarianceStamped__fini(&msg->pose);
}

bool
isaac_ros_apriltag_interfaces__msg__AprilTagDetection__are_equal(const isaac_ros_apriltag_interfaces__msg__AprilTagDetection * lhs, const isaac_ros_apriltag_interfaces__msg__AprilTagDetection * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // family
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->family), &(rhs->family)))
  {
    return false;
  }
  // id
  if (lhs->id != rhs->id) {
    return false;
  }
  // center
  if (!geometry_msgs__msg__Point__are_equal(
      &(lhs->center), &(rhs->center)))
  {
    return false;
  }
  // corners
  for (size_t i = 0; i < 4; ++i) {
    if (!geometry_msgs__msg__Point__are_equal(
        &(lhs->corners[i]), &(rhs->corners[i])))
    {
      return false;
    }
  }
  // pose
  if (!geometry_msgs__msg__PoseWithCovarianceStamped__are_equal(
      &(lhs->pose), &(rhs->pose)))
  {
    return false;
  }
  return true;
}

bool
isaac_ros_apriltag_interfaces__msg__AprilTagDetection__copy(
  const isaac_ros_apriltag_interfaces__msg__AprilTagDetection * input,
  isaac_ros_apriltag_interfaces__msg__AprilTagDetection * output)
{
  if (!input || !output) {
    return false;
  }
  // family
  if (!rosidl_runtime_c__String__copy(
      &(input->family), &(output->family)))
  {
    return false;
  }
  // id
  output->id = input->id;
  // center
  if (!geometry_msgs__msg__Point__copy(
      &(input->center), &(output->center)))
  {
    return false;
  }
  // corners
  for (size_t i = 0; i < 4; ++i) {
    if (!geometry_msgs__msg__Point__copy(
        &(input->corners[i]), &(output->corners[i])))
    {
      return false;
    }
  }
  // pose
  if (!geometry_msgs__msg__PoseWithCovarianceStamped__copy(
      &(input->pose), &(output->pose)))
  {
    return false;
  }
  return true;
}

isaac_ros_apriltag_interfaces__msg__AprilTagDetection *
isaac_ros_apriltag_interfaces__msg__AprilTagDetection__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  isaac_ros_apriltag_interfaces__msg__AprilTagDetection * msg = (isaac_ros_apriltag_interfaces__msg__AprilTagDetection *)allocator.allocate(sizeof(isaac_ros_apriltag_interfaces__msg__AprilTagDetection), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(isaac_ros_apriltag_interfaces__msg__AprilTagDetection));
  bool success = isaac_ros_apriltag_interfaces__msg__AprilTagDetection__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
isaac_ros_apriltag_interfaces__msg__AprilTagDetection__destroy(isaac_ros_apriltag_interfaces__msg__AprilTagDetection * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    isaac_ros_apriltag_interfaces__msg__AprilTagDetection__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
isaac_ros_apriltag_interfaces__msg__AprilTagDetection__Sequence__init(isaac_ros_apriltag_interfaces__msg__AprilTagDetection__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  isaac_ros_apriltag_interfaces__msg__AprilTagDetection * data = NULL;

  if (size) {
    data = (isaac_ros_apriltag_interfaces__msg__AprilTagDetection *)allocator.zero_allocate(size, sizeof(isaac_ros_apriltag_interfaces__msg__AprilTagDetection), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = isaac_ros_apriltag_interfaces__msg__AprilTagDetection__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        isaac_ros_apriltag_interfaces__msg__AprilTagDetection__fini(&data[i - 1]);
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
isaac_ros_apriltag_interfaces__msg__AprilTagDetection__Sequence__fini(isaac_ros_apriltag_interfaces__msg__AprilTagDetection__Sequence * array)
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
      isaac_ros_apriltag_interfaces__msg__AprilTagDetection__fini(&array->data[i]);
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

isaac_ros_apriltag_interfaces__msg__AprilTagDetection__Sequence *
isaac_ros_apriltag_interfaces__msg__AprilTagDetection__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  isaac_ros_apriltag_interfaces__msg__AprilTagDetection__Sequence * array = (isaac_ros_apriltag_interfaces__msg__AprilTagDetection__Sequence *)allocator.allocate(sizeof(isaac_ros_apriltag_interfaces__msg__AprilTagDetection__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = isaac_ros_apriltag_interfaces__msg__AprilTagDetection__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
isaac_ros_apriltag_interfaces__msg__AprilTagDetection__Sequence__destroy(isaac_ros_apriltag_interfaces__msg__AprilTagDetection__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    isaac_ros_apriltag_interfaces__msg__AprilTagDetection__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
isaac_ros_apriltag_interfaces__msg__AprilTagDetection__Sequence__are_equal(const isaac_ros_apriltag_interfaces__msg__AprilTagDetection__Sequence * lhs, const isaac_ros_apriltag_interfaces__msg__AprilTagDetection__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!isaac_ros_apriltag_interfaces__msg__AprilTagDetection__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
isaac_ros_apriltag_interfaces__msg__AprilTagDetection__Sequence__copy(
  const isaac_ros_apriltag_interfaces__msg__AprilTagDetection__Sequence * input,
  isaac_ros_apriltag_interfaces__msg__AprilTagDetection__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(isaac_ros_apriltag_interfaces__msg__AprilTagDetection);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    isaac_ros_apriltag_interfaces__msg__AprilTagDetection * data =
      (isaac_ros_apriltag_interfaces__msg__AprilTagDetection *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!isaac_ros_apriltag_interfaces__msg__AprilTagDetection__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          isaac_ros_apriltag_interfaces__msg__AprilTagDetection__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!isaac_ros_apriltag_interfaces__msg__AprilTagDetection__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
