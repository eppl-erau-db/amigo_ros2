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

#include "nvblox/map/common_names.h"
#include "nvblox/map/internal/block_memory_pool.h"

using namespace nvblox;

static constexpr size_t kInitialCapacity = 10;

TEST(BlockMemoryPool, popBeyondCapacity) {
  // The pool should resize internally if we pop beyond capacity
  BlockMemoryPool<TsdfBlock> pool(MemoryType::kHost, kInitialCapacity);
  for (size_t i = 0; i < 2 * kInitialCapacity; ++i) {
    auto block = pool.popBlock(CudaStreamOwning());
    ASSERT_TRUE(block != nullptr);
  }
}

TEST(BlockMemoryPool, pushAndPop) {
  BlockMemoryPool<TsdfBlock> pool(MemoryType::kHost);

  auto popped_block = pool.popBlock(CudaStreamOwning());
  ASSERT_TRUE(popped_block != nullptr);
  pool.pushBlock(popped_block);
  auto repopped_block = pool.popBlock(CudaStreamOwning());

  // We should get the same pointer back
  ASSERT_EQ(popped_block.get(), repopped_block.get());
}

int main(int argc, char** argv) {
  FLAGS_alsologtostderr = true;
  google::InitGoogleLogging(argv[0]);
  google::InstallFailureSignalHandler();
  testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
