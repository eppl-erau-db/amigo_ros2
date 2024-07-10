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
#include <gtest/gtest.h>

#include "nvblox/core/types.h"
#include "nvblox/core/unified_ptr.h"
#include "nvblox/gpu_hash/gpu_layer_view.h"
#include "nvblox/gpu_hash/internal/cuda/gpu_hash_interface.cuh"
#include "nvblox/gpu_hash/internal/cuda/gpu_indexing.cuh"
#include "nvblox/map/common_names.h"
#include "nvblox/map/layer.h"

using namespace nvblox;

__global__ void copyBlockAtOrigin(
    Index3DDeviceHashMapType<EsdfBlock> block_hash, EsdfBlock* output_block) {
  const Index3D block_idx(blockIdx.x, blockIdx.y, blockIdx.z);
  const Index3D thread_idx(threadIdx.x, threadIdx.y, threadIdx.z);
  __shared__ EsdfBlock* block_ptr;
  if ((thread_idx.array() == Index3D::Zero().array()).all()) {
    block_ptr = getBlockPtr(block_hash, block_idx);
  }
  __syncthreads();

  if (block_ptr == nullptr) {
    return;
  }

  // Copy to output
  output_block->voxels[threadIdx.z][threadIdx.y][threadIdx.x]
      .squared_distance_vox =
      block_ptr->voxels[threadIdx.z][threadIdx.y][threadIdx.x]
          .squared_distance_vox;
}

float getTestValue(const Index3D& idx) {
  constexpr int kMaxValue = 1000;
  return static_cast<float>(Index3DHash()(idx) % kMaxValue);
}

void checkBlockValues(const EsdfBlock& block,
                      std::function<float(const Index3D&)> get_value) {
  for (int x = 0; x < EsdfBlock::kVoxelsPerSide; x++) {
    for (int y = 0; y < EsdfBlock::kVoxelsPerSide; y++) {
      for (int z = 0; z < EsdfBlock::kVoxelsPerSide; z++) {
        EXPECT_EQ(block.voxels[x][y][z].squared_distance_vox,
                  get_value(Index3D(x, y, z)));
      }
    }
  }
}

void setBlockValues(EsdfBlock* block,
                    std::function<float(const Index3D&)> get_value) {
  for (int x = 0; x < EsdfBlock::kVoxelsPerSide; x++) {
    for (int y = 0; y < EsdfBlock::kVoxelsPerSide; y++) {
      for (int z = 0; z < EsdfBlock::kVoxelsPerSide; z++) {
        block->voxels[x][y][z].squared_distance_vox =
            get_value(Index3D(x, y, z));
      }
    }
  }
}

TEST(QueryAfterClear, SingleBlock) {
  constexpr float kVoxelSize = 0.05f;
  EsdfLayer esdf_layer(kVoxelSize, MemoryType::kUnified);
  auto block_ptr = esdf_layer.allocateBlockAtIndex(Index3D(0, 0, 0));

  auto get_test_value = [](const Index3D& idx) -> float {
    return getTestValue(idx);
  };
  auto get_zero = [](const Index3D&) -> float { return 0.0f; };

  // Test values
  setBlockValues(block_ptr.get(), get_test_value);

  // Output block
  auto output_block_ptr = EsdfBlock::allocate(MemoryType::kUnified);

  // Query on the GPU
  constexpr int kNumBlocks = 1;
  constexpr int kVoxelsPerSide = VoxelBlock<EsdfVoxel>::kVoxelsPerSide;
  const dim3 kThreadsPerBlock(kVoxelsPerSide, kVoxelsPerSide, kVoxelsPerSide);
  copyBlockAtOrigin<<<kNumBlocks, kThreadsPerBlock>>>(
      esdf_layer.getGpuLayerView().getHash().impl_, output_block_ptr.get());
  cudaDeviceSynchronize();
  cudaPeekAtLastError();

  // Check
  LOG(INFO) << "Testing copy had an effect.";
  checkBlockValues(*output_block_ptr, get_test_value);

  // Clear the layer
  esdf_layer.clear();

  // Set the output block zero
  setBlockValues(output_block_ptr.get(), get_zero);

  // Try to copy again, should be a no-op.
  copyBlockAtOrigin<<<kNumBlocks, kThreadsPerBlock>>>(
      esdf_layer.getGpuLayerView().getHash().impl_, output_block_ptr.get());
  cudaDeviceSynchronize();
  cudaPeekAtLastError();

  // Check that the last kernel didn't affect the output.
  LOG(INFO) << "Testing copy didn't happen.";
  checkBlockValues(*output_block_ptr, get_zero);
}

int main(int argc, char** argv) {
  google::InitGoogleLogging(argv[0]);
  FLAGS_alsologtostderr = true;
  google::InstallFailureSignalHandler();
  testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
