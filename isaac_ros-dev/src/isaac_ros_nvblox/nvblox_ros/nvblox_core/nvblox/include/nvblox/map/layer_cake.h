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
#pragma once

#include <memory>
#include <typeindex>
#include <unordered_map>

#include "nvblox/core/types.h"
#include "nvblox/map/layer.h"

namespace nvblox {

/// Holds a collection of layers. Currently a restriction that only 1 layer
/// of each type can be stored, and all layers should have the same voxel
/// (or block) size.
class LayerCake {
 public:
  /// Default constructor.
  LayerCake() = default;

  /// Constructor
  /// @param voxel_size Voxel size passed to the contained layers. In the case
  /// of (non-voxel) BlockLayer, the voxel size is transformed to a block size.
  LayerCake(float voxel_size) : voxel_size_(voxel_size) {}

  /// Deep Copy (disallowed for now)
  LayerCake(const LayerCake& other) = delete;
  LayerCake& operator=(const LayerCake& other) = delete;

  /// Move
  LayerCake(LayerCake&& other) = default;
  LayerCake& operator=(LayerCake&& other) = default;

  /// Creates a new layer in the cake.
  /// Note that only a single layer of each type may be added. Calls to try to
  /// add multiple layers of the same type will have no effect.
  /// @tparam LayerType The desired type of the added layer.
  /// @param memory_type The \ref MemoryType of the added layer.
  /// @return A pointer to the added layer.
  template <typename LayerType>
  LayerType* add(MemoryType memory_type);

  /// Moves a layer into the layer cake, transferring ownership.
  /// @param type_index The type index of the added layer.
  /// @param layer A (base class) pointer to the added layer.
  inline void insert(const std::type_index& type_index,
                     std::unique_ptr<BaseLayer>&& layer);

  /// Get a layer by type.
  /// @tparam LayerType The type of the layer to get.
  /// @return A pointer to the layer in the cake, or nullptr if no layer of this
  /// type exists in the cake.
  template <typename LayerType>
  LayerType* getPtr();
  /// See \ref getPtr.
  template <typename LayerType>
  const LayerType* getConstPtr() const;

  /// Get a layer by type.
  /// Terminates the program if the layer cake does not contain a layer of the
  /// specified type. See \ref getPtr for a more resilient interface.
  /// @tparam LayerType The type of the layer to get.
  /// @return A reference to the layer in the cake.
  template <typename LayerType>
  const LayerType& get() const;

  /// Check if a layer of the specified type exists in the cake.
  /// @tparam LayerType The type of the layer.
  /// @return True if a layer of the specified type exists in the cake.
  template <typename LayerType>
  bool exists() const;

  /// Check if the layer cake is empty.
  /// @return True if the layer cake contains no layers.
  bool empty() const { return layers_.empty(); }

  /// Delete all layers in the cake, deallocate all associated memory.
  void clear() { layers_.clear(); }

  /// Factory. Creates a LayerCake containing several layers
  /// @tparam ...LayerTypes A list of layer types to add to the cake.
  /// @param voxel_size The voxel size of the contained layers.
  /// @param memory_type Memory type passed to contained layers.
  /// @return A LayerCake containing the layers.
  template <typename... LayerTypes>
  static LayerCake create(float voxel_size, MemoryType memory_type);
  /// See \ref create
  /// Additionally accepts a list of memory types. One per layer.
  template <typename... LayerTypes, typename... MemoryTypes>
  static LayerCake create(float voxel_size, MemoryTypes... memory_type);

  /// Retrieve all layers in the cake by reference.
  /// @return A map containing the layers.
  const std::unordered_map<std::type_index, std::unique_ptr<BaseLayer>>&
  get_layers() const {
    return layers_;
  }

  /// Get the voxel size (in meters) of the contained layers.
  /// @return The voxel size.
  float voxel_size() const { return voxel_size_; }
  /// Get the block size (in meters) of the contained layers.
  /// @return The block size.
  float block_size() const {
    return voxel_size_ * VoxelBlock<bool>::kVoxelsPerSide;
  }

 private:
  /// The voxel size of contained layers.
  float voxel_size_ = 0.0f;

  /// Stored layers
  /// Note(alexmillane): Currently we restrict the cake to storing a single
  /// layer of each type.
  std::unordered_map<std::type_index, std::unique_ptr<BaseLayer>> layers_;
};

}  // namespace nvblox

#include "nvblox/map/internal/impl/layer_cake_impl.h"
