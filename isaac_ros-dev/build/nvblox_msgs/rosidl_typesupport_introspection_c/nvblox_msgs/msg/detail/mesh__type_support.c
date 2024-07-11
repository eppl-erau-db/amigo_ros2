// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from nvblox_msgs:msg/Mesh.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "nvblox_msgs/msg/detail/mesh__rosidl_typesupport_introspection_c.h"
#include "nvblox_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "nvblox_msgs/msg/detail/mesh__functions.h"
#include "nvblox_msgs/msg/detail/mesh__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `block_indices`
#include "nvblox_msgs/msg/index3_d.h"
// Member `block_indices`
#include "nvblox_msgs/msg/detail/index3_d__rosidl_typesupport_introspection_c.h"
// Member `blocks`
#include "nvblox_msgs/msg/mesh_block.h"
// Member `blocks`
#include "nvblox_msgs/msg/detail/mesh_block__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__Mesh_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  nvblox_msgs__msg__Mesh__init(message_memory);
}

void nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__Mesh_fini_function(void * message_memory)
{
  nvblox_msgs__msg__Mesh__fini(message_memory);
}

size_t nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__size_function__Mesh__block_indices(
  const void * untyped_member)
{
  const nvblox_msgs__msg__Index3D__Sequence * member =
    (const nvblox_msgs__msg__Index3D__Sequence *)(untyped_member);
  return member->size;
}

const void * nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__get_const_function__Mesh__block_indices(
  const void * untyped_member, size_t index)
{
  const nvblox_msgs__msg__Index3D__Sequence * member =
    (const nvblox_msgs__msg__Index3D__Sequence *)(untyped_member);
  return &member->data[index];
}

void * nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__get_function__Mesh__block_indices(
  void * untyped_member, size_t index)
{
  nvblox_msgs__msg__Index3D__Sequence * member =
    (nvblox_msgs__msg__Index3D__Sequence *)(untyped_member);
  return &member->data[index];
}

void nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__fetch_function__Mesh__block_indices(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const nvblox_msgs__msg__Index3D * item =
    ((const nvblox_msgs__msg__Index3D *)
    nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__get_const_function__Mesh__block_indices(untyped_member, index));
  nvblox_msgs__msg__Index3D * value =
    (nvblox_msgs__msg__Index3D *)(untyped_value);
  *value = *item;
}

void nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__assign_function__Mesh__block_indices(
  void * untyped_member, size_t index, const void * untyped_value)
{
  nvblox_msgs__msg__Index3D * item =
    ((nvblox_msgs__msg__Index3D *)
    nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__get_function__Mesh__block_indices(untyped_member, index));
  const nvblox_msgs__msg__Index3D * value =
    (const nvblox_msgs__msg__Index3D *)(untyped_value);
  *item = *value;
}

bool nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__resize_function__Mesh__block_indices(
  void * untyped_member, size_t size)
{
  nvblox_msgs__msg__Index3D__Sequence * member =
    (nvblox_msgs__msg__Index3D__Sequence *)(untyped_member);
  nvblox_msgs__msg__Index3D__Sequence__fini(member);
  return nvblox_msgs__msg__Index3D__Sequence__init(member, size);
}

size_t nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__size_function__Mesh__blocks(
  const void * untyped_member)
{
  const nvblox_msgs__msg__MeshBlock__Sequence * member =
    (const nvblox_msgs__msg__MeshBlock__Sequence *)(untyped_member);
  return member->size;
}

const void * nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__get_const_function__Mesh__blocks(
  const void * untyped_member, size_t index)
{
  const nvblox_msgs__msg__MeshBlock__Sequence * member =
    (const nvblox_msgs__msg__MeshBlock__Sequence *)(untyped_member);
  return &member->data[index];
}

void * nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__get_function__Mesh__blocks(
  void * untyped_member, size_t index)
{
  nvblox_msgs__msg__MeshBlock__Sequence * member =
    (nvblox_msgs__msg__MeshBlock__Sequence *)(untyped_member);
  return &member->data[index];
}

void nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__fetch_function__Mesh__blocks(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const nvblox_msgs__msg__MeshBlock * item =
    ((const nvblox_msgs__msg__MeshBlock *)
    nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__get_const_function__Mesh__blocks(untyped_member, index));
  nvblox_msgs__msg__MeshBlock * value =
    (nvblox_msgs__msg__MeshBlock *)(untyped_value);
  *value = *item;
}

void nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__assign_function__Mesh__blocks(
  void * untyped_member, size_t index, const void * untyped_value)
{
  nvblox_msgs__msg__MeshBlock * item =
    ((nvblox_msgs__msg__MeshBlock *)
    nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__get_function__Mesh__blocks(untyped_member, index));
  const nvblox_msgs__msg__MeshBlock * value =
    (const nvblox_msgs__msg__MeshBlock *)(untyped_value);
  *item = *value;
}

bool nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__resize_function__Mesh__blocks(
  void * untyped_member, size_t size)
{
  nvblox_msgs__msg__MeshBlock__Sequence * member =
    (nvblox_msgs__msg__MeshBlock__Sequence *)(untyped_member);
  nvblox_msgs__msg__MeshBlock__Sequence__fini(member);
  return nvblox_msgs__msg__MeshBlock__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__Mesh_message_member_array[5] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(nvblox_msgs__msg__Mesh, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "block_size",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(nvblox_msgs__msg__Mesh, block_size),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "block_indices",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(nvblox_msgs__msg__Mesh, block_indices),  // bytes offset in struct
    NULL,  // default value
    nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__size_function__Mesh__block_indices,  // size() function pointer
    nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__get_const_function__Mesh__block_indices,  // get_const(index) function pointer
    nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__get_function__Mesh__block_indices,  // get(index) function pointer
    nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__fetch_function__Mesh__block_indices,  // fetch(index, &value) function pointer
    nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__assign_function__Mesh__block_indices,  // assign(index, value) function pointer
    nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__resize_function__Mesh__block_indices  // resize(index) function pointer
  },
  {
    "blocks",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(nvblox_msgs__msg__Mesh, blocks),  // bytes offset in struct
    NULL,  // default value
    nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__size_function__Mesh__blocks,  // size() function pointer
    nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__get_const_function__Mesh__blocks,  // get_const(index) function pointer
    nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__get_function__Mesh__blocks,  // get(index) function pointer
    nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__fetch_function__Mesh__blocks,  // fetch(index, &value) function pointer
    nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__assign_function__Mesh__blocks,  // assign(index, value) function pointer
    nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__resize_function__Mesh__blocks  // resize(index) function pointer
  },
  {
    "clear",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(nvblox_msgs__msg__Mesh, clear),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__Mesh_message_members = {
  "nvblox_msgs__msg",  // message namespace
  "Mesh",  // message name
  5,  // number of fields
  sizeof(nvblox_msgs__msg__Mesh),
  nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__Mesh_message_member_array,  // message members
  nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__Mesh_init_function,  // function to initialize message memory (memory has to be allocated)
  nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__Mesh_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__Mesh_message_type_support_handle = {
  0,
  &nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__Mesh_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_nvblox_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, nvblox_msgs, msg, Mesh)() {
  nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__Mesh_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__Mesh_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, nvblox_msgs, msg, Index3D)();
  nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__Mesh_message_member_array[3].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, nvblox_msgs, msg, MeshBlock)();
  if (!nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__Mesh_message_type_support_handle.typesupport_identifier) {
    nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__Mesh_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &nvblox_msgs__msg__Mesh__rosidl_typesupport_introspection_c__Mesh_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
