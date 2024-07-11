// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from unitree_go:msg/SportModeState.idl
// generated code does not contain a copyright notice

#ifndef UNITREE_GO__MSG__DETAIL__SPORT_MODE_STATE__TRAITS_HPP_
#define UNITREE_GO__MSG__DETAIL__SPORT_MODE_STATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "unitree_go/msg/detail/sport_mode_state__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'stamp'
#include "unitree_go/msg/detail/time_spec__traits.hpp"
// Member 'imu_state'
#include "unitree_go/msg/detail/imu_state__traits.hpp"

namespace unitree_go
{

namespace msg
{

inline void to_flow_style_yaml(
  const SportModeState & msg,
  std::ostream & out)
{
  out << "{";
  // member: stamp
  {
    out << "stamp: ";
    to_flow_style_yaml(msg.stamp, out);
    out << ", ";
  }

  // member: error_code
  {
    out << "error_code: ";
    rosidl_generator_traits::value_to_yaml(msg.error_code, out);
    out << ", ";
  }

  // member: imu_state
  {
    out << "imu_state: ";
    to_flow_style_yaml(msg.imu_state, out);
    out << ", ";
  }

  // member: mode
  {
    out << "mode: ";
    rosidl_generator_traits::value_to_yaml(msg.mode, out);
    out << ", ";
  }

  // member: progress
  {
    out << "progress: ";
    rosidl_generator_traits::value_to_yaml(msg.progress, out);
    out << ", ";
  }

  // member: gait_type
  {
    out << "gait_type: ";
    rosidl_generator_traits::value_to_yaml(msg.gait_type, out);
    out << ", ";
  }

  // member: foot_raise_height
  {
    out << "foot_raise_height: ";
    rosidl_generator_traits::value_to_yaml(msg.foot_raise_height, out);
    out << ", ";
  }

  // member: position
  {
    if (msg.position.size() == 0) {
      out << "position: []";
    } else {
      out << "position: [";
      size_t pending_items = msg.position.size();
      for (auto item : msg.position) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: body_height
  {
    out << "body_height: ";
    rosidl_generator_traits::value_to_yaml(msg.body_height, out);
    out << ", ";
  }

  // member: velocity
  {
    if (msg.velocity.size() == 0) {
      out << "velocity: []";
    } else {
      out << "velocity: [";
      size_t pending_items = msg.velocity.size();
      for (auto item : msg.velocity) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: yaw_speed
  {
    out << "yaw_speed: ";
    rosidl_generator_traits::value_to_yaml(msg.yaw_speed, out);
    out << ", ";
  }

  // member: range_obstacle
  {
    if (msg.range_obstacle.size() == 0) {
      out << "range_obstacle: []";
    } else {
      out << "range_obstacle: [";
      size_t pending_items = msg.range_obstacle.size();
      for (auto item : msg.range_obstacle) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
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

  // member: foot_position_body
  {
    if (msg.foot_position_body.size() == 0) {
      out << "foot_position_body: []";
    } else {
      out << "foot_position_body: [";
      size_t pending_items = msg.foot_position_body.size();
      for (auto item : msg.foot_position_body) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: foot_speed_body
  {
    if (msg.foot_speed_body.size() == 0) {
      out << "foot_speed_body: []";
    } else {
      out << "foot_speed_body: [";
      size_t pending_items = msg.foot_speed_body.size();
      for (auto item : msg.foot_speed_body) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SportModeState & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stamp:\n";
    to_block_style_yaml(msg.stamp, out, indentation + 2);
  }

  // member: error_code
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "error_code: ";
    rosidl_generator_traits::value_to_yaml(msg.error_code, out);
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

  // member: mode
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "mode: ";
    rosidl_generator_traits::value_to_yaml(msg.mode, out);
    out << "\n";
  }

  // member: progress
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "progress: ";
    rosidl_generator_traits::value_to_yaml(msg.progress, out);
    out << "\n";
  }

  // member: gait_type
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "gait_type: ";
    rosidl_generator_traits::value_to_yaml(msg.gait_type, out);
    out << "\n";
  }

  // member: foot_raise_height
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "foot_raise_height: ";
    rosidl_generator_traits::value_to_yaml(msg.foot_raise_height, out);
    out << "\n";
  }

  // member: position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.position.size() == 0) {
      out << "position: []\n";
    } else {
      out << "position:\n";
      for (auto item : msg.position) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: body_height
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "body_height: ";
    rosidl_generator_traits::value_to_yaml(msg.body_height, out);
    out << "\n";
  }

  // member: velocity
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.velocity.size() == 0) {
      out << "velocity: []\n";
    } else {
      out << "velocity:\n";
      for (auto item : msg.velocity) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: yaw_speed
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "yaw_speed: ";
    rosidl_generator_traits::value_to_yaml(msg.yaw_speed, out);
    out << "\n";
  }

  // member: range_obstacle
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.range_obstacle.size() == 0) {
      out << "range_obstacle: []\n";
    } else {
      out << "range_obstacle:\n";
      for (auto item : msg.range_obstacle) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
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

  // member: foot_position_body
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.foot_position_body.size() == 0) {
      out << "foot_position_body: []\n";
    } else {
      out << "foot_position_body:\n";
      for (auto item : msg.foot_position_body) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: foot_speed_body
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.foot_speed_body.size() == 0) {
      out << "foot_speed_body: []\n";
    } else {
      out << "foot_speed_body:\n";
      for (auto item : msg.foot_speed_body) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SportModeState & msg, bool use_flow_style = false)
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
  const unitree_go::msg::SportModeState & msg,
  std::ostream & out, size_t indentation = 0)
{
  unitree_go::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use unitree_go::msg::to_yaml() instead")]]
inline std::string to_yaml(const unitree_go::msg::SportModeState & msg)
{
  return unitree_go::msg::to_yaml(msg);
}

template<>
inline const char * data_type<unitree_go::msg::SportModeState>()
{
  return "unitree_go::msg::SportModeState";
}

template<>
inline const char * name<unitree_go::msg::SportModeState>()
{
  return "unitree_go/msg/SportModeState";
}

template<>
struct has_fixed_size<unitree_go::msg::SportModeState>
  : std::integral_constant<bool, has_fixed_size<unitree_go::msg::IMUState>::value && has_fixed_size<unitree_go::msg::TimeSpec>::value> {};

template<>
struct has_bounded_size<unitree_go::msg::SportModeState>
  : std::integral_constant<bool, has_bounded_size<unitree_go::msg::IMUState>::value && has_bounded_size<unitree_go::msg::TimeSpec>::value> {};

template<>
struct is_message<unitree_go::msg::SportModeState>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // UNITREE_GO__MSG__DETAIL__SPORT_MODE_STATE__TRAITS_HPP_
