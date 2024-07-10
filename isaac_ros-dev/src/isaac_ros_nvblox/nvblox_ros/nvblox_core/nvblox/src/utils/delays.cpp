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
#include "nvblox/utils/delays.h"

namespace nvblox {
namespace timing {

void DelayTicker::tick(const Time reference_timestamp_ns,
                       const Time delayed_timestamp_ns) {
  const Time delay_ns = delayed_timestamp_ns - reference_timestamp_ns;
  acc_.Add(int64_t(delay_ns));
}

double DelayTicker::getRollingMeanDelayInNanoSeconds() const {
  if (acc_.TotalSamples() == 0) {
    return 0.0f;
  }
  return acc_.RollingMean();
}

double DelayTicker::getRollingMeanDelayInSeconds() const {
  constexpr double kNanoSecondsPerSecond = 1.0e9;
  return getRollingMeanDelayInNanoSeconds() / kNanoSecondsPerSecond;
}

int DelayTicker::getNumSamples() const { return acc_.WindowSamples(); }

Delays& Delays::getInstance() {
  static Delays delays;
  return delays;
}

DelayTicker& Delays::getTicker(const std::string& tag) {
  std::lock_guard<std::mutex> lock(getInstance().mutex_);
  TickerMap& tickers = getInstance().tickers_;
  auto it = tickers.find(tag);
  if (it != tickers.end()) {
    // Ticker already exists so return what we've found.
    return it->second;
  } else {
    // This tag hasn't been ticked before. Let's create it, and return the new
    // ticker.
    auto insert_status = tickers.emplace(tag, DelayTicker());
    getInstance().max_tag_length_ =
        std::max(getInstance().max_tag_length_, tag.size());
    return insert_status.first->second;
  }
}

void Delays::tick(const std::string& tag, const Time reference_timestamp_ns,
                  const Time delayed_timestamp_ns) {
  DelayTicker& ticker = getInstance().getTicker(tag);
  std::lock_guard<std::mutex> lock(getInstance().mutex_);
  ticker.tick(reference_timestamp_ns, delayed_timestamp_ns);
}

bool Delays::exists(const std::string& tag) {
  return !(getInstance().tickers_.find(tag) == getInstance().tickers_.end());
}

double Delays::getRollingMeanDelayInNanoSeconds(const std::string& tag) {
  if (!exists(tag)) {
    return 0.0f;
  }
  return getTicker(tag).getRollingMeanDelayInNanoSeconds();
}

double Delays::getRollingMeanDelayInSeconds(const std::string& tag) {
  if (!exists(tag)) {
    return 0.0f;
  }
  return getTicker(tag).getRollingMeanDelayInSeconds();
}

std::string Delays::delayToString(double delay_s) {
  char buffer[256];
  snprintf(buffer, sizeof(buffer), "%0.3f", delay_s);
  return buffer;
}

void Delays::Print(std::ostream& out) {
  out << "\nNVBlox Delays\n";
  out << "namespace/tag - NumSamples (Window Length) - Mean Delay (seconds) \n";
  out << "-----------\n";

  for (const auto& tag_ticker_pair : getInstance().tickers_) {
    const std::string& ticker_name = tag_ticker_pair.first;

    out.width(static_cast<std::streamsize>(getInstance().max_tag_length_));
    out.setf(std::ios::left, std::ios::adjustfield);
    out << ticker_name << "\t";
    out.width(7);

    const DelayTicker& ticker = tag_ticker_pair.second;
    const int num_samples = ticker.getNumSamples();
    out << num_samples << "\t";
    if (num_samples > 0) {
      const float mean_delay_s = ticker.getRollingMeanDelayInSeconds();
      out << delayToString(mean_delay_s);
    }
    out << std::endl;
  }
  out << "-----------\n";
}

std::string Delays::Print() {
  std::stringstream ss;
  Print(ss);
  return ss.str();
}

}  // namespace timing
}  // namespace nvblox
