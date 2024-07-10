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
#include <gtest/gtest.h>
#include <algorithm>
#include "nvblox/mesh/mesh_integrator.h"
#include "nvblox/primitives/scene.h"
#include "nvblox/serialization/layer_serializer_gpu.h"
#include "nvblox/tests/utils.h"

using namespace nvblox;

class LayerSerializerGpuTestFixture : public ::testing::Test {
 protected:
  void SetUp() override {
    std::srand(0);

    // Create a SDF layer scene
    primitives::Scene scene;
    scene.aabb() = AxisAlignedBoundingBox(Vector3f(-3.0f, -3.0f, 0.0f),
                                          Vector3f(3.0f, 3.0f, 3.0f));
    scene.addPrimitive(std::make_unique<primitives::Plane>(
        Vector3f(0.0, 0.0, 0.0), Vector3f(-1, 0, 0)));
    scene.generateLayerFromScene(4 * kVoxelSize, &tsdf_layer_);
    CHECK(tsdf_layer_.size() > 10);
  }
  static constexpr float kVoxelSize = 0.1;
  TsdfLayer tsdf_layer_{kVoxelSize, MemoryType::kUnified};
};

TEST_F(LayerSerializerGpuTestFixture, serializeAllBlocks) {
  std::vector<Index3D> block_indices = tsdf_layer_.getAllBlockIndices();
  TsdfLayerSerializerGpu serializer;

  auto serialized_tsdf =
      serializer.serialize(tsdf_layer_, block_indices, CudaStreamOwning());

  EXPECT_EQ(serialized_tsdf->block_indices.size(), block_indices.size());

  for (size_t i = 0; i < block_indices.size(); ++i) {
    EXPECT_EQ(block_indices[i], serialized_tsdf->block_indices[i]);

    const int offset = serialized_tsdf->block_offsets[i];
    const int voxels_in_block = serialized_tsdf->block_offsets[i + 1] - offset;
    EXPECT_EQ(voxels_in_block, TsdfBlock::kNumVoxels);

    for (int j = 0; j < TsdfBlock::kNumVoxels; ++j) {
      EXPECT_EQ(
          serialized_tsdf->voxels[offset + j].weight,
          (&tsdf_layer_.getBlockAtIndex(block_indices[i])->voxels[0][0][0] + j)
              ->weight);
      EXPECT_EQ(
          serialized_tsdf->voxels[offset + j].distance,
          (&tsdf_layer_.getBlockAtIndex(block_indices[i])->voxels[0][0][0] + j)
              ->distance);
    }
  }
}

TEST_F(LayerSerializerGpuTestFixture, serializeNoBlocks) {
  std::vector<Index3D> block_indices = {};
  TsdfLayerSerializerGpu serializer;

  auto serialized_tsdf =
      serializer.serialize(tsdf_layer_, block_indices, CudaStreamOwning());

  EXPECT_EQ(serialized_tsdf->voxels.size(), 0);
  EXPECT_EQ(serialized_tsdf->block_indices.size(), 0);
}

TEST_F(LayerSerializerGpuTestFixture, serializeEmptyLayer) {
  std::vector<Index3D> block_indices = tsdf_layer_.getAllBlockIndices();
  tsdf_layer_.clear();

  TsdfLayerSerializerGpu serializer;

  auto serialized_tsdf =
      serializer.serialize(tsdf_layer_, block_indices, CudaStreamOwning());

  EXPECT_EQ(serialized_tsdf->block_indices.size(), block_indices.size());
  EXPECT_EQ(serialized_tsdf->voxels.size(), 0);
}

int main(int argc, char** argv) {
  google::InitGoogleLogging(argv[0]);
  FLAGS_alsologtostderr = true;
  google::InstallFailureSignalHandler();
  testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
