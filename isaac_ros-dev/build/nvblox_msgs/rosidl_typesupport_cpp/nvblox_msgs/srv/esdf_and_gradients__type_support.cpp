// generated from rosidl_typesupport_cpp/resource/idl__type_support.cpp.em
// with input from nvblox_msgs:srv/EsdfAndGradients.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "nvblox_msgs/srv/detail/esdf_and_gradients__struct.hpp"
#include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
#include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace nvblox_msgs
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _EsdfAndGradients_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _EsdfAndGradients_Request_type_support_ids_t;

static const _EsdfAndGradients_Request_type_support_ids_t _EsdfAndGradients_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _EsdfAndGradients_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _EsdfAndGradients_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _EsdfAndGradients_Request_type_support_symbol_names_t _EsdfAndGradients_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, nvblox_msgs, srv, EsdfAndGradients_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, nvblox_msgs, srv, EsdfAndGradients_Request)),
  }
};

typedef struct _EsdfAndGradients_Request_type_support_data_t
{
  void * data[2];
} _EsdfAndGradients_Request_type_support_data_t;

static _EsdfAndGradients_Request_type_support_data_t _EsdfAndGradients_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _EsdfAndGradients_Request_message_typesupport_map = {
  2,
  "nvblox_msgs",
  &_EsdfAndGradients_Request_message_typesupport_ids.typesupport_identifier[0],
  &_EsdfAndGradients_Request_message_typesupport_symbol_names.symbol_name[0],
  &_EsdfAndGradients_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t EsdfAndGradients_Request_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_EsdfAndGradients_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace nvblox_msgs

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<nvblox_msgs::srv::EsdfAndGradients_Request>()
{
  return &::nvblox_msgs::srv::rosidl_typesupport_cpp::EsdfAndGradients_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, nvblox_msgs, srv, EsdfAndGradients_Request)() {
  return get_message_type_support_handle<nvblox_msgs::srv::EsdfAndGradients_Request>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "nvblox_msgs/srv/detail/esdf_and_gradients__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace nvblox_msgs
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _EsdfAndGradients_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _EsdfAndGradients_Response_type_support_ids_t;

static const _EsdfAndGradients_Response_type_support_ids_t _EsdfAndGradients_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _EsdfAndGradients_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _EsdfAndGradients_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _EsdfAndGradients_Response_type_support_symbol_names_t _EsdfAndGradients_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, nvblox_msgs, srv, EsdfAndGradients_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, nvblox_msgs, srv, EsdfAndGradients_Response)),
  }
};

typedef struct _EsdfAndGradients_Response_type_support_data_t
{
  void * data[2];
} _EsdfAndGradients_Response_type_support_data_t;

static _EsdfAndGradients_Response_type_support_data_t _EsdfAndGradients_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _EsdfAndGradients_Response_message_typesupport_map = {
  2,
  "nvblox_msgs",
  &_EsdfAndGradients_Response_message_typesupport_ids.typesupport_identifier[0],
  &_EsdfAndGradients_Response_message_typesupport_symbol_names.symbol_name[0],
  &_EsdfAndGradients_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t EsdfAndGradients_Response_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_EsdfAndGradients_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace nvblox_msgs

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<nvblox_msgs::srv::EsdfAndGradients_Response>()
{
  return &::nvblox_msgs::srv::rosidl_typesupport_cpp::EsdfAndGradients_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, nvblox_msgs, srv, EsdfAndGradients_Response)() {
  return get_message_type_support_handle<nvblox_msgs::srv::EsdfAndGradients_Response>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "nvblox_msgs/srv/detail/esdf_and_gradients__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/service_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace nvblox_msgs
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _EsdfAndGradients_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _EsdfAndGradients_type_support_ids_t;

static const _EsdfAndGradients_type_support_ids_t _EsdfAndGradients_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _EsdfAndGradients_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _EsdfAndGradients_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _EsdfAndGradients_type_support_symbol_names_t _EsdfAndGradients_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, nvblox_msgs, srv, EsdfAndGradients)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, nvblox_msgs, srv, EsdfAndGradients)),
  }
};

typedef struct _EsdfAndGradients_type_support_data_t
{
  void * data[2];
} _EsdfAndGradients_type_support_data_t;

static _EsdfAndGradients_type_support_data_t _EsdfAndGradients_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _EsdfAndGradients_service_typesupport_map = {
  2,
  "nvblox_msgs",
  &_EsdfAndGradients_service_typesupport_ids.typesupport_identifier[0],
  &_EsdfAndGradients_service_typesupport_symbol_names.symbol_name[0],
  &_EsdfAndGradients_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t EsdfAndGradients_service_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_EsdfAndGradients_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace nvblox_msgs

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<nvblox_msgs::srv::EsdfAndGradients>()
{
  return &::nvblox_msgs::srv::rosidl_typesupport_cpp::EsdfAndGradients_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp
