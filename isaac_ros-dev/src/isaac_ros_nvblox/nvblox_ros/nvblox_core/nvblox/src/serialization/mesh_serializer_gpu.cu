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

#include "nvblox/serialization/mesh_serializer_gpu.h"

#include <cuda_runtime.h>
#include <string>

#include "glog/logging.h"
#include "nvblox/core/internal/error_check.h"

namespace nvblox {

std::shared_ptr<const SerializedMesh> MeshSerializerGpu::serializeMesh(
    const MeshLayer& mesh_layer,
    const std::vector<Index3D>& block_indices_to_serialize,
    const CudaStream cuda_stream) {
  vertex_serializer_.serializeAsync(
      mesh_layer, block_indices_to_serialize, serialized_mesh_->vertices,
      serialized_mesh_->vertex_block_offsets,
      [](const MeshBlock* mesh_block) -> const std::pair<const Vector3f*, int> {
        return std::make_pair(mesh_block->vertices.data(),
                              mesh_block->vertices.size());
      },
      cuda_stream);

  color_serializer_.serializeAsync(
      mesh_layer, block_indices_to_serialize, serialized_mesh_->colors,
      serialized_mesh_->vertex_block_offsets,
      [](const MeshBlock* mesh_block) -> const std::pair<const Color*, int> {
        return std::make_pair(mesh_block->colors.data(),
                              mesh_block->colors.size());
      },
      cuda_stream);

  triangle_index_serializer_.serializeAsync(
      mesh_layer, block_indices_to_serialize,
      serialized_mesh_->triangle_indices,
      serialized_mesh_->triangle_index_block_offsets,
      [](const MeshBlock* mesh_block) -> const std::pair<const int*, int> {
        return std::make_pair(mesh_block->triangles.data(),
                              mesh_block->triangles.size());
      },
      cuda_stream);

  // Create an unique identifier for each block.
  serialized_mesh_->block_indices = block_indices_to_serialize;

  cuda_stream.synchronize();

  return serialized_mesh_;
}

MeshSerializerGpu::MeshSerializerGpu()
    : serialized_mesh_(std::make_shared<SerializedMesh>()) {}

}  // namespace nvblox
