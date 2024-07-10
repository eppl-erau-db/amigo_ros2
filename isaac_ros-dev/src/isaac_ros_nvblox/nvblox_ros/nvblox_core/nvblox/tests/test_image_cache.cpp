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

#include <glog/logging.h>
#include <gtest/gtest.h>

#include "nvblox/sensors/image.h"
#include "nvblox/sensors/internal/image_cache.h"

using namespace nvblox;

constexpr float kEpsilon = 1e-4;

class ImageCacheTest : public ::testing::Test {
 protected:
  ImageCacheTest() {}

  void SetUp() override {}

  ImageCache<DepthImage> image_cache;
};

TEST_F(ImageCacheTest, SingleImage) {
  const int rows = 2;
  const int cols = 2;
  const MemoryType memory_type = MemoryType::kUnified;
  DepthImage* image_ptr_1 = image_cache.get(rows, cols, memory_type);
  EXPECT_EQ(image_ptr_1->rows(), rows);
  EXPECT_EQ(image_ptr_1->cols(), cols);
  EXPECT_EQ(image_ptr_1->memory_type(), memory_type);

  (*image_ptr_1)(0, 0) = 1.0f;

  DepthImage* image_ptr_2 = image_cache.get(rows, cols, memory_type);

  constexpr float kEps = 1e-6;
  EXPECT_NEAR((*image_ptr_1)(0, 0), 1.0f, kEps);
  EXPECT_EQ(image_ptr_1, image_ptr_2);
}

TEST_F(ImageCacheTest, DoubleImage) {
  const int rows_1 = 2;
  const int cols_1 = 2;
  const MemoryType memory_type = MemoryType::kUnified;
  DepthImage* image_ptr_1_1 = image_cache.get(rows_1, cols_1, memory_type);

  const int rows_2 = 3;
  const int cols_2 = 3;
  DepthImage* image_ptr_2_1 = image_cache.get(rows_2, cols_2, memory_type);

  DepthImage* image_ptr_1_2 = image_cache.get(rows_1, cols_1, memory_type);
  DepthImage* image_ptr_2_2 = image_cache.get(rows_2, cols_2, memory_type);

  CHECK_EQ(image_ptr_1_1, image_ptr_1_2);
  CHECK_EQ(image_ptr_2_1, image_ptr_2_2);

  CHECK_NE(image_ptr_1_1, image_ptr_2_1);
}

int main(int argc, char** argv) {
  google::InitGoogleLogging(argv[0]);
  FLAGS_alsologtostderr = true;
  google::InstallFailureSignalHandler();
  testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
