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

#include "nvblox/geometry/bounding_boxes.h"
#include "nvblox/map/unified_3d_grid.h"

namespace nvblox {

/// Copies a VoxelLayer into a dense Unified3DGrid.
/// @tparam VoxelType The type of the voxel in the voxel layer.
/// @param layer The voxel layer that is the source of the copy.
/// @param aabb The AABB inside which to copy. The AABB is inclusive, in that we
/// copy the voxels touched by the edges.
/// @param default_value The default value in the output where the layer has
/// missing data.
/// @param grid The output grid to copy into.
/// @param cuda_stream The stream on which to process the work.
template <typename VoxelType>
void voxelLayerToDenseVoxelGridInAABBAsync(
    const VoxelBlockLayer<VoxelType>& layer,  // NOLINT
    const AxisAlignedBoundingBox& aabb,       // NOLINT
    const VoxelType default_value,            // NOLINT
    Unified3DGrid<VoxelType>* grid,           // NOLINT
    CudaStream cuda_stream);

/// Copies a VoxelLayer into a dense Unified3DGrid with conversion
/// @tparam InputVoxelType The type of the voxel in the voxel layer.
/// @tparam OutputCellType The type of the cell in the otput grid.
/// @tparam ConversionFunctor Functor for converting from InputVoxelType to
/// OutputCellType.
/// @param layer The voxel layer that is the source of the copy.
/// @param aabb The AABB inside which to copy. The AABB is inclusive, in that we
/// copy the voxels touched by the edges.
/// @param default_value The default value in the output where the layer has
/// missing data.
/// @param grid The output grid to copy into.
/// @param cuda_stream The stream on which to process the work.
template <typename InputVoxelType, typename OutputCellType,
          typename ConversionFunctor>
void voxelLayerToDenseVoxelGridInAABBAsync(
    const VoxelBlockLayer<InputVoxelType>& layer,
    const AxisAlignedBoundingBox& aabb, const OutputCellType default_value,
    const ConversionFunctor& conversion_op, Unified3DGrid<OutputCellType>* grid,
    CudaStream cuda_stream);

}  // namespace nvblox

#include "nvblox/map/internal/cuda/impl/layer_to_3d_grid_impl.cuh"
