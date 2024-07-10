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

#include <functional>
#include <unordered_map>

#include "nvblox/core/types.h"
#include "nvblox/sensors/image.h"

namespace nvblox {

bool ImageCacheKey::operator==(const ImageCacheKey& other) const {
  return rows == other.rows && cols == other.cols &&
         memory_type == other.memory_type;
}

std::size_t ImageCacheKeyHash::operator()(const ImageCacheKey& key) const {
  // NOTE(alexmillane): No doubt just adding these together is suboptimal.
  // But we don't need good performance from this hash.
  const auto int_hash = std::hash<int>();
  return int_hash(key.rows) + int_hash(key.cols) +
         int_hash(static_cast<int>(key.memory_type));
}

template <typename ImageType>
ImageType* ImageCache<ImageType>::get(const int rows, const int cols,
                                      const MemoryType memory_type) {
  ImageCacheKey key = {.rows = rows, .cols = cols, .memory_type = memory_type};
  auto it = image_cache_.find(key);
  if (it == image_cache_.end()) {
    LOG(INFO) << "Allocating a new cached image";
    auto res = image_cache_.emplace(
        key, std::make_shared<ImageType>(rows, cols, memory_type));
    return res.first->second.get();
  } else {
    return it->second.get();
  }
}

}  // namespace nvblox
