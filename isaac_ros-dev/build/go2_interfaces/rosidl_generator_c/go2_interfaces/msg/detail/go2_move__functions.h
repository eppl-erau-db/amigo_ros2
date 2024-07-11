// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from go2_interfaces:msg/Go2Move.idl
// generated code does not contain a copyright notice

#ifndef GO2_INTERFACES__MSG__DETAIL__GO2_MOVE__FUNCTIONS_H_
#define GO2_INTERFACES__MSG__DETAIL__GO2_MOVE__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "go2_interfaces/msg/rosidl_generator_c__visibility_control.h"

#include "go2_interfaces/msg/detail/go2_move__struct.h"

/// Initialize msg/Go2Move message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * go2_interfaces__msg__Go2Move
 * )) before or use
 * go2_interfaces__msg__Go2Move__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_go2_interfaces
bool
go2_interfaces__msg__Go2Move__init(go2_interfaces__msg__Go2Move * msg);

/// Finalize msg/Go2Move message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_go2_interfaces
void
go2_interfaces__msg__Go2Move__fini(go2_interfaces__msg__Go2Move * msg);

/// Create msg/Go2Move message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * go2_interfaces__msg__Go2Move__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_go2_interfaces
go2_interfaces__msg__Go2Move *
go2_interfaces__msg__Go2Move__create();

/// Destroy msg/Go2Move message.
/**
 * It calls
 * go2_interfaces__msg__Go2Move__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_go2_interfaces
void
go2_interfaces__msg__Go2Move__destroy(go2_interfaces__msg__Go2Move * msg);

/// Check for msg/Go2Move message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_go2_interfaces
bool
go2_interfaces__msg__Go2Move__are_equal(const go2_interfaces__msg__Go2Move * lhs, const go2_interfaces__msg__Go2Move * rhs);

/// Copy a msg/Go2Move message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_go2_interfaces
bool
go2_interfaces__msg__Go2Move__copy(
  const go2_interfaces__msg__Go2Move * input,
  go2_interfaces__msg__Go2Move * output);

/// Initialize array of msg/Go2Move messages.
/**
 * It allocates the memory for the number of elements and calls
 * go2_interfaces__msg__Go2Move__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_go2_interfaces
bool
go2_interfaces__msg__Go2Move__Sequence__init(go2_interfaces__msg__Go2Move__Sequence * array, size_t size);

/// Finalize array of msg/Go2Move messages.
/**
 * It calls
 * go2_interfaces__msg__Go2Move__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_go2_interfaces
void
go2_interfaces__msg__Go2Move__Sequence__fini(go2_interfaces__msg__Go2Move__Sequence * array);

/// Create array of msg/Go2Move messages.
/**
 * It allocates the memory for the array and calls
 * go2_interfaces__msg__Go2Move__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_go2_interfaces
go2_interfaces__msg__Go2Move__Sequence *
go2_interfaces__msg__Go2Move__Sequence__create(size_t size);

/// Destroy array of msg/Go2Move messages.
/**
 * It calls
 * go2_interfaces__msg__Go2Move__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_go2_interfaces
void
go2_interfaces__msg__Go2Move__Sequence__destroy(go2_interfaces__msg__Go2Move__Sequence * array);

/// Check for msg/Go2Move message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_go2_interfaces
bool
go2_interfaces__msg__Go2Move__Sequence__are_equal(const go2_interfaces__msg__Go2Move__Sequence * lhs, const go2_interfaces__msg__Go2Move__Sequence * rhs);

/// Copy an array of msg/Go2Move messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_go2_interfaces
bool
go2_interfaces__msg__Go2Move__Sequence__copy(
  const go2_interfaces__msg__Go2Move__Sequence * input,
  go2_interfaces__msg__Go2Move__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // GO2_INTERFACES__MSG__DETAIL__GO2_MOVE__FUNCTIONS_H_
