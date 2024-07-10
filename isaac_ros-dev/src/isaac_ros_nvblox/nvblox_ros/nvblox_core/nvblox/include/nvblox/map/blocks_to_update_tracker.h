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

#include <future>

#include "nvblox/core/hash.h"
#include "nvblox/core/types.h"

namespace nvblox {

/// @brief Types of blocks being tracked.
enum class BlocksToUpdateType { kEsdf, kMesh, kFreespace };

/// @brief Class to keep track of esdf, mesh and freespace blocks that need to
/// be updated.
class BlocksToUpdateTracker {
 public:
  BlocksToUpdateTracker(ProjectiveLayerType projective_layer_type)
      : projective_layer_type_(projective_layer_type){};

  /// @brief Adding blocks that need an update.
  /// @param blocks_to_update Vector of block indices that need an update.
  void addBlocksToUpdate(const std::vector<Index3D>& blocks_to_update);

  /// @brief Removing blocks from the set of blocks that need an update.
  /// @param blocks_to_remove Vector of block indices that don't need an update.
  void removeBlocksToUpdate(const std::vector<Index3D>& blocks_to_remove);

  /// @brief Get the esdf, mesh or freespace blocks that need and update.
  /// @param blocks_to_update_type The type of blocks you want to get the vector
  /// for.
  /// @return Vector of block indices that need an update for the chosen block
  /// type.
  std::vector<Index3D> getBlocksToUpdate(
      BlocksToUpdateType blocks_to_update_type) const;

  /// @brief Mark all blocks of a block type to be updated.
  /// @param blocks_to_update_type The type of blocks that got updated.
  void markBlocksAsUpdated(BlocksToUpdateType blocks_to_update_type);

 private:
  ProjectiveLayerType projective_layer_type_;

  /// These collections keep track of the blocks which need to be updated on
  /// the next calls to updateMesh(), updateFreespace() upd updateEsdf()
  /// respectively.
  Index3DSet esdf_blocks_to_update_;
  Index3DSet mesh_blocks_to_update_;
  Index3DSet freespace_blocks_to_update_;

  // Object to synchronize async functions (initialize to valid)
  mutable std::future<void> future_ = std::async(std::launch::async, []() {});
};

}  // namespace nvblox
