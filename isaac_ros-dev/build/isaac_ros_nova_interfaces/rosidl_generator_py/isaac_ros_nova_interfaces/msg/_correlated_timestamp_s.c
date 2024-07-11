// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from isaac_ros_nova_interfaces:msg/CorrelatedTimestamp.idl
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
#include "isaac_ros_nova_interfaces/msg/detail/correlated_timestamp__struct.h"
#include "isaac_ros_nova_interfaces/msg/detail/correlated_timestamp__functions.h"

ROSIDL_GENERATOR_C_IMPORT
bool std_msgs__msg__header__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * std_msgs__msg__header__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool isaac_ros_nova_interfaces__msg__correlated_timestamp__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[72];
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
    assert(strncmp("isaac_ros_nova_interfaces.msg._correlated_timestamp.CorrelatedTimestamp", full_classname_dest, 71) == 0);
  }
  isaac_ros_nova_interfaces__msg__CorrelatedTimestamp * ros_message = _ros_message;
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
  {  // phc_val
    PyObject * field = PyObject_GetAttrString(_pymsg, "phc_val");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->phc_val = PyLong_AsUnsignedLongLong(field);
    Py_DECREF(field);
  }
  {  // tsc_val
    PyObject * field = PyObject_GetAttrString(_pymsg, "tsc_val");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->tsc_val = PyLong_AsUnsignedLongLong(field);
    Py_DECREF(field);
  }
  {  // phc2_val
    PyObject * field = PyObject_GetAttrString(_pymsg, "phc2_val");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->phc2_val = PyLong_AsUnsignedLongLong(field);
    Py_DECREF(field);
  }
  {  // sys_val
    PyObject * field = PyObject_GetAttrString(_pymsg, "sys_val");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->sys_val = PyLong_AsUnsignedLongLong(field);
    Py_DECREF(field);
  }
  {  // phc_latency
    PyObject * field = PyObject_GetAttrString(_pymsg, "phc_latency");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->phc_latency = PyLong_AsUnsignedLongLong(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * isaac_ros_nova_interfaces__msg__correlated_timestamp__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of CorrelatedTimestamp */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("isaac_ros_nova_interfaces.msg._correlated_timestamp");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "CorrelatedTimestamp");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  isaac_ros_nova_interfaces__msg__CorrelatedTimestamp * ros_message = (isaac_ros_nova_interfaces__msg__CorrelatedTimestamp *)raw_ros_message;
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
  {  // phc_val
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLongLong(ros_message->phc_val);
    {
      int rc = PyObject_SetAttrString(_pymessage, "phc_val", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // tsc_val
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLongLong(ros_message->tsc_val);
    {
      int rc = PyObject_SetAttrString(_pymessage, "tsc_val", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // phc2_val
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLongLong(ros_message->phc2_val);
    {
      int rc = PyObject_SetAttrString(_pymessage, "phc2_val", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // sys_val
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLongLong(ros_message->sys_val);
    {
      int rc = PyObject_SetAttrString(_pymessage, "sys_val", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // phc_latency
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLongLong(ros_message->phc_latency);
    {
      int rc = PyObject_SetAttrString(_pymessage, "phc_latency", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
