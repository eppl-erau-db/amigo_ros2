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

namespace nvblox {

template <class LayerType>
std::shared_ptr<const SerializedLayer<typename LayerType::BlockType::VoxelType>>
LayerSerializerGpu<LayerType>::serialize(
    const LayerType& layer,
    const std::vector<Index3D>& block_indices_to_serialize,
    const CudaStream cuda_stream) {
  serializer_.serializeAsync(
      layer, block_indices_to_serialize, serialized_layer_->voxels,
      serialized_layer_->block_offsets,
      [](const BlockType* block) -> const std::pair<const VoxelType*, int> {
        if (block == nullptr) {
          return {nullptr, 0};
        } else {
          return std::make_pair(&block->voxels[0][0][0], BlockType::kNumVoxels);
        }
      },
      cuda_stream);

  serialized_layer_->block_indices = block_indices_to_serialize;

  cuda_stream.synchronize();
  return serialized_layer_;
}

}  // namespace nvblox
