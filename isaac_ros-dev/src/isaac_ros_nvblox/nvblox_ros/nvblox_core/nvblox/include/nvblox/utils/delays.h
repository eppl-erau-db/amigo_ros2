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

#include <numeric>
#include <string>
#include <unordered_map>

#include <glog/logging.h>

#include <nvblox/core/time.h>
#include <nvblox/utils/timing.h>

namespace nvblox {
namespace timing {

/// Accumulates delay measurements for a single tag.
struct DelayTicker {
  DelayTicker() = default;
  ~DelayTicker() = default;

  /// Add a delay measurement
  /// The delay is calculated as (delayed_timestamp_ns - reference_timestamp_ns)
  /// @param reference_timestamp_ns The reference time stamp in nanoseconds.
  /// @param delayed_timestamp_ns The delayed time stamp in nanoseconds. When
  /// this value is greater that the reference time stamp, delay is positive.
  void tick(const Time reference_timestamp_ns, const Time delayed_timestamp_ns);

  /// Return windowed average of the delay in nanoseconds.
  /// @return The average delay.
  double getRollingMeanDelayInNanoSeconds() const;

  /// Return windowed average of the delay is seconds.
  /// @return The average delay.
  double getRollingMeanDelayInSeconds() const;

  /// Return the number of samples in the rolling window used to compute the
  /// average.
  /// @return The number of samples.
  int getNumSamples() const;

 protected:
  /// Create an accumulator with specified window size.
  static constexpr int kAccumulatorSize = 100;
  using DelayAccumulatorType = Accumulator<int64_t, int64_t, kAccumulatorSize>;
  DelayAccumulatorType acc_;
};

class Delays {
 public:
  /// Adds a measurement to a tag.
  /// @param tag The name associated with the measurement.
  /// @param reference_timestamp_ns The reference time stamp in nanoseconds.
  /// @param delayed_timestamp_ns The delayed time stamp in nanoseconds. When
  /// this value is greater that the reference time stamp, delay is positive.
  static void tick(const std::string& tag, const Time reference_timestamp_ns,
                   const Time delayed_timestamp_ns);

  /// Get a reference to the Delays singleton
  /// @return A reference to this program's delays singleton
  static Delays& getInstance();

  /// Gets a ticker by tag. Creates one if it doesn't already exist.
  /// @param tag The ticker's name.
  /// @return The ticker.
  static DelayTicker& getTicker(const std::string& tag);

  /// Does a ticker associated with the tag already exist (and have
  /// measurements).
  /// @param tag The name of the ticker.
  /// @return True if the ticker exists.
  static bool exists(const std::string& tag);

  /// Return windowed average of the delay in nanoseconds.
  /// @param tag The ticker's name.
  /// @return The average delay.
  static double getRollingMeanDelayInNanoSeconds(const std::string& tag);

  /// Return windowed average of the delay is seconds.
  /// @param tag The ticker's name.
  /// @return The average delay.
  static double getRollingMeanDelayInSeconds(const std::string& tag);

  /// Output interface. Prints a table of the delays of the ticked tags.
  /// @param out The stream to be printed to.
  static void Print(std::ostream& out);

  /// Output interface. Prints a table of the delays of the ticked tags.
  /// @return A table of the delays of the ticked tags as a string.
  static std::string Print();

 private:
  Delays() = default;
  ~Delays() = default;

  // Formats a floating point delay for writing to our table string.
  static std::string delayToString(double delay_s);

  using TickerMap = std::unordered_map<std::string, DelayTicker>;

  std::mutex mutex_;
  TickerMap tickers_;
  size_t max_tag_length_ = 0;
};

}  // namespace timing
}  // namespace nvblox
