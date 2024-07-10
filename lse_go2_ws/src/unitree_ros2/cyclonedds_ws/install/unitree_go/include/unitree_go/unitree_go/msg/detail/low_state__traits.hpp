// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from unitree_go:msg/LowState.idl
// generated code does not contain a copyright notice

#ifndef UNITREE_GO__MSG__DETAIL__LOW_STATE__TRAITS_HPP_
#define UNITREE_GO__MSG__DETAIL__LOW_STATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "unitree_go/msg/detail/low_state__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'imu_state'
#include "unitree_go/msg/detail/imu_state__traits.hpp"
// Member 'motor_state'
#include "unitree_go/msg/detail/motor_state__traits.hpp"
// Member 'bms_state'
#include "unitree_go/msg/detail/bms_state__traits.hpp"

namespace unitree_go
{

namespace msg
{

inline void to_flow_style_yaml(
  const LowState & msg,
  std::ostream & out)
{
  out << "{";
  // member: head
  {
    if (msg.head.size() == 0) {
      out << "head: []";
    } else {
      out << "head: [";
      size_t pending_items = msg.head.size();
      for (auto item : msg.head) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: level_flag
  {
    out << "level_flag: ";
    rosidl_generator_traits::value_to_yaml(msg.level_flag, out);
    out << ", ";
  }

  // member: frame_reserve
  {
    out << "frame_reserve: ";
    rosidl_generator_traits::value_to_yaml(msg.frame_reserve, out);
    out << ", ";
  }

  // member: sn
  {
    if (msg.sn.size() == 0) {
      out << "sn: []";
    } else {
      out << "sn: [";
      size_t pending_items = msg.sn.size();
      for (auto item : msg.sn) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: version
  {
    if (msg.version.size() == 0) {
      out << "version: []";
    } else {
      out << "version: [";
      size_t pending_items = msg.version.size();
      for (auto item : msg.version) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: bandwidth
  {
    out << "bandwidth: ";
    rosidl_generator_traits::value_to_yaml(msg.bandwidth, out);
    out << ", ";
  }

  // member: imu_state
  {
    out << "imu_state: ";
    to_flow_style_yaml(msg.imu_state, out);
    out << ", ";
  }

  // member: motor_state
  {
    if (msg.motor_state.size() == 0) {
      out << "motor_state: []";
    } else {
      out << "motor_state: [";
      size_t pending_items = msg.motor_state.size();
      for (auto item : msg.motor_state) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: bms_state
  {
    out << "bms_state: ";
    to_flow_style_yaml(msg.bms_state, out);
    out << ", ";
  }

  // member: foot_force
  {
    if (msg.foot_force.size() == 0) {
      out << "foot_force: []";
    } else {
      out << "foot_force: [";
      size_t pending_items = msg.foot_force.size();
      for (auto item : msg.foot_force) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: foot_force_est
  {
    if (msg.foot_force_est.size() == 0) {
      out << "foot_force_est: []";
    } else {
      out << "foot_force_est: [";
      size_t pending_items = msg.foot_force_est.size();
      for (auto item : msg.foot_force_est) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: tick
  {
    out << "tick: ";
    rosidl_generator_traits::value_to_yaml(msg.tick, out);
    out << ", ";
  }

  // member: wireless_remote
  {
    if (msg.wireless_remote.size() == 0) {
      out << "wireless_remote: []";
    } else {
      out << "wireless_remote: [";
      size_t pending_items = msg.wireless_remote.size();
      for (auto item : msg.wireless_remote) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: bit_flag
  {
    out << "bit_flag: ";
    rosidl_generator_traits::value_to_yaml(msg.bit_flag, out);
    out << ", ";
  }

  // member: adc_reel
  {
    out << "adc_reel: ";
    rosidl_generator_traits::value_to_yaml(msg.adc_reel, out);
    out << ", ";
  }

  // member: temperature_ntc1
  {
    out << "temperature_ntc1: ";
    rosidl_generator_traits::value_to_yaml(msg.temperature_ntc1, out);
    out << ", ";
  }

  // member: temperature_ntc2
  {
    out << "temperature_ntc2: ";
    rosidl_generator_traits::value_to_yaml(msg.temperature_ntc2, out);
    out << ", ";
  }

  // member: power_v
  {
    out << "power_v: ";
    rosidl_generator_traits::value_to_yaml(msg.power_v, out);
    out << ", ";
  }

  // member: power_a
  {
    out << "power_a: ";
    rosidl_generator_traits::value_to_yaml(msg.power_a, out);
    out << ", ";
  }

  // member: fan_frequency
  {
    if (msg.fan_frequency.size() == 0) {
      out << "fan_frequency: []";
    } else {
      out << "fan_frequency: [";
      size_t pending_items = msg.fan_frequency.size();
      for (auto item : msg.fan_frequency) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: reserve
  {
    out << "reserve: ";
    rosidl_generator_traits::value_to_yaml(msg.reserve, out);
    out << ", ";
  }

  // member: crc
  {
    out << "crc: ";
    rosidl_generator_traits::value_to_yaml(msg.crc, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const LowState & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: head
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.head.size() == 0) {
      out << "head: []\n";
    } else {
      out << "head:\n";
      for (auto item : msg.head) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: level_flag
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "level_flag: ";
    rosidl_generator_traits::value_to_yaml(msg.level_flag, out);
    out << "\n";
  }

  // member: frame_reserve
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "frame_reserve: ";
    rosidl_generator_traits::value_to_yaml(msg.frame_reserve, out);
    out << "\n";
  }

  // member: sn
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.sn.size() == 0) {
      out << "sn: []\n";
    } else {
      out << "sn:\n";
      for (auto item : msg.sn) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: version
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.version.size() == 0) {
      out << "version: []\n";
    } else {
      out << "version:\n";
      for (auto item : msg.version) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: bandwidth
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "bandwidth: ";
    rosidl_generator_traits::value_to_yaml(msg.bandwidth, out);
    out << "\n";
  }

  // member: imu_state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "imu_state:\n";
    to_block_style_yaml(msg.imu_state, out, indentation + 2);
  }

  // member: motor_state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.motor_state.size() == 0) {
      out << "motor_state: []\n";
    } else {
      out << "motor_state:\n";
      for (auto item : msg.motor_state) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: bms_state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "bms_state:\n";
    to_block_style_yaml(msg.bms_state, out, indentation + 2);
  }

  // member: foot_force
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.foot_force.size() == 0) {
      out << "foot_force: []\n";
    } else {
      out << "foot_force:\n";
      for (auto item : msg.foot_force) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: foot_force_est
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.foot_force_est.size() == 0) {
      out << "foot_force_est: []\n";
    } else {
      out << "foot_force_est:\n";
      for (auto item : msg.foot_force_est) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: tick
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "tick: ";
    rosidl_generator_traits::value_to_yaml(msg.tick, out);
    out << "\n";
  }

  // member: wireless_remote
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.wireless_remote.size() == 0) {
      out << "wireless_remote: []\n";
    } else {
      out << "wireless_remote:\n";
      for (auto item : msg.wireless_remote) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: bit_flag
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "bit_flag: ";
    rosidl_generator_traits::value_to_yaml(msg.bit_flag, out);
    out << "\n";
  }

  // member: adc_reel
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "adc_reel: ";
    rosidl_generator_traits::value_to_yaml(msg.adc_reel, out);
    out << "\n";
  }

  // member: temperature_ntc1
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "temperature_ntc1: ";
    rosidl_generator_traits::value_to_yaml(msg.temperature_ntc1, out);
    out << "\n";
  }

  // member: temperature_ntc2
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "temperature_ntc2: ";
    rosidl_generator_traits::value_to_yaml(msg.temperature_ntc2, out);
    out << "\n";
  }

  // member: power_v
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "power_v: ";
    rosidl_generator_traits::value_to_yaml(msg.power_v, out);
    out << "\n";
  }

  // member: power_a
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "power_a: ";
    rosidl_generator_traits::value_to_yaml(msg.power_a, out);
    out << "\n";
  }

  // member: fan_frequency
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.fan_frequency.size() == 0) {
      out << "fan_frequency: []\n";
    } else {
      out << "fan_frequency:\n";
      for (auto item : msg.fan_frequency) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: reserve
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "reserve: ";
    rosidl_generator_traits::value_to_yaml(msg.reserve, out);
    out << "\n";
  }

  // member: crc
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "crc: ";
    rosidl_generator_traits::value_to_yaml(msg.crc, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const LowState & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace unitree_go

namespace rosidl_generator_traits
{

[[deprecated("use unitree_go::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const unitree_go::msg::LowState & msg,
  std::ostream & out, size_t indentation = 0)
{
  unitree_go::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use unitree_go::msg::to_yaml() instead")]]
inline std::string to_yaml(const unitree_go::msg::LowState & msg)
{
  return unitree_go::msg::to_yaml(msg);
}

template<>
inline const char * data_type<unitree_go::msg::LowState>()
{
  return "unitree_go::msg::LowState";
}

template<>
inline const char * name<unitree_go::msg::LowState>()
{
  return "unitree_go/msg/LowState";
}

template<>
struct has_fixed_size<unitree_go::msg::LowState>
  : std::integral_constant<bool, has_fixed_size<unitree_go::msg::BmsState>::value && has_fixed_size<unitree_go::msg::IMUState>::value && has_fixed_size<unitree_go::msg::MotorState>::value> {};

template<>
struct has_bounded_size<unitree_go::msg::LowState>
  : std::integral_constant<bool, has_bounded_size<unitree_go::msg::BmsState>::value && has_bounded_size<unitree_go::msg::IMUState>::value && has_bounded_size<unitree_go::msg::MotorState>::value> {};

template<>
struct is_message<unitree_go::msg::LowState>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // UNITREE_GO__MSG__DETAIL__LOW_STATE__TRAITS_HPP_
