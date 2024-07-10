// Copyright 2021 Ericsson AB
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "rmw/error_handling.h"
#include "rmw/get_network_flow_endpoints.h"
#include "rmw/rmw.h"
#include "rmw/types.h"

extern "C"
{
rmw_ret_t
rmw_publisher_get_network_flow_endpoints(
  const rmw_publisher_t * publisher,
  rcutils_allocator_t * allocator,
  rmw_network_flow_endpoint_array_t * network_flow_endpoint_array)
{
  (void) publisher;
  (void) allocator;
  (void) network_flow_endpoint_array;
  RMW_SET_ERROR_MSG("rmw_publisher_get_network_flow_endpoints not implemented");
  return RMW_RET_UNSUPPORTED;
}

rmw_ret_t
rmw_subscription_get_network_flow_endpoints(
  const rmw_subscription_t * subscription,
  rcutils_allocator_t * allocator,
  rmw_network_flow_endpoint_array_t * network_flow_endpoint_array)
{
  (void) subscription;
  (void) allocator;
  (void) network_flow_endpoint_array;
  RMW_SET_ERROR_MSG("rmw_subscription_get_network_flow_endpoints not implemented");
  return RMW_RET_UNSUPPORTED;
}
}  // extern "C"
