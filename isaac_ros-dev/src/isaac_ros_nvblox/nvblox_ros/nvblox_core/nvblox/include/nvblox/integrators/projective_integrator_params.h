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

#include "nvblox/integrators/weighting_function.h"
#include "nvblox/utils/params.h"

namespace nvblox {

// ======= SHARED PARAMS =======
constexpr Param<
    float>::Description kProjectiveIntegratorMaxIntegrationDistanceMParamDesc{
    "projective_integrator_max_integration_distance_m", 7.f,
    "The maximum distance, in meters, to integrate the depth or color image "
    "values."};

constexpr Param<float>::Description
    kLidarProjectiveIntegratorMaxIntegrationDistanceMParamDesc{
        "lidar_projective_integrator_max_integration_distance_m", 10.f,
        "The maximum distance, in meters, to integrate the depth values for "
        "LiDAR scans."};

constexpr Param<
    float>::Description kProjectiveIntegratorTruncationDistanceVoxParamDesc{
    "projective_integrator_truncation_distance_vox", 4.f,
    "The truncation distance, in units of voxels, for the TSDF or occupancy "
    "map."};

constexpr Param<WeightingFunctionType>::Description
    kProjectiveIntegratorWeightingModeParamDesc{
        "projective_integrator_weighting_mode",
        WeightingFunctionType::kInverseSquareWeight,
        "The weighting mode, applied to TSDF and color integrations.  "
        "Options: [0:constant, 1:constant_dropoff, 2:inverse_square, "
        "3:inverse_square_dropoff, 4:inverse_square_tsdf_distance_penalty]"};

constexpr Param<float>::Description kProjectiveIntegratorMaxWeightParamDesc{
    "projective_integrator_max_weight", 5.f,
    "Maximum weight for the TSDF and color integrations. Setting this number "
    "higher will lead to higher-quality reconstructions but worse "
    "performance in dynamic scenes."};
}  // namespace nvblox
