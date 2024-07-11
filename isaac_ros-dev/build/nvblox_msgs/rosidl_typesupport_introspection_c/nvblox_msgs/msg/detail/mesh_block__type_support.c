// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from nvblox_msgs:msg/MeshBlock.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "nvblox_msgs/msg/detail/mesh_block__rosidl_typesupport_introspection_c.h"
#include "nvblox_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "nvblox_msgs/msg/detail/mesh_block__functions.h"
#include "nvblox_msgs/msg/detail/mesh_block__struct.h"


// Include directives for member types
// Member `vertices`
// Member `normals`
#include "geometry_msgs/msg/point32.h"
// Member `vertices`
// Member `normals`
#include "geometry_msgs/msg/detail/point32__rosidl_typesupport_introspection_c.h"
// Member `colors`
#include "std_msgs/msg/color_rgba.h"
// Member `colors`
#include "std_msgs/msg/detail/color_rgba__rosidl_typesupport_introspection_c.h"
// Member `triangles`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__MeshBlock_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  nvblox_msgs__msg__MeshBlock__init(message_memory);
}

void nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__MeshBlock_fini_function(void * message_memory)
{
  nvblox_msgs__msg__MeshBlock__fini(message_memory);
}

size_t nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__size_function__MeshBlock__vertices(
  const void * untyped_member)
{
  const geometry_msgs__msg__Point32__Sequence * member =
    (const geometry_msgs__msg__Point32__Sequence *)(untyped_member);
  return member->size;
}

const void * nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__get_const_function__MeshBlock__vertices(
  const void * untyped_member, size_t index)
{
  const geometry_msgs__msg__Point32__Sequence * member =
    (const geometry_msgs__msg__Point32__Sequence *)(untyped_member);
  return &member->data[index];
}

void * nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__get_function__MeshBlock__vertices(
  void * untyped_member, size_t index)
{
  geometry_msgs__msg__Point32__Sequence * member =
    (geometry_msgs__msg__Point32__Sequence *)(untyped_member);
  return &member->data[index];
}

void nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__fetch_function__MeshBlock__vertices(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const geometry_msgs__msg__Point32 * item =
    ((const geometry_msgs__msg__Point32 *)
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__get_const_function__MeshBlock__vertices(untyped_member, index));
  geometry_msgs__msg__Point32 * value =
    (geometry_msgs__msg__Point32 *)(untyped_value);
  *value = *item;
}

void nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__assign_function__MeshBlock__vertices(
  void * untyped_member, size_t index, const void * untyped_value)
{
  geometry_msgs__msg__Point32 * item =
    ((geometry_msgs__msg__Point32 *)
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__get_function__MeshBlock__vertices(untyped_member, index));
  const geometry_msgs__msg__Point32 * value =
    (const geometry_msgs__msg__Point32 *)(untyped_value);
  *item = *value;
}

bool nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__resize_function__MeshBlock__vertices(
  void * untyped_member, size_t size)
{
  geometry_msgs__msg__Point32__Sequence * member =
    (geometry_msgs__msg__Point32__Sequence *)(untyped_member);
  geometry_msgs__msg__Point32__Sequence__fini(member);
  return geometry_msgs__msg__Point32__Sequence__init(member, size);
}

size_t nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__size_function__MeshBlock__normals(
  const void * untyped_member)
{
  const geometry_msgs__msg__Point32__Sequence * member =
    (const geometry_msgs__msg__Point32__Sequence *)(untyped_member);
  return member->size;
}

const void * nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__get_const_function__MeshBlock__normals(
  const void * untyped_member, size_t index)
{
  const geometry_msgs__msg__Point32__Sequence * member =
    (const geometry_msgs__msg__Point32__Sequence *)(untyped_member);
  return &member->data[index];
}

void * nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__get_function__MeshBlock__normals(
  void * untyped_member, size_t index)
{
  geometry_msgs__msg__Point32__Sequence * member =
    (geometry_msgs__msg__Point32__Sequence *)(untyped_member);
  return &member->data[index];
}

void nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__fetch_function__MeshBlock__normals(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const geometry_msgs__msg__Point32 * item =
    ((const geometry_msgs__msg__Point32 *)
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__get_const_function__MeshBlock__normals(untyped_member, index));
  geometry_msgs__msg__Point32 * value =
    (geometry_msgs__msg__Point32 *)(untyped_value);
  *value = *item;
}

void nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__assign_function__MeshBlock__normals(
  void * untyped_member, size_t index, const void * untyped_value)
{
  geometry_msgs__msg__Point32 * item =
    ((geometry_msgs__msg__Point32 *)
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__get_function__MeshBlock__normals(untyped_member, index));
  const geometry_msgs__msg__Point32 * value =
    (const geometry_msgs__msg__Point32 *)(untyped_value);
  *item = *value;
}

bool nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__resize_function__MeshBlock__normals(
  void * untyped_member, size_t size)
{
  geometry_msgs__msg__Point32__Sequence * member =
    (geometry_msgs__msg__Point32__Sequence *)(untyped_member);
  geometry_msgs__msg__Point32__Sequence__fini(member);
  return geometry_msgs__msg__Point32__Sequence__init(member, size);
}

size_t nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__size_function__MeshBlock__colors(
  const void * untyped_member)
{
  const std_msgs__msg__ColorRGBA__Sequence * member =
    (const std_msgs__msg__ColorRGBA__Sequence *)(untyped_member);
  return member->size;
}

const void * nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__get_const_function__MeshBlock__colors(
  const void * untyped_member, size_t index)
{
  const std_msgs__msg__ColorRGBA__Sequence * member =
    (const std_msgs__msg__ColorRGBA__Sequence *)(untyped_member);
  return &member->data[index];
}

void * nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__get_function__MeshBlock__colors(
  void * untyped_member, size_t index)
{
  std_msgs__msg__ColorRGBA__Sequence * member =
    (std_msgs__msg__ColorRGBA__Sequence *)(untyped_member);
  return &member->data[index];
}

void nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__fetch_function__MeshBlock__colors(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const std_msgs__msg__ColorRGBA * item =
    ((const std_msgs__msg__ColorRGBA *)
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__get_const_function__MeshBlock__colors(untyped_member, index));
  std_msgs__msg__ColorRGBA * value =
    (std_msgs__msg__ColorRGBA *)(untyped_value);
  *value = *item;
}

void nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__assign_function__MeshBlock__colors(
  void * untyped_member, size_t index, const void * untyped_value)
{
  std_msgs__msg__ColorRGBA * item =
    ((std_msgs__msg__ColorRGBA *)
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__get_function__MeshBlock__colors(untyped_member, index));
  const std_msgs__msg__ColorRGBA * value =
    (const std_msgs__msg__ColorRGBA *)(untyped_value);
  *item = *value;
}

bool nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__resize_function__MeshBlock__colors(
  void * untyped_member, size_t size)
{
  std_msgs__msg__ColorRGBA__Sequence * member =
    (std_msgs__msg__ColorRGBA__Sequence *)(untyped_member);
  std_msgs__msg__ColorRGBA__Sequence__fini(member);
  return std_msgs__msg__ColorRGBA__Sequence__init(member, size);
}

size_t nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__size_function__MeshBlock__triangles(
  const void * untyped_member)
{
  const rosidl_runtime_c__int32__Sequence * member =
    (const rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return member->size;
}

const void * nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__get_const_function__MeshBlock__triangles(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__int32__Sequence * member =
    (const rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return &member->data[index];
}

void * nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__get_function__MeshBlock__triangles(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__int32__Sequence * member =
    (rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return &member->data[index];
}

void nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__fetch_function__MeshBlock__triangles(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const int32_t * item =
    ((const int32_t *)
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__get_const_function__MeshBlock__triangles(untyped_member, index));
  int32_t * value =
    (int32_t *)(untyped_value);
  *value = *item;
}

void nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__assign_function__MeshBlock__triangles(
  void * untyped_member, size_t index, const void * untyped_value)
{
  int32_t * item =
    ((int32_t *)
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__get_function__MeshBlock__triangles(untyped_member, index));
  const int32_t * value =
    (const int32_t *)(untyped_value);
  *item = *value;
}

bool nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__resize_function__MeshBlock__triangles(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__int32__Sequence * member =
    (rosidl_runtime_c__int32__Sequence *)(untyped_member);
  rosidl_runtime_c__int32__Sequence__fini(member);
  return rosidl_runtime_c__int32__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__MeshBlock_message_member_array[4] = {
  {
    "vertices",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(nvblox_msgs__msg__MeshBlock, vertices),  // bytes offset in struct
    NULL,  // default value
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__size_function__MeshBlock__vertices,  // size() function pointer
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__get_const_function__MeshBlock__vertices,  // get_const(index) function pointer
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__get_function__MeshBlock__vertices,  // get(index) function pointer
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__fetch_function__MeshBlock__vertices,  // fetch(index, &value) function pointer
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__assign_function__MeshBlock__vertices,  // assign(index, value) function pointer
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__resize_function__MeshBlock__vertices  // resize(index) function pointer
  },
  {
    "normals",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(nvblox_msgs__msg__MeshBlock, normals),  // bytes offset in struct
    NULL,  // default value
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__size_function__MeshBlock__normals,  // size() function pointer
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__get_const_function__MeshBlock__normals,  // get_const(index) function pointer
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__get_function__MeshBlock__normals,  // get(index) function pointer
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__fetch_function__MeshBlock__normals,  // fetch(index, &value) function pointer
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__assign_function__MeshBlock__normals,  // assign(index, value) function pointer
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__resize_function__MeshBlock__normals  // resize(index) function pointer
  },
  {
    "colors",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(nvblox_msgs__msg__MeshBlock, colors),  // bytes offset in struct
    NULL,  // default value
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__size_function__MeshBlock__colors,  // size() function pointer
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__get_const_function__MeshBlock__colors,  // get_const(index) function pointer
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__get_function__MeshBlock__colors,  // get(index) function pointer
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__fetch_function__MeshBlock__colors,  // fetch(index, &value) function pointer
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__assign_function__MeshBlock__colors,  // assign(index, value) function pointer
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__resize_function__MeshBlock__colors  // resize(index) function pointer
  },
  {
    "triangles",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(nvblox_msgs__msg__MeshBlock, triangles),  // bytes offset in struct
    NULL,  // default value
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__size_function__MeshBlock__triangles,  // size() function pointer
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__get_const_function__MeshBlock__triangles,  // get_const(index) function pointer
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__get_function__MeshBlock__triangles,  // get(index) function pointer
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__fetch_function__MeshBlock__triangles,  // fetch(index, &value) function pointer
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__assign_function__MeshBlock__triangles,  // assign(index, value) function pointer
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__resize_function__MeshBlock__triangles  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__MeshBlock_message_members = {
  "nvblox_msgs__msg",  // message namespace
  "MeshBlock",  // message name
  4,  // number of fields
  sizeof(nvblox_msgs__msg__MeshBlock),
  nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__MeshBlock_message_member_array,  // message members
  nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__MeshBlock_init_function,  // function to initialize message memory (memory has to be allocated)
  nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__MeshBlock_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__MeshBlock_message_type_support_handle = {
  0,
  &nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__MeshBlock_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_nvblox_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, nvblox_msgs, msg, MeshBlock)() {
  nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__MeshBlock_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Point32)();
  nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__MeshBlock_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Point32)();
  nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__MeshBlock_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, ColorRGBA)();
  if (!nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__MeshBlock_message_type_support_handle.typesupport_identifier) {
    nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__MeshBlock_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &nvblox_msgs__msg__MeshBlock__rosidl_typesupport_introspection_c__MeshBlock_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
