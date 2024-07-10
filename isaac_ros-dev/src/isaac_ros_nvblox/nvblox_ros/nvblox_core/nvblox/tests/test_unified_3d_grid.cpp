/*
Copyright 2022 NVIDIA CORPORATION

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

#include "nvblox/map/unified_3d_grid.h"
#include "nvblox/tests/test_utils_cuda.h"
#include "nvblox/tests/utils.h"

using namespace nvblox;

void testValuesInGrid(int value, const Index3D& min_index,
                      const Index3D& aabb_size, Unified3DGrid<int>& grid) {
  for (int x = 0; x < aabb_size.x(); x++) {
    for (int y = 0; y < aabb_size.y(); y++) {
      for (int z = 0; z < aabb_size.z(); z++) {
        Index3D global_idx = Index3D(x, y, z) + min_index;
        EXPECT_TRUE(grid.isInsideGrid(global_idx));
        EXPECT_EQ(grid(global_idx), value);
      }
    }
  }
}

TEST(Unified3DGridTest, SetGridToValue) {
  const Index3D min_index(10, 20, 30);
  const Index3D aabb_size(10, 10, 10);
  CudaStreamOwning cuda_stream;

  // Generate gpu grid and set zero
  Unified3DGrid<int> device_3d_grid(MemoryType::kDevice);
  device_3d_grid.setAABBAsync(min_index, aabb_size, cuda_stream);
  device_3d_grid.setZeroAsync(cuda_stream);

  // Copy grid to CPU
  Unified3DGrid<int> host_3d_grid_zeroed(MemoryType::kHost);
  host_3d_grid_zeroed.copyFromAsync(device_3d_grid, cuda_stream);
  checkCudaErrors(cudaDeviceSynchronize());
  checkCudaErrors(cudaPeekAtLastError());

  // Check that all cells are set to zero
  testValuesInGrid(0, min_index, aabb_size, host_3d_grid_zeroed);

  constexpr int kValueToSet = 1;
  test_utils::fill3DGridWithConstant(kValueToSet, cuda_stream, &device_3d_grid);

  // Copy grid to CPU
  Unified3DGrid<int> host_3d_grid_ones(MemoryType::kHost);
  host_3d_grid_ones.copyFromAsync(device_3d_grid, cuda_stream);
  checkCudaErrors(cudaDeviceSynchronize());
  checkCudaErrors(cudaPeekAtLastError());

  // Check that all cells are set to one
  testValuesInGrid(1, min_index, aabb_size, host_3d_grid_ones);

  // Check isInsideGrid function
  const Index3D max_index = min_index + aabb_size - Index3D::Ones();
  EXPECT_TRUE(host_3d_grid_ones.isInsideGrid(max_index));
  EXPECT_FALSE(
      host_3d_grid_ones.isInsideGrid(Index3D(max_index.x() + 1, 0, 0)));
  EXPECT_FALSE(
      host_3d_grid_ones.isInsideGrid(Index3D(0, max_index.y() + 1, 0)));
  EXPECT_FALSE(
      host_3d_grid_ones.isInsideGrid(Index3D(0, 0, max_index.z() + 1)));
}

int main(int argc, char** argv) {
  FLAGS_alsologtostderr = true;
  google::InitGoogleLogging(argv[0]);
  google::InstallFailureSignalHandler();
  testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
