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
#include <string>
#include "nvblox/utils/params.h"

namespace nvblox {

constexpr Param<int>::Description kParamTestDescription{"my_param", 10,
                                                        "my_description"};

constexpr Param<std::string, const char*>::Description kStringParamDescription{
    "my_string_param", "the_awesome_string", "my_description"};

TEST(ParamTest, assignAndGet) {
  Param<int> param(kParamTestDescription);

  param = 11;
  EXPECT_EQ(param.get(), 11);
  EXPECT_EQ(param.description().default_value, 10);
  EXPECT_EQ(param.description().name, "my_param");
}

TEST(ParamTest, assignTo) {
  Param<int> param(kParamTestDescription);
  int value = param;
  EXPECT_EQ(value, 10);
}

TEST(ParamTest, stringParam) {
  StringParam param(kStringParamDescription);
  std::string value = param;
  EXPECT_EQ(value, "the_awesome_string");
}

}  // namespace nvblox
int main(int argc, char** argv) {
  FLAGS_alsologtostderr = true;
  google::InitGoogleLogging(argv[0]);
  google::InstallFailureSignalHandler();
  testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
