// generated from rosidl_generator_py/resource/_idl_pkg_typesupport_entry_point.c.em
// generated code does not contain a copyright notice
#include <Python.h>

static PyMethodDef isaac_ros_pointcloud_interfaces__methods[] = {
  {NULL, NULL, 0, NULL}  /* sentinel */
};

static struct PyModuleDef isaac_ros_pointcloud_interfaces__module = {
  PyModuleDef_HEAD_INIT,
  "_isaac_ros_pointcloud_interfaces_support",
  "_isaac_ros_pointcloud_interfaces_doc",
  -1,  /* -1 means that the module keeps state in global variables */
  isaac_ros_pointcloud_interfaces__methods,
  NULL,
  NULL,
  NULL,
  NULL,
};

#include <stdbool.h>
#include <stdint.h>
#include "rosidl_runtime_c/visibility_control.h"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_runtime_c/service_type_support_struct.h"
#include "rosidl_runtime_c/action_type_support_struct.h"
#include "isaac_ros_pointcloud_interfaces/msg/detail/flat_scan__type_support.h"
#include "isaac_ros_pointcloud_interfaces/msg/detail/flat_scan__struct.h"
#include "isaac_ros_pointcloud_interfaces/msg/detail/flat_scan__functions.h"

static void * isaac_ros_pointcloud_interfaces__msg__flat_scan__create_ros_message(void)
{
  return isaac_ros_pointcloud_interfaces__msg__FlatScan__create();
}

static void isaac_ros_pointcloud_interfaces__msg__flat_scan__destroy_ros_message(void * raw_ros_message)
{
  isaac_ros_pointcloud_interfaces__msg__FlatScan * ros_message = (isaac_ros_pointcloud_interfaces__msg__FlatScan *)raw_ros_message;
  isaac_ros_pointcloud_interfaces__msg__FlatScan__destroy(ros_message);
}

ROSIDL_GENERATOR_C_IMPORT
bool isaac_ros_pointcloud_interfaces__msg__flat_scan__convert_from_py(PyObject * _pymsg, void * ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * isaac_ros_pointcloud_interfaces__msg__flat_scan__convert_to_py(void * raw_ros_message);


ROSIDL_GENERATOR_C_IMPORT
const rosidl_message_type_support_t *
ROSIDL_GET_MSG_TYPE_SUPPORT(isaac_ros_pointcloud_interfaces, msg, FlatScan);

int8_t
_register_msg_type__msg__flat_scan(PyObject * pymodule)
{
  int8_t err;

  PyObject * pyobject_create_ros_message = NULL;
  pyobject_create_ros_message = PyCapsule_New(
    (void *)&isaac_ros_pointcloud_interfaces__msg__flat_scan__create_ros_message,
    NULL, NULL);
  if (!pyobject_create_ros_message) {
    // previously added objects will be removed when the module is destroyed
    return -1;
  }
  err = PyModule_AddObject(
    pymodule,
    "create_ros_message_msg__msg__flat_scan",
    pyobject_create_ros_message);
  if (err) {
    // the created capsule needs to be decremented
    Py_XDECREF(pyobject_create_ros_message);
    // previously added objects will be removed when the module is destroyed
    return err;
  }

  PyObject * pyobject_destroy_ros_message = NULL;
  pyobject_destroy_ros_message = PyCapsule_New(
    (void *)&isaac_ros_pointcloud_interfaces__msg__flat_scan__destroy_ros_message,
    NULL, NULL);
  if (!pyobject_destroy_ros_message) {
    // previously added objects will be removed when the module is destroyed
    return -1;
  }
  err = PyModule_AddObject(
    pymodule,
    "destroy_ros_message_msg__msg__flat_scan",
    pyobject_destroy_ros_message);
  if (err) {
    // the created capsule needs to be decremented
    Py_XDECREF(pyobject_destroy_ros_message);
    // previously added objects will be removed when the module is destroyed
    return err;
  }

  PyObject * pyobject_convert_from_py = NULL;
  pyobject_convert_from_py = PyCapsule_New(
    (void *)&isaac_ros_pointcloud_interfaces__msg__flat_scan__convert_from_py,
    NULL, NULL);
  if (!pyobject_convert_from_py) {
    // previously added objects will be removed when the module is destroyed
    return -1;
  }
  err = PyModule_AddObject(
    pymodule,
    "convert_from_py_msg__msg__flat_scan",
    pyobject_convert_from_py);
  if (err) {
    // the created capsule needs to be decremented
    Py_XDECREF(pyobject_convert_from_py);
    // previously added objects will be removed when the module is destroyed
    return err;
  }

  PyObject * pyobject_convert_to_py = NULL;
  pyobject_convert_to_py = PyCapsule_New(
    (void *)&isaac_ros_pointcloud_interfaces__msg__flat_scan__convert_to_py,
    NULL, NULL);
  if (!pyobject_convert_to_py) {
    // previously added objects will be removed when the module is destroyed
    return -1;
  }
  err = PyModule_AddObject(
    pymodule,
    "convert_to_py_msg__msg__flat_scan",
    pyobject_convert_to_py);
  if (err) {
    // the created capsule needs to be decremented
    Py_XDECREF(pyobject_convert_to_py);
    // previously added objects will be removed when the module is destroyed
    return err;
  }

  PyObject * pyobject_type_support = NULL;
  pyobject_type_support = PyCapsule_New(
    (void *)ROSIDL_GET_MSG_TYPE_SUPPORT(isaac_ros_pointcloud_interfaces, msg, FlatScan),
    NULL, NULL);
  if (!pyobject_type_support) {
    // previously added objects will be removed when the module is destroyed
    return -1;
  }
  err = PyModule_AddObject(
    pymodule,
    "type_support_msg__msg__flat_scan",
    pyobject_type_support);
  if (err) {
    // the created capsule needs to be decremented
    Py_XDECREF(pyobject_type_support);
    // previously added objects will be removed when the module is destroyed
    return err;
  }
  return 0;
}

PyMODINIT_FUNC
PyInit_isaac_ros_pointcloud_interfaces_s__rosidl_typesupport_c(void)
{
  PyObject * pymodule = NULL;
  pymodule = PyModule_Create(&isaac_ros_pointcloud_interfaces__module);
  if (!pymodule) {
    return NULL;
  }
  int8_t err;

  err = _register_msg_type__msg__flat_scan(pymodule);
  if (err) {
    Py_XDECREF(pymodule);
    return NULL;
  }

  return pymodule;
}
