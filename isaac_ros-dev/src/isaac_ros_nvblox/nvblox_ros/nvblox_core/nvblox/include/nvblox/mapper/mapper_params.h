/*
Copyright 2023 NVIDIA CORPORATION

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

#include "nvblox/integrators/esdf_integrator.h"
#include "nvblox/integrators/freespace_integrator.h"
#include "nvblox/integrators/occupancy_decay_integrator.h"
#include "nvblox/integrators/projective_color_integrator.h"
#include "nvblox/integrators/projective_integrator_params.h"
#include "nvblox/integrators/projective_occupancy_integrator.h"
#include "nvblox/integrators/projective_tsdf_integrator.h"
#include "nvblox/integrators/tsdf_decay_integrator.h"
#include "nvblox/mesh/mesh_integrator.h"
#include "nvblox/mesh/mesh_streamer.h"
#include "nvblox/utils/params.h"

namespace nvblox {

// ======= DEPTH PRE-PROCESSING =======
constexpr Param<bool>::Description kDoDepthPrepocessingParamDesc{
    "do_depth_preprocessing", false,
    "Whether or not to run the preprocessing pipeline on the input depth "
    "image. Currently, this preprocessing only consists of dilating invalid "
    "regions in the input depth image."};

constexpr Param<int>::Description kDepthPreprocessingNumDilationsParamDesc{
    "depth_preprocessing_num_dilations", 4,
    "Number of times to run the invalid region dilation in the depth "
    "preprocessing pipeline (if do_depth_preprocessing is enabled)."};

// ======= 2D ESDF SLICE =======
constexpr Param<float>::Description kEsdfSliceMinHeightParamDesc{
    "esdf_slice_min_height", 0.f,
    "The minimum height, in meters, to consider obstacles part of the 2D "
    "ESDF slice."};

constexpr Param<float>::Description kEsdfSliceMaxHeightParamDesc{
    "esdf_slice_max_height", 1.f,
    "The maximum height, in meters, to consider obstacles part of the 2D "
    "ESDF slice."};

constexpr Param<float>::Description kEsdfSliceHeightParamDesc{
    "esdf_slice_height", 1.f,
    "The output slice height for the distance slice and ESDF pointcloud. "
    "Does not need to be within min and max height below. In units of "
    "meters."};

// ======= DECAY =======
constexpr Param<bool>::Description kExcludeLastViewFromDecayParamDesc{
    "exclude_last_view_from_decay", false,
    "Whether contributions from the last depth frame should be excluded when "
    "decaying"};

// ======= MESH STREAMER =======
constexpr Param<float>::Description kMeshBandwidthLimitMbpsParamDesc{
    "mesh_bandwidth_limit_mbps", 25.f,
    "Limits the mesh size returned by updatemesh."};

constexpr Param<float>::Description kMeshStreamerExclusionHeightMParamDesc{
    "mesh_streamer_exclusion_height_m",
    MeshStreamerOldestBlocks::kDefaultExclusionHeightM,
    "Mesh blocks above this height will not be streamed."};

constexpr Param<float>::Description kMeshStreamerExclusionRadiusMParamDesc{
    "mesh_streamer_exclusion_radius_m",
    MeshStreamerOldestBlocks::kDefaultExclusionRadiusM,
    "Mesh blocks outside this radius (centered on the robot) will not be "
    "streamed."};

/// A structure containing the mapper parameters. This object can be used to set
/// all parameters of a mapper.
struct MapperParams {
  Param<bool> do_depth_preprocessing{kDoDepthPrepocessingParamDesc};
  Param<int> depth_preprocessing_num_dilations{
      kDepthPreprocessingNumDilationsParamDesc};
  Param<float> esdf_slice_min_height{kEsdfSliceMinHeightParamDesc};
  Param<float> esdf_slice_max_height{kEsdfSliceMaxHeightParamDesc};
  Param<float> esdf_slice_height{kEsdfSliceHeightParamDesc};
  Param<bool> exclude_last_view_from_decay{kExcludeLastViewFromDecayParamDesc};
  Param<float> projective_integrator_max_integration_distance_m{
      kProjectiveIntegratorMaxIntegrationDistanceMParamDesc};
  Param<float> lidar_projective_integrator_max_integration_distance_m{
      kLidarProjectiveIntegratorMaxIntegrationDistanceMParamDesc};
  Param<float> projective_integrator_truncation_distance_vox{
      kProjectiveIntegratorTruncationDistanceVoxParamDesc};
  Param<WeightingFunctionType> projective_integrator_weighting_mode{
      kProjectiveIntegratorWeightingModeParamDesc};
  Param<float> projective_integrator_max_weight{
      kProjectiveIntegratorMaxWeightParamDesc};
  Param<float> free_region_occupancy_probability{
      kFreeRegionOccupancyProbabilityParamDesc};
  Param<float> occupied_region_occupancy_probability{
      kOccupiedRegionOccupancyProbabilityParamDesc};
  Param<float> unobserved_region_occupancy_probability{
      kUnobservedRegionOccupancyProbabilityParamDesc};
  Param<float> occupied_region_half_width_m{kOccupiedRegionHalfWidthMParamDesc};
  Param<float> esdf_integrator_max_distance_m{
      kEsdfIntegratorMaxDistanceMParamDesc};
  Param<float> esdf_integrator_min_weight{kEsdfIntegratorMinWeightParamDesc};
  Param<float> esdf_integrator_max_site_distance_vox{
      kEsdfIntegratorMaxSiteDistanceVoxParamDesc};
  Param<float> mesh_integrator_min_weight{kMeshIntegratorMinWeightParamDesc};
  Param<bool> mesh_integrator_weld_vertices{
      kMeshIntegratorWeldVerticesParamDesc};
  Param<float> tsdf_decay_factor{kTsdfDecayFactorParamDesc};
  Param<float> tsdf_decayed_weight_threshold{kTsdfDecayedWeightThresholdDesc};
  Param<bool> tsdf_set_free_distance_on_decayed{
      kTsdfSetFreeDistanceOnDecayedDesc};
  Param<float> tsdf_decayed_free_distance_vox{kTsdfDecayedFreeDistanceVoxDesc};
  Param<bool> tsdf_deallocate_decayed_blocks{
      kDecayIntegratorBaseDeallocateDecayedBlocks};
  Param<float> free_region_decay_probability{
      kFreeRegionDecayProbabilityParamDesc};
  Param<float> occupied_region_decay_probability{
      kOccupiedRegionDecayProbabilityParamDesc};
  Param<bool> occupancy_deallocate_decayed_blocks{
      kDecayIntegratorBaseDeallocateDecayedBlocks};
  Param<float> max_tsdf_distance_for_occupancy_m{
      kMaxTsdfDistanceForOccupancyMParamDesc};
  Param<Time> max_unobserved_to_keep_consecutive_occupancy_ms{
      kMaxUnobservedToKeepConsecutiveOccupancyMsParamDesc};
  Param<Time> min_duration_since_occupied_for_freespace_ms{
      kMinDurationSinceOccupiedForFreespaceMsParamDesc};
  Param<Time> min_consecutive_occupancy_duration_for_reset_ms{
      kMinConsecutiveOccupancyDurationForResetMsParamDesc};
  Param<bool> check_neighborhood{kCheckNeighborhoodParamDesc};
  Param<float> mesh_bandwidth_limit_mbps{kMeshBandwidthLimitMbpsParamDesc};
  Param<float> mesh_streamer_exclusion_height_m{
      kMeshStreamerExclusionHeightMParamDesc};
  Param<float> mesh_streamer_exclusion_radius_m{
      kMeshStreamerExclusionRadiusMParamDesc};
};

}  // namespace nvblox
