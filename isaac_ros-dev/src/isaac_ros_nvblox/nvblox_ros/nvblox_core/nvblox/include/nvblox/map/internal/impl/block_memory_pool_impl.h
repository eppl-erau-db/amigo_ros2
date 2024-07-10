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

#include "nvblox/map/internal/block_memory_pool.h"

namespace nvblox {

template <class BlockType>
BlockMemoryPool<BlockType>::BlockMemoryPool(const MemoryType memory_type,
                                            const int num_preallocated_blocks)
    : memory_type_(memory_type) {
  expand(num_preallocated_blocks, CudaStreamOwning());
}

template <class BlockType>
typename BlockType::Ptr BlockMemoryPool<BlockType>::popBlock(
    const CudaStream cuda_stream) {
  if (blocks_.size() == 0) {
    expand(kExpansionFactor * num_allocated_blocks_, cuda_stream);
  }
  typename BlockType::Ptr popped = blocks_.top();
  BlockType::initAsync(popped.get(), memory_type_, cuda_stream);
  blocks_.pop();
  return popped;
}

template <class BlockType>
void BlockMemoryPool<BlockType>::pushBlock(
    const typename BlockType::Ptr block) {
  blocks_.push(block);
}

template <class BlockType>
void BlockMemoryPool<BlockType>::expand(const size_t num_blocks_to_allocate,
                                        const CudaStream cuda_stream) {
  for (size_t i = 0; i < num_blocks_to_allocate; ++i) {
    blocks_.push(BlockType::allocateAsync(memory_type_, cuda_stream));
  }
  num_allocated_blocks_ += num_blocks_to_allocate;

  LOG(INFO) << "Expanding the memory pool with " << num_blocks_to_allocate
            << " blocks. Number of allocated blocks: " << num_allocated_blocks_;

  cuda_stream.synchronize();
}

}  // namespace nvblox
