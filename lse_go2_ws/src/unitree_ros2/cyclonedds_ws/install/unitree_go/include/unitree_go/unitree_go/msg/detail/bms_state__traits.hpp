// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from unitree_go:msg/BmsState.idl
// generated code does not contain a copyright notice

#ifndef UNITREE_GO__MSG__DETAIL__BMS_STATE__TRAITS_HPP_
#define UNITREE_GO__MSG__DETAIL__BMS_STATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "unitree_go/msg/detail/bms_state__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace unitree_go
{

namespace msg
{

inline void to_flow_style_yaml(
  const BmsState & msg,
  std::ostream & out)
{
  out << "{";
  // member: version_high
  {
    out << "version_high: ";
    rosidl_generator_traits::value_to_yaml(msg.version_high, out);
    out << ", ";
  }

  // member: version_low
  {
    out << "version_low: ";
    rosidl_generator_traits::value_to_yaml(msg.version_low, out);
    out << ", ";
  }

  // member: status
  {
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << ", ";
  }

  // member: soc
  {
    out << "soc: ";
    rosidl_generator_traits::value_to_yaml(msg.soc, out);
    out << ", ";
  }

  // member: current
  {
    out << "current: ";
    rosidl_generator_traits::value_to_yaml(msg.current, out);
    out << ", ";
  }

  // member: cycle
  {
    out << "cycle: ";
    rosidl_generator_traits::value_to_yaml(msg.cycle, out);
    out << ", ";
  }

  // member: bq_ntc
  {
    if (msg.bq_ntc.size() == 0) {
      out << "bq_ntc: []";
    } else {
      out << "bq_ntc: [";
      size_t pending_items = msg.bq_ntc.size();
      for (auto item : msg.bq_ntc) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: mcu_ntc
  {
    if (msg.mcu_ntc.size() == 0) {
      out << "mcu_ntc: []";
    } else {
      out << "mcu_ntc: [";
      size_t pending_items = msg.mcu_ntc.size();
      for (auto item : msg.mcu_ntc) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: cell_vol
  {
    if (msg.cell_vol.size() == 0) {
      out << "cell_vol: []";
    } else {
      out << "cell_vol: [";
      size_t pending_items = msg.cell_vol.size();
      for (auto item : msg.cell_vol) {
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
  const BmsState & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: version_high
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "version_high: ";
    rosidl_generator_traits::value_to_yaml(msg.version_high, out);
    out << "\n";
  }

  // member: version_low
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "version_low: ";
    rosidl_generator_traits::value_to_yaml(msg.version_low, out);
    out << "\n";
  }

  // member: status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << "\n";
  }

  // member: soc
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "soc: ";
    rosidl_generator_traits::value_to_yaml(msg.soc, out);
    out << "\n";
  }

  // member: current
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "current: ";
    rosidl_generator_traits::value_to_yaml(msg.current, out);
    out << "\n";
  }

  // member: cycle
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "cycle: ";
    rosidl_generator_traits::value_to_yaml(msg.cycle, out);
    out << "\n";
  }

  // member: bq_ntc
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.bq_ntc.size() == 0) {
      out << "bq_ntc: []\n";
    } else {
      out << "bq_ntc:\n";
      for (auto item : msg.bq_ntc) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: mcu_ntc
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.mcu_ntc.size() == 0) {
      out << "mcu_ntc: []\n";
    } else {
      out << "mcu_ntc:\n";
      for (auto item : msg.mcu_ntc) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: cell_vol
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.cell_vol.size() == 0) {
      out << "cell_vol: []\n";
    } else {
      out << "cell_vol:\n";
      for (auto item : msg.cell_vol) {
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

inline std::string to_yaml(const BmsState & msg, bool use_flow_style = false)
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
  const unitree_go::msg::BmsState & msg,
  std::ostream & out, size_t indentation = 0)
{
  unitree_go::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use unitree_go::msg::to_yaml() instead")]]
inline std::string to_yaml(const unitree_go::msg::BmsState & msg)
{
  return unitree_go::msg::to_yaml(msg);
}

template<>
inline const char * data_type<unitree_go::msg::BmsState>()
{
  return "unitree_go::msg::BmsState";
}

template<>
inline const char * name<unitree_go::msg::BmsState>()
{
  return "unitree_go/msg/BmsState";
}

template<>
struct has_fixed_size<unitree_go::msg::BmsState>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<unitree_go::msg::BmsState>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<unitree_go::msg::BmsState>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // UNITREE_GO__MSG__DETAIL__BMS_STATE__TRAITS_HPP_
