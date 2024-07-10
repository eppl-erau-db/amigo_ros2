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

#include "nvblox/core/cuda_stream.h"
#include "nvblox/core/types.h"
#include "nvblox/core/unified_vector.h"

namespace nvblox {

template <typename CellType>
class GPU3DGridView;

/// A class for representing a 3D grid of cells.
/// It stores the data in a unified vector and implements data access by 3D
/// indices. The data can be copied from an to device.
template <typename CellType>
class Unified3DGrid {
 public:
  Unified3DGrid(MemoryType memory_type)
      : data_vector_(unified_vector<CellType>(memory_type)) {}
  virtual ~Unified3DGrid() = default;

  /// Accessors for the underlying grid
  bool isInsideGrid(const Index3D& index) const;
  CellType& operator()(const Index3D& index);
  const CellType& operator()(const Index3D& index) const;

  /// Deep copies with and without stream synchronization
  void copyFromAsync(const Unified3DGrid<CellType>& other,
                     const CudaStream& cuda_stream);
  void copyFrom(const Unified3DGrid<CellType>& other);

  /// Set the entire *memory* of the grid to zero.
  void setZeroAsync(const CudaStream& cuda_stream);
  void setZero();

  /// Setting the AABB and resizing the data vector according to the aabb size.
  void setAABBAsync(const Index3D& min_index, const Index3D& aabb_size,
                    const CudaStream& cuda_stream);
  void setAABB(const Index3D& min_index, const Index3D& aabb_size);

  GPU3DGridView<CellType> getGPUView();

  /// A parameter getter
  /// @returns the minimum index of the AABB.
  Index3D min_index() const { return min_index_; }

  /// A parameter getter
  /// @returns the size of the AABB.
  Index3D aabb_size() const { return aabb_size_; }

  /// Returns the underlying data vector.
  /// @return The vector contain grid data.
  unified_vector<CellType>& data() { return data_vector_; }

  /// Returns the underlying data vector.
  /// @return The vector contain grid data.
  const unified_vector<CellType>& data() const { return data_vector_; }

 private:
  /// AABB definition
  Index3D min_index_;
  Index3D aabb_size_;

  /// The actual data
  unified_vector<CellType> data_vector_;
};

/// A view of the Unified3DGrid class for accessing the grid on the GPU.
template <typename CellType>
class GPU3DGridView {
 public:
  GPU3DGridView(const Index3D& min_index, const Index3D& aabb_size,
                CellType* data)
      : min_index_(min_index), aabb_size_(aabb_size), data_(data) {}

  /// Accessors for the underlying grid
  __device__ bool isInsideGrid(const Index3D& index) const;
  __device__ CellType& operator()(const Index3D& index);
  __device__ const CellType& operator()(const Index3D& index) const;

 private:
  Index3D min_index_;
  Index3D aabb_size_;
  CellType* data_;
};

}  // namespace nvblox

#include "nvblox/map/internal/impl/unified_3d_grid_impl.h"
