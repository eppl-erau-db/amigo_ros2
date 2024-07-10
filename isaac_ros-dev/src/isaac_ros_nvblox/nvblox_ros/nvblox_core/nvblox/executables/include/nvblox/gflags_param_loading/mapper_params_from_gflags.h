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

#include <gflags/gflags.h>

#include "nvblox/mapper/mapper_params.h"

namespace nvblox {

// <<<<<<<<<<<<<<<<<<<<<<<<<< DEFINE THE PARAMS >>>>>>>>>>>>>>>>>>>>>>>>>>

// ======= MAPPER =======
DEFINE_bool(do_depth_preprocessing, kDoDepthPrepocessingParamDesc.default_value,
            kDoDepthPrepocessingParamDesc.help_string);

DEFINE_int32(depth_preprocessing_num_dilations,
             kDepthPreprocessingNumDilationsParamDesc.default_value,
             kDepthPreprocessingNumDilationsParamDesc.help_string);

DEFINE_double(esdf_slice_min_height, kEsdfSliceMinHeightParamDesc.default_value,
              kEsdfSliceMinHeightParamDesc.help_string);

DEFINE_double(esdf_slice_max_height, kEsdfSliceMaxHeightParamDesc.default_value,
              kEsdfSliceMaxHeightParamDesc.help_string);

DEFINE_double(esdf_slice_height, kEsdfSliceHeightParamDesc.default_value,
              kEsdfSliceHeightParamDesc.help_string);

// ======= PROJECTIVE INTEGRATOR (TSDF/COLOR/OCCUPANCY) =======
DEFINE_double(
    projective_integrator_max_integration_distance_m,
    kProjectiveIntegratorMaxIntegrationDistanceMParamDesc.default_value,
    kProjectiveIntegratorMaxIntegrationDistanceMParamDesc.help_string);

DEFINE_double(projective_integrator_truncation_distance_vox,
              kProjectiveIntegratorTruncationDistanceVoxParamDesc.default_value,
              kProjectiveIntegratorTruncationDistanceVoxParamDesc.help_string);

DEFINE_double(projective_integrator_max_weight,
              kProjectiveIntegratorMaxWeightParamDesc.default_value,
              kProjectiveIntegratorMaxWeightParamDesc.help_string);

DEFINE_int32(
    projective_integrator_weighting_mode,
    static_cast<int>(kProjectiveIntegratorWeightingModeParamDesc.default_value),
    kProjectiveIntegratorWeightingModeParamDesc.help_string);

// ======= OCCUPANCY INTEGRATOR =======
DEFINE_double(free_region_occupancy_probability,
              kFreeRegionOccupancyProbabilityParamDesc.default_value,
              kFreeRegionOccupancyProbabilityParamDesc.help_string);

DEFINE_double(occupied_region_occupancy_probability,
              kOccupiedRegionOccupancyProbabilityParamDesc.default_value,
              kOccupiedRegionOccupancyProbabilityParamDesc.help_string);

DEFINE_double(unobserved_region_occupancy_probability,
              kUnobservedRegionOccupancyProbabilityParamDesc.default_value,
              kUnobservedRegionOccupancyProbabilityParamDesc.help_string);

DEFINE_double(occupied_region_half_width_m,
              kOccupiedRegionHalfWidthMParamDesc.default_value,
              kOccupiedRegionHalfWidthMParamDesc.help_string);

// ======= ESDF INTEGRATOR =======
DEFINE_double(esdf_integrator_max_distance_m,
              kEsdfIntegratorMaxDistanceMParamDesc.default_value,
              kEsdfIntegratorMaxDistanceMParamDesc.help_string);

DEFINE_double(esdf_integrator_min_weight,
              kEsdfIntegratorMinWeightParamDesc.default_value,
              kEsdfIntegratorMinWeightParamDesc.help_string);

DEFINE_double(esdf_integrator_max_site_distance_vox,
              kEsdfIntegratorMaxSiteDistanceVoxParamDesc.default_value,
              kEsdfIntegratorMaxSiteDistanceVoxParamDesc.help_string);

// ======= MESH INTEGRATOR =======
DEFINE_double(mesh_integrator_min_weight,
              kMeshIntegratorMinWeightParamDesc.default_value,
              kMeshIntegratorMinWeightParamDesc.help_string);

DEFINE_bool(mesh_integrator_weld_vertices,
            kMeshIntegratorWeldVerticesParamDesc.default_value,
            kMeshIntegratorWeldVerticesParamDesc.help_string);

// ======= TSDF DECAY INTEGRATOR =======
DEFINE_double(tsdf_decay_factor, kTsdfDecayFactorParamDesc.default_value,
              kTsdfDecayFactorParamDesc.help_string);

DEFINE_double(tsdf_decayed_weight_threshold,
              kTsdfDecayedWeightThresholdDesc.default_value,
              kTsdfDecayedWeightThresholdDesc.help_string);

DEFINE_bool(tsdf_set_free_distance_on_decayed,
            kTsdfSetFreeDistanceOnDecayedDesc.default_value,
            kTsdfSetFreeDistanceOnDecayedDesc.help_string);

DEFINE_double(tsdf_decayed_free_distance_vox,
              kTsdfDecayedFreeDistanceVoxDesc.default_value,
              kTsdfDecayedFreeDistanceVoxDesc.help_string);

DEFINE_bool(tsdf_deallocate_decayed_blocks,
            kDecayIntegratorBaseDeallocateDecayedBlocks.default_value,
            kDecayIntegratorBaseDeallocateDecayedBlocks.help_string);

// ======= OCCUPANCY DECAY INTEGRATOR =======
DEFINE_double(free_region_decay_probability,
              kFreeRegionDecayProbabilityParamDesc.default_value,
              kFreeRegionDecayProbabilityParamDesc.help_string);

DEFINE_double(occupied_region_decay_probability,
              kOccupiedRegionDecayProbabilityParamDesc.default_value,
              kOccupiedRegionDecayProbabilityParamDesc.help_string);

DEFINE_bool(occupancy_deallocate_decayed_blocks,
            kDecayIntegratorBaseDeallocateDecayedBlocks.default_value,
            kDecayIntegratorBaseDeallocateDecayedBlocks.help_string);

// ======= FREESPACE INTEGRATOR =======
DEFINE_double(max_tsdf_distance_for_occupancy_m,
              kMaxTsdfDistanceForOccupancyMParamDesc.default_value,
              kMaxTsdfDistanceForOccupancyMParamDesc.help_string);

DEFINE_int64(
    max_unobserved_to_keep_consecutive_occupancy_ms,
    static_cast<int64_t>(
        kMaxUnobservedToKeepConsecutiveOccupancyMsParamDesc.default_value),
    kMaxUnobservedToKeepConsecutiveOccupancyMsParamDesc.help_string);

DEFINE_int64(
    min_duration_since_occupied_for_freespace_ms,
    static_cast<int64_t>(
        kMinDurationSinceOccupiedForFreespaceMsParamDesc.default_value),
    kMinDurationSinceOccupiedForFreespaceMsParamDesc.help_string);

DEFINE_int64(
    min_consecutive_occupancy_duration_for_reset_ms,
    static_cast<int64_t>(
        kMinConsecutiveOccupancyDurationForResetMsParamDesc.default_value),
    kMinConsecutiveOccupancyDurationForResetMsParamDesc.help_string);

DEFINE_bool(check_neighborhood, kCheckNeighborhoodParamDesc.default_value,
            kCheckNeighborhoodParamDesc.help_string);

// <<<<<<<<<<<<<<<<<<<<<<<<<< GET THE PARAMS >>>>>>>>>>>>>>>>>>>>>>>>>>

inline MapperParams get_mapper_params_from_gflags() {
  MapperParams params;
  // ======= MAPPER =======
  // depth preprocessing
  if (!gflags::GetCommandLineFlagInfoOrDie("do_depth_preprocessing")
           .is_default) {
    LOG(INFO) << "command line parameter found: "
                 "do_depth_preprocessing = "
              << FLAGS_do_depth_preprocessing;
    params.do_depth_preprocessing = FLAGS_do_depth_preprocessing;
  }
  if (!gflags::GetCommandLineFlagInfoOrDie("depth_preprocessing_num_dilations")
           .is_default) {
    LOG(INFO) << "command line parameter found: "
                 "depth_preprocessing_num_dilations = "
              << FLAGS_depth_preprocessing_num_dilations;
    params.depth_preprocessing_num_dilations =
        FLAGS_depth_preprocessing_num_dilations;
  }
  // 2D esdf slice
  if (!gflags::GetCommandLineFlagInfoOrDie("esdf_slice_min_height")
           .is_default) {
    LOG(INFO) << "Command line parameter found: esdf_slice_min_height = "
              << FLAGS_esdf_slice_min_height;
    params.esdf_slice_min_height =
        static_cast<float>(FLAGS_esdf_slice_min_height);
  }
  if (!gflags::GetCommandLineFlagInfoOrDie("esdf_slice_max_height")
           .is_default) {
    LOG(INFO) << "Command line parameter found: esdf_slice_max_height = "
              << FLAGS_esdf_slice_max_height;
    params.esdf_slice_max_height =
        static_cast<float>(FLAGS_esdf_slice_max_height);
  }
  if (!gflags::GetCommandLineFlagInfoOrDie("esdf_slice_height").is_default) {
    LOG(INFO) << "Command line parameter found: esdf_slice_height = "
              << FLAGS_esdf_slice_height;
    params.esdf_slice_height = static_cast<float>(FLAGS_esdf_slice_height);
  }

  // ======= PROJECTIVE INTEGRATOR (TSDF/COLOR/OCCUPANCY) =======
  // max integration distance
  if (!gflags::GetCommandLineFlagInfoOrDie(
           "projective_integrator_max_integration_distance_m")
           .is_default) {
    LOG(INFO) << "Command line parameter found: "
                 "projective_integrator_max_integration_distance_m= "
              << FLAGS_projective_integrator_max_integration_distance_m;
    params.projective_integrator_max_integration_distance_m =
        FLAGS_projective_integrator_max_integration_distance_m;
  }
  // truncation distance
  if (!gflags::GetCommandLineFlagInfoOrDie(
           "projective_integrator_truncation_distance_vox")
           .is_default) {
    LOG(INFO) << "Command line parameter found: "
                 "projective_integrator_truncation_distance_vox = "
              << FLAGS_projective_integrator_truncation_distance_vox;
    params.projective_integrator_truncation_distance_vox =
        FLAGS_projective_integrator_truncation_distance_vox;
  }
  // weighting
  if (!gflags::GetCommandLineFlagInfoOrDie(
           "projective_integrator_weighting_mode")
           .is_default) {
    LOG(INFO)
        << "Command line parameter found: projective_integrator_weighting_mode "
        << FLAGS_projective_integrator_weighting_mode;
    params.projective_integrator_weighting_mode =
        static_cast<WeightingFunctionType>(
            FLAGS_projective_integrator_weighting_mode);
  }
  // max weight
  if (!gflags::GetCommandLineFlagInfoOrDie("projective_integrator_max_weight")
           .is_default) {
    LOG(INFO)
        << "Command line parameter found: projective_integrator_max_weight = "
        << FLAGS_projective_integrator_max_weight;
    params.projective_integrator_max_weight =
        FLAGS_projective_integrator_max_weight;
  }

  // ======= OCCUPANCY INTEGRATOR =======
  if (!gflags::GetCommandLineFlagInfoOrDie("free_region_occupancy_probability")
           .is_default) {
    LOG(INFO) << "Command line parameter found: "
                 "free_region_occupancy_probability = "
              << FLAGS_free_region_occupancy_probability;
    params.free_region_occupancy_probability =
        FLAGS_free_region_occupancy_probability;
  }
  if (!gflags::GetCommandLineFlagInfoOrDie(
           "occupied_region_occupancy_probability")
           .is_default) {
    LOG(INFO) << "Command line parameter found: "
                 "occupied_region_occupancy_probability = "
              << FLAGS_occupied_region_occupancy_probability;
    params.occupied_region_occupancy_probability =
        FLAGS_occupied_region_occupancy_probability;
  }
  if (!gflags::GetCommandLineFlagInfoOrDie(
           "unobserved_region_occupancy_probability")
           .is_default) {
    LOG(INFO) << "Command line parameter found: "
                 "unobserved_region_occupancy_probability = "
              << FLAGS_unobserved_region_occupancy_probability;
    params.unobserved_region_occupancy_probability =
        FLAGS_unobserved_region_occupancy_probability;
  }
  if (!gflags::GetCommandLineFlagInfoOrDie("occupied_region_half_width_m")
           .is_default) {
    LOG(INFO) << "Command line parameter found: occupied_region_half_width_m = "
              << FLAGS_occupied_region_half_width_m;
    params.occupied_region_half_width_m = FLAGS_occupied_region_half_width_m;
  }

  // ======= ESDF INTEGRATOR =======
  if (!gflags::GetCommandLineFlagInfoOrDie("esdf_integrator_min_weight")
           .is_default) {
    LOG(INFO) << "Command line parameter found: esdf_integrator_min_weight = "
              << FLAGS_esdf_integrator_min_weight;
    params.esdf_integrator_min_weight = FLAGS_esdf_integrator_min_weight;
  }
  if (!gflags::GetCommandLineFlagInfoOrDie(
           "esdf_integrator_max_site_distance_vox")
           .is_default) {
    LOG(INFO) << "Command line parameter found: "
                 "esdf_integrator_max_site_distance_vox = "
              << FLAGS_esdf_integrator_max_site_distance_vox;
    params.esdf_integrator_max_site_distance_vox =
        FLAGS_esdf_integrator_max_site_distance_vox;
  }
  if (!gflags::GetCommandLineFlagInfoOrDie("esdf_integrator_max_distance_m")
           .is_default) {
    LOG(INFO)
        << "Command line parameter found: esdf_integrator_max_distance_m = "
        << FLAGS_esdf_integrator_max_distance_m;
    params.esdf_integrator_max_distance_m =
        FLAGS_esdf_integrator_max_distance_m;
  }

  // ======= MESH INTEGRATOR =======
  if (!gflags::GetCommandLineFlagInfoOrDie("mesh_integrator_min_weight")
           .is_default) {
    LOG(INFO) << "Command line parameter found: mesh_integrator_min_weight = "
              << FLAGS_mesh_integrator_min_weight;
    params.mesh_integrator_min_weight = FLAGS_mesh_integrator_min_weight;
  }
  if (!gflags::GetCommandLineFlagInfoOrDie("mesh_integrator_weld_vertices")
           .is_default) {
    LOG(INFO)
        << "Command line parameter found: mesh_integrator_weld_vertices = "
        << FLAGS_mesh_integrator_weld_vertices;
    params.mesh_integrator_weld_vertices = FLAGS_mesh_integrator_weld_vertices;
  }

  // ======= TSDF DECAY INTEGRATOR =======
  if (!gflags::GetCommandLineFlagInfoOrDie("tsdf_decay_factor").is_default) {
    LOG(INFO) << "command line parameter found: "
                 "tsdf_decay_factor = "
              << FLAGS_tsdf_decay_factor;
    params.tsdf_decay_factor = FLAGS_tsdf_decay_factor;
  }
  if (!gflags::GetCommandLineFlagInfoOrDie("tsdf_decayed_weight_threshold")
           .is_default) {
    LOG(INFO) << "command line parameter found: "
                 "tsdf_decayed_weight_threshold = "
              << FLAGS_tsdf_decayed_weight_threshold;
    params.tsdf_decayed_weight_threshold = FLAGS_tsdf_decayed_weight_threshold;
  }
  if (!gflags::GetCommandLineFlagInfoOrDie("tsdf_set_free_distance_on_decayed")
           .is_default) {
    LOG(INFO) << "command line parameter found: "
                 "tsdf_set_free_distance_on_decayed = "
              << FLAGS_tsdf_set_free_distance_on_decayed;
    params.tsdf_set_free_distance_on_decayed =
        FLAGS_tsdf_set_free_distance_on_decayed;
  }
  if (!gflags::GetCommandLineFlagInfoOrDie("tsdf_decayed_free_distance_vox")
           .is_default) {
    LOG(INFO) << "command line parameter found: "
                 "tsdf_decayed_free_distance_vox = "
              << FLAGS_tsdf_decayed_free_distance_vox;
    params.tsdf_decayed_free_distance_vox =
        FLAGS_tsdf_decayed_free_distance_vox;
  }
  if (!gflags::GetCommandLineFlagInfoOrDie("tsdf_deallocate_decayed_blocks")
           .is_default) {
    LOG(INFO) << "command line parameter found: "
                 "tsdf_deallocate_decayed_blocks = "
              << FLAGS_tsdf_deallocate_decayed_blocks;
    params.tsdf_deallocate_decayed_blocks =
        FLAGS_tsdf_deallocate_decayed_blocks;
  }

  // ======= OCCUPANCY DECAY INTEGRATOR =======
  if (!gflags::GetCommandLineFlagInfoOrDie("free_region_decay_probability")
           .is_default) {
    LOG(INFO) << "command line parameter found: "
                 "free_region_decay_probability = "
              << FLAGS_free_region_decay_probability;
    params.free_region_decay_probability = FLAGS_free_region_decay_probability;
  }
  if (!gflags::GetCommandLineFlagInfoOrDie("occupied_region_decay_probability")
           .is_default) {
    LOG(INFO) << "command line parameter found: "
                 "occupied_region_decay_probability = "
              << FLAGS_occupied_region_decay_probability;
    params.occupied_region_decay_probability =
        FLAGS_occupied_region_decay_probability;
  }
  if (!gflags::GetCommandLineFlagInfoOrDie(
           "occupancy_deallocate_decayed_blocks")
           .is_default) {
    LOG(INFO) << "command line parameter found: "
                 "occupancy_deallocate_decayed_blocks = "
              << FLAGS_occupancy_deallocate_decayed_blocks;
    params.occupancy_deallocate_decayed_blocks =
        FLAGS_occupancy_deallocate_decayed_blocks;
  }

  // ======= FREESPACE INTEGRATOR =======
  if (!gflags::GetCommandLineFlagInfoOrDie("max_tsdf_distance_for_occupancy_m")
           .is_default) {
    LOG(INFO) << "command line parameter found: "
                 "max_tsdf_distance_for_occupancy_m = "
              << FLAGS_max_tsdf_distance_for_occupancy_m;
    params.max_tsdf_distance_for_occupancy_m =
        FLAGS_max_tsdf_distance_for_occupancy_m;
  }
  if (!gflags::GetCommandLineFlagInfoOrDie(
           "max_unobserved_to_keep_consecutive_occupancy_ms")
           .is_default) {
    LOG(INFO) << "command line parameter found: "
                 "max_unobserved_to_keep_consecutive_occupancy_ms = "
              << FLAGS_max_unobserved_to_keep_consecutive_occupancy_ms;
    params.max_unobserved_to_keep_consecutive_occupancy_ms =
        Time(FLAGS_max_unobserved_to_keep_consecutive_occupancy_ms);
  }
  if (!gflags::GetCommandLineFlagInfoOrDie(
           "min_duration_since_occupied_for_freespace_ms")
           .is_default) {
    LOG(INFO) << "command line parameter found: "
                 "min_duration_since_occupied_for_freespace_ms = "
              << FLAGS_min_duration_since_occupied_for_freespace_ms;
    params.min_duration_since_occupied_for_freespace_ms =
        Time(FLAGS_min_duration_since_occupied_for_freespace_ms);
  }
  if (!gflags::GetCommandLineFlagInfoOrDie(
           "min_consecutive_occupancy_duration_for_reset_ms")
           .is_default) {
    LOG(INFO) << "command line parameter found: "
                 "min_consecutive_occupancy_duration_for_reset_ms = "
              << FLAGS_min_consecutive_occupancy_duration_for_reset_ms;
    params.min_consecutive_occupancy_duration_for_reset_ms =
        Time(FLAGS_min_consecutive_occupancy_duration_for_reset_ms);
  }
  if (!gflags::GetCommandLineFlagInfoOrDie("check_neighborhood").is_default) {
    LOG(INFO) << "command line parameter found: "
                 "check_neighborhood = "
              << FLAGS_check_neighborhood;
    params.check_neighborhood = FLAGS_check_neighborhood;
  }

  // return the written params
  return params;
}

}  // namespace nvblox
