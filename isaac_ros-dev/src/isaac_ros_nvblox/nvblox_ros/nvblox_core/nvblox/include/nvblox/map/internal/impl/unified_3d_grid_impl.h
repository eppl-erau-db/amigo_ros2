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

#include "nvblox/map/unified_3d_grid.h"

namespace nvblox {

// AABB linear indexing
// - We index in z-major, i.e. z is varied first, then y, then x.
// - Linear indexing within an AABB is relative and starts at zero. This is
//   not true for AABB 3D indexing which is w.r.t. the layer origin.
__host__ __device__ inline size_t layerIndexToAabbLinearIndex(
    const Index3D& index, const Index3D& aabb_min, const Index3D& aabb_size) {
  const Index3D index_shifted = index - aabb_min;
  return index_shifted.z() +                                 // NOLINT
         index_shifted.y() * aabb_size.z() +                 // NOLINT
         index_shifted.x() * aabb_size.z() * aabb_size.y();  // NOLINT
}

__host__ __device__ inline bool isInsideAABB(const Index3D& index,
                                             const Index3D& aabb_min,
                                             const Index3D& aabb_size) {
  const Index3D index_shifted = index - aabb_min;
  return (index_shifted.x() < aabb_size.x()) &&  // NOLINT
         (index_shifted.y() < aabb_size.y()) &&  // NOLINT
         (index_shifted.z() < aabb_size.z()) &&  // NOLINT
         (index_shifted.x() >= 0) &&             // NOLINT
         (index_shifted.y() >= 0) &&             // NOLINT
         (index_shifted.z() >= 0);               // NOLINT
}

template <typename CellType>
bool Unified3DGrid<CellType>::isInsideGrid(const Index3D& index) const {
  return isInsideAABB(index, min_index_, aabb_size_);
}

template <typename CellType>
CellType& Unified3DGrid<CellType>::operator()(const Index3D& index) {
  return data_vector_[layerIndexToAabbLinearIndex(index, min_index_,
                                                  aabb_size_)];
}

template <typename CellType>
const CellType& Unified3DGrid<CellType>::operator()(
    const Index3D& index) const {
  return data_vector_[layerIndexToAabbLinearIndex(index, min_index_,
                                                  aabb_size_)];
}

template <typename CellType>
void Unified3DGrid<CellType>::copyFromAsync(
    const Unified3DGrid<CellType>& other, const CudaStream& cuda_stream) {
  setAABBAsync(other.min_index_, other.aabb_size_, cuda_stream);
  data_vector_.copyFromAsync(other.data_vector_, cuda_stream);
}

template <typename CellType>
void Unified3DGrid<CellType>::copyFrom(const Unified3DGrid<CellType>& other) {
  copyFromAsync(other, CudaStreamOwning());
}

template <typename CellType>
void Unified3DGrid<CellType>::setZeroAsync(const CudaStream& cuda_stream) {
  data_vector_.setZeroAsync(cuda_stream);
}

template <typename CellType>
void Unified3DGrid<CellType>::setZero() {
  setZeroAsync(CudaStreamOwning());
}

template <typename CellType>
void Unified3DGrid<CellType>::setAABBAsync(const Index3D& min_index,
                                           const Index3D& aabb_size,
                                           const CudaStream& cuda_stream) {
  min_index_ = min_index;
  aabb_size_ = aabb_size;
  const size_t aabb_linear_size =
      aabb_size_.x() * aabb_size_.y() * aabb_size_.z();

  // Expand the buffers when needed
  if (aabb_linear_size > data_vector_.capacity()) {
    constexpr float kBufferExpansionFactor = 1.5f;
    const int new_size =
        static_cast<int>(kBufferExpansionFactor * aabb_linear_size);
    data_vector_.reserveAsync(new_size, cuda_stream);
  }

  // Resize according to AABB size
  data_vector_.resizeAsync(aabb_linear_size, cuda_stream);
}

template <typename CellType>
void Unified3DGrid<CellType>::setAABB(const Index3D& min_index,
                                      const Index3D& aabb_size) {
  setAABBAsync(min_index, aabb_size, CudaStreamOwning());
}

template <typename CellType>
GPU3DGridView<CellType> Unified3DGrid<CellType>::getGPUView() {
  return GPU3DGridView<CellType>(min_index_, aabb_size_, data_vector_.data());
}

template <typename CellType>
__device__ bool GPU3DGridView<CellType>::isInsideGrid(
    const Index3D& index) const {
  return isInsideAABB(index, min_index_, aabb_size_);
}

template <typename CellType>
__device__ CellType& GPU3DGridView<CellType>::operator()(const Index3D& index) {
  return data_[layerIndexToAabbLinearIndex(index, min_index_, aabb_size_)];
}

template <typename CellType>
__device__ const CellType& GPU3DGridView<CellType>::operator()(
    const Index3D& index) const {
  return data_[layerIndexToAabbLinearIndex(index, min_index_, aabb_size_)];
}

}  // namespace nvblox
