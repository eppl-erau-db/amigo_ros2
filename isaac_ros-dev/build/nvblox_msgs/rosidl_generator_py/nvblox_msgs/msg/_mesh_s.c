// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from nvblox_msgs:msg/Mesh.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "nvblox_msgs/msg/detail/mesh__struct.h"
#include "nvblox_msgs/msg/detail/mesh__functions.h"

#include "rosidl_runtime_c/primitives_sequence.h"
#include "rosidl_runtime_c/primitives_sequence_functions.h"

// Nested array functions includes
#include "nvblox_msgs/msg/detail/index3_d__functions.h"
#include "nvblox_msgs/msg/detail/mesh_block__functions.h"
// end nested array functions include
ROSIDL_GENERATOR_C_IMPORT
bool std_msgs__msg__header__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * std_msgs__msg__header__convert_to_py(void * raw_ros_message);
bool nvblox_msgs__msg__index3_d__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * nvblox_msgs__msg__index3_d__convert_to_py(void * raw_ros_message);
bool nvblox_msgs__msg__mesh_block__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * nvblox_msgs__msg__mesh_block__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool nvblox_msgs__msg__mesh__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[27];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("nvblox_msgs.msg._mesh.Mesh", full_classname_dest, 26) == 0);
  }
  nvblox_msgs__msg__Mesh * ros_message = _ros_message;
  {  // header
    PyObject * field = PyObject_GetAttrString(_pymsg, "header");
    if (!field) {
      return false;
    }
    if (!std_msgs__msg__header__convert_from_py(field, &ros_message->header)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // block_size
    PyObject * field = PyObject_GetAttrString(_pymsg, "block_size");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->block_size = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // block_indices
    PyObject * field = PyObject_GetAttrString(_pymsg, "block_indices");
    if (!field) {
      return false;
    }
    PyObject * seq_field = PySequence_Fast(field, "expected a sequence in 'block_indices'");
    if (!seq_field) {
      Py_DECREF(field);
      return false;
    }
    Py_ssize_t size = PySequence_Size(field);
    if (-1 == size) {
      Py_DECREF(seq_field);
      Py_DECREF(field);
      return false;
    }
    if (!nvblox_msgs__msg__Index3D__Sequence__init(&(ros_message->block_indices), size)) {
      PyErr_SetString(PyExc_RuntimeError, "unable to create nvblox_msgs__msg__Index3D__Sequence ros_message");
      Py_DECREF(seq_field);
      Py_DECREF(field);
      return false;
    }
    nvblox_msgs__msg__Index3D * dest = ros_message->block_indices.data;
    for (Py_ssize_t i = 0; i < size; ++i) {
      if (!nvblox_msgs__msg__index3_d__convert_from_py(PySequence_Fast_GET_ITEM(seq_field, i), &dest[i])) {
        Py_DECREF(seq_field);
        Py_DECREF(field);
        return false;
      }
    }
    Py_DECREF(seq_field);
    Py_DECREF(field);
  }
  {  // blocks
    PyObject * field = PyObject_GetAttrString(_pymsg, "blocks");
    if (!field) {
      return false;
    }
    PyObject * seq_field = PySequence_Fast(field, "expected a sequence in 'blocks'");
    if (!seq_field) {
      Py_DECREF(field);
      return false;
    }
    Py_ssize_t size = PySequence_Size(field);
    if (-1 == size) {
      Py_DECREF(seq_field);
      Py_DECREF(field);
      return false;
    }
    if (!nvblox_msgs__msg__MeshBlock__Sequence__init(&(ros_message->blocks), size)) {
      PyErr_SetString(PyExc_RuntimeError, "unable to create nvblox_msgs__msg__MeshBlock__Sequence ros_message");
      Py_DECREF(seq_field);
      Py_DECREF(field);
      return false;
    }
    nvblox_msgs__msg__MeshBlock * dest = ros_message->blocks.data;
    for (Py_ssize_t i = 0; i < size; ++i) {
      if (!nvblox_msgs__msg__mesh_block__convert_from_py(PySequence_Fast_GET_ITEM(seq_field, i), &dest[i])) {
        Py_DECREF(seq_field);
        Py_DECREF(field);
        return false;
      }
    }
    Py_DECREF(seq_field);
    Py_DECREF(field);
  }
  {  // clear
    PyObject * field = PyObject_GetAttrString(_pymsg, "clear");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->clear = (Py_True == field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * nvblox_msgs__msg__mesh__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of Mesh */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("nvblox_msgs.msg._mesh");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "Mesh");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  nvblox_msgs__msg__Mesh * ros_message = (nvblox_msgs__msg__Mesh *)raw_ros_message;
  {  // header
    PyObject * field = NULL;
    field = std_msgs__msg__header__convert_to_py(&ros_message->header);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "header", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // block_size
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->block_size);
    {
      int rc = PyObject_SetAttrString(_pymessage, "block_size", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // block_indices
    PyObject * field = NULL;
    size_t size = ros_message->block_indices.size;
    field = PyList_New(size);
    if (!field) {
      return NULL;
    }
    nvblox_msgs__msg__Index3D * item;
    for (size_t i = 0; i < size; ++i) {
      item = &(ros_message->block_indices.data[i]);
      PyObject * pyitem = nvblox_msgs__msg__index3_d__convert_to_py(item);
      if (!pyitem) {
        Py_DECREF(field);
        return NULL;
      }
      int rc = PyList_SetItem(field, i, pyitem);
      (void)rc;
      assert(rc == 0);
    }
    assert(PySequence_Check(field));
    {
      int rc = PyObject_SetAttrString(_pymessage, "block_indices", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // blocks
    PyObject * field = NULL;
    size_t size = ros_message->blocks.size;
    field = PyList_New(size);
    if (!field) {
      return NULL;
    }
    nvblox_msgs__msg__MeshBlock * item;
    for (size_t i = 0; i < size; ++i) {
      item = &(ros_message->blocks.data[i]);
      PyObject * pyitem = nvblox_msgs__msg__mesh_block__convert_to_py(item);
      if (!pyitem) {
        Py_DECREF(field);
        return NULL;
      }
      int rc = PyList_SetItem(field, i, pyitem);
      (void)rc;
      assert(rc == 0);
    }
    assert(PySequence_Check(field));
    {
      int rc = PyObject_SetAttrString(_pymessage, "blocks", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // clear
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->clear ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "clear", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
