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

#include <stack>
#include <vector>
#include "nvblox/core/unified_ptr.h"

namespace nvblox {

/// Storage class for pre-allcoated blocks
///
/// Maintains a large number of blocks (unified pointers) that are pre-allocated
/// up front. This reduces the need for exepensive calls to cudaMmalloc and
/// cudaFree during runtime.
///
/// Whenever the client needs to allocate a new block, popBlock() should be
/// used which returns (and transfers ownership) of a pre-alloacated block.
///
/// Whenever the client needs to free a block, pushblock() should be used
/// which returns the block to the pool and makes it ready for re-use.
template <class BlockType>
class BlockMemoryPool {
 public:
  /// Constructor that allocates blocks
  /// @param memory_type              Memory type
  /// @param num_preallocated_blocks  Number of blocks allocated on construction
  BlockMemoryPool(const MemoryType memory_type,
                  const int num_preallocated_blocks = 2048);

  /// Obtain a block from the pool. Should be used instead of allocating a new
  /// block. The pool is expanded if there are no more blocks remaining.
  /// @param cuda_stream Used when allocating memory in case the buffer needs
  ///                    expansion. Will be synchronized.
  typename BlockType::Ptr popBlock(const CudaStream cuda_stream);

  /// Return a block to the pool. Should be used instead of de-allocating the
  /// block.
  /// @param block  Block to push
  void pushBlock(const typename BlockType::Ptr block);

 private:
  /// Expand the memory pool and synchronize the stream
  void expand(const size_t num_blocks_to_allocate,
              const CudaStream cuda_stream);

  /// Container for storing the memory in the pool
  std::stack<typename BlockType::Ptr> blocks_;

  /// Type of memory stored
  MemoryType memory_type_;
  int num_allocated_blocks_ = 0;

  /// When expanding the pool, this number is muliplied with the current
  /// num_allocated_blocks to get the new size.3
  static constexpr int kExpansionFactor = 2;
};

}  // namespace nvblox

#include "nvblox/map/internal/impl/block_memory_pool_impl.h"
