// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from unitree_go:msg/UwbState.idl
// generated code does not contain a copyright notice

#ifndef UNITREE_GO__MSG__DETAIL__UWB_STATE__TRAITS_HPP_
#define UNITREE_GO__MSG__DETAIL__UWB_STATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "unitree_go/msg/detail/uwb_state__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace unitree_go
{

namespace msg
{

inline void to_flow_style_yaml(
  const UwbState & msg,
  std::ostream & out)
{
  out << "{";
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

  // member: channel
  {
    out << "channel: ";
    rosidl_generator_traits::value_to_yaml(msg.channel, out);
    out << ", ";
  }

  // member: joy_mode
  {
    out << "joy_mode: ";
    rosidl_generator_traits::value_to_yaml(msg.joy_mode, out);
    out << ", ";
  }

  // member: orientation_est
  {
    out << "orientation_est: ";
    rosidl_generator_traits::value_to_yaml(msg.orientation_est, out);
    out << ", ";
  }

  // member: pitch_est
  {
    out << "pitch_est: ";
    rosidl_generator_traits::value_to_yaml(msg.pitch_est, out);
    out << ", ";
  }

  // member: distance_est
  {
    out << "distance_est: ";
    rosidl_generator_traits::value_to_yaml(msg.distance_est, out);
    out << ", ";
  }

  // member: yaw_est
  {
    out << "yaw_est: ";
    rosidl_generator_traits::value_to_yaml(msg.yaw_est, out);
    out << ", ";
  }

  // member: tag_roll
  {
    out << "tag_roll: ";
    rosidl_generator_traits::value_to_yaml(msg.tag_roll, out);
    out << ", ";
  }

  // member: tag_pitch
  {
    out << "tag_pitch: ";
    rosidl_generator_traits::value_to_yaml(msg.tag_pitch, out);
    out << ", ";
  }

  // member: tag_yaw
  {
    out << "tag_yaw: ";
    rosidl_generator_traits::value_to_yaml(msg.tag_yaw, out);
    out << ", ";
  }

  // member: base_roll
  {
    out << "base_roll: ";
    rosidl_generator_traits::value_to_yaml(msg.base_roll, out);
    out << ", ";
  }

  // member: base_pitch
  {
    out << "base_pitch: ";
    rosidl_generator_traits::value_to_yaml(msg.base_pitch, out);
    out << ", ";
  }

  // member: base_yaw
  {
    out << "base_yaw: ";
    rosidl_generator_traits::value_to_yaml(msg.base_yaw, out);
    out << ", ";
  }

  // member: joystick
  {
    if (msg.joystick.size() == 0) {
      out << "joystick: []";
    } else {
      out << "joystick: [";
      size_t pending_items = msg.joystick.size();
      for (auto item : msg.joystick) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: error_state
  {
    out << "error_state: ";
    rosidl_generator_traits::value_to_yaml(msg.error_state, out);
    out << ", ";
  }

  // member: buttons
  {
    out << "buttons: ";
    rosidl_generator_traits::value_to_yaml(msg.buttons, out);
    out << ", ";
  }

  // member: enabled_from_app
  {
    out << "enabled_from_app: ";
    rosidl_generator_traits::value_to_yaml(msg.enabled_from_app, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const UwbState & msg,
  std::ostream & out, size_t indentation = 0)
{
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

  // member: channel
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "channel: ";
    rosidl_generator_traits::value_to_yaml(msg.channel, out);
    out << "\n";
  }

  // member: joy_mode
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "joy_mode: ";
    rosidl_generator_traits::value_to_yaml(msg.joy_mode, out);
    out << "\n";
  }

  // member: orientation_est
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "orientation_est: ";
    rosidl_generator_traits::value_to_yaml(msg.orientation_est, out);
    out << "\n";
  }

  // member: pitch_est
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "pitch_est: ";
    rosidl_generator_traits::value_to_yaml(msg.pitch_est, out);
    out << "\n";
  }

  // member: distance_est
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "distance_est: ";
    rosidl_generator_traits::value_to_yaml(msg.distance_est, out);
    out << "\n";
  }

  // member: yaw_est
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "yaw_est: ";
    rosidl_generator_traits::value_to_yaml(msg.yaw_est, out);
    out << "\n";
  }

  // member: tag_roll
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "tag_roll: ";
    rosidl_generator_traits::value_to_yaml(msg.tag_roll, out);
    out << "\n";
  }

  // member: tag_pitch
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "tag_pitch: ";
    rosidl_generator_traits::value_to_yaml(msg.tag_pitch, out);
    out << "\n";
  }

  // member: tag_yaw
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "tag_yaw: ";
    rosidl_generator_traits::value_to_yaml(msg.tag_yaw, out);
    out << "\n";
  }

  // member: base_roll
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "base_roll: ";
    rosidl_generator_traits::value_to_yaml(msg.base_roll, out);
    out << "\n";
  }

  // member: base_pitch
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "base_pitch: ";
    rosidl_generator_traits::value_to_yaml(msg.base_pitch, out);
    out << "\n";
  }

  // member: base_yaw
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "base_yaw: ";
    rosidl_generator_traits::value_to_yaml(msg.base_yaw, out);
    out << "\n";
  }

  // member: joystick
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.joystick.size() == 0) {
      out << "joystick: []\n";
    } else {
      out << "joystick:\n";
      for (auto item : msg.joystick) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: error_state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "error_state: ";
    rosidl_generator_traits::value_to_yaml(msg.error_state, out);
    out << "\n";
  }

  // member: buttons
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "buttons: ";
    rosidl_generator_traits::value_to_yaml(msg.buttons, out);
    out << "\n";
  }

  // member: enabled_from_app
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "enabled_from_app: ";
    rosidl_generator_traits::value_to_yaml(msg.enabled_from_app, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const UwbState & msg, bool use_flow_style = false)
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
  const unitree_go::msg::UwbState & msg,
  std::ostream & out, size_t indentation = 0)
{
  unitree_go::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use unitree_go::msg::to_yaml() instead")]]
inline std::string to_yaml(const unitree_go::msg::UwbState & msg)
{
  return unitree_go::msg::to_yaml(msg);
}

template<>
inline const char * data_type<unitree_go::msg::UwbState>()
{
  return "unitree_go::msg::UwbState";
}

template<>
inline const char * name<unitree_go::msg::UwbState>()
{
  return "unitree_go/msg/UwbState";
}

template<>
struct has_fixed_size<unitree_go::msg::UwbState>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<unitree_go::msg::UwbState>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<unitree_go::msg::UwbState>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // UNITREE_GO__MSG__DETAIL__UWB_STATE__TRAITS_HPP_
