/*
Copyright 2024 NVIDIA CORPORATION

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
#pragma once

#include "nvblox/utils/params.h"

namespace nvblox {

constexpr Param<float>::Description kEsdfIntegratorMaxDistanceMParamDesc{
    "esdf_integrator_max_distance_m", 2.f,
    "Maximum distance to compute the ESDF up to, in meters."};
constexpr Param<float>::Description kEsdfIntegratorMinWeightParamDesc{
    "esdf_integrator_min_weight", 1e-4,
    "Minimum weight of the TSDF to consider for inclusion in the ESDF."};
constexpr Param<float>::Description kEsdfIntegratorMaxSiteDistanceVoxParamDesc{
    "esdf_integrator_max_site_distance_vox", 1.f,
    "Maximum distance to consider a voxel within a surface for the ESDF "
    "calculation."};

}  // namespace nvblox
