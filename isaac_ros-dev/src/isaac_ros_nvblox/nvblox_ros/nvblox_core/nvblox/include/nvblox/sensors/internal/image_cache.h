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

struct ImageCacheKey {
  int rows;
  int cols;
  MemoryType memory_type;

  inline bool operator==(const ImageCacheKey& other) const;
};

struct ImageCacheKeyHash {
  inline std::size_t operator()(const ImageCacheKey& key) const;
};

template <typename ImageType>
class ImageCache {
 public:
  ImageCache() = default;
  ~ImageCache() = default;

  /// Returns an already allocated image if one of the right size and memory
  /// type has been requested before, or allocates and returns that image.
  /// @param rows The number of rows in the returned image.
  /// @param cols The number of cols in the returned image.
  /// @param memory_type The memory type of the returned image.
  /// @return The image.
  ImageType* get(const int rows, const int cols, const MemoryType memory_type);

 private:
  using ImageCacheMap =
      std::unordered_map<ImageCacheKey, std::shared_ptr<ImageType>,
                         ImageCacheKeyHash, std::equal_to<ImageCacheKey>>;

  ImageCacheMap image_cache_;
};

}  // namespace nvblox

#include "nvblox/sensors/internal/impl/image_cache_impl.h"
