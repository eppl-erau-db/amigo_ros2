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

#include <glog/logging.h>
#include <iostream>
#include <vector>

#include <cuda_runtime.h>

#include <Eigen/Core>
#include <Eigen/Geometry>

namespace nvblox {

/// Whether the storage or processing is happening on CPU, GPU, or any future
/// amazing hardware- accelerated platform.
enum class DeviceType { kCPU, kGPU };

// Making a templated version of std::to_string, which can be specialized for
// nvblox types.
template <typename ParameterType>
inline std::string toString(const ParameterType& val) {
  return std::to_string(val);
}
// In the case of a string just return it.
template <>
inline std::string toString(const std::string& val) {
  return val;
}

/// How GPU data is stored, either in Device-only or unified (both) memory.
/// NOTE(alexmillane): tag: c++17, switch to constexpr when we move to c++17.
enum class MemoryType { kDevice, kUnified, kHost };
template <>
inline std::string toString(const MemoryType& memory_type) {
  switch (memory_type) {
    case MemoryType::kDevice:
      return "kDevice";
      break;
    case MemoryType::kUnified:
      return "kUnified";
      break;
    default:
      return "kHost";
      break;
  }
}
inline bool isGpuMemory(const MemoryType memory_type) {
  return ((memory_type == MemoryType::kDevice) ||
          (memory_type == MemoryType::kUnified));
}

// Which type of mapping to do.
enum class ProjectiveLayerType { kTsdf, kTsdfWithFreespace, kOccupancy, kNone };
template <>
inline std::string toString(const ProjectiveLayerType& layer_type) {
  switch (layer_type) {
    case ProjectiveLayerType::kTsdf:
      return "kTsdf";
      break;
    case ProjectiveLayerType::kTsdfWithFreespace:
      return "kTsdfWithFreespace";
      break;
    case ProjectiveLayerType::kOccupancy:
      return "kOccupancy";
      break;
    case ProjectiveLayerType::kNone:
      return "kNone";
      break;
    default:
      LOG(FATAL) << "Not implemented";
      break;
  }
  return "";
}

/// Whether we are maintaining a tsdf layer.
inline bool hasTsdfLayer(ProjectiveLayerType layer_type) {
  if (layer_type == ProjectiveLayerType::kTsdf ||
      layer_type == ProjectiveLayerType::kTsdfWithFreespace) {
    return true;
  }
  return false;
}

/// Whether we are maintaining a freespace layer.
inline bool hasFreespaceLayer(ProjectiveLayerType layer_type) {
  if (layer_type == ProjectiveLayerType::kTsdfWithFreespace) {
    return true;
  }
  return false;
}

typedef Eigen::Vector3i Index3D;
typedef Eigen::Vector2i Index2D;

typedef Eigen::Vector3f Vector3f;
typedef Eigen::Vector2f Vector2f;

typedef Eigen::AlignedBox3f AxisAlignedBoundingBox;

typedef Eigen::Isometry3f Transform;

/// This can be replaced with std::byte once we go to C++17.
typedef uint8_t Byte;

/// Aligned Eigen containers
template <typename Type>
using AlignedVector = std::vector<Type, Eigen::aligned_allocator<Type>>;

enum class InterpolationType { kNearestNeighbor, kLinear };

typedef Eigen::ParametrizedLine<float, 3> Ray;

}  // namespace nvblox
