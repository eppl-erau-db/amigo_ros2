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

#include <string>

namespace nvblox {

/// Class for storing a parameter with description and default value
///
/// The class supports implicit conversion from/to the wrapped type.
///
/// @tparam T Type of the parameter
/// @tparam DefaultValueType  Type of the default value of the parameter. Should
/// normally be the same as T, but might differ e.g. for
/// std::string where we wish to store the default value as a constexpr string
/// literal instead of an std::string (that cannot be constexpr)
template <typename _T, typename DefaultValueType = _T>
class Param {
 public:
  using T = _T;
  /// Description of a parameter.
  struct Description {
    /// Name of the parameter - how it will appear in a cmdline parser, etc.
    const char* name;
    /// Default value of the parameter.
    DefaultValueType default_value;
    /// Help text for the parameter.
    const char* help_string;
  };

  /// Construct a parameter given a name, default value and a description
  /// @attention description must be a constexpr, otherwise the program won't
  /// build
  Param(const Description& description)
      : description_(description), value_(description.default_value) {}

  /// Allow for assignment to wrapped type, e.g. int a = Param
  operator T() const { return value_; }

  /// Allow for assignment from wrapped value, e.g. Param p = 2
  Param& operator=(const T value) {
    value_ = value;
    return *this;
  }

  /// Explicit getter
  T get() const { return value_; }

  /// Explicit setter
  void set(const T value) { value_ = value; }

  /// Return description
  constexpr Description& description() { return description_; }

 private:
  Description description_;
  T value_;
};

// String param stores value as std::string, but the default value as a literal
// string s.t. it can remain constexpr.
using StringParam = Param<std::string, const char*>;

}  // namespace nvblox
