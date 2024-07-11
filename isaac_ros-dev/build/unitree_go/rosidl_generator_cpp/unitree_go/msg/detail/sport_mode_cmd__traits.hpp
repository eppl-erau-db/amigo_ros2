// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from unitree_go:msg/SportModeCmd.idl
// generated code does not contain a copyright notice

#ifndef UNITREE_GO__MSG__DETAIL__SPORT_MODE_CMD__TRAITS_HPP_
#define UNITREE_GO__MSG__DETAIL__SPORT_MODE_CMD__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "unitree_go/msg/detail/sport_mode_cmd__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'bms_cmd'
#include "unitree_go/msg/detail/bms_cmd__traits.hpp"
// Member 'path_point'
#include "unitree_go/msg/detail/path_point__traits.hpp"

namespace unitree_go
{

namespace msg
{

inline void to_flow_style_yaml(
  const SportModeCmd & msg,
  std::ostream & out)
{
  out << "{";
  // member: mode
  {
    out << "mode: ";
    rosidl_generator_traits::value_to_yaml(msg.mode, out);
    out << ", ";
  }

  // member: gait_type
  {
    out << "gait_type: ";
    rosidl_generator_traits::value_to_yaml(msg.gait_type, out);
    out << ", ";
  }

  // member: speed_level
  {
    out << "speed_level: ";
    rosidl_generator_traits::value_to_yaml(msg.speed_level, out);
    out << ", ";
  }

  // member: foot_raise_height
  {
    out << "foot_raise_height: ";
    rosidl_generator_traits::value_to_yaml(msg.foot_raise_height, out);
    out << ", ";
  }

  // member: body_height
  {
    out << "body_height: ";
    rosidl_generator_traits::value_to_yaml(msg.body_height, out);
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

  // member: euler
  {
    if (msg.euler.size() == 0) {
      out << "euler: []";
    } else {
      out << "euler: [";
      size_t pending_items = msg.euler.size();
      for (auto item : msg.euler) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
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

  // member: bms_cmd
  {
    out << "bms_cmd: ";
    to_flow_style_yaml(msg.bms_cmd, out);
    out << ", ";
  }

  // member: path_point
  {
    if (msg.path_point.size() == 0) {
      out << "path_point: []";
    } else {
      out << "path_point: [";
      size_t pending_items = msg.path_point.size();
      for (auto item : msg.path_point) {
        to_flow_style_yaml(item, out);
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
  const SportModeCmd & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: mode
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "mode: ";
    rosidl_generator_traits::value_to_yaml(msg.mode, out);
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

  // member: speed_level
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "speed_level: ";
    rosidl_generator_traits::value_to_yaml(msg.speed_level, out);
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

  // member: body_height
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "body_height: ";
    rosidl_generator_traits::value_to_yaml(msg.body_height, out);
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

  // member: euler
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.euler.size() == 0) {
      out << "euler: []\n";
    } else {
      out << "euler:\n";
      for (auto item : msg.euler) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
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

  // member: bms_cmd
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "bms_cmd:\n";
    to_block_style_yaml(msg.bms_cmd, out, indentation + 2);
  }

  // member: path_point
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.path_point.size() == 0) {
      out << "path_point: []\n";
    } else {
      out << "path_point:\n";
      for (auto item : msg.path_point) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SportModeCmd & msg, bool use_flow_style = false)
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
  const unitree_go::msg::SportModeCmd & msg,
  std::ostream & out, size_t indentation = 0)
{
  unitree_go::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use unitree_go::msg::to_yaml() instead")]]
inline std::string to_yaml(const unitree_go::msg::SportModeCmd & msg)
{
  return unitree_go::msg::to_yaml(msg);
}

template<>
inline const char * data_type<unitree_go::msg::SportModeCmd>()
{
  return "unitree_go::msg::SportModeCmd";
}

template<>
inline const char * name<unitree_go::msg::SportModeCmd>()
{
  return "unitree_go/msg/SportModeCmd";
}

template<>
struct has_fixed_size<unitree_go::msg::SportModeCmd>
  : std::integral_constant<bool, has_fixed_size<unitree_go::msg::BmsCmd>::value && has_fixed_size<unitree_go::msg::PathPoint>::value> {};

template<>
struct has_bounded_size<unitree_go::msg::SportModeCmd>
  : std::integral_constant<bool, has_bounded_size<unitree_go::msg::BmsCmd>::value && has_bounded_size<unitree_go::msg::PathPoint>::value> {};

template<>
struct is_message<unitree_go::msg::SportModeCmd>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // UNITREE_GO__MSG__DETAIL__SPORT_MODE_CMD__TRAITS_HPP_
