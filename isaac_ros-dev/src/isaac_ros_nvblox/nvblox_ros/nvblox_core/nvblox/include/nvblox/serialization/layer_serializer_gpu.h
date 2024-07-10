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

#include <memory>
#include <vector>

#include "nvblox/core/cuda_stream.h"
#include "nvblox/core/types.h"
#include "nvblox/core/unified_vector.h"
#include "nvblox/map/common_names.h"
#include "nvblox/map/layer.h"
#include "nvblox/serialization/internal/serialization_gpu.h"

namespace nvblox {

/// Serialized Layer
template <typename VoxelType>
struct SerializedLayer {
  /// Indices of serialized blocks
  std::vector<Index3D> block_indices;

  /// Vector of voxels
  host_vector<VoxelType> voxels;

  /// Store offset in voxels for each block in block_indices.
  /// Get the first voxel of block i: voxels[block_offsets[i]]
  /// Get the size of block i: block_offsets[i+1] - block_offsets[i]
  host_vector<int32_t> block_offsets;
};

using SerializedTsdfLayer = SerializedLayer<TsdfVoxel>;
using SerializedColorLayer = SerializedLayer<ColorVoxel>;
using SerializedOccupancyLayer = SerializedLayer<OccupancyVoxel>;
using SerializedFreespaceLayer = SerializedLayer<FreespaceVoxel>;
using SerializedEsdfLayer = SerializedLayer<EsdfVoxel>;

/// Class for effective serialization of a TSDF layer from GPU to host
///
/// This is a wrapper around LayerSerializerGpuInternal which also stores the
/// serialized data.
template <class LayerType>
class LayerSerializerGpu {
 public:
  using BlockType = typename LayerType::BlockType;
  using VoxelType = typename BlockType::VoxelType;
  using SerializedLayerType = SerializedLayer<VoxelType>;

  virtual ~LayerSerializerGpu() = default;
  LayerSerializerGpu()
      : serialized_layer_(std::make_shared<SerializedLayerType>()) {}

  /// Serialize a layer and return a pointer to the result
  ///
  /// See @LayerSerializerGpuInternal::serializeAsync for details on the output
  /// format
  ///
  /// layer                       Layer to serialize
  /// block_indices_to_serialize  Block indices to serialize
  /// cuda_stream                 Cuda stream. Will be synced
  std::shared_ptr<const SerializedLayerType> serialize(
      const LayerType& layer,
      const std::vector<Index3D>& block_indices_to_serialize,
      const CudaStream cuda_stream);

 private:
  LayerSerializerGpuInternal<LayerType, VoxelType> serializer_;

  std::shared_ptr<SerializedLayerType> serialized_layer_;
};

using TsdfLayerSerializerGpu = LayerSerializerGpu<TsdfLayer>;
using ColorLayerSerializerGpu = LayerSerializerGpu<ColorLayer>;
using OccupancyLayerSerializerGpu = LayerSerializerGpu<OccupancyLayer>;
using FreespaceLayerSerializerGpu = LayerSerializerGpu<FreespaceLayer>;
using EsdfLayerSerializerGpu = LayerSerializerGpu<EsdfLayer>;

}  // namespace nvblox

#include "nvblox/serialization/internal/impl/layer_serializer_gpu_impl.h"
