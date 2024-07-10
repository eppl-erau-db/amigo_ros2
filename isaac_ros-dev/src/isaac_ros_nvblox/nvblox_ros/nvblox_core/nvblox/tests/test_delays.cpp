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
#include <gtest/gtest.h>

#include <chrono>
#include <thread>

#include "nvblox/core/time.h"
#include "nvblox/utils/delays.h"

using namespace nvblox;

TEST(DelaysTest, ExistsTest) {
  const std::string test_tag = "ExistsTest";

  EXPECT_FALSE(timing::Delays::exists(test_tag));
  timing::Delays::tick(test_tag, Time(0l), Time(0l));
  EXPECT_TRUE(timing::Delays::exists(test_tag));
}

TEST(DelaysTest, DelayTest) {
  const std::string test_tag = "DelayTest";

  constexpr Time reference_time_ns(0l);
  constexpr Time delayed_time_ns(1l);

  timing::Delays::tick(test_tag, reference_time_ns, delayed_time_ns);

  constexpr double kEps = 1.0e-6;
  const double delay_ns =
      timing::Delays::getRollingMeanDelayInNanoSeconds(test_tag);
  EXPECT_NEAR(delay_ns, 1.0, kEps);
}

TEST(DelaysTest, MultipleDelayTest) {
  // Create a series of tickers
  auto index_to_tag = [](int index) { return "tag_" + std::to_string(index); };
  constexpr int kNumTickers = 10;
  for (int ticker_idx = 0; ticker_idx < kNumTickers; ticker_idx++) {
    const std::string tag = index_to_tag(ticker_idx);
    constexpr int kNumSamples = 200;
    for (int sample_idx = 0; sample_idx < kNumSamples; sample_idx++) {
      // Create a number of samples with delays equal to ticker index
      constexpr int64_t kNanoSecondsToSeconds = 1e9;
      const Time reference_timestamp_ns(0);
      const Time delayed_timestamp_ns(ticker_idx * kNanoSecondsToSeconds);
      timing::Delays::tick(tag, reference_timestamp_ns, delayed_timestamp_ns);
    }
  }

  LOG(INFO) << timing::Delays::Print();

  // Check
  for (int ticker_idx = 0; ticker_idx < kNumTickers; ticker_idx++) {
    const double measured_delay_s =
        timing::Delays::getRollingMeanDelayInSeconds(index_to_tag(ticker_idx));
    const double expected_delay_s = static_cast<double>(ticker_idx);
    constexpr double kEps = 1e-6;
    EXPECT_NEAR(measured_delay_s, expected_delay_s, kEps);
  }
}

int main(int argc, char** argv) {
  google::InitGoogleLogging(argv[0]);
  FLAGS_alsologtostderr = true;
  google::InstallFailureSignalHandler();
  testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
