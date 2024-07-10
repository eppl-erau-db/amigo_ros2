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

constexpr Param<float>::Description kTsdfDecayFactorParamDesc{
    "tsdf_decay_factor", .95f,
    "Decay factor that is applied to the TSDF weight when the TSDF decay is "
    "called."};

constexpr Param<float>::Description kTsdfDecayedWeightThresholdDesc{
    "tsdf_decayed_weight_threshold", 1e-3,
    "The weight of a TSDF voxel below which we consider it fully decayed."};

constexpr Param<bool>::Description kTsdfSetFreeDistanceOnDecayedDesc{
    "tsdf_set_free_distance_on_decayed", false,
    "If true we set fully decayed voxels to the free distance."};

constexpr Param<float>::Description kTsdfDecayedFreeDistanceVoxDesc{
    "tsdf_decayed_free_distance_vox", 4.0,
    "The distance in voxels that we give to fully decayed voxels "
    "(if requested)."};

}  // namespace nvblox
